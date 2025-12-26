# ICAN Study Material Ingestor

A robust Python tool that automatically extracts ICAN study materials from the official ICAN website and uploads them to a Supabase Storage bucket, structured by ICAN exam levels.

This project is designed to be **safe, re-runnable, and lossless** — no materials are skipped, and duplicates are avoided.

---

## 🎯 What This Tool Does

- Scrapes **all PDF study materials** from ICAN’s official study text page
- Automatically categorizes materials into:
  - `foundation`
  - `skills`
  - `professional`
- Falls back to `unclassified` if a subject cannot be confidently mapped
- Renames PDFs using clean, readable subject names
- Uploads files to **Supabase Storage (S3-compatible)**
- Skips re-uploading files that already exist (duplicate-safe)

---

## 📁 Final Storage Structure

```text
ican-study-texts/
├── foundation/
├── skills/
├── professional/
└── unclassified/
# ican-study-material-ingestor
A Python tool that ingests ICAN study PDFs, organizes them by exam level, and uploads them to Supabase Storage with duplicate-safe re-runs.

🧠 ICAN Level Mapping Logic

The script uses an authoritative ICAN syllabus-based subject map to determine the correct level.

If a material cannot be matched confidently:

It is not skipped

It is uploaded into the unclassified/ folder

This guarantees zero data loss.

⚙️ Requirements

Python 3.9+

Supabase project with Storage enabled

Internet connection

📦 Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/ican-study-material-ingestor.git
cd ican-study-material-ingestor


Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt

🔐 Environment Variables

Set the following environment variables (DO NOT hardcode credentials):

Linux / macOS
export SUPABASE_ACCESS_KEY="YOUR_SUPABASE_KEY"
export SUPABASE_SECRET_KEY="YOUR_SUPABASE_SECRET"
export SUPABASE_BUCKET_NAME="ican-study-texts"

Windows (PowerShell)
setx SUPABASE_ACCESS_KEY "YOUR_SUPABASE_KEY"
setx SUPABASE_SECRET_KEY "YOUR_SUPABASE_SECRET"
setx SUPABASE_BUCKET_NAME "ican-study-texts"


Restart your terminal after setting them.

▶️ Usage

Run the ingestion script:

python ext.py


The script can be run multiple times safely.
Already uploaded materials will be skipped automatically.

🛡️ Safety & Best Practices

Credentials are loaded via environment variables

Duplicate uploads are prevented via storage existence checks

Script is resilient to minor website changes

No materials are skipped — ever

⚠️ Legal Notice

ICAN study materials are copyrighted content.

This tool is intended for:

Personal study systems

Internal educational platforms

Authorized distribution only

Ensure you have appropriate rights before redistributing any materials publicly.

🚀 Possible Extensions

Store metadata in Supabase Database

Generate signed download URLs

Admin review UI for unclassified materials

Async downloads for faster ingestion

Cron / CI-based ingestion

🧑‍💻 Author

Built for ICAN-focused learning platforms and education tooling.
BY John Emmanuel ~ REDJOHN ~ CODEVIPER



