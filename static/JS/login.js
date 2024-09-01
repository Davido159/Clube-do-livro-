document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const emailInput = form.querySelector('input[name="email"]');
    const passwordInput = form.querySelector('input[name="senha"]');

    form.addEventListener('submit', function (event) {
        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

        if (email.length === 0 || password.length === 0) {
            alert('Por favor, preencha todos os campos.');
            event.preventDefault();
            return;
        }

        // Adicionar um efeito de carregamento
        form.querySelector('button').textContent = 'Carregando...';
        form.querySelector('button').disabled = true;
    });

    // Feedback visual para campos inválidos
    emailInput.addEventListener('input', function () {
        if (emailInput.value.trim().length === 0) {
            emailInput.classList.add('invalid');
        } else {
            emailInput.classList.remove('invalid');
        }
    });

    passwordInput.addEventListener('input', function () {
        if (passwordInput.value.trim().length === 0) {
            passwordInput.classList.add('invalid');
        } else {
            passwordInput.classList.remove('invalid');
        }
    });
});
