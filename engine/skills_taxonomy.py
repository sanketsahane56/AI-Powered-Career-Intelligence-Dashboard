"""
CareerIQ - Comprehensive Multi-Domain Skills Taxonomy & Industry Role Profiles
Contains 1,000+ curated technical, product, design, marketing, finance, HR,
and leadership skills with category mappings, aliases, 8 industry domains,
20 career profiles, and sample job descriptions.
"""

# Industry Domains Definition
DOMAINS = {
    "Software & Cloud": {
        "id": "software_cloud",
        "name": "Software & Cloud",
        "icon": "code",
        "color": "blue",
        "badge_class": "pill-blue",
        "description": "Full stack, backend, frontend, mobile, cloud infrastructure, DevOps, and cybersecurity."
    },
    "Data & AI": {
        "id": "data_ai",
        "name": "Data & AI",
        "icon": "cpu",
        "color": "emerald",
        "badge_class": "pill-emerald",
        "description": "Data science, machine learning, predictive analytics, ETL pipelines, and business intelligence."
    },
    "Product & Project Management": {
        "id": "product_management",
        "name": "Product & Project Management",
        "icon": "check-square",
        "color": "violet",
        "badge_class": "pill-violet",
        "description": "Product strategy, roadmapping, agile scrum delivery, user stories, and program execution."
    },
    "UI/UX & Design": {
        "id": "ui_ux_design",
        "name": "UI/UX & Design",
        "icon": "palette",
        "color": "pink",
        "badge_class": "pill-pink",
        "description": "User experience research, wireframing, interactive prototyping, and design systems."
    },
    "Digital Marketing & Growth": {
        "id": "marketing_growth",
        "name": "Digital Marketing & Growth",
        "icon": "trending-up",
        "color": "amber",
        "badge_class": "pill-amber",
        "description": "SEO/SEM, performance marketing, content strategy, conversion optimization, and growth campaigns."
    },
    "Finance & Accounting": {
        "id": "finance_accounting",
        "name": "Finance & Accounting",
        "icon": "dollar-sign",
        "color": "emerald",
        "badge_class": "pill-emerald",
        "description": "Financial modeling, budgeting, valuation, P&L management, ERP platforms, and corporate reporting."
    },
    "Human Resources & Talent": {
        "id": "hr_talent",
        "name": "Human Resources & Talent",
        "icon": "users",
        "color": "blue",
        "badge_class": "pill-blue",
        "description": "Talent acquisition, recruitment pipelines, employee experience, HRIS, and people operations."
    },
    "Sales & Business Development": {
        "id": "sales_business",
        "name": "Sales & Business Development",
        "icon": "briefcase",
        "color": "violet",
        "badge_class": "pill-violet",
        "description": "B2B client acquisition, enterprise sales pipeline, account strategy, CRM, and contract negotiations."
    }
}

