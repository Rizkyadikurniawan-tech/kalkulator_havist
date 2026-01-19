document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm');
    const inputs = document.querySelectorAll('input');
    
    // Focus effect
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
    });
    
    // Form validation
    form.addEventListener('submit', function(e) {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        if (!username || !password) {
            e.preventDefault();
            showNotification('Mohon isi semua field!', 'error');
            return false;
        }
    });
    
    // Password visibility toggle
    const passwordInput = document.getElementById('password');
    passwordInput.addEventListener('input', function() {
        if (this.value.length > 0) {
            // Tambahkan eye icon jika diperlukan
        }
    });
});

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'check-circle'}"></i>
        ${message}
    `;
    document.querySelector('.login-box').insertBefore(notification, document.querySelector('form'));
    
    setTimeout(() => {
        notification.remove();
    }, 4000);
}
