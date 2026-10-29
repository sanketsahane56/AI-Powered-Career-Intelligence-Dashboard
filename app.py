"""
CareerIQ - AI-Powered Career Intelligence Dashboard
Main Flask Application Server
"""

import os
import io
import json
from pathlib import Path
from flask import (
    Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
)
from werkzeug.utils import secure_filename

from config import Config
from engine.extractor import ResumeExtractor
from engine.analyzer import CareerAnalyzer
from engine.skills_taxonomy import (
    DOMAINS, SKILLS_TAXONOMY, CAREER_PROFILES, SAMPLE_JOB_DESCRIPTIONS
)
from engine.report_generator import ReportGenerator
from database.db import Database

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
Config.init_app()

# Initialize Database tables
Database.init_db()


def allowed_file(filename: str) -> bool:
    """Checks if uploaded file has an authorized extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS


# ---------------------------------------------------------
# Web Page Routes
# ---------------------------------------------------------

@app.route("/")
def dashboard():
    """Main executive dashboard overview."""
    stats = Database.get_analytics_summary()
    recent_scans = Database.get_recent_analyses(limit=6)
    return render_template(
        "dashboard.html",
        stats=stats,
        recent_scans=recent_scans,
        domains=DOMAINS,
        active_page="dashboard"
    )


@app.route("/scanner")
def scanner():
    """Interactive ATS Resume Scanner page with multi-domain intelligence."""
    session_id = request.args.get("session_id")
    existing_data = None
    if session_id:
        existing_data = Database.get_analysis_by_session_id(session_id)
    return render_template(
        "scanner.html",
        active_page="scanner",
        existing_data=existing_data,
        domains=DOMAINS
    )


@app.route("/job-match")
def job_match():
    """Job Description comparison and skill gap analyzer across domains."""
    session_id = request.args.get("session_id")
    skills_list = []
    candidate_name = ""
    if session_id:
        analysis = Database.get_analysis_by_session_id(session_id)
        if analysis and analysis.get("skills"):
            skills_list = analysis["skills"].get("all_skills", [])
            candidate_name = analysis.get("candidate_name", "")

    return render_template(
        "job_match.html",
        active_page="job_match",
        presets=SAMPLE_JOB_DESCRIPTIONS,
        domains=DOMAINS,
        skills_list=skills_list,
        candidate_name=candidate_name
    )


@app.route("/roles")
def roles_explorer():
    """Career role market taxonomy and skill requirements explorer across multiple domains."""
    return render_template(
        "roles.html",
        active_page="roles",
        roles=CAREER_PROFILES,
        domains=DOMAINS
    )


@app.route("/history")
def history():
    """View, manage, and inspect historical analysis records."""
    analyses = Database.get_recent_analyses(limit=50)
    stats = Database.get_analytics_summary()
    return render_template(
        "history.html",
        active_page="history",
        analyses=analyses,
        stats=stats
    )


@app.route("/guide")
def guide():
    """ATS Optimization & Modern Resume Engineering Guide."""
    return render_template(
        "guide.html",
        active_page="guide"
    )


# ---------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------

@app.route("/api/analyze-resume", methods=["POST"])
def api_analyze_resume():
    """
    Analyzes resume uploaded as PDF or submitted as raw text.
    Extracts text, metadata, runs multi-dimensional ATS scoring,
    persists in SQLite, and returns comprehensive JSON.
    """
    raw_text = ""
    word_count = 0
    page_count = 1

    # Check for file upload
    if "resume_file" in request.files:
        file = request.files["resume_file"]
        if file and file.filename != "":
            if not allowed_file(file.filename):
                return jsonify({"success": False, "error": "Invalid file type. Please upload a PDF or TXT file."}), 400
            
            filename = secure_filename(file.filename)
            ext = filename.rsplit(".", 1)[1].lower()

            if ext == "pdf":
                extracted = ResumeExtractor.extract_from_pdf(file.stream)
            else:
                text_content = file.read().decode("utf-8", errors="ignore")
                extracted = ResumeExtractor.extract_from_text(text_content)

            if not extracted.get("success"):
                return jsonify({"success": False, "error": extracted.get("error", "Failed to extract text.")}), 400

            raw_text = extracted["text"]
            word_count = extracted.get("word_count", len(raw_text.split()))
            page_count = extracted.get("page_count", 1)

    # Check for raw text input
    if not raw_text and "resume_text" in request.form:
        text_input = request.form["resume_text"].strip()
        if text_input:
            extracted = ResumeExtractor.extract_from_text(text_input)
            if not extracted.get("success"):
                return jsonify({"success": False, "error": extracted.get("error", "Text too short.")}), 400
            raw_text = extracted["text"]
            word_count = extracted.get("word_count", len(raw_text.split()))
            page_count = extracted.get("page_count", 1)

    if not raw_text:
        return jsonify({"success": False, "error": "No resume document or text was provided."}), 400

    # Parse candidate metadata (name, emails, phones, detected sections)
    metadata = ResumeExtractor.parse_metadata(raw_text)

    # Perform CareerIQ scoring & analysis
    analysis_data = CareerAnalyzer.compute_full_analysis(raw_text, metadata, word_count)
    analysis_data["word_count"] = word_count
    analysis_data["page_count"] = page_count

    # Save to SQLite database
    session_id = Database.save_analysis(analysis_data, metadata, raw_text)

    return jsonify({
        "success": True,
        "session_id": session_id,
        "metadata": metadata,
        "analysis": analysis_data
    })


@app.route("/api/compare-job", methods=["POST"])
def api_compare_job():
    """
    Compares candidate skills against job description text or preset.
    """
    data = request.get_json(silent=True) or request.form.to_dict()
    
    # Extract skills
    skills = data.get("skills", [])
    if isinstance(skills, str):
        # Could be JSON string or comma-separated
        try:
            skills = json.loads(skills)
        except Exception:
            skills = [s.strip() for s in skills.split(",") if s.strip()]

    # Extract job description
    preset_key = data.get("preset_key")
    jd_text = data.get("job_description", "")

    if preset_key and preset_key in SAMPLE_JOB_DESCRIPTIONS:
        jd_text = SAMPLE_JOB_DESCRIPTIONS[preset_key]["text"]

    if not jd_text or len(jd_text.strip()) < 30:
        return jsonify({"success": False, "error": "Please provide a job description with at least 30 characters."}), 400

    gap_analysis = CareerAnalyzer.compare_with_job_description(skills, jd_text)
    return jsonify({
        "success": True,
        "comparison": gap_analysis
    })


@app.route("/api/sample-resume", methods=["GET"])
def api_sample_resume():
    """Returns pre-loaded sample resumes for 1-click testing across multiple domains."""
    domain = request.args.get("domain", "software").lower()
    domain_file_map = {
        "software": "sample_resume.txt",
        "product": "sample_resume_product.txt",
        "data": "sample_resume_data.txt",
        "design": "sample_resume_design.txt",
        "marketing": "sample_resume_marketing.txt",
        "finance": "sample_resume_finance.txt",
        "hr": "sample_resume_hr.txt",
        "cybersecurity": "sample_resume_cybersecurity.txt"
    }
    filename = domain_file_map.get(domain, "sample_resume.txt")
    sample_path = Config.BASE_DIR / "data" / filename
    if sample_path.exists():
        with open(sample_path, "r", encoding="utf-8") as f:
            content = f.read()
        return jsonify({
            "success": True,
            "domain": domain,
            "filename": filename,
            "text": content
        })
    return jsonify({"success": False, "error": f"Sample resume for {domain} not found."}), 404


@app.route("/api/download-report/<session_id>", methods=["GET"])
def api_download_report(session_id: str):
    """Generates and streams the executive PDF report."""
    record = Database.get_analysis_by_session_id(session_id)
    if not record:
        flash("Analysis record not found.", "error")
        return redirect(url_for("dashboard"))

    analysis_data = {
        "overall_score": record.get("overall_score", 0),
        "primary_domain": record.get("top_domain", "Software & Cloud"),
        "dimensions": record.get("dimensions", {}),
        "skills": record.get("skills", {}),
        "metrics": {"count": record.get("word_count", 0)},
        "verbs": {"strong_count": 8},
        "role_matches": record.get("role_matches", []),
        "action_plan": record.get("action_plan", [])
    }
    metadata = {
        "candidate_name": record.get("candidate_name", "Candidate"),
        "email": record.get("email"),
        "phone": record.get("phone")
    }

    pdf_buffer = ReportGenerator.generate_pdf(analysis_data, metadata)
    candidate_slug = "".join(c for c in record.get("candidate_name", "Candidate") if c.isalnum() or c == "_")
    filename = f"CareerIQ_Report_{candidate_slug}_{session_id}.pdf"

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )


@app.route("/api/analysis/<session_id>", methods=["DELETE"])
def api_delete_analysis(session_id: str):
    """Deletes an analysis record."""
    success = Database.delete_analysis(session_id)
    return jsonify({"success": success})


@app.route("/health")
def health():
    """Health check endpoint for cloud monitoring."""
    return jsonify({
        "status": "healthy",
        "service": "CareerIQ - AI Career Intelligence Dashboard",
        "version": "1.0.0"
    }), 200


@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 handler."""
    return render_template("404.html"), 404


# ---------------------------------------------------------
# Application Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"[*] Starting CareerIQ Server on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
