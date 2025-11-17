const buttons123 = document.querySelectorAll('.payment-option');
buttons123.forEach(btn => {
    btn.addEventListener('click', () => {

        buttons123.forEach(b => b.classList.remove('active'));

        btn.classList.add('active');
    });
});
console.log("deu certo")

