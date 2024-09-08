document.addEventListener('DOMContentLoaded', function () {
    const bookItems = document.querySelectorAll('.book-item');
    const toggleButton = document.getElementById('toggle-books');
    const booksContent = document.getElementById('books-content');
    const revealElements = document.querySelectorAll('.reveal');

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

        revealElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;

            if (elementTop < windowHeight) {
                element.classList.add('active');
            }
        });
    };

    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll(); // Para mostrar os elementos ao carregar a página

    // Toggle de visibilidade do acervo de livros
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

    // Adicionar visibilidade aos elementos com a classe 'reveal'
    revealElements.forEach(element => {
        element.classList.add('visible');
    });
});
