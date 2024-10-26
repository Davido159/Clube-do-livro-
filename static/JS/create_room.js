document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const nomeSalaInput = form.querySelector('input[name="nome_sala"]');
    const senhaSalaInput = form.querySelector('input[name="senha_sala"]');
    const errorElement = document.querySelector('#error-message');

    nomeSalaInput.addEventListener('input', function () {
        const nomeSala = nomeSalaInput.value.trim();
        
        if (nomeSala.length === 0) {
            errorElement.textContent = 'O nome da sala é obrigatório.';
        } else {
            errorElement.textContent = '';
        }
    });

    senhaSalaInput.addEventListener('input', function () {
        const senhaSala = senhaSalaInput.value.trim();

        if (senhaSala.length === 0) {
            errorElement.textContent = 'A senha da sala é obrigatória.';
        } else {
            errorElement.textContent = '';
        }
    });

    form.addEventListener('submit', function (event) {
        const nomeSala = nomeSalaInput.value.trim();
        const senhaSala = senhaSalaInput.value.trim();

        if (nomeSala.length === 0) {
            alert('O nome da sala é obrigatório.');
            event.preventDefault();
        }

        if (senhaSala.length === 0) {
            alert('Senha obrigatória.');
            event.preventDefault();
        }
    });
});

    
