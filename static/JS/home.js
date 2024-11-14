document.addEventListener('DOMContentLoaded', function () {
    const bookItems = document.querySelectorAll('.book-item');
    const toggleButton = document.getElementById('toggle-books');
    const booksContent = document.getElementById('books-content');
    const revealElements = document.querySelectorAll('.reveal');
    const roomCards = document.querySelectorAll('.room-card');

    // Função para buscar a capa do livro via Open Library API
    async function fetchBookCover(isbn, bookId) {
        const url = `https://covers.openlibrary.org/b/isbn/${isbn}-L.jpg`;
        const imageElement = document.getElementById(`book-image-${bookId}`);

        try {
            const response = await fetch(url);
            if (response.ok) {
                // Se a imagem foi encontrada, atualiza o conteúdo da div
                imageElement.innerHTML = `<img src="${url}" alt="Capa do livro" class="book-cover">`;
            } else {
                // Caso não encontre uma capa, pode exibir uma imagem padrão
                imageElement.innerHTML = `<img src="/static/images/no-cover.jpg" alt="Capa não disponível" class="book-cover">`;
            }
        } catch (error) {
            console.error('Erro ao buscar capa do livro:', error);
            imageElement.innerHTML = `<img src="/static/images/no-cover.jpg" alt="Erro ao carregar capa" class="book-cover">`;
        }
    }

    // Iterar sobre os livros e buscar as capas
    const livros = [
        { id: 1, isbn: '9788520927239' },
        { id: 2, isbn: '9788578271481' }
        // Adicione mais livros aqui com seus respectivos ISBNs
    ];

    livros.forEach(livro => {
        fetchBookCover(livro.isbn, livro.id);
    });

    // Efeito de destaque nas salas ao passar o mouse
    roomCards.forEach(card => {
        card.addEventListener('mouseover', () => {
            card.classList.add('highlight');
        });
        card.addEventListener('mouseout', () => {
            card.classList.remove('highlight');
        });
    });

    // Scroll para revelar seções
    const revealOnScroll = () => {
        const windowHeight = window.innerHeight;

        revealElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;

            if (elementTop < windowHeight) {
                element.classList.add('visible');
            }
        });
    };

    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll(); // Para mostrar os elementos ao carregar a página

    // Toggle de visibilidade do acervo de livros
    if (toggleButton && booksContent) {
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
    }

    // Adicionar visibilidade aos elementos com a classe 'reveal'
    revealElements.forEach(element => {
        element.classList.add('visible');
    });
});
