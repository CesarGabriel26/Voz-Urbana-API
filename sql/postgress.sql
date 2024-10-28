-- Criação do banco de dados
CREATE DATABASE "VozUrbana";

-- Uso do banco de dados
\c VozUrbana;

-- Tabela para os usuários
DROP TABLE IF EXISTS usuarios;
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    pfp TEXT
);

-- Tabela para os reports (reclamações)
DROP TABLE IF EXISTS reports;
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    conteudo TEXT NOT NULL,
    imagem TEXT NOT NULL,
    aceito BOOLEAN NOT NULL DEFAULT FALSE,
    data TIMESTAMP NOT NULL,
    adress TEXT DEFAULT '',
    status int DEFAULT 0,  -- Coluna status adicionada com valor padrão
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabela para as petições
DROP TABLE IF EXISTS peticoes;
CREATE TABLE peticoes (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    signatures INT DEFAULT 0,
    required_signatures INT DEFAULT 100,
    aberto BOOLEAN NOT NULL DEFAULT FALSE,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_limite TIMESTAMP NOT NULL,         -- Data limite para coleta de assinaturas
    status int DEFAULT 0,      -- Nova coluna status com valor padrão
    causa TEXT,                              -- Nova coluna causa para descrever a causa da petição
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Excluir usuários existentes
DELETE FROM usuarios WHERE id > 0;

-- Selecionar todas as petições
SELECT * FROM peticoes;
