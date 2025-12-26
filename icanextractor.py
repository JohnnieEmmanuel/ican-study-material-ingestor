import os
import re
import requests
from bs4 import BeautifulSoup
from slugify import slugify
from urllib.parse import urljoin, urlparse
import boto3
from botocore.exceptions import ClientError

# ================= CONFIG =================
ICAN_URL = "https://icanig.org/pro-study-text-2021"
DOWNLOAD_DIR = "downloads"

SUPABASE_ENDPOINT = "https://fbjekiepmbsxknkhtzbj.storage.supabase.co/storage/v1/s3"
BUCKET_NAME = os.getenv("SUPABASE_BUCKET_NAME")

AWS_ACCESS_KEY_ID = os.getenv("SUPABASE_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("SUPABASE_SECRET_KEY")

if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET_NAME]):
    raise RuntimeError("Missing Supabase credentials")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ================= ICAN SUBJECT MAP =================
ICAN_SUBJECTS = {
    "foundation": [
        "quantitative techniques in business",
        "business and finance",
        "financial accounting",
        "management accounting",
        "corporate and business law",
        "business law"
    ],
    "skills": [
        "financial reporting",
        "audit assurance and forensics",
        "audit assurance & forensics",
        "taxation",
        "performance management",
        "public sector accounting and finance",
        "management governance and ethics"
    ],
    "professional": [
        "strategic business reporting",
        "corporate reporting",
        "advanced audit assurance and forensics",
        "strategic financial management",
        "advanced taxation",
        "case study"
    ]
}

# ================= HELPERS =================
def normalize(text: str) -> str:
    text = text.lower()
    text = text.replace("&", "and")
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def detect_level(subject_text):
    clean = normalize(subject_text)
    for level, subjects in ICAN_SUBJECTS.items():
        for s in subjects:
            if s in clean:
                return level, s
    return "unclassified", clean

def extract_subject_name(link_text, pdf_url):
    if link_text:
        return link_text.strip()
    filename = os.path.basename(urlparse(pdf_url).path)
    return filename.replace(".pdf", "").replace("_", " ")

def exists_in_bucket(s3, bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        raise

# ================= S3 CLIENT =================
s3 = boto3.client(
    "s3",
    endpoint_url=SUPABASE_ENDPOINT,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

# ================= SCRAPE =================
print("🔍 Fetching ICAN study page...")
resp = requests.get(ICAN_URL, timeout=30)
resp.raise_for_status()

soup = BeautifulSoup(resp.text, "html.parser")
links = soup.find_all("a", href=True)

pdfs = []

for link in links:
    href = link["href"]
    if href.lower().endswith(".pdf"):
        pdf_url = urljoin(ICAN_URL, href)
        subject_raw = extract_subject_name(link.get_text(strip=True), pdf_url)

        level, normalized_subject = detect_level(subject_raw)

        pdfs.append({
            "level": level,
            "subject": subject_raw,
            "normalized_subject": normalized_subject,
            "url": pdf_url
        })

if not pdfs:
    raise RuntimeError("No PDFs found on the page")

# ================= PROCESS =================
for item in pdfs:
    level = item["level"]
    subject = item["subject"]
    url = item["url"]

    filename = f"{slugify(subject)}.pdf"
    s3_key = f"{level}/{filename}"

    if exists_in_bucket(s3, BUCKET_NAME, s3_key):
        print(f"⏭️  Exists, skipped upload: {s3_key}")
        continue

    print(f"⬇️  Downloading: {subject}")
    r = requests.get(url, stream=True, timeout=60)
    r.raise_for_status()

    local_path = os.path.join(DOWNLOAD_DIR, filename)
    with open(local_path, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)

    print(f"☁️  Uploading → {s3_key}")
    s3.upload_file(
        local_path,
        BUCKET_NAME,
        s3_key,
        ExtraArgs={"ContentType": "application/pdf"}
    )

print("\n✅ ALL ICAN materials uploaded (no skips, no duplicates)")
