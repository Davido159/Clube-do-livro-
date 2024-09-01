document.addEventListener('DOMContentLoaded', function () {
    const bookItems = document.querySelectorAll('.book-item');
    const roomsSection = document.querySelector('.rooms-section');
    const booksSection = document.querySelector('.books-section');

    // Adicionar efeitos de destaque e escala aos itens da lista de livros
    bookItems.forEach(item => {
        item.addEventListener('mouseover', function () {
            item.classList.add('highlight');
        });

        item.addEventListener('mouseout', function () {
            item.classList.remove('highlight');
        });
    });

    // Scroll para revelar seções
    const revealOnScroll = () => {
        const windowHeight = window.innerHeight;
        const revealElements = document.querySelectorAll('.reveal');

        revealElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;

            if (elementTop < windowHeight) {
                element.classList.add('active');
            }
        });
    };

    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll(); // Para mostrar os elementos ao carregar a página
});

document.addEventListener('DOMContentLoaded', () => {
    const revealElements = document.querySelectorAll('.reveal');

    revealElements.forEach(element => {
        element.classList.add('visible');
    });
});
document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('toggle-books');
    const booksContent = document.getElementById('books-content');

    toggleButton.addEventListener('click', () => {
        if (booksContent.classList.contains('hidden')) {
            booksContent.classList.remove('hidden');
            booksContent.classList.add('visible');
            toggleButton.textContent = 'Esconder Acervo de Livros';
        } else {
            booksContent.classList.remove('visible');
            booksContent.classList.add('hidden');
            toggleButton.textContent = 'Mostrar Acervo de Livros';
        }
    });
});