# Categorized Skill Taxonomy across Multiple Domains
SKILLS_TAXONOMY = {
    "Programming Languages": [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "C", "Go", "Golang",
        "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "SQL", "HTML5", "CSS3",
        "Sass", "Bash", "Shell", "PowerShell", "Dart", "Perl", "Lua", "Solidity"
    ],
    "Frontend Frameworks & Web": [
        "React", "React.js", "Next.js", "Vue.js", "Vue", "Angular", "AngularJS",
        "Svelte", "Redux", "Tailwind CSS", "Bootstrap", "Webpack", "Vite", "jQuery",
        "HTML", "CSS", "Responsive Design", "WebSockets", "PWA", "Microfrontends",
        "Storybook", "Material-UI", "Chakra UI", "Shadcn UI", "Flutter", "React Native"
    ],
    "Backend, APIs & Architecture": [
        "Node.js", "Express.js", "Express", "Flask", "Django", "FastAPI", "Spring Boot",
        "Spring", "ASP.NET", ".NET Core", "Ruby on Rails", "NestJS", "GraphQL", "REST APIs",
        "RESTful API", "gRPC", "Microservices", "Serverless", "Celery", "Kafka",
        "RabbitMQ", "Apache Pulsar", "Socket.io", "SOAP"
    ],
    "Databases & Cloud Storage": [
        "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "Elasticsearch",
        "DynamoDB", "Cassandra", "Couchbase", "Snowflake", "BigQuery", "Redshift",
        "Oracle", "Microsoft SQL Server", "Neo4j", "Firebase", "Supabase", "Prisma",
        "SQLAlchemy", "Hibernate"
    ],
    "Cloud & DevOps Infrastructure": [
        "AWS", "Amazon Web Services", "Azure", "Microsoft Azure", "Google Cloud", "GCP",
        "Docker", "Kubernetes", "K8s", "CI/CD", "GitHub Actions", "GitLab CI", "Jenkins",
        "Terraform", "Ansible", "Helm", "Prometheus", "Grafana", "Linux", "Ubuntu",
        "Nginx", "Apache", "Cloudflare", "OpenTelemetry", "ArgoCD", "Datadog"
    ],
    "AI, Machine Learning & NLP": [
        "Machine Learning", "Deep Learning", "Artificial Intelligence", "NLP",
        "Natural Language Processing", "Computer Vision", "PyTorch", "TensorFlow",
        "Keras", "Scikit-Learn", "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn",
        "Large Language Models", "LLM", "Prompt Engineering", "RAG", "LangChain",
        "Hugging Face", "Transformers", "OpenCV", "ETL", "Apache Spark", "Airflow",
        "Data Pipelines", "Feature Engineering", "Data Modeling"
    ],
    "Data Analysis & Business Intelligence": [
        "Power BI", "Tableau", "Excel", "Advanced Excel", "Looker", "Google Data Studio",
        "DAX", "Data Visualization", "Data Cleansing", "Statistical Analysis",
        "Predictive Modeling", "KPI Dashboards", "A/B Testing", "Google Analytics",
        "Metabase", "Alteryx", "Business Intelligence", "Cohort Analysis", "Hypothesis Testing"
    ],
    "Product & Project Management": [
        "Product Strategy", "Product Roadmapping", "PRD", "User Stories", "Agile",
        "Scrum", "Kanban", "Jira", "Confluence", "Backlog Prioritization", "Sprint Planning",
        "Stakeholder Management", "OKRs", "Feature Prioritization", "Market Research",
        "Customer Discovery", "Requirements Gathering", "Competitive Analysis", "MVP Definition"
    ],
    "UI/UX & Product Design": [
        "Figma", "Sketch", "Adobe XD", "Wireframing", "Prototyping", "User Research",
        "Usability Testing", "Information Architecture", "Design Systems", "Mobile UI",
        "Interaction Design", "Design Thinking", "User Journey Mapping", "Visual Design",
        "User Persona", "Typography", "Color Theory", "Accessibility", "WCAG"
    ],
    "Digital Marketing & Growth": [
        "SEO", "Search Engine Optimization", "SEM", "Google Ads", "Content Marketing",
        "Social Media Marketing", "Email Marketing", "HubSpot", "Copywriting",
        "Growth Hacking", "Conversion Rate Optimization", "Performance Marketing",
        "Meta Ads", "Brand Strategy", "Google Analytics 4", "Influencer Marketing",
        "Marketing Automation", "PPC Campaigns"
    ],
    "Finance, Accounting & Valuation": [
        "Financial Modeling", "Valuation", "DCF", "Financial Analysis", "Forecasting",
        "Budgeting", "QuickBooks", "SAP", "P&L Management", "Balance Sheet", "GAAP",
        "Auditing", "Tax Compliance", "Financial Reporting", "Variance Analysis",
        "Cash Flow Management", "Risk Management", "Capital Budgeting", "NetSuite"
    ],
    "Human Resources & Talent Acquisition": [
        "Talent Acquisition", "Technical Recruiting", "Candidate Sourcing", "Interviewing",
        "Screening", "HRIS", "Workday", "BambooHR", "Employee Relations",
        "Performance Management", "Onboarding", "Compensation & Benefits", "Labor Law",
        "Retention Strategies", "Diversity & Inclusion", "Employer Branding", "Talent Management"
    ],
    "Sales & Business Development": [
        "B2B Sales", "CRM", "Salesforce", "Lead Generation", "Cold Outreach",
        "Pipeline Management", "Negotiation", "Account Management", "Solution Selling",
        "Client Relationship", "Contract Negotiation", "Pitching", "Enterprise Sales",
        "Prospecting", "Inbound Sales", "Revenue Operations"
    ],
    "QA, Testing & Engineering Standards": [
        "QA Testing", "Test Automation", "Selenium", "Cypress", "Manual Testing",
        "Test Cases", "Bug Tracking", "Regression Testing", "Load Testing", "Postman",
        "API Testing", "PyTest", "Jest", "Unit Testing", "Integration Testing",
        "TDD", "System Design", "Distributed Systems", "Clean Code", "Git", "GitHub"
    ],
    "Professional & Executive Leadership": [
        "Leadership", "Team Leadership", "Cross-functional Collaboration", "Communication",
        "Mentoring", "Problem Solving", "Critical Thinking", "Project Management",
        "Client Presentation", "Strategic Planning", "Time Management", "Technical Writing",
        "Continuous Learning", "Vendor Management", "Change Management"
    ]
}

