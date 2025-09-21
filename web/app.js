// JACAI - Frontend JavaScript
class JacAI {
    constructor() {
        this.currentPost = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateStats('Ready to generate');
    }

    bindEvents() {
        // Form submission
        document.getElementById('generateForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.generateContent();
        });

        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // Copy buttons
        document.querySelectorAll('.copy-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.copyContent(e.target.dataset.copy);
            });
        });

        // Action buttons
        document.getElementById('regenerateBtn')?.addEventListener('click', () => {
            this.regenerateContent();
        });

        document.getElementById('newBtn')?.addEventListener('click', () => {
            this.newContent();
        });
    }

    async generateContent() {
        const formData = new FormData(document.getElementById('generateForm'));
        const data = {
            topic: formData.get('topic'),
            platform: formData.get('platform'),
            style: formData.get('style')
        };

        this.showLoading();
        this.updateStats('Generating content...');

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                this.currentPost = result.post;
                this.displayResults(result.post);
                this.updateStats(`Generated for ${data.platform} • ${data.style} style`);
            } else {
                this.showError(result.error || 'Failed to generate content');
                this.updateStats('Generation failed');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showError('Network error. Please try again.');
            this.updateStats('Connection error');
        } finally {
            this.hideLoading();
        }
    }

    displayResults(post) {
        // Update content
        document.getElementById('captionText').textContent = post.caption;
        document.getElementById('hashtagsText').textContent = post.hashtags;
        document.getElementById('imageText').textContent = post.image_prompt;

        // Show results section
        document.getElementById('resultsSection').style.display = 'block';
        
        // Scroll to results
        document.getElementById('resultsSection').scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });

        // Add success animation
        document.querySelector('.result-card').classList.add('success-flash');
        setTimeout(() => {
            document.querySelector('.result-card').classList.remove('success-flash');
        }, 600);
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');
    }

    async copyContent(type) {
        let text = '';
        
        switch(type) {
            case 'caption':
                text = document.getElementById('captionText').textContent;
                break;
            case 'hashtags':
                text = document.getElementById('hashtagsText').textContent;
                break;
            case 'image':
                text = document.getElementById('imageText').textContent;
                break;
        }

        try {
            await navigator.clipboard.writeText(text);
            this.showCopySuccess(type);
        } catch (err) {
            // Fallback for older browsers
            this.fallbackCopy(text);
            this.showCopySuccess(type);
        }
    }

    fallbackCopy(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
    }

    showCopySuccess(type) {
        const btn = document.querySelector(`[data-copy="${type}"]`);
        const originalText = btn.innerHTML;
        
        btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        btn.style.background = 'var(--success)';
        
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.style.background = 'var(--primary)';
        }, 2000);
    }

    regenerateContent() {
        if (this.currentPost) {
            // Use the same parameters but regenerate
            const form = document.getElementById('generateForm');
            const formData = new FormData(form);
            
            this.generateContent();
        }
    }

    newContent() {
        // Hide results and reset form
        document.getElementById('resultsSection').style.display = 'none';
        document.getElementById('generateForm').reset();
        document.getElementById('topic').focus();
        this.currentPost = null;
        this.updateStats('Ready to generate');
    }

    showLoading() {
        document.getElementById('loading').style.display = 'block';
        document.getElementById('generateBtn').disabled = true;
        document.getElementById('generateBtn').innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
    }

    hideLoading() {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('generateBtn').disabled = false;
        document.getElementById('generateBtn').innerHTML = '<i class="fas fa-rocket"></i> <span>Generate Content</span>';
    }

    showError(message) {
        // Create error notification
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-notification';
        errorDiv.innerHTML = `
            <div style="
                background: var(--error);
                color: white;
                padding: 1rem 1.5rem;
                border-radius: 0.5rem;
                margin: 1rem 0;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                animation: slideDown 0.3s ease-out;
            ">
                <i class="fas fa-exclamation-triangle"></i>
                ${message}
            </div>
        `;

        const container = document.querySelector('.input-card');
        container.appendChild(errorDiv);

        // Remove after 5 seconds
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }

    updateStats(message) {
        const stats = document.getElementById('stats');
        stats.innerHTML = `<span><i class="fas fa-clock"></i> ${message}</span>`;
    }

    // Utility function to format time
    formatTime(dateString) {
        const date = new Date(dateString);
        return date.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new JacAI();
    
    // Add some nice loading effects
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease-in';
        document.body.style.opacity = '1';
    }, 100);
});

// Add CSS for error notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);