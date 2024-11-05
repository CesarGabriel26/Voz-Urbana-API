DROP TABLE IF EXISTS usuarios;
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    cpf CHAR(11) UNIQUE NOT NULL,
    pfp TEXT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS reports;
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    conteudo TEXT NOT NULL,
    imagem TEXT DEFAULT NULL,
    aceito BOOLEAN NOT NULL DEFAULT FALSE,
    data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    adress TEXT DEFAULT '',
    status INT DEFAULT 0,
    prioridade INT DEFAULT 2,
    categoria VARCHAR(50),
    
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS petitions;
CREATE TABLE petitions (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    signatures INT DEFAULT 0,
    required_signatures INT DEFAULT 100,
    aberto BOOLEAN NOT NULL DEFAULT FALSE,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_limite TIMESTAMP NOT NULL,
    data_conclusao TIMESTAMP,
    status INT DEFAULT 0,
    motivo_encerramento TEXT,
    local VARCHAR(100),
    categoria VARCHAR(50),
    apoiadores INT[] DEFAULT {},
    data_ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Trigger para atualizar o campo updated_at
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_usuario_timestamp
BEFORE UPDATE ON usuarios
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER update_petition_timestamp
BEFORE UPDATE ON petition
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();
