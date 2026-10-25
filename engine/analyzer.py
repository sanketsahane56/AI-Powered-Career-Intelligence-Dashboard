"""
CareerIQ - Core Career Intelligence & ATS Scoring Engine
Provides transparent resume scoring, skill extraction, role matching,
and job description skill gap analysis without requiring third-party paid APIs.
"""

import re
from typing import Dict, Any, List, Set, Tuple
from collections import Counter
from engine.skills_taxonomy import (
    SKILLS_TAXONOMY,
    SKILL_ALIASES,
    CAREER_PROFILES,
    STRONG_ACTION_VERBS,
    WEAK_VERBS
)
from engine.extractor import ResumeExtractor


class CareerAnalyzer:
    """Analyzes resume text for ATS friendliness, technical skills, and market role fit."""

    # Metric detection regex (percentages, money, multipliers, metrics)
    METRIC_REGEX = re.compile(
        r"(\d+(?:\.\d+)?%|"
        r"\$\s*\d+(?:,\d+)*(?:\.\d+)?[kKmMbB]?|"
        r"\b\d+(?:\.\d+)?\s*[kKmMbB]\b|"
        r"\b\d+\s*(?:million|billion|users|customers|queries|requests|req/sec|tps|ms|seconds|x|fold)\b|"
        r"(?:increased|decreased|reduced|improved|boosted|grew|saved)\s+by\s+\d+)",
        re.IGNORECASE
    )

    @classmethod
    def extract_skills(cls, text: str) -> Dict[str, Any]:
        """
        Extracts verified technical and professional skills from text.
        Uses boundary-safe matching and taxonomy alias normalization.
        """
        normalized_text = f" {text.lower()} "
        found_skills_set: Set[str] = set()
        categorized_skills: Dict[str, List[str]] = {cat: [] for cat in SKILLS_TAXONOMY.keys()}

        # 1. Check direct taxonomy skills
        for category, skill_list in SKILLS_TAXONOMY.items():
            for skill in skill_list:
                # Use word boundaries for safe matching (special handling for C++, C#, .NET)
                escaped = re.escape(skill.lower())
                if skill.lower() in ["c++", "c#", ".net", "r", "c"]:
                    pattern = rf"(?:^|[\s,;/()\[\]]){escaped}(?:$|[\s,;/()\[\]])"
                else:
                    pattern = rf"\b{escaped}\b"

                if re.search(pattern, normalized_text, re.IGNORECASE):
                    # Canonical name
                    canonical = skill
                    found_skills_set.add(canonical)
                    if canonical not in categorized_skills[category]:
                        categorized_skills[category].append(canonical)

        # 2. Check alias map
        for alias, target in SKILL_ALIASES.items():
            escaped = re.escape(alias.lower())
            pattern = rf"\b{escaped}\b"
            if re.search(pattern, normalized_text, re.IGNORECASE):
                found_skills_set.add(target)
                # Find matching category for target
                for cat, skill_list in SKILLS_TAXONOMY.items():
                    if target in skill_list and target not in categorized_skills[cat]:
                        categorized_skills[cat].append(target)

        # Remove empty categories from display list
        active_categories = {k: v for k, v in categorized_skills.items() if len(v) > 0}

        return {
            "all_skills": sorted(list(found_skills_set)),
            "total_count": len(found_skills_set),
            "by_category": active_categories,
            "category_counts": {k: len(v) for k, v in categorized_skills.items()}
        }

    @classmethod
    def evaluate_metrics_and_impact(cls, text: str) -> Dict[str, Any]:
        """Evaluates quantified business and technical metrics within the resume."""
        matches = cls.METRIC_REGEX.findall(text)
        metric_snippets = [m if isinstance(m, str) else m[0] for m in matches]
        
        # Calculate impact score
        count = len(metric_snippets)
        if count >= 8:
            score = 100
            rating = "Exceptional"
            feedback = "Superb use of quantifiable metrics, financial numbers, and measurable performance results."
        elif count >= 5:
            score = 85
            rating = "Strong"
            feedback = "Good presence of measurable outcomes. A few more percentage improvements will make it stellar."
        elif count >= 2:
            score = 65
            rating = "Moderate"
            feedback = "Some measurable data present, but many achievements lack numeric scale (%, $, throughput, time saved)."
        elif count >= 1:
            score = 45
            rating = "Basic"
            feedback = "Only 1 quantifiable metric found. Modern ATS algorithms and hiring managers favor data-backed bullets."
        else:
            score = 25
            rating = "Needs Improvement"
            feedback = "No quantifiable metrics found! Transform generic duties into measurable accomplishments (e.g., 'reduced latency by 35%')."

        return {
            "score": score,
            "count": count,
            "rating": rating,
            "feedback": feedback,
            "examples_found": metric_snippets[:6]
        }

    @classmethod
    def evaluate_action_verbs(cls, text: str) -> Dict[str, Any]:
        """Evaluates the strength and variety of action verbs in resume sentences."""
        lower_text = text.lower()
        found_strong_verbs = []
        found_weak_phrases = []

        # Find strong verbs
        for group, verbs in STRONG_ACTION_VERBS.items():
            for verb in verbs:
                if re.search(rf"\b{verb}\b", lower_text):
                    found_strong_verbs.append((verb, group))

        # Find weak or passive phrases
        for weak in WEAK_VERBS:
            if weak in lower_text:
                found_weak_phrases.append(weak)

        strong_count = len(found_strong_verbs)
        weak_count = len(found_weak_phrases)

        # Base score on strong verbs minus penalty for weak phrases
        raw_score = min(100, (strong_count * 15)) - (weak_count * 8)
        score = max(20, min(100, raw_score))

        if score >= 80:
            rating = "Dynamic & Leadership-Driven"
            feedback = "Excellent active voice! You use authoritative action verbs that signal ownership and leadership."
        elif score >= 60:
            rating = "Good Action Voice"
            feedback = "Solid selection of action verbs. Consider swapping any passive descriptions with high-impact engineering terms."
        else:
            rating = "Passive Voice Detected"
            feedback = "Noticeable use of passive phrasing ('responsible for', 'assisted with'). Upgrade to strong verbs like 'architected', 'spearheaded', 'optimized'."

        return {
            "score": score,
            "strong_count": strong_count,
            "weak_count": weak_count,
            "rating": rating,
            "feedback": feedback,
            "strong_verbs": [v[0] for v in found_strong_verbs[:10]],
            "weak_phrases": found_weak_phrases
        }

    @classmethod
    def evaluate_structure(cls, metadata: Dict[str, Any], word_count: int) -> Dict[str, Any]:
        """Evaluates section completeness and ATS document format."""
        sections = metadata.get("detected_sections", {})
        score = 0
        missing = []
        present = []

        section_weights = {
            "experience": 30,
            "skills": 25,
            "education": 20,
            "projects": 15,
            "summary": 10
        }

        for sec, weight in section_weights.items():
            if sections.get(sec, False):
                score += weight
                present.append(sec.title())
            else:
                missing.append(sec.title())

        # Contact info check
        has_email = bool(metadata.get("email"))
        has_phone = bool(metadata.get("phone"))
        has_links = bool(metadata.get("linkedin") or metadata.get("github"))

        contact_score = 100 if (has_email and has_phone and has_links) else (70 if (has_email and has_phone) else 40)

        # Word count check (Ideal 350-1000 words)
        if 400 <= word_count <= 950:
            length_rating = "Optimal (1-2 pages)"
            length_score = 100
        elif 250 <= word_count < 400 or 950 < word_count <= 1400:
            length_rating = "Acceptable"
            length_score = 80
        else:
            length_rating = "Suboptimal (Too short or excessively long)"
            length_score = 50

        # Combine section, contact, and length into structure score
        final_structure_score = int((score * 0.5) + (contact_score * 0.3) + (length_score * 0.2))

        return {
            "score": final_structure_score,
            "sections_present": present,
            "sections_missing": missing,
            "has_email": has_email,
            "has_phone": has_phone,
            "has_links": has_links,
            "length_rating": length_rating,
            "feedback": f"Detected {len(present)} of 5 standard ATS sections. " + (f"Missing sections: {', '.join(missing)}." if missing else "All key sections detected!")
        }

    @classmethod
    def compute_full_analysis(cls, text: str, metadata: Dict[str, Any], word_count: int) -> Dict[str, Any]:
        """
        Runs the comprehensive transparent multi-dimensional analysis on the candidate resume.
        Computes overall CareerIQ score and detailed sub-metrics.
        """
        # 1. Skill extraction
        skills_data = cls.extract_skills(text)
        skill_count = skills_data["total_count"]
        
        # Skill breadth score (0-100)
        # 18+ skills with category diversity yields 100
        cat_count = sum(1 for c in skills_data["category_counts"].values() if c > 0)
        skill_score = min(100, int((min(skill_count, 18) / 18 * 70) + (min(cat_count, 5) / 5 * 30)))

        # 2. Metric & Impact evaluation
        metrics_data = cls.evaluate_metrics_and_impact(text)

        # 3. Action verbs evaluation
        verbs_data = cls.evaluate_action_verbs(text)

        # 4. Structure & completeness
        structure_data = cls.evaluate_structure(metadata, word_count)

        # 5. Readability & ATS formatting
        # Formatting score based on bullet structure and absence of parsing errors
        has_bullets = bool(re.search(r"[•\-\*]\s+[A-Z]", text))
        readability_score = 90 if has_bullets else 70

        # Overall CareerIQ Weighted Score
        # Skills: 30%, Impact: 25%, Verbs: 20%, Structure: 15%, Readability: 10%
        overall_score = int(
            (skill_score * 0.30) +
            (metrics_data["score"] * 0.25) +
            (verbs_data["score"] * 0.20) +
            (structure_data["score"] * 0.15) +
            (readability_score * 0.10)
        )

        # Career Role Matching
        role_matches = cls.match_career_roles(skills_data["all_skills"])

        # Construct actionable recommendations list
        action_plan = []
        if skill_score < 75:
            action_plan.append("Expand technical skills section with cloud/DevOps tools (Docker, CI/CD, AWS) or relational databases.")
        if metrics_data["score"] < 70:
            action_plan.append("Incorporate at least 4-6 quantified metrics (percentages, revenue, performance improvements, team sizes) in work history.")
        if verbs_data["score"] < 75:
            action_plan.append("Replace passive phrases ('responsible for', 'handled') with impactful action verbs ('architected', 'spearheaded', 'optimized').")
        if structure_data["sections_missing"]:
            action_plan.append(f"Add missing standard ATS sections: {', '.join(structure_data['sections_missing'])}.")
        if not structure_data["has_links"]:
            action_plan.append("Include clickable links to your GitHub profile and LinkedIn page in your contact header.")
        if not action_plan:
            action_plan.append("Your resume meets top-tier ATS standards! Tailor specific keywords for each job application.")

        return {
            "overall_score": overall_score,
            "dimensions": {
                "skill_breadth": {
                    "name": "Skill Breadth & Diversity",
                    "score": skill_score,
                    "weight": "30%",
                    "detail": f"{skill_count} verified skills across {cat_count} categories"
                },
                "impact_metrics": {
                    "name": "Quantifiable Impact & Data",
                    "score": metrics_data["score"],
                    "weight": "25%",
                    "detail": f"{metrics_data['count']} measurable metrics identified"
                },
                "action_verbs": {
                    "name": "Action Verbs & Voice",
                    "score": verbs_data["score"],
                    "weight": "20%",
                    "detail": f"{verbs_data['strong_count']} strong verbs, {verbs_data['weak_count']} passive phrases"
                },
                "structure": {
                    "name": "ATS Structure & Completeness",
                    "score": structure_data["score"],
                    "weight": "15%",
                    "detail": f"{len(structure_data['sections_present'])}/5 standard sections detected"
                },
                "readability": {
                    "name": "Readability & Format",
                    "score": readability_score,
                    "weight": "10%",
                    "detail": "Standard ATS-friendly layout with bullet points"
                }
            },
            "skills": skills_data,
            "metrics": metrics_data,
            "verbs": verbs_data,
            "structure": structure_data,
            "role_matches": role_matches,
            "action_plan": action_plan
        }

    @classmethod
    def match_career_roles(cls, candidate_skills: List[str]) -> List[Dict[str, Any]]:
        """Compares candidate skills against industry standard career profiles."""
        cand_set = set(candidate_skills)
        matches = []

        for role_name, profile in CAREER_PROFILES.items():
            core_skills = profile["core_skills"]
            secondary_skills = profile["secondary_skills"]

            matched_core = [s for s in core_skills if s in cand_set]
            missing_core = [s for s in core_skills if s not in cand_set]

            matched_sec = [s for s in secondary_skills if s in cand_set]
            missing_sec = [s for s in secondary_skills if s not in cand_set]

            # Weighted compatibility: core counts for 70%, secondary for 30%
            core_ratio = len(matched_core) / max(len(core_skills), 1)
            sec_ratio = len(matched_sec) / max(len(secondary_skills), 1)
            fit_percentage = int((core_ratio * 70) + (sec_ratio * 30))

            matches.append({
                "role": role_name,
                "icon": profile["icon"],
                "description": profile["description"],
                "fit_percentage": fit_percentage,
                "matched_core": matched_core,
                "missing_core": missing_core,
                "matched_secondary": matched_sec,
                "missing_secondary": missing_sec,
                "core_count": f"{len(matched_core)}/{len(core_skills)}"
            })

        # Sort by best fit percentage descending
        matches.sort(key=lambda x: x["fit_percentage"], reverse=True)
        return matches

    @classmethod
    def compare_with_job_description(cls, resume_skills: List[str], jd_text: str) -> Dict[str, Any]:
        """
        Deep comparison between candidate resume skills and a specific Job Description (JD).
        Returns match percentage, matched skills, missing skills, and category radar data.
        """
        jd_skills_data = cls.extract_skills(jd_text)
        jd_skills = jd_skills_data["all_skills"]

        resume_set = set(resume_skills)
        jd_set = set(jd_skills)

        matched = sorted(list(resume_set.intersection(jd_set)))
        missing = sorted(list(jd_set.difference(resume_set)))
        extra = sorted(list(resume_set.difference(jd_set)))

        match_score = int((len(matched) / max(len(jd_skills), 1)) * 100) if jd_skills else 0

        # Compute category distribution for Radar Chart
        categories = list(SKILLS_TAXONOMY.keys())
        radar_labels = [c.replace(" & ", "\n& ") for c in categories]
        resume_category_counts = []
        jd_category_counts = []

        for cat in categories:
            cat_skills = set(SKILLS_TAXONOMY[cat])
            # Resume count in this category
            r_count = len(resume_set.intersection(cat_skills))
            # JD count in this category
            j_count = len(jd_set.intersection(cat_skills))

            resume_category_counts.append(r_count)
            jd_category_counts.append(j_count)

        # Strategic advice
        advice = []
        if missing:
            priority_missing = missing[:5]
            advice.append(f"High-priority missing keywords to add if you possess them: {', '.join(priority_missing)}.")
        if match_score >= 80:
            advice.append("Outstanding match! Your profile aligns directly with the core qualifications of this role.")
        elif match_score >= 60:
            advice.append("Solid alignment. Bridging 2-3 missing skills will significantly increase your callback odds.")
        else:
            advice.append("Moderate skill overlap. Tailor your resume summary and projects to prominently display the target competencies.")

        return {
            "match_score": match_score,
            "matched_skills": matched,
            "missing_skills": missing,
            "extra_skills": extra,
            "total_jd_skills": len(jd_skills),
            "matched_count": len(matched),
            "missing_count": len(missing),
            "radar_data": {
                "labels": radar_labels,
                "resume_counts": resume_category_counts,
                "jd_counts": jd_category_counts
            },
            "advice": advice
        }