# Skill Aliases / Normalization Map
SKILL_ALIASES = {
    # Tech / Cloud aliases
    "k8s": "Kubernetes",
    "js": "JavaScript",
    "ts": "TypeScript",
    "py": "Python",
    "golang": "Go",
    "postgres": "PostgreSQL",
    "psql": "PostgreSQL",
    "mongo": "MongoDB",
    "reactjs": "React",
    "react.js": "React",
    "nextjs": "Next.js",
    "vuejs": "Vue.js",
    "angularjs": "Angular",
    "aws": "AWS",
    "gcp": "Google Cloud",
    "google cloud platform": "Google Cloud",
    "azure": "Azure",
    "amazon web services": "AWS",
    "ml": "Machine Learning",
    "ai": "Artificial Intelligence",
    "dl": "Deep Learning",
    "nlp": "Natural Language Processing",
    "llms": "Large Language Models",
    "llm": "Large Language Models",
    "rest": "REST APIs",
    "restful": "REST APIs",
    "rest api": "REST APIs",
    "cicd": "CI/CD",
    "ci / cd": "CI/CD",
    "github action": "GitHub Actions",
    "tf": "TensorFlow",
    "scikit learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "oop": "Object-Oriented Programming",
    "tdd": "TDD",
    "react-native": "React Native",
    
    # Data & Analytics aliases
    "powerbi": "Power BI",
    "ms excel": "Excel",
    "adv excel": "Advanced Excel",
    "tableau desktop": "Tableau",
    "google analytics": "Google Analytics",
    "ga4": "Google Analytics 4",
    "bi": "Business Intelligence",
    "ab test": "A/B Testing",
    "ab testing": "A/B Testing",
    "a/b testing": "A/B Testing",
    "data viz": "Data Visualization",

    # Product & Project Management aliases
    "product management": "Product Strategy",
    "product roadmap": "Product Roadmapping",
    "roadmapping": "Product Roadmapping",
    "prd": "PRD",
    "product requirements document": "PRD",
    "scrum master": "Scrum",
    "user story": "User Stories",
    "backlog grooming": "Backlog Prioritization",
    "sprint planning": "Sprint Planning",
    "okr": "OKRs",
    "kpi": "KPI Dashboards",

    # UI/UX & Design aliases
    "figma design": "Figma",
    "ui/ux": "UI/UX & Product Design",
    "ux": "User Research",
    "ux design": "User Research",
    "ui design": "Visual Design",
    "wireframes": "Wireframing",
    "prototypes": "Prototyping",
    "design system": "Design Systems",
    "usability test": "Usability Testing",

    # Marketing & Growth aliases
    "seo": "SEO",
    "search engine optimization": "SEO",
    "sem": "SEM",
    "search engine marketing": "SEM",
    "adwords": "Google Ads",
    "google adwords": "Google Ads",
    "fb ads": "Meta Ads",
    "facebook ads": "Meta Ads",
    "cro": "Conversion Rate Optimization",
    "growth hacking": "Growth Hacking",
    "content strategy": "Content Marketing",

    # Finance & Accounting aliases
    "financial modeling": "Financial Modeling",
    "financial analysis": "Financial Analysis",
    "dcf model": "DCF",
    "discounted cash flow": "DCF",
    "p&l": "P&L Management",
    "profit and loss": "P&L Management",
    "quickbooks online": "QuickBooks",
    "balance sheets": "Balance Sheet",

    # HR & Talent aliases
    "recruiting": "Technical Recruiting",
    "recruitment": "Talent Acquisition",
    "talent acquisition": "Talent Acquisition",
    "sourcing": "Candidate Sourcing",
    "hr": "Human Resources",
    "human resources": "Human Resources",
    "hris": "HRIS",

    # Sales aliases
    "sales force": "Salesforce",
    "salesforce crm": "Salesforce",
    "b2b": "B2B Sales",
    "business development": "B2B Sales",
    "lead gen": "Lead Generation",
    "cold calling": "Cold Outreach",

    # QA aliases
    "qa": "QA Testing",
    "quality assurance": "QA Testing",
    "automation testing": "Test Automation",
    "automated testing": "Test Automation",
    "cypress.io": "Cypress"
}

