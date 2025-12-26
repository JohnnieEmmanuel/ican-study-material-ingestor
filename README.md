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
