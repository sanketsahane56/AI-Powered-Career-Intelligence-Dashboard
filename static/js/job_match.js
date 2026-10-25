/**
 * CareerIQ - Job Match & Skill Gap Controller
 */

let comparisonRadarChart = null;

document.addEventListener('DOMContentLoaded', () => {
    initPresetSelector();
    initJobMatchForm();
});

// Preset Job Selector
function initPresetSelector() {
    const presetSelect = document.getElementById('preset-select');
    const jdTextarea = document.getElementById('jd-textarea');

    if (!presetSelect || !jdTextarea) return;

    presetSelect.addEventListener('change', () => {
        const selectedOption = presetSelect.options[presetSelect.selectedIndex];
        const jdText = selectedOption.getAttribute('data-text');
        if (jdText) {
            jdTextarea.value = jdText.trim();
            showToast(`Loaded preset: ${selectedOption.text}`, 'info');
        }
    });
}

// Form Submission & Analysis
function initJobMatchForm() {
    const form = document.getElementById('job-match-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const jdText = document.getElementById('jd-textarea').value.trim();
        const skillsText = document.getElementById('skills-input').value.trim();

        if (jdText.length < 30) {
            showToast('Please provide a job description of at least 30 characters.', 'warning');
            return;
        }

        // Skills list from comma-separated input or pre-filled tokens
        const skillsList = skillsText ? skillsText.split(',').map(s => s.trim()).filter(Boolean) : [];

        showLoading('Comparing Profile with Job Description...', 'Extracting technical requirements from target JD...');

        try {
            const response = await fetch('/api/compare-job', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    job_description: jdText,
                    skills: skillsList
                })
            });

            const result = await response.json();
            hideLoading();

            if (!result.success) {
                showToast(result.error || 'Failed to compare job description.', 'error');
                return;
            }

            renderComparisonResults(result.comparison);
            showToast('Job skill-overlap analysis complete!', 'success');

            const resultsSection = document.getElementById('comparison-results');
            if (resultsSection) {
                resultsSection.style.display = 'block';
                resultsSection.scrollIntoView({ behavior: 'smooth' });
            }

        } catch (error) {
            hideLoading();
            showToast('Error during comparison: ' + error.message, 'error');
        }
    });
}

// Render Comparison View
function renderComparisonResults(comp) {
    // 1. Match Score
    const scoreValEl = document.getElementById('match-score-value');
    const scoreRatingEl = document.getElementById('match-score-rating');
    const scoreCircleEl = document.getElementById('match-score-circle');

    const score = comp.match_score || 0;
    if (scoreValEl) scoreValEl.textContent = `${score}%`;

    let scoreColor = '#10B981';
    let rating = 'HIGH ALIGNMENT';
    if (score < 50) {
        scoreColor = '#EF4444';
        rating = 'SIGNIFICANT GAPS';
    } else if (score < 75) {
        scoreColor = '#F59E0B';
        rating = 'MODERATE OVERLAP';
    }

    if (scoreCircleEl) {
        scoreCircleEl.style.boxShadow = `inset 0 0 0 10px ${scoreColor}`;
        scoreCircleEl.style.color = scoreColor;
    }
    if (scoreRatingEl) {
        scoreRatingEl.textContent = rating;
        scoreRatingEl.style.color = scoreColor;
    }

    // 2. Matched Skills (Green)
    const matchedContainer = document.getElementById('matched-skills-tags');
    if (matchedContainer) {
        matchedContainer.innerHTML = '';
        if (comp.matched_skills && comp.matched_skills.length > 0) {
            comp.matched_skills.forEach(s => {
                const tag = document.createElement('span');
                tag.className = 'skill-tag matched';
                tag.innerHTML = `<i data-lucide="check" style="width: 14px; height: 14px;"></i> ${s}`;
                matchedContainer.appendChild(tag);
            });
        } else {
            matchedContainer.innerHTML = '<span style="font-size: 0.85rem; color: #94a3b8;">No overlapping skills identified.</span>';
        }
    }

    // 3. Missing Skills (Red)
    const missingContainer = document.getElementById('missing-skills-tags');
    if (missingContainer) {
        missingContainer.innerHTML = '';
        if (comp.missing_skills && comp.missing_skills.length > 0) {
            comp.missing_skills.forEach(s => {
                const tag = document.createElement('span');
                tag.className = 'skill-tag missing';
                tag.innerHTML = `<i data-lucide="alert-circle" style="width: 14px; height: 14px;"></i> ${s}`;
                missingContainer.appendChild(tag);
            });
        } else {
            missingContainer.innerHTML = '<span style="font-size: 0.85rem; color: #10b981; font-weight: 500;">Zero skill gaps! You match all cataloged job requirements.</span>';
        }
    }

    // 4. Strategic Advice
    const adviceContainer = document.getElementById('comparison-advice');
    if (adviceContainer && comp.advice) {
        adviceContainer.innerHTML = comp.advice.map((item, idx) => `
            <div style="display: flex; gap: 10px; margin-bottom: 8px; align-items: flex-start;">
                <span class="pill pill-blue" style="flex-shrink: 0; width: 20px; height: 20px; padding: 0; justify-content: center; font-size: 0.75rem;">${idx + 1}</span>
                <span style="font-size: 0.88rem; color: #334155;">${item}</span>
            </div>
        `).join('');
    }

    // 5. Radar Chart (Resume vs Job Description)
    renderComparisonRadar(comp.radar_data);

    if (window.lucide) window.lucide.createIcons();
}

function renderComparisonRadar(radarData) {
    const canvas = document.getElementById('comparisonRadarCanvas');
    if (!canvas || !radarData) return;

    if (comparisonRadarChart) {
        comparisonRadarChart.destroy();
    }

    const ctx = canvas.getContext('2d');
    comparisonRadarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: radarData.labels,
            datasets: [
                {
                    label: 'Your Resume Competencies',
                    data: radarData.resume_counts,
                    backgroundColor: 'rgba(37, 99, 235, 0.25)',
                    borderColor: '#2563EB',
                    borderWidth: 2,
                    pointBackgroundColor: '#2563EB'
                },
                {
                    label: 'Target Job Requirements',
                    data: radarData.jd_counts,
                    backgroundColor: 'rgba(239, 68, 68, 0.2)',
                    borderColor: '#EF4444',
                    borderWidth: 2,
                    pointBackgroundColor: '#EF4444'
                }
            ]
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
                legend: {
                    position: 'bottom',
                    labels: { boxWidth: 12, font: { family: 'Inter', size: 12 } }
                }
            }
        }
    });
}