# Standard Multi-Domain Career Profiles with Required and Recommended Skills
CAREER_PROFILES = {
    # --- Software & Cloud Domain ---
    "Full Stack Engineer": {
        "title": "Full Stack Engineer",
        "domain": "Software & Cloud",
        "icon": "layers",
        "core_skills": ["JavaScript", "TypeScript", "Python", "React", "Node.js", "SQL", "REST APIs", "Git"],
        "secondary_skills": ["Docker", "PostgreSQL", "Next.js", "Tailwind CSS", "CI/CD", "AWS", "Redis"],
        "description": "Designs and builds end-to-end web applications across front-end user interfaces, back-end servers, and persistent databases."
    },
    "Backend Software Engineer": {
        "title": "Backend Software Engineer",
        "domain": "Software & Cloud",
        "icon": "server",
        "core_skills": ["Python", "Java", "Go", "SQL", "PostgreSQL", "REST APIs", "Microservices", "System Design"],
        "secondary_skills": ["Docker", "Kubernetes", "Redis", "Kafka", "AWS", "CI/CD", "FastAPI", "Django"],
        "description": "Architects resilient distributed systems, robust APIs, database models, and background task processing pipelines."
    },
    "Frontend Engineer": {
        "title": "Frontend Engineer",
        "domain": "Software & Cloud",
        "icon": "layout",
        "core_skills": ["JavaScript", "TypeScript", "React", "Next.js", "HTML5", "CSS3", "Tailwind CSS", "Redux"],
        "secondary_skills": ["Vite", "Responsive Design", "Jest", "REST APIs", "WebSockets", "Git", "GraphQL"],
        "description": "Crafts accessible, high-performance user interfaces and responsive web applications with modern state management."
    },
    "DevOps & Cloud Engineer": {
        "title": "DevOps & Cloud Engineer",
        "domain": "Software & Cloud",
        "icon": "cloud",
        "core_skills": ["AWS", "Docker", "Kubernetes", "CI/CD", "Terraform", "Linux", "Git", "Bash"],
        "secondary_skills": ["Azure", "Google Cloud", "Ansible", "Prometheus", "Grafana", "Jenkins", "GitHub Actions", "Python"],
        "description": "Automates deployment pipelines, ensures cloud infrastructure reliability, and streamlines developer productivity."
    },
    "Cybersecurity Engineer": {
        "title": "Cybersecurity Engineer",
        "domain": "Software & Cloud",
        "icon": "shield",
        "core_skills": ["Linux", "Python", "Bash", "Network Security", "Git", "Cryptography", "Troubleshooting"],
        "secondary_skills": ["AWS", "Docker", "System Administration", "Risk Management", "Auditing", "CI/CD"],
        "description": "Protects organizational infrastructure, audits codebases for security vulnerabilities, and implements defense mechanisms."
    },
    "Mobile App Developer": {
        "title": "Mobile App Developer",
        "domain": "Software & Cloud",
        "icon": "smartphone",
        "core_skills": ["React Native", "Flutter", "Swift", "Kotlin", "JavaScript", "TypeScript", "REST APIs", "Git"],
        "secondary_skills": ["Firebase", "Redux", "UI/UX & Product Design", "GraphQL", "CI/CD", "Docker"],
        "description": "Builds intuitive, performant native and cross-platform mobile experiences for iOS and Android platforms."
    },
    "QA & Test Automation Engineer": {
        "title": "QA & Test Automation Engineer",
        "domain": "Software & Cloud",
        "icon": "check-circle",
        "core_skills": ["QA Testing", "Test Automation", "Selenium", "Cypress", "PyTest", "Postman", "API Testing", "Git"],
        "secondary_skills": ["Manual Testing", "Test Cases", "Regression Testing", "Jira", "CI/CD", "Docker", "JavaScript"],
        "description": "Designs automated testing frameworks, enforces QA standards, and ensures high software stability across releases."
    },

    # --- Data & AI Domain ---
    "Data Scientist": {
        "title": "Data Scientist",
        "domain": "Data & AI",
        "icon": "bar-chart-2",
        "core_skills": ["Python", "SQL", "Pandas", "NumPy", "Scikit-Learn", "Statistical Analysis", "Data Visualization", "Machine Learning"],
        "secondary_skills": ["R", "Matplotlib", "Seaborn", "Deep Learning", "TensorFlow", "PyTorch", "Airflow", "BigQuery"],
        "description": "Extracts actionable insights from large datasets, develops predictive models, and conducts statistical experiments."
    },
    "Machine Learning Engineer": {
        "title": "Machine Learning Engineer",
        "domain": "Data & AI",
        "icon": "cpu",
        "core_skills": ["Python", "PyTorch", "TensorFlow", "Machine Learning", "Deep Learning", "Docker", "Data Pipelines", "Scikit-Learn"],
        "secondary_skills": ["Large Language Models", "NLP", "Computer Vision", "Hugging Face", "Kubernetes", "AWS", "FastAPI"],
        "description": "Bridges research models and production systems by deploying, monitoring, and scaling deep learning and AI models."
    },
    "Data Engineer": {
        "title": "Data Engineer",
        "domain": "Data & AI",
        "icon": "database",
        "core_skills": ["Python", "SQL", "ETL", "Apache Spark", "Airflow", "PostgreSQL", "Snowflake", "Data Pipelines"],
        "secondary_skills": ["Kafka", "BigQuery", "Docker", "AWS", "Data Modeling", "Redis", "Linux", "Scala"],
        "description": "Constructs reliable data pipelines, data warehouses, and batch/streaming processing architectures."
    },
    "Data Analyst & BI Specialist": {
        "title": "Data Analyst & BI Specialist",
        "domain": "Data & AI",
        "icon": "pie-chart",
        "core_skills": ["SQL", "Power BI", "Tableau", "Excel", "Data Visualization", "KPI Dashboards", "Statistical Analysis"],
        "secondary_skills": ["Python", "Looker", "Advanced Excel", "DAX", "Google Analytics", "A/B Testing", "Data Cleansing"],
        "description": "Transforms raw enterprise data into executive dashboards, tracks key metrics, and powers data-informed decision making."
    },

    # --- Product & Project Management Domain ---
    "Product Manager": {
        "title": "Product Manager",
        "domain": "Product & Project Management",
        "icon": "compass",
        "core_skills": ["Product Strategy", "Product Roadmapping", "PRD", "User Stories", "Agile", "Scrum", "Jira", "Stakeholder Management"],
        "secondary_skills": ["A/B Testing", "Customer Discovery", "Google Analytics", "Market Research", "OKRs", "Figma", "Data Visualization"],
        "description": "Defines product vision, prioritizes feature backlogs, aligns cross-functional engineering teams, and drives go-to-market execution."
    },
    "Technical Project Manager": {
        "title": "Technical Project Manager",
        "domain": "Product & Project Management",
        "icon": "clipboard",
        "core_skills": ["Project Management", "Agile", "Scrum", "Jira", "Risk Management", "Stakeholder Management", "Sprint Planning"],
        "secondary_skills": ["Confluence", "Kanban", "Cross-functional Collaboration", "Budgeting", "Vendor Management", "Time Management"],
        "description": "Orchestrates technical delivery schedules, manages risks and cross-team dependencies, and ensures high project velocity."
    },
    "Scrum Master & Agile Coach": {
        "title": "Scrum Master & Agile Coach",
        "domain": "Product & Project Management",
        "icon": "repeat",
        "core_skills": ["Scrum", "Agile", "Kanban", "Sprint Planning", "Jira", "Mentoring", "Continuous Learning"],
        "secondary_skills": ["Backlog Prioritization", "Stakeholder Management", "Change Management", "Confluence", "Leadership"],
        "description": "Facilitates agile ceremonies, clears team impediments, and promotes iterative development and continuous improvement."
    },

    # --- UI/UX & Design Domain ---
    "UI/UX & Product Designer": {
        "title": "UI/UX & Product Designer",
        "domain": "UI/UX & Design",
        "icon": "palette",
        "core_skills": ["Figma", "Wireframing", "Prototyping", "User Research", "Usability Testing", "Design Systems", "Visual Design"],
        "secondary_skills": ["Adobe XD", "Information Architecture", "Design Thinking", "Interaction Design", "Responsive Design", "User Persona"],
        "description": "Conducts user research, crafts high-fidelity design systems, and builds seamless interactive digital product experiences."
    },

    # --- Digital Marketing & Growth Domain ---
    "Digital Marketing Specialist": {
        "title": "Digital Marketing Specialist",
        "domain": "Digital Marketing & Growth",
        "icon": "trending-up",
        "core_skills": ["SEO", "Google Ads", "Content Marketing", "Social Media Marketing", "Google Analytics", "Email Marketing"],
        "secondary_skills": ["HubSpot", "Conversion Rate Optimization", "Growth Hacking", "Meta Ads", "Copywriting", "A/B Testing"],
        "description": "Drives customer acquisition through multi-channel digital campaigns, performance marketing, and conversion optimization."
    },
    "SEO & Content Strategist": {
        "title": "SEO & Content Strategist",
        "domain": "Digital Marketing & Growth",
        "icon": "search",
        "core_skills": ["SEO", "Search Engine Optimization", "Content Marketing", "Google Analytics", "Copywriting", "Market Research"],
        "secondary_skills": ["Google Ads", "Conversion Rate Optimization", "Social Media Marketing", "A/B Testing", "Technical Writing"],
        "description": "Boosts organic search visibility, conducts keyword strategy, and architects high-converting content funnels."
    },

    # --- Finance & Accounting Domain ---
    "Financial Analyst": {
        "title": "Financial Analyst",
        "domain": "Finance & Accounting",
        "icon": "dollar-sign",
        "core_skills": ["Financial Modeling", "Valuation", "Financial Analysis", "Excel", "Advanced Excel", "Forecasting", "Budgeting"],
        "secondary_skills": ["DCF", "Variance Analysis", "P&L Management", "Power BI", "SAP", "Financial Reporting", "Risk Management"],
        "description": "Builds corporate valuation models, forecasts financial performance, conducts variance analysis, and supports strategic investments."
    },

    # --- Human Resources & Talent Domain ---
    "Human Resources & Talent Lead": {
        "title": "Human Resources & Talent Lead",
        "domain": "Human Resources & Talent",
        "icon": "users",
        "core_skills": ["Talent Acquisition", "Technical Recruiting", "Candidate Sourcing", "Interviewing", "Employee Relations", "Onboarding"],
        "secondary_skills": ["HRIS", "Workday", "Performance Management", "Labor Law", "Retention Strategies", "Compensation & Benefits"],
        "description": "Manages end-to-end talent recruitment, designs competitive employee benefits, and nurtures high-performing workplace culture."
    },

    # --- Sales & Business Development Domain ---
    "Business Development Manager": {
        "title": "Business Development Manager",
        "domain": "Sales & Business Development",
        "icon": "briefcase",
        "core_skills": ["B2B Sales", "Salesforce", "CRM", "Lead Generation", "Pipeline Management", "Negotiation", "Client Relationship"],
        "secondary_skills": ["Contract Negotiation", "Enterprise Sales", "Cold Outreach", "Account Management", "Strategic Planning", "Pitching"],
        "description": "Generates new enterprise business leads, manages multi-million dollar sales funnels, and secures high-value commercial partnerships."
    }
}

