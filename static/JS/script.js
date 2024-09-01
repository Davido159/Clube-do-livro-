document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    
    form.addEventListener('submit', (e) => {
        const nomeSala = document.querySelector('input[name="nome_sala"]').value;
        const senhaSala = document.querySelector('input[name="senha_sala"]').value;

        if (nomeSala === '' || senhaSala === '') {
            e.preventDefault();
            alert('Por favor, preencha todos os campos.');
        }
    });
});
