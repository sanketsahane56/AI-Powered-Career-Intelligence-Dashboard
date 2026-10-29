"""
Unit Tests for Career Intelligence Analyzer & ATS Engine
"""
import pytest
from engine.analyzer import CareerAnalyzer


def test_extract_skills():
    text = """
    Proficient in Python, JavaScript, TypeScript, React, Next.js, and Docker.
    Built microservices with PostgreSQL, Redis, and deployed to AWS.
    Experienced in machine learning with PyTorch and scikit-learn.
    """
    skills_data = CareerAnalyzer.extract_skills(text)
    skills = skills_data["all_skills"]

    assert "Python" in skills
    assert "React" in skills
    assert "TypeScript" in skills
    assert "Docker" in skills
    assert "PostgreSQL" in skills
    assert "AWS" in skills
    assert "PyTorch" in skills
    assert skills_data["total_count"] >= 8


def test_evaluate_metrics():
    text = "Boosted API response time by 45%, managed a $500k cloud budget, and scaled to 2M active users."
    metrics = CareerAnalyzer.evaluate_metrics_and_impact(text)
    assert metrics["count"] >= 3
    assert metrics["score"] >= 65


def test_evaluate_action_verbs():
    text = "Spearheaded platform migration, architected microservices, and optimized latency."
    verbs = CareerAnalyzer.evaluate_action_verbs(text)
    assert verbs["strong_count"] >= 3
    assert verbs["score"] >= 40


def test_compute_full_analysis():
    sample_text = """
    Alex Johnson
    alex@test.com | (555) 987-6543
    linkedin.com/in/alex-j | github.com/alex-j

    PROFESSIONAL SUMMARY
    Full Stack Engineer with 5 years experience scaling web applications.

    SKILLS
    Python, JavaScript, TypeScript, React, Node.js, PostgreSQL, Docker, AWS, Git, CI/CD

    EXPERIENCE
    • Architected high-performance web APIs with Python and React, increasing throughput by 35%.
    • Spearheaded database optimization with PostgreSQL and Redis, saving $50k annually.
    • Deployed containerized applications with Docker and Kubernetes to AWS.

    EDUCATION
    BS in Computer Science.
    """
    metadata = {
        "candidate_name": "Alex Johnson",
        "email": "alex@test.com",
        "phone": "(555) 987-6543",
        "linkedin": "https://linkedin.com/in/alex-j",
        "github": "https://github.com/alex-j",
        "detected_sections": {"experience": True, "skills": True, "education": True, "summary": True, "projects": False}
    }
    analysis = CareerAnalyzer.compute_full_analysis(sample_text, metadata, len(sample_text.split()))

    assert 50 <= analysis["overall_score"] <= 100
    assert "dimensions" in analysis
    assert len(analysis["role_matches"]) > 0
    assert analysis["role_matches"][0]["fit_percentage"] > 50


def test_compare_with_job_description():
    resume_skills = ["Python", "React", "PostgreSQL", "Docker", "Git"]
    jd_text = """
    We require an engineer with Python, React, PostgreSQL, Docker, Kubernetes, AWS, and Redis.
    """
    comp = CareerAnalyzer.compare_with_job_description(resume_skills, jd_text)
    
    assert comp["match_score"] > 40
    assert "Python" in comp["matched_skills"]
    assert "React" in comp["matched_skills"]
    assert "Kubernetes" in comp["missing_skills"]
    assert "AWS" in comp["missing_skills"]
    assert len(comp["radar_data"]["labels"]) > 0


def test_multi_domain_skill_extraction():
    pm_text = """
    Priya Sharma | Product Manager
    Skilled in Product Strategy, Product Roadmapping, PRD, User Stories, Agile, Scrum, Jira, and OKRs.
    Led A/B Testing experiments and customer discovery sessions in Figma.
    """
    skills_data = CareerAnalyzer.extract_skills(pm_text)
    skills = skills_data["all_skills"]
    assert "Product Strategy" in skills
    assert "Product Roadmapping" in skills
    assert "PRD" in skills
    assert "User Stories" in skills
    assert "Agile" in skills
    assert "Scrum" in skills
    assert "Jira" in skills
    assert "A/B Testing" in skills
    assert "Figma" in skills


def test_multi_domain_role_matching():
    # Product manager profile test
    pm_skills = ["Product Strategy", "Product Roadmapping", "PRD", "User Stories", "Agile", "Scrum", "Jira", "Stakeholder Management", "A/B Testing"]
    matches = CareerAnalyzer.match_career_roles(pm_skills)
    assert len(matches) > 0
    top_role = matches[0]
    assert top_role["role"] == "Product Manager"
    assert top_role["domain"] == "Product & Project Management"
    assert top_role["fit_percentage"] >= 70

    # Domain filtered matching test
    tech_matches = CareerAnalyzer.match_career_roles(pm_skills, target_domain="Software & Cloud")
    assert all(r["domain"] == "Software & Cloud" for r in tech_matches)


def test_domain_affinity_computation():
    role_matches = [
        {"role": "Product Manager", "domain": "Product & Project Management", "fit_percentage": 90},
        {"role": "Technical Project Manager", "domain": "Product & Project Management", "fit_percentage": 80},
        {"role": "Full Stack Engineer", "domain": "Software & Cloud", "fit_percentage": 25}
    ]
    affinities = CareerAnalyzer.compute_domain_affinities(role_matches)
    assert affinities["primary_domain"] == "Product & Project Management"
    assert affinities["top_domain_fit"] >= 80

