# CareerIQ REST API Reference

CareerIQ provides internal and automation-friendly REST endpoints for resume scanning, job matching, and report generation.

---

## 1. Health Check
`GET /health`

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "CareerIQ - AI Career Intelligence Dashboard",
  "version": "1.0.0"
}
```

---

## 2. Analyze Resume
`POST /api/analyze-resume`

**Content-Type**: `multipart/form-data` or `application/x-www-form-urlencoded`

**Parameters:**
- `resume_file`: (File, optional) Uploaded PDF or TXT file.
- `resume_text`: (String, optional) Plain text resume content.

**Response (200 OK):**
```json
{
  "success": true,
  "session_id": "a1b2c3d4",
  "metadata": {
    "candidate_name": "Samantha Vance",
    "email": "sam.vance@example.com",
    "phone": "(415) 555-8765"
  },
  "analysis": {
    "overall_score": 92,
    "primary_domain": "Software & Cloud",
    "dimensions": { ... },
    "skills": { "total_count": 34, "all_skills": [ ... ] }
  }
}
```

---

## 3. Sample Resume Preloader
`GET /api/sample-resume?domain=<domain_name>`

**Parameters:**
- `domain`: `software` | `product` | `data` | `design` | `marketing` | `finance`

**Response (200 OK):**
```json
{
  "success": true,
  "domain": "product",
  "filename": "sample_resume_product.txt",
  "text": "..."
}
```

---

## 4. Compare with Job Description
`POST /api/compare-job`

**Content-Type**: `application/json`

**Body:**
```json
{
  "job_description": "We need an engineer with Python, PostgreSQL, and Docker...",
  "skills": ["Python", "Docker"]
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "comparison": {
    "match_score": 67,
    "matched_skills": ["Docker", "Python"],
    "missing_skills": ["PostgreSQL"],
    "total_jd_skills": 3
  }
}
```

---

## 5. Download Executive PDF Report
`GET /api/download-report/<session_id>`

Streams the binary vector `%PDF-` document directly to the client as an attachment.
