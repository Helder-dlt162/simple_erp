CREATE TABLE
    IF NOT EXISTS consultas_audiencias_opine (
        id SERIAL PRIMARY KEY,
        dedup_id VARCHAR NOT NULL UNIQUE,
        tipo_consult tipo_consult_enum NOT NULL,
        nom_titulo VARCHAR NOT NULL,
        nom_orgao VARCHAR,
        data_abertura DATE,
        data_encerramento DATE,
        hora VARCHAR,
        titulo_status VARCHAR,
        resumo VARCHAR,
        cont_text TEXT,
        cont_html TEXT,
        area VARCHAR,
        sigla VARCHAR,
        setor VARCHAR,
        descricao TEXT,
        dsc_urlamigavel VARCHAR,
        url VARCHAR,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
