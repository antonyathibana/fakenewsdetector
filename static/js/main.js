// Fake News Detection - Main JavaScript

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Form validation
    const predictForms = document.querySelectorAll('#predictForm');
    predictForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const newsText = form.querySelector('[name="news_text"]');
            if (newsText && newsText.value.trim().length < 10) {
                e.preventDefault();
                alert('Please enter more text for accurate prediction (at least 10 characters).');
            }
        });
    });
});

// Copy to clipboard function
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        alert('Copied to clipboard!');
    }, function(err) {
        console.error('Could not copy text: ', err);
    });
}

// Format date function
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

document.addEventListener("DOMContentLoaded", function () {
    const bar = document.querySelector(".progress-bar");
    if (bar) {
        const width = bar.getAttribute("data-width");
        bar.style.width = width + "%";
    }
});
