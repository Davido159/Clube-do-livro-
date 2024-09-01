document.addEventListener('DOMContentLoaded', function () {
    const bookItems = document.querySelectorAll('.book-item');

    // Adicionar efeitos de destaque e escala aos itens da lista de livros
    bookItems.forEach(item => {
        item.addEventListener('mouseover', function () {
            item.classList.add('highlight');
        });

        item.addEventListener('mouseout', function () {
            item.classList.remove('highlight');
        });
    });
});
