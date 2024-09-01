document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const senhaInput = form.querySelector('input[name="senha"]');
    const confirmarSenhaInput = form.querySelector('input[name="confirmar_senha"]');
    const errorElement = document.querySelector('#error-message');

    // Confirmar senha
    form.addEventListener('submit', function (event) {
        const senha = senhaInput.value.trim();
        const confirmarSenha = confirmarSenhaInput.value.trim();

        if (senha !== confirmarSenha) {
            errorElement.textContent = 'As senhas não coincidem.';
            event.preventDefault();
        } else {
            errorElement.textContent = '';
        }
    });

    confirmarSenhaInput.addEventListener('input', function () {
        if (confirmarSenhaInput.value.trim() !== senhaInput.value.trim()) {
            confirmarSenhaInput.classList.add('invalid');
        } else {
            confirmarSenhaInput.classList.remove('invalid');
        }
    });
});
