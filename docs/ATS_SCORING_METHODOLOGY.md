# ATS Scoring Methodology & Formula Specifications

CareerIQ scores resumes using a transparent, multi-factor rubric based on industry Applicant Tracking System (ATS) parsing rules, hiring manager preferences, and recruiter screen criteria.

---

## 🧮 Overall ATS Score Formula

The Overall ATS Score ($S_{\text{overall}}$) is a weighted sum of 5 independent dimensions:

$$S_{\text{overall}} = (0.30 \times S_{\text{skills}}) + (0.25 \times S_{\text{metrics}}) + (0.20 \times S_{\text{verbs}}) + (0.15 \times S_{\text{structure}}) + (0.10 \times S_{\text{readability}})$$

---

## 📐 Dimension Breakdowns

### 1. Skill Breadth & Diversity (30%)
- **Objective**: Evaluates whether the candidate has broad competency across relevant categories (Languages, Frameworks, Cloud, Databases, Tooling).
- **Scale**:
  - 15+ verified skills across 4+ categories: **100%**
  - 10–14 verified skills: **85%**
  - 6–9 verified skills: **70%**
  - 3–5 verified skills: **50%**
  - <3 skills: **30%**

### 2. Quantifiable Impact & Metrics (25%)
- **Objective**: Identifies measurable accomplishments ($ values, percentages, scale, throughput, efficiency gains).
- **Scale**:
  - 8+ metrics found: **100%**
  - 5–7 metrics: **85%**
  - 2–4 metrics: **65%**
  - 1 metric: **45%**
  - 0 metrics: **25%**

### 3. Action Verbs & Voice (20%)
- **Objective**: Penalizes passive phrasing (e.g., "responsible for", "assisted with") and rewards active engineering and leadership verbs (e.g., "architected", "engineered", "spearheaded").
- **Scale**:
  - Base score: $S_{\text{verbs}} = \min(100, \text{strong\_count} \times 12) - (\text{weak\_count} \times 8)$

### 4. ATS Structure & Completeness (15%)
- **Objective**: Confirms that standard ATS section headings and contact fields exist.
- Standard sections: Experience, Education, Skills, Projects, Summary.
- Missing any section results in deductions; presence of portfolio links rewards bonus points.

### 5. Readability & Formatting (10%)
- **Objective**: Evaluates word density, concise bullet structure, and optimal length (300–800 words).
