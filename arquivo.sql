CREATE DATABASE IF NOT EXISTS clube_do_livro;
USE clube_do_livro;

-- Criação das tabelas
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    usuario VARCHAR(255) NOT NULL,
    nome_completo VARCHAR(255),
    data_nascimento DATE
);

CREATE TABLE IF NOT EXISTS salas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255),
    criador_id INT,
    FOREIGN KEY (criador_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS livros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(255),
    genero VARCHAR(255),
    pais_origem VARCHAR(255),
    quantidade_paginas INT
);

CREATE TABLE IF NOT EXISTS sala_livros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sala_id INT,
    livro_id INT,
    data_encontro DATE,
    FOREIGN KEY (sala_id) REFERENCES salas(id),
    FOREIGN KEY (livro_id) REFERENCES livros(id)
);

CREATE TABLE IF NOT EXISTS votos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    livro_id INT,
    sala_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (livro_id) REFERENCES livros(id),
    FOREIGN KEY (sala_id) REFERENCES salas(id)
);