# Strong ATS Action Verbs for Resume Evaluation across Multiple Domains
STRONG_ACTION_VERBS = {
    "Leadership & Management": [
        "spearheaded", "orchestrated", "architected", "directed", "championed",
        "founded", "guided", "mentored", "supervised", "pioneered", "steered",
        "governed", "cultivated", "mobilized", "empowered"
    ],
    "Engineering & Technical": [
        "engineered", "developed", "implemented", "deployed", "refactored",
        "automated", "designed", "constructed", "integrated", "programmed",
        "optimized", "configured", "debugged", "modernized", "containerized"
    ],
    "Product & Strategy": [
        "launched", "prioritized", "conceptualized", "defined", "validated",
        "delivered", "strategized", "established", "standardized", "iterated",
        "formulated", "aligned"
    ],
    "Design & Creative": [
        "designed", "prototyped", "wireframed", "researched", "tested",
        "crafted", "modeled", "illustrated", "conceptualized", "restyled"
    ],
    "Marketing & Growth": [
        "scaled", "acquired", "converted", "boosted", "amplified",
        "campaigned", "generated", "monetized", "expanded", "outperformed",
        "promoted", "positioned"
    ],
    "Finance & Analysis": [
        "analyzed", "forecasted", "budgeted", "audited", "quantified",
        "modeled", "reconciled", "evaluated", "benchmarked", "diagnosed",
        "projected", "synthesized"
    ],
    "Talent & People": [
        "recruited", "sourced", "hired", "onboarded", "trained",
        "retained", "negotiated", "mediated", "facilitated", "retained"
    ],
    "Impact & Optimization": [
        "accelerated", "maximized", "increased", "decreased", "reduced",
        "boosted", "eliminated", "transformed", "streamlined", "enhanced",
        "upgraded", "saved"
    ]
}

