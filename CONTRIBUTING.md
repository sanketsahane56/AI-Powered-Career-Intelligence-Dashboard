# Contributing to CareerIQ

Thank you for your interest in contributing to **CareerIQ**! We welcome contributions from developers, designers, data scientists, and career coaches of all skill levels.

---

## 🛠️ Development Setup

### 1. Fork and Clone
```bash
git clone https://github.com/<your-username>/AI-Powered-Career-Intelligence-Dashboard.git
cd AI-Powered-Career-Intelligence-Dashboard
```

### 2. Set Up Virtual Environment
**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Local Tests
```bash
pytest -v
```

---

## 🌿 Branching Strategy & Git Workflow

1. Create a descriptive feature branch from `main`:
   ```bash
   git checkout -b feature/add-new-skill-taxonomy
   # or
   git checkout -b fix/pdf-text-normalizer
   ```
2. Keep commits atomic and use clear, imperative commit messages (e.g. `Add financial modeling keyword taxonomy`).
3. Make sure tests pass before pushing:
   ```bash
   pytest
   ```
4. Push your branch and open a Pull Request against `main`.

---

## 📐 Code Style & Guidelines

- **Python**: Follow PEP 8 guidelines. Write clear docstrings for public classes and functions.
- **Frontend**: Keep styling in vanilla modern CSS (`static/css/style.css`). Avoid unnecessary utility bloat.
- **Taxonomy Updates**: If adding new skills or roles, ensure alias normalization is defined in `engine/skills_taxonomy.py`.
- **Zero Paid APIs**: Maintain our core commitment to 100% offline, privacy-first, zero-paid-API operation.

---

## 🧪 Testing Checklist

Every PR should:
- Pass all existing tests in `tests/`.
- Add new unit tests for any new parser, analyzer heuristic, or API route.
- Verify both the web interface (`app.py`) and CLI interface (`cli.py`).

Thank you for helping build a transparent, private, and open career analytics platform!
