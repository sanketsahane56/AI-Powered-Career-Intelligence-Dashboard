# Security Policy

The CareerIQ team takes the security and privacy of user career data and documents seriously. Because CareerIQ is engineered as a 100% local, privacy-first platform, candidate resumes and contact details are never sent to external servers or third-party AI APIs.

---

## 🛡️ Supported Versions

We provide security updates and patches for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

---

## 🔒 Reporting a Vulnerability

If you discover a security vulnerability, potential privilege escalation, or unsafe PDF parsing issue in CareerIQ, please report it responsibly:

1. **Do not** file a public GitHub issue.
2. Email the maintainer directly at: [sanketsahane56@gmail.com](mailto:sanketsahane56@gmail.com).
3. Include:
   - A detailed description of the vulnerability.
   - Steps or proof-of-concept to reproduce the behavior.
   - Potential impact on users or host systems.

### Response Timelines
- **Initial acknowledgment**: Within 48 hours.
- **Triage and assessment**: Within 5 business days.
- **Patch release**: As soon as a verified fix has been regression-tested.

---

## 🛡️ Built-in Security Protections

CareerIQ incorporates multiple defense-in-depth security measures:
- **Upload Sanitization**: Uploaded filenames are sanitized using `werkzeug.utils.secure_filename`.
- **Payload Size Limits**: File uploads are strictly capped at 10MB (`MAX_CONTENT_LENGTH`).
- **Input Neutralization**: Job description inputs and metadata strings are sanitized before regex matching.
- **Local Isolation**: SQLite database and session files are excluded from Git via `.gitignore`.
