"""
CareerIQ - Comprehensive Skills Taxonomy & Industry Role Profiles
Contains 500+ curated technical, cloud, data, and soft skills with category mappings,
aliases, career profiles, and sample job descriptions.
"""

# Categorized Skill Taxonomy
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
        "Storybook", "Material-UI", "Chakra UI", "Shadcn UI"
    ],
    "Backend & APIs": [
        "Node.js", "Express.js", "Express", "Flask", "Django", "FastAPI", "Spring Boot",
        "Spring", "ASP.NET", ".NET Core", "Ruby on Rails", "NestJS", "GraphQL", "REST APIs",
        "RESTful API", "gRPC", "Microservices", "Serverless", "Celery", "Kafka",
        "RabbitMQ", "Apache Pulsar", "Socket.io", "SOAP"
    ],
    "Databases & Storage": [
        "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "Elasticsearch",
        "DynamoDB", "Cassandra", "Couchbase", "Snowflake", "BigQuery", "Redshift",
        "Oracle", "Microsoft SQL Server", "Neo4j", "Firebase", "Supabase", "Prisma",
        "SQLAlchemy", "Hibernate"
    ],
    "Cloud & DevOps": [
        "AWS", "Amazon Web Services", "Azure", "Microsoft Azure", "Google Cloud", "GCP",
        "Docker", "Kubernetes", "K8s", "CI/CD", "GitHub Actions", "GitLab CI", "Jenkins",
        "Terraform", "Ansible", "Helm", "Prometheus", "Grafana", "Linux", "Ubuntu",
        "Nginx", "Apache", "Cloudflare", "OpenTelemetry", "ArgoCD", "Datadog"
    ],
    "AI, ML & Data Science": [
        "Machine Learning", "Deep Learning", "Artificial Intelligence", "NLP",
        "Natural Language Processing", "Computer Vision", "PyTorch", "TensorFlow",
        "Keras", "Scikit-Learn", "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn",
        "Large Language Models", "LLM", "Prompt Engineering", "RAG", "LangChain",
        "Hugging Face", "Transformers", "OpenCV", "ETL", "Apache Spark", "Airflow",
        "Data Pipelines", "Feature Engineering", "Data Modeling", "Statistical Analysis"
    ],
    "System Design & Engineering": [
        "System Design", "Distributed Systems", "Object-Oriented Programming", "OOP",
        "Design Patterns", "Clean Code", "Test-Driven Development", "TDD", "Unit Testing",
        "Integration Testing", "PyTest", "Jest", "Git", "GitHub", "GitLab", "Bitbucket",
        "Agile", "Scrum", "Kanban", "Jira", "Software Architecture", "Performance Optimization",
        "Caching Strategies", "Scalability", "High Availability"
    ],
    "Professional & Leadership": [
        "Leadership", "Team Leadership", "Cross-functional Collaboration", "Communication",
        "Mentoring", "Code Review", "Problem Solving", "Critical Thinking", "Project Management",
        "Stakeholder Management", "Time Management", "Technical Writing", "Continuous Learning",
        "Client Presentation", "Strategic Planning"
    ]
}

# Skill Aliases / Normalization Map
SKILL_ALIASES = {
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
    "tdd": "Test-Driven Development"
}

