create database if not exists VozUrbana;

use VozUrbana;

-- Tabela para os usuários
DROP TABLE IF EXISTS usuarios;
CREATE TABLE usuarios (
    id INT PRIMARY KEY auto_increment,
    nome VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    pfp TEXT
);

-- Tabela para os reports
DROP TABLE IF EXISTS reports;
CREATE TABLE reports (
    id INT PRIMARY KEY auto_increment,
    user_id INT NOT NULL,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    conteudo TEXT NOT NULL,
    imagem TEXT NOT NULL,
    aceito bool not null default false,
    data TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES usuarios(id)
);

-- Tabela para as petitions
DROP TABLE IF EXISTS peticoes;
CREATE TABLE peticoes (
    id int PRIMARY KEY auto_increment,
    user_id int NOT NULL,
    content TEXT NOT NULL,
    signatures INTEGER DEFAULT 0,
    required_signatures INTEGER DEFAULT 100,
    aberto bool not null default false,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES usuarios(id)
);

delete from usuarios where id > 0;
select * from peticoes;

