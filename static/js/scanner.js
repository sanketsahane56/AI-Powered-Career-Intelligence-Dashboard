/**
 * CareerIQ - ATS Resume Scanner & Analytics Controller
 */

let skillsRadarChart = null;

document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initDropzone();
    initSampleResumeButton();
    initScannerForm();
});

// Tab Switcher (PDF vs Text Paste)
function initTabs() {
    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            const target = tab.getAttribute('data-target');
            document.querySelectorAll('.tab-pane').forEach(p => p.style.display = 'none');
            const activePane = document.getElementById(target);
            if (activePane) activePane.style.display = 'block';
        });
    });
}

// Drag & Drop File Upload
function initDropzone() {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('resume-file-input');
    const fileNameDisplay = document.getElementById('selected-file-name');

    if (!dropzone || !fileInput) return;

    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.remove('dragover');
        });
    });

    dropzone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            updateFileName(files[0].name);
        }
    });

    dropzone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            updateFileName(fileInput.files[0].name);
        }
    });

    function updateFileName(name) {
        if (fileNameDisplay) {
            fileNameDisplay.innerHTML = `<span class="pill pill-blue"><i data-lucide="file-text"></i> ${name}</span>`;
            if (window.lucide) window.lucide.createIcons();
        }
    }
}

// 1-Click Multi-Domain Sample Resume Loader
function initSampleResumeButton() {
    const sampleBtn = document.getElementById('btn-load-sample');
    const textArea = document.getElementById('resume-text-input');
    const textTab = document.querySelector('[data-target="pane-text"]');
    const domainSelect = document.getElementById('sample-domain-select');

    if (sampleBtn && textArea) {
        sampleBtn.addEventListener('click', async () => {
            const domain = domainSelect ? domainSelect.value : 'software';
            try {
                sampleBtn.disabled = true;
                sampleBtn.innerHTML = 'Loading sample...';
                const res = await fetch(`/api/sample-resume?domain=${encodeURIComponent(domain)}`);
                const data = await res.json();
                if (data.success) {
                    textArea.value = data.text;
                    if (textTab) textTab.click();
                    const selectedLabel = domainSelect ? domainSelect.options[domainSelect.selectedIndex].text : domain;
                    showToast(`Loaded sample resume: ${selectedLabel}`, 'success');
                } else {
                    showToast('Failed to load sample resume: ' + (data.error || ''), 'error');
                }
            } catch (err) {
                showToast('Network error loading sample', 'error');
            } finally {
                sampleBtn.disabled = false;
                sampleBtn.innerHTML = '<i data-lucide="sparkles"></i> Load Sample';
                if (window.lucide) window.lucide.createIcons();
            }
        });
    }
}

// Form Submission & Analysis
function initScannerForm() {
    const form = document.getElementById('scanner-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const fileInput = document.getElementById('resume-file-input');
        const textArea = document.getElementById('resume-text-input');
        const activeTab = document.querySelector('.tab-btn.active');
        const isFileTab = activeTab && activeTab.getAttribute('data-target') === 'pane-upload';

        const formData = new FormData();

        if (isFileTab) {
            if (!fileInput.files || fileInput.files.length === 0) {
                showToast('Please select a PDF or TXT resume document.', 'warning');
                return;
            }
            formData.append('resume_file', fileInput.files[0]);
        } else {
            const textVal = textArea.value.trim();
            if (!textVal || textVal.length < 30) {
                showToast('Please paste at least 30 characters of resume text.', 'warning');
                return;
            }
            formData.append('resume_text', textVal);
        }

        // Animated progress steps
        showLoading('Analyzing Resume...', '1/4 Parsing document structure & contact info...');
        const stepTimer1 = setTimeout(() => updateLoadingStep('2/4 Extracting technical skills & competencies...'), 600);
        const stepTimer2 = setTimeout(() => updateLoadingStep('3/4 Calculating transparent ATS dimension metrics...'), 1200);
        const stepTimer3 = setTimeout(() => updateLoadingStep('4/4 Matching market career profiles...'), 1800);

        try {
            const response = await fetch('/api/analyze-resume', {
                method: 'POST',
                body: formData
            });

            clearTimeout(stepTimer1);
            clearTimeout(stepTimer2);
            clearTimeout(stepTimer3);

            const result = await response.json();
            hideLoading();

            if (!result.success) {
                showToast(result.error || 'Failed to analyze resume.', 'error');
                return;
            }

            // Render complete results
            renderResults(result.session_id, result.metadata, result.analysis);
            showToast('Resume analyzed successfully! Score generated.', 'success');

            // Scroll down to results section
            const resultsCard = document.getElementById('results-section');
            if (resultsCard) {
                resultsCard.scrollIntoView({ behavior: 'smooth' });
            }

        } catch (error) {
            hideLoading();
            showToast('An unexpected server error occurred: ' + error.message, 'error');
        }
    });
}

