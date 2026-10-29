#!/usr/bin/env python3
"""
CareerIQ CLI - Command-Line Resume Analytics & Career Intelligence Tool
Run ATS scoring and job description gap analysis directly from the terminal.
"""

import sys
import json
import argparse
from pathlib import Path

from config import Config
from engine.extractor import ResumeExtractor
from engine.analyzer import CareerAnalyzer


def print_banner():
    banner = r"""
   ______                           ________  ____ 
  / ____/___ _________  ___  _____ /  _/ __ \/ __ \
 / /   / __ `/ ___/ _ \/ _ \/ ___/ / // / / / / / /
/ /___/ /_/ / /  /  __/  __/ /   _/ // /_/ / /_/ / 
\____/\__,_/_/   \___/\___/_/   /___/\___\_\___\_\ 
  AI-Powered ATS Resume Scanner & Career Intelligence
"""
    print(banner)


def parse_resume_document(path: Path):
    """Extracts text and metadata from either a PDF or text resume file."""
    if path.suffix.lower() == ".pdf":
        res = ResumeExtractor.extract_from_pdf(str(path))
        text = res.get("text", "")
    else:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        res = ResumeExtractor.extract_from_text(raw)
        text = res.get("text", "")

    if not text.strip():
        print(f"[Error] No readable text found in {path.name}", file=sys.stderr)
        sys.exit(1)

    metadata = ResumeExtractor.parse_metadata(text)
    return text, metadata


def scan_resume(file_path: str, as_json: bool = False):
    """Scans and analyzes a resume file (PDF or TXT)."""
    path = Path(file_path)
    if not path.exists():
        print(f"[Error] File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    text, metadata = parse_resume_document(path)
    word_count = len(text.split())
    analysis = CareerAnalyzer.compute_full_analysis(text, metadata, word_count)

    if as_json:
        output = {
            "metadata": metadata,
            "analysis": analysis
        }
        print(json.dumps(output, indent=2))
        return

    # Formatted terminal display
    print_banner()
    print("=" * 65)
    print(f" Candidate: {metadata.get('candidate_name', 'Unknown')}")
    print(f" Email:     {metadata.get('email', 'N/A')}")
    print(f" Phone:     {metadata.get('phone', 'N/A')}")
    print("=" * 65)
    print(f"\n OVERALL ATS SCORE: {analysis['overall_score']} / 100")
    print(f" Primary Domain:    {analysis.get('primary_domain', 'N/A')}")
    print(f" Word Count:        {word_count}")
    print(f" Extracted Skills:  {analysis['skills'].get('total_count', 0)}")
    print("\n" + "-" * 65)
    print(" 5-DIMENSION SCORECARD BREAKDOWN:")
    print("-" * 65)
    for dim_key, dim in analysis["dimensions"].items():
        score = dim["score"]
        bar_len = int(score / 5)
        bar = "=" * bar_len + "." * (20 - bar_len)
        weight_str = dim.get("weight", "")
        print(f" * {dim['name']:<30} [{bar}] {score:>3}% (wt: {weight_str})")

    print("\n" + "-" * 65)
    print(" TOP 3 CAREER ROLE MATCHES:")
    print("-" * 65)
    for idx, role in enumerate(analysis.get("role_matches", [])[:3], 1):
        role_title = role.get("role", "Role")
        fit = role.get("fit_percentage", 0)
        domain = role.get("domain", "")
        print(f" {idx}. {role_title:<28} Fit: {fit:>3}% [{domain}]")

    print("\n" + "-" * 65)
    print(" ACTIONABLE RECOMMENDATIONS:")
    print("-" * 65)
    for idx, plan_item in enumerate(analysis.get("action_plan", [])[:4], 1):
        print(f" {idx}. {plan_item}")

    print("\n" + "=" * 65)


def compare_job(file_path: str, jd_text: str, as_json: bool = False):
    """Compares candidate resume skills against a job description."""
    path = Path(file_path)
    if not path.exists():
        print(f"[Error] File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    text, metadata = parse_resume_document(path)
    word_count = len(text.split())
    analysis = CareerAnalyzer.compute_full_analysis(text, metadata, word_count)

    candidate_skills = analysis["skills"].get("all_skills", [])
    comparison = CareerAnalyzer.compare_with_job_description(candidate_skills, jd_text)

    if as_json:
        print(json.dumps(comparison, indent=2))
        return

    print_banner()
    print("=" * 65)
    print(f" TARGET JOB COMPARISON FOR: {metadata.get('candidate_name', 'Candidate')}")
    print("=" * 65)
    print(f"\n MATCH SCORE: {comparison['match_score']}%")
    print(f" Matched Skills ({len(comparison['matched_skills'])}): {', '.join(comparison['matched_skills']) or 'None'}")
    print(f" Missing Skills ({len(comparison['missing_skills'])}): {', '.join(comparison['missing_skills']) or 'None'}")
    print("\n" + "=" * 65)


def main():
    parser = argparse.ArgumentParser(
        description="CareerIQ CLI - AI-Powered ATS Resume Scanner and Skill Gap Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--version", action="version", version="CareerIQ CLI 1.0.0")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # scan command
    scan_parser = subparsers.add_parser("scan", help="Scan and analyze a resume file")
    scan_parser.add_argument("file", help="Path to resume file (PDF or TXT)")
    scan_parser.add_argument("--json", action="store_true", help="Output raw JSON analysis")

    # compare command
    compare_parser = subparsers.add_parser("compare", help="Compare resume against a target job description")
    compare_parser.add_argument("file", help="Path to candidate resume file")
    compare_parser.add_argument("job_description", help="Job description text or string")
    compare_parser.add_argument("--json", action="store_true", help="Output raw JSON comparison")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "scan":
        scan_resume(args.file, as_json=args.json)
    elif args.command == "compare":
        compare_job(args.file, args.job_description, as_json=args.json)


if __name__ == "__main__":
    main()
