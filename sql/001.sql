create database if not exists db_sesiBiblioteca;

use db_sesiBiblioteca;
drop table editoras;
create table editoras(
	id_editora int auto_increment primary key,
    nome varchar(255)
);

create table usuarios(
	id_usuario int auto_increment primary key,
    nome varchar(255),
    senha varchar(255) not null
);

drop table livros;
CREATE TABLE livros (
    id_livro INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255),
    autor VARCHAR(80),
    foto VARCHAR(255),
    id_editora INT,
    id_usuario INT,
    
    FOREIGN KEY (id_editora) REFERENCES editoras (id_editora) ON DELETE SET NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario) ON DELETE SET NULL
);

insert into editoras(nome) values("GARNIER"), ("JOSÉ OLYMPIO"), ("COMPANHIA DAS LETRAS"), ("ATICA"), ("Caneta Azul Company");

insert into usuarios(nome, senha) values("Ricardo", "123");

insert into livros(titulo, autor, foto, id_editora, id_usuario) values("Dom Casmurro", "Machado de Assis", 'https://cdn.kobo.com/book-images/f18cefb4-bb45-4774-9b89-49a91af37e87/1200/1200/False/dom-casmurro-8.jpg', 1,1);



SELECT l.id_livro, l.titulo, l.autor, l.foto, e.nome AS nome_editora, u.nome AS nome_usuario
FROM livros l JOIN editora e ON l.id_editora = e.id_editora
LEFT JOIN usuarios u ON l.id_usuario = u.id_usuario
WHERE l.id_usuario = 0;