// Render Results View
function renderResults(sessionId, metadata, analysis) {
    const resultsContainer = document.getElementById('results-section');
    if (!resultsContainer) return;

    resultsContainer.style.display = 'block';

    // 1. Candidate Info
    const candNameEl = document.getElementById('res-candidate-name');
    const candEmailEl = document.getElementById('res-candidate-email');
    const candPhoneEl = document.getElementById('res-candidate-phone');
    const candMetaEl = document.getElementById('res-doc-meta');
    const candDomainEl = document.getElementById('res-primary-domain');
    const candDomainText = document.getElementById('res-primary-domain-text');

    if (candNameEl) candNameEl.textContent = metadata.candidate_name || 'Candidate';
    if (candEmailEl) candEmailEl.textContent = metadata.email || 'Email not listed';
    if (candPhoneEl) candPhoneEl.textContent = metadata.phone || 'Phone not listed';
    if (candMetaEl) candMetaEl.textContent = `${analysis.word_count || 0} words • ${analysis.page_count || 1} pages`;

    if (candDomainEl && analysis.primary_domain) {
        candDomainEl.style.display = 'inline-flex';
        if (candDomainText) candDomainText.textContent = `Domain: ${analysis.primary_domain}`;
    }

    // 2. Overall Score Gauge
    const scoreValEl = document.getElementById('res-score-value');
    const scoreCircleEl = document.getElementById('res-score-circle');
    const scoreRatingEl = document.getElementById('res-score-rating');

    const score = analysis.overall_score || 0;
    if (scoreValEl) scoreValEl.textContent = score;

    let scoreColor = '#10B981'; // Emerald
    let ratingText = 'EXCEPTIONAL ATS FIT';
    if (score < 60) {
        scoreColor = '#EF4444'; // Rose
        ratingText = 'NEEDS OPTIMIZATION';
    } else if (score < 80) {
        scoreColor = '#F59E0B'; // Amber
        ratingText = 'SOLID COMPETENCY';
    }

    if (scoreCircleEl) {
        scoreCircleEl.style.boxShadow = `inset 0 0 0 10px ${scoreColor}`;
        scoreCircleEl.style.color = scoreColor;
    }
    if (scoreRatingEl) {
        scoreRatingEl.textContent = ratingText;
        scoreRatingEl.style.color = scoreColor;
    }

    // 3. Dimensions Breakdown
    const dimsContainer = document.getElementById('res-dimensions-grid');
    if (dimsContainer && analysis.dimensions) {
        dimsContainer.innerHTML = '';
        Object.values(analysis.dimensions).forEach(dim => {
            const card = document.createElement('div');
            card.className = 'card';
            card.style.padding = '16px';

            const barColor = dim.score >= 80 ? 'emerald' : (dim.score >= 60 ? 'amber' : 'rose');
            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <span style="font-weight: 600; font-size: 0.9rem;">${dim.name}</span>
                    <span class="pill pill-blue">${dim.weight}</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                    <span style="font-size: 1.4rem; font-weight: 700; font-family: Outfit;">${dim.score} <span style="font-size: 0.75rem; color: #94a3b8;">/ 100</span></span>
                    <span style="font-size: 0.78rem; color: #64748b;">${dim.detail}</span>
                </div>
                <div class="progress-container">
                    <div class="progress-bar ${barColor}" style="width: ${dim.score}%"></div>
                </div>
            `;
            dimsContainer.appendChild(card);
        });
    }

    // 4. Skills Inventory Tags
    const skillsTagContainer = document.getElementById('res-skills-container');
    if (skillsTagContainer && analysis.skills) {
        skillsTagContainer.innerHTML = '';
        const byCat = analysis.skills.by_category || {};
        
        Object.entries(byCat).forEach(([catName, skillList]) => {
            const catBlock = document.createElement('div');
            catBlock.style.marginBottom = '16px';
            catBlock.innerHTML = `
                <div style="font-size: 0.85rem; font-weight: 600; color: #475569; margin-bottom: 8px;">
                    ${catName} <span class="pill pill-gray" style="font-size: 0.7rem;">${skillList.length}</span>
                </div>
                <div class="skill-tags">
                    ${skillList.map(s => `<span class="skill-tag">${s}</span>`).join('')}
                </div>
            `;
            skillsTagContainer.appendChild(catBlock);
        });
    }

    // 5. Radar Chart for Categories
    renderRadarChart(analysis.skills);

    // 6. Action Plan
    const actionListEl = document.getElementById('res-action-plan');
    if (actionListEl && analysis.action_plan) {
        actionListEl.innerHTML = analysis.action_plan.map((act, idx) => `
            <div style="display: flex; gap: 12px; margin-bottom: 12px; align-items: flex-start;">
                <span class="pill pill-violet" style="flex-shrink: 0; width: 24px; height: 24px; justify-content: center; padding: 0;">${idx + 1}</span>
                <span style="font-size: 0.9rem; color: #334155;">${act}</span>
            </div>
        `).join('');
    }

    // 7. Role Compatibility (Multi-Domain)
    const rolesContainer = document.getElementById('res-role-matches');
    const allMatches = analysis.role_matches || [];
    const primDomain = analysis.primary_domain || '';

    function renderRoleList(filterType) {
        if (!rolesContainer) return;
        let filtered = allMatches;
        if (filterType === 'domain' && primDomain) {
            filtered = allMatches.filter(r => (r.domain || '').toLowerCase() === primDomain.toLowerCase());
            if (filtered.length === 0) filtered = allMatches;
        }

        rolesContainer.innerHTML = filtered.slice(0, 5).map(r => `
            <div style="padding: 12px; border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 10px; background: #fafafa;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; flex-wrap: wrap; gap: 6px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-weight: 600; font-size: 0.95rem;">${r.role}</span>
                        ${r.domain ? `<span class="pill pill-gray" style="font-size: 0.7rem;">${r.domain}</span>` : ''}
                    </div>
                    <span class="pill ${r.fit_percentage >= 70 ? 'pill-emerald' : 'pill-blue'}">${r.fit_percentage}% Fit</span>
                </div>
                <p style="font-size: 0.8rem; color: #64748b; margin-bottom: 6px;">${r.description}</p>
                <div class="progress-container">
                    <div class="progress-bar ${r.fit_percentage >= 70 ? 'emerald' : 'blue'}" style="width: ${r.fit_percentage}%"></div>
                </div>
            </div>
        `).join('');
        if (window.lucide) window.lucide.createIcons();
    }

    renderRoleList('all');

    // Attach role toggle filter listeners
    const toggleBtns = document.querySelectorAll('.role-toggle-btn');
    toggleBtns.forEach(btn => {
        btn.onclick = () => {
            toggleBtns.forEach(b => {
                b.classList.remove('btn-primary');
                b.classList.add('btn-secondary');
            });
            btn.classList.add('btn-primary');
            btn.classList.remove('btn-secondary');
            renderRoleList(btn.getAttribute('data-filter'));
        };
    });

    // 8. Setup Action Buttons (Download PDF and Compare with Job)
    const dlBtn = document.getElementById('btn-download-pdf');
    if (dlBtn) {
        dlBtn.onclick = () => {
            window.location.href = `/api/download-report/${sessionId}`;
        };
    }

    const jobBtn = document.getElementById('btn-go-job-match');
    if (jobBtn) {
        jobBtn.onclick = () => {
            window.location.href = `/job-match?session_id=${sessionId}`;
        };
    }

    if (window.lucide) window.lucide.createIcons();
}

// Render Adaptive Chart.js Radar Chart
function renderRadarChart(skillsData) {
    const canvas = document.getElementById('skillsRadarCanvas');
    if (!canvas || !skillsData) return;

    const counts = skillsData.category_counts || {};
    // Select categories with recorded skills or top categories for proper radar shape
    const withCount = Object.entries(counts).filter(([_, v]) => v > 0);
    let selectedEntries = withCount;
    if (selectedEntries.length < 5) {
        selectedEntries = Object.entries(counts).slice(0, 6);
    }

    const labels = selectedEntries.map(([l]) => 
        l.replace(' Frameworks & Web', '')
         .replace(', APIs & Architecture', '')
         .replace(' Infrastructure', '')
         .replace(', Machine Learning & NLP', '')
         .replace(' & Business Intelligence', '')
         .replace(' & Project Management', '')
         .replace(' & Product Design', '')
         .replace(' & Growth', '')
         .replace(', Accounting & Valuation', '')
         .replace(' & Talent Acquisition', '')
         .replace(' & Business Development', '')
         .replace(', Testing & Engineering Standards', '')
         .replace(' & Executive Leadership', '')
    );
    const values = selectedEntries.map(([_, v]) => v);

    if (skillsRadarChart) {
        skillsRadarChart.destroy();
    }

    const ctx = canvas.getContext('2d');
    skillsRadarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Competencies Cataloged',
                data: values,
                backgroundColor: 'rgba(37, 99, 235, 0.2)',
                borderColor: '#2563EB',
                borderWidth: 2,
                pointBackgroundColor: '#2563EB',
                pointBorderColor: '#ffffff',
                pointHoverBackgroundColor: '#ffffff',
                pointHoverBorderColor: '#2563EB'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: '#e2e8f0' },
                    grid: { color: '#e2e8f0' },
                    pointLabels: {
                        font: { size: 10, family: 'Inter' },
                        color: '#475569'
                    },
                    ticks: {
                        display: false,
                        beginAtZero: true
                    }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}