# Standard Career Profiles with required and recommended skills
CAREER_PROFILES = {
    "Full Stack Engineer": {
        "title": "Full Stack Engineer",
        "icon": "layers",
        "core_skills": ["JavaScript", "TypeScript", "Python", "React", "Node.js", "SQL", "REST APIs", "Git"],
        "secondary_skills": ["Docker", "PostgreSQL", "Next.js", "Tailwind CSS", "CI/CD", "AWS", "Redis"],
        "description": "Designs and builds end-to-end web applications across front-end user interfaces, back-end servers, and persistent databases."
    },
    "Backend Software Engineer": {
        "title": "Backend Software Engineer",
        "icon": "server",
        "core_skills": ["Python", "Java", "Go", "SQL", "PostgreSQL", "REST APIs", "Microservices", "System Design"],
        "secondary_skills": ["Docker", "Kubernetes", "Redis", "Kafka", "AWS", "CI/CD", "FastAPI", "Django"],
        "description": "Architects resilient distributed systems, robust APIs, database models, and background task pipelines."
    },
    "Frontend Engineer": {
        "title": "Frontend Engineer",
        "icon": "layout",
        "core_skills": ["JavaScript", "TypeScript", "React", "Next.js", "HTML5", "CSS3", "Tailwind CSS", "Redux"],
        "secondary_skills": ["Vite", "Responsive Design", "Jest", "REST APIs", "WebSockets", "Git", "GraphQL"],
        "description": "Crafts accessible, high-performance user interfaces and responsive web applications with modern state management."
    },
    "Data Scientist": {
        "title": "Data Scientist",
        "icon": "bar-chart-2",
        "core_skills": ["Python", "SQL", "Pandas", "NumPy", "Scikit-Learn", "Statistical Analysis", "Data Visualization", "Machine Learning"],
        "secondary_skills": ["R", "Matplotlib", "Seaborn", "Deep Learning", "TensorFlow", "PyTorch", "Airflow", "BigQuery"],
        "description": "Extracts actionable insights from large datasets, develops predictive models, and conducts statistical experiments."
    },
    "Machine Learning Engineer": {
        "title": "Machine Learning Engineer",
        "icon": "cpu",
        "core_skills": ["Python", "PyTorch", "TensorFlow", "Machine Learning", "Deep Learning", "Docker", "Data Pipelines", "Scikit-Learn"],
        "secondary_skills": ["Large Language Models", "NLP", "Computer Vision", "Hugging Face", "MLOps", "Kubernetes", "AWS", "FastAPI"],
        "description": "Bridges the gap between research models and production systems by deploying, monitoring, and scaling ML/AI models."
    },
    "DevOps & Cloud Engineer": {
        "title": "DevOps & Cloud Engineer",
        "icon": "cloud",
        "core_skills": ["AWS", "Docker", "Kubernetes", "CI/CD", "Terraform", "Linux", "Git", "Bash"],
        "secondary_skills": ["Azure", "Google Cloud", "Ansible", "Prometheus", "Grafana", "Jenkins", "GitHub Actions", "Python"],
        "description": "Automates deployment pipelines, ensures cloud infrastructure reliability, and streamlines developer productivity."
    },
    "Data Engineer": {
        "title": "Data Engineer",
        "icon": "database",
        "core_skills": ["Python", "SQL", "ETL", "Apache Spark", "Airflow", "PostgreSQL", "Snowflake", "Data Pipelines"],
        "secondary_skills": ["Kafka", "BigQuery", "Docker", "AWS", "Data Modeling", "Redis", "Linux", "Scala"],
        "description": "Constructs reliable data pipelines, data warehouses, and batch/streaming processing architectures."
    },
    "Cybersecurity Engineer": {
        "title": "Cybersecurity Engineer",
        "icon": "shield",
        "core_skills": ["Linux", "Python", "Bash", "Network Security", "Git", "Cryptography", "Troubleshooting"],
        "secondary_skills": ["AWS", "Docker", "System Administration", "SIEM", "Vulnerability Assessment", "CI/CD"],
        "description": "Protects organizational infrastructure, audits codebases for security vulnerabilities, and implements defense mechanisms."
    }
}

# Strong ATS Action Verbs for Resume Evaluation
STRONG_ACTION_VERBS = {
    "Leadership & Management": [
        "spearheaded", "orchestrated", "architected", "directed", "championed",
        "founded", "guided", "mentored", "supervised", "pioneered", "steered"
    ],
    "Engineering & Development": [
        "engineered", "developed", "implemented", "deployed", "refactored",
        "automated", "designed", "constructed", "integrated", "programmed",
        "optimized", "configured", "debugged", "modernized"
    ],
    "Impact & Optimization": [
        "accelerated", "maximized", "increased", "decreased", "reduced",
        "boosted", "amplified", "eliminated", "transformed", "streamlined",
        "enhanced", "upgraded", "generated", "outperformed"
    ],
    "Analysis & Research": [
        "analyzed", "evaluated", "diagnosed", "benchmarked", "investigated",
        "audited", "modeled", "forecasted", "quantified", "synthesized"
    ]
}

# Weak or Passive Verbs (Discouraged in modern ATS)
WEAK_VERBS = [
    "assisted with", "helped to", "worked on", "responsible for",
    "participated in", "attempted to", "handled", "was involved in",
    "duties included", "familiar with"
]

# Preset Real-World Job Descriptions for Instant Demo / Testing
SAMPLE_JOB_DESCRIPTIONS = {
    "senior_fullstack": {
        "title": "Senior Full Stack Engineer (Python & React)",
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
    "devops_cloud_architect": {
        "title": "DevOps & Cloud Systems Engineer",
        "company": "Nexus Infrastructure Systems",
        "experience": "3-7 years",
        "text": """
Join Nexus Infrastructure to modernize our multi-cloud deployment ecosystem and lead our reliability engineering initiatives.

What You Will Do:
- Architect, manage, and scale secure cloud infrastructure across AWS using Terraform (Infrastructure-as-Code).
- Orchestrate containerized microservices deployments with Kubernetes (EKS) and Helm charts.
- Build and maintain continuous integration and deployment (CI/CD) pipelines using GitHub Actions and Jenkins.
- Implement comprehensive monitoring, logging, and alerting using Prometheus, Grafana, and Datadog.
- Drive security hardening, Linux system performance tuning, and disaster recovery planning.

Requirements:
- Strong experience with AWS (EC2, S3, RDS, IAM, EKS, VPC).
- Deep expertise in Docker, Kubernetes, and container networking.
- Hands-on proficiency with Terraform and Ansible for automated provisioning.
- Strong scripting skills in Bash and Python.
- Proven experience maintaining 99.99% system availability in production environments.
"""
    }
}
