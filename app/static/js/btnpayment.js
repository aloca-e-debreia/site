document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.payment-option').forEach(btn => {
        btn.addEventListener('click', () => {
            btn.classList.remove('active');
            btn.classList.add('active');
        });
    });
})