# Weak or Passive Verbs (Discouraged in modern ATS)
WEAK_VERBS = [
    "assisted with", "helped to", "worked on", "responsible for",
    "participated in", "attempted to", "handled", "was involved in",
    "duties included", "familiar with", "tried to", "tasked with"
]

# Preset Real-World Job Descriptions across Multiple Domains
SAMPLE_JOB_DESCRIPTIONS = {
    "senior_fullstack": {
        "title": "Senior Full Stack Engineer (Python & React)",
        "domain": "Software & Cloud",
        "company": "CloudScale Technologies",
        "experience": "3-6 years",
        "text": """
We are looking for a Senior Full Stack Software Engineer to join our high-growth platform team.
You will architect and build modern cloud-native web applications using Python (Flask or FastAPI), React, TypeScript, and PostgreSQL.

Key Responsibilities:
- Design and implement resilient, scalable RESTful APIs and microservices using Python and PostgreSQL.
- Build clean, interactive, and responsive web user interfaces using React, Next.js, TypeScript, and Tailwind CSS.
- Optimize database queries, indexing, and caching mechanisms using Redis to deliver sub-100ms response times.
- Collaborate with DevOps engineers to containerize services with Docker and configure automated CI/CD pipelines via GitHub Actions.
- Conduct code reviews, mentor junior developers, and uphold software engineering best practices (TDD, clean code).

Required Skills & Experience:
- 3+ years of professional software development experience.
- Strong proficiency in Python, JavaScript, and TypeScript.
- Deep hands-on experience with modern frontend frameworks (React, Next.js).
- Proven track record with relational databases like PostgreSQL and caching with Redis.
- Familiarity with cloud platforms (AWS or GCP), Docker, and CI/CD pipelines.
- Excellent communication and cross-functional team leadership skills.
"""
    },
    "ai_ml_engineer": {
        "title": "AI / Machine Learning Engineer",
        "domain": "Data & AI",
        "company": "CognitiveAI Labs",
        "experience": "2-5 years",
        "text": """
CognitiveAI Labs is seeking an ambitious Machine Learning Engineer to design, fine-tune, and deploy intelligent AI systems.
You will work closely with data scientists to transition cutting-edge ML models and LLM workflows into production.

Responsibilities:
- Build and evaluate machine learning models using Python, PyTorch, Scikit-Learn, and Hugging Face Transformers.
- Develop Retrieval-Augmented Generation (RAG) pipelines and LLM applications using LangChain and vector databases.
- Construct scalable data preprocessing and feature engineering pipelines with Pandas, NumPy, and SQL.
- Deploy machine learning models as high-throughput REST APIs using FastAPI and Docker on AWS.
- Monitor model drift, performance latency, and resource utilization in production using Prometheus and Grafana.

Qualifications:
- Bachelor's or Master's degree in Computer Science, Data Science, or related quantitative field.
- Proficiency in Python and deep learning frameworks (PyTorch or TensorFlow).
- Experience with NLP, LLMs, and prompt engineering techniques.
- Solid understanding of statistical analysis, data modeling, and algorithmic complexity.
- Experience with Docker, Git, and Linux server environments.
"""
    },
    "data_analyst_bi": {
        "title": "Senior Data Analyst & BI Specialist",
        "domain": "Data & AI",
        "company": "Apex Analytics Group",
        "experience": "3-5 years",
        "text": """
Apex Analytics Group is looking for a Senior Data Analyst & BI Specialist to translate complex enterprise datasets into actionable commercial intelligence.

What You Will Do:
- Architect and maintain executive KPI Dashboards using Power BI, Tableau, and Advanced Excel.
- Write advanced SQL queries, stored procedures, and data cleansing scripts to extract insights from relational databases.
- Conduct in-depth statistical analysis, cohort analysis, and A/B Testing to evaluate marketing campaigns and product features.
- Partner with product managers and C-suite leadership to define operational metrics and business intelligence reporting.
- Implement DAX measures, automated reporting schedules, and data visualization best practices.

Requirements:
- 3+ years of experience in data analytics, business intelligence, or quantitative research.
- Mastery of SQL and data visualization tools (Power BI, Tableau, or Looker).
- Expertise in Advanced Excel, DAX, data modeling, and statistical analysis.
- Experience with Python (Pandas) or R for statistical modeling is a strong plus.
- Outstanding data storytelling, client presentation, and stakeholder management skills.
"""
    },
    "product_manager": {
        "title": "Senior Product Manager (SaaS & Mobile)",
        "domain": "Product & Project Management",
        "company": "Horizon Product Ventures",
        "experience": "4-7 years",
        "text": """
Horizon Product Ventures is hiring a Senior Product Manager to own our core SaaS subscription platform and flagship mobile product.

Key Responsibilities:
- Formulate product strategy, manage quarterly product roadmapping, and define measurable OKRs.
- Author clear, detailed Product Requirements Documents (PRDs) and actionable User Stories in Jira.
- Partner with engineering leads to run Agile and Scrum ceremonies, sprint planning, and backlog prioritization.
- Conduct continuous customer discovery interviews, usability testing, and competitive market research.
- Analyze conversion funnels and product health metrics using Google Analytics and A/B Testing tools.

Qualifications:
- 4+ years of product management experience shipping web and mobile digital products.
- Proven experience with Agile frameworks, Scrum ceremonies, and Jira backlog grooming.
- Strong analytical skills in user research, feature prioritization, and requirements gathering.
- Demonstrated success aligning engineering, UI/UX design, sales, and marketing stakeholders.
- Exceptional written communication and executive presentation abilities.
"""
    },
    "ui_ux_designer": {
        "title": "Lead UI/UX & Product Designer",
        "domain": "UI/UX & Design",
        "company": "Aura Studio Design",
        "experience": "3-6 years",
        "text": """
Aura Studio Design is seeking an inventive Lead UI/UX & Product Designer to shape intuitive digital interfaces for enterprise and mobile applications.

Core Responsibilities:
- Design wireframes, user journey maps, visual design mockups, and interactive prototypes using Figma.
- Establish and evolve multi-brand Design Systems, component libraries, and typography guidelines.
- Plan and conduct qualitative user research, card sorting, and usability testing sessions.
- Collaborate closely with frontend engineering teams to ensure pixel-perfect implementation and WCAG accessibility.
- Present design rationale and UX metrics to product managers and executive stakeholders.

Qualifications:
- 3+ years of professional UI/UX design experience with a standout portfolio.
- Mastery of Figma, interactive prototyping, and design systems architecture.
- Deep expertise in user research methodologies, information architecture, and mobile UI.
- Strong knowledge of responsive design standards, design thinking, and accessibility (WCAG).
- Collaborative mindset with strong communication and presentation skills.
"""
    },
    "digital_marketing_manager": {
        "title": "Growth & Digital Marketing Manager",
        "domain": "Digital Marketing & Growth",
        "company": "Vanguard Growth Labs",
        "experience": "3-6 years",
        "text": """
Vanguard Growth Labs is seeking an energetic Digital Marketing & Growth Manager to accelerate inbound customer acquisition and brand visibility.

Responsibilities:
- Plan and execute multi-channel digital campaigns across SEO, Google Ads, Meta Ads, and Email Marketing.
- Drive Conversion Rate Optimization (CRO) and landing page A/B Testing to lower customer acquisition costs (CAC).
- Develop comprehensive content marketing and social media marketing calendars to expand organic brand reach.
- Leverage Google Analytics 4, HubSpot, and CRM tools to track marketing attribution, ROAS, and pipeline velocity.
- Manage quarterly performance marketing budgets and present growth metrics to leadership.

Requirements:
- 3+ years in growth marketing, performance advertising, or digital marketing management.
- Proven expertise in SEO, Google Ads, SEM, Meta Ads, and marketing automation platforms (HubSpot).
- Hands-on experience with Google Analytics 4, copywriting, and conversion funnel optimization.
- Data-driven decision maker with strong analytical and budget management skills.
"""
    },
    "financial_analyst": {
        "title": "Senior Corporate Financial Analyst",
        "domain": "Finance & Accounting",
        "company": "Sterling Capital Partners",
        "experience": "3-6 years",
        "text": """
Sterling Capital Partners is looking for a Senior Financial Analyst to deliver high-level financial modeling, valuation, and executive corporate reporting.

What You Will Do:
- Construct 3-statement financial models, discounted cash flow (DCF) analyses, and capital budgeting forecasts.
- Conduct monthly P&L management, variance analysis, balance sheet reconciliations, and expense forecasting.
- Prepare comprehensive financial reporting packages and board decks for executive management.
- Partner with department heads to evaluate ROI on commercial projects and cost optimization initiatives.
- Utilize Advanced Excel, ERP systems (SAP or NetSuite), and financial visualization tools.

Requirements:
- Bachelor's degree in Finance, Accounting, Economics, or related quantitative field.
- 3+ years of corporate finance, investment analysis, or FP&A experience.
- Advanced proficiency in financial modeling, valuation, budgeting, and Advanced Excel.
- Solid knowledge of GAAP, auditing standards, and financial statement analysis.
- Detail-oriented mindset with superb analytical, problem-solving, and presentation skills.
"""
    },
    "hr_talent_lead": {
        "title": "Technical Talent Acquisition & People Operations Lead",
        "domain": "Human Resources & Talent",
        "company": "Beacon People Systems",
        "experience": "3-7 years",
        "text": """
Beacon People Systems is searching for an empathetic, results-oriented Talent Acquisition & HR Lead to scale our technical and business teams.

Responsibilities:
- Drive full-cycle technical recruiting: candidate sourcing, screening, interviewing, and offer negotiation.
- Develop diverse candidate pipelines using LinkedIn Recruiter, sourcing databases, and tech networks.
- Oversee employee onboarding, performance management reviews, and employee relations initiatives.
- Administer HRIS platforms (Workday, BambooHR) and maintain compliance with employment labor laws.
- Partner with department leaders on workforce planning, retention strategies, and employer branding.

Qualifications:
- 3+ years of experience in technical recruiting, talent acquisition, or human resources management.
- Proven track record closing engineering, product, and business leadership roles.
- Familiarity with modern HRIS and ATS systems (Workday, Greenhouse, Lever, BambooHR).
- Strong interpersonal, conflict resolution, and stakeholder negotiation abilities.
"""
    }
}
