/**
 * CareerIQ - Global Client Utilities
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Sidebar Toggle
    const mobileBtn = document.getElementById('mobile-menu-toggle');
    const sidebar = document.getElementById('app-sidebar');

    if (mobileBtn && sidebar) {
        mobileBtn.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });

        // Close sidebar on outside click
        document.addEventListener('click', (e) => {
            if (sidebar.classList.contains('open') && 
                !sidebar.contains(e.target) && 
                !mobileBtn.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        });
    }

    // 2. Format Header Date
    const dateEl = document.getElementById('header-date');
    if (dateEl) {
        const options = { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' };
        dateEl.textContent = new Date().toLocaleDateString('en-US', options);
    }
});

// Toast notification helper
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let icon = 'check-circle';
    if (type === 'error') icon = 'alert-triangle';
    if (type === 'warning') icon = 'alert-circle';

    toast.innerHTML = `
        <i data-lucide="${icon}"></i>
        <div>${message}</div>
    `;

    container.appendChild(toast);
    if (window.lucide) {
        window.lucide.createIcons();
    }

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(40px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Global Loading Overlay
function showLoading(title = 'Analyzing Document...', step = 'Extracting resume structure...') {
    const overlay = document.getElementById('global-loading');
    if (overlay) {
        const titleEl = document.getElementById('loading-title');
        const stepEl = document.getElementById('loading-step');
        if (titleEl) titleEl.textContent = title;
        if (stepEl) stepEl.textContent = step;
        overlay.classList.add('active');
    }
}

function updateLoadingStep(step) {
    const stepEl = document.getElementById('loading-step');
    if (stepEl) stepEl.textContent = step;
}

function hideLoading() {
    const overlay = document.getElementById('global-loading');
    if (overlay) {
        overlay.classList.remove('active');
    }
}
