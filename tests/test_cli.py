"""
Unit Tests for CareerIQ Command-Line Interface (cli.py)
"""
import subprocess
import sys
import json
from pathlib import Path


def test_cli_version():
    cmd = [sys.executable, "cli.py", "--version"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert "CareerIQ CLI" in res.stdout or "CareerIQ CLI" in res.stderr


def test_cli_scan_json():
    sample_file = Path("data") / "sample_resume.txt"
    cmd = [sys.executable, "cli.py", "scan", str(sample_file), "--json"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    data = json.loads(res.stdout)
    assert "analysis" in data
    assert data["analysis"]["overall_score"] >= 70
    assert data["metadata"]["candidate_name"] == "Alex Morgan"


def test_cli_compare_json():
    sample_file = Path("data") / "sample_resume.txt"
    jd = "Seeking a developer skilled in Python, Docker, and PostgreSQL."
    cmd = [sys.executable, "cli.py", "compare", str(sample_file), jd, "--json"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    data = json.loads(res.stdout)
    assert "match_score" in data
    assert data["match_score"] > 0
    assert "Python" in data["matched_skills"]
