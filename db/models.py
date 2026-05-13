from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Text,
    JSON,
    ARRAY,
    ForeignKey,
    CheckConstraint,
    Enum,
    DateTime,
    Boolean,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()


class TipoTermo(enum.Enum):
    inclusao = 'inclusao'
    exclusao = 'exclusao'
    pessoal = 'pessoal'
    corporativo = 'corporativo'


class Coordenadoria(Base):
    __tablename__ = 'coordenadorias'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    clientes = relationship("Cliente", back_populates="coordenadoria")

    def __repr__(self):
        return f"<Coordenadoria(nome={self.nome})>"


class Setor(Base):
    __tablename__ = 'setores'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    clientes = relationship(
        "Cliente", secondary="clientes_setores", back_populates="setores")
    termos = relationship("Termo", back_populates="setor")

    def __repr__(self):
        return f"<Setor(nome={self.nome})>"


class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    coordenadoria_id = Column(Integer, ForeignKey(
        'coordenadorias.id', ondelete='CASCADE'), nullable=False)
    nome = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    coordenadoria = relationship("Coordenadoria", back_populates="clientes")
    setores = relationship(
        "Setor", secondary="clientes_setores", back_populates="clientes")
    termos = relationship("Termo", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente(nome={self.nome}, coordenadoria_id={self.coordenadoria_id})>"


class ClienteSetor(Base):
    __tablename__ = 'clientes_setores'

    cliente_id = Column(Integer, ForeignKey(
        'clientes.id', ondelete='CASCADE'), primary_key=True)
    setor_id = Column(Integer, ForeignKey(
        'setores.id', ondelete='CASCADE'), primary_key=True)


class Termo(Base):
    __tablename__ = 'termos'

    id = Column(Integer, primary_key=True)
    setor_id = Column(Integer, ForeignKey('setores.id', ondelete='CASCADE'))
    cliente_id = Column(Integer, ForeignKey('clientes.id', ondelete='CASCADE'))
    termo = Column(String, nullable=False)
    tipo_termo = Column(Enum(TipoTermo), nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    setor = relationship("Setor", back_populates="termos")
    cliente = relationship("Cliente", back_populates="termos")

    __table_args__ = (
        CheckConstraint('setor_id IS NOT NULL OR cliente_id IS NOT NULL'),
    )

    def __repr__(self):
        return f"<Termo(termo={self.termo}, tipo_termo={self.tipo_termo})>"


class DouItemTermo(Base):
    __tablename__ = 'dou_items_termos'

    dou_item_id = Column(Integer, ForeignKey(
        'dou_items.id', ondelete='CASCADE'), primary_key=True)
    termo_id = Column(Integer, ForeignKey(
        'termos.id', ondelete='CASCADE'), primary_key=True)


class TipoConsult(enum.Enum):
    consulta = 'consulta'
    audiencia = 'audiencia'
    opine = 'opine'


class TipoPub(enum.Enum):
    noticia = 'noticia'
    aviso_pauta = 'aviso_pauta'
    nota_imprensa = 'nota_imprensa'
    alerta = 'alerta'
    ata_resolucao = 'ata_resolucao'
    aviso = 'aviso'
    discurso_artigo_entrevista = 'discurso_artigo_entrevista'


class TipoDivisao(enum.Enum):
    ministerio = 'ministerio'
    ministerio_internacional = 'ministerio_internacional'
    agencia_reguladora_nacional = 'agencia_reguladora_nacional'
    agencia_reguladora_internacional = 'agencia_reguladora_internacional'
    associacao_setorial = 'associacao_setorial'
    associacao_setorial_internacional = 'associacao_setorial_internacional'
    imprensa = 'imprensa'
    imprensa_internacional = 'imprensa_internacional'


class Consulta(Base):
    __tablename__ = 'consultas_audiencias_opine'

    id = Column(Integer, primary_key=True)
    dedup_id = Column(String, nullable=False, unique=True)
    tipo_consult = Column(Enum(TipoConsult), nullable=False)
    nom_titulo = Column(String, nullable=False)
    nom_orgao = Column(String)
    data_abertura = Column(Date)
    data_encerramento = Column(Date)
    hora = Column(String)
    titulo_status = Column(String)
    resumo = Column(String)
    cont_text = Column(Text)
    cont_html = Column(Text)
    area = Column(String)
    sigla = Column(String)
    setor = Column(String)
    descricao = Column(Text)
    dsc_urlamigavel = Column(String)
    url = Column(String)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    def __repr__(self):
        return f"<Consulta(sigla={self.sigla}, nom_orgao={self.nom_orgao}, nom_titulo={self.nom_titulo})>"


class Publicacao(Base):
    __tablename__ = 'publicacoes'

    id = Column(Integer, primary_key=True)
    tipo_pub = Column(Enum(TipoPub), nullable=False)
    tipo_divisao = Column(Enum(TipoDivisao), nullable=False)
    nom_titulo = Column(String, nullable=False)
    nom_subtitulo = Column(String)
    data = Column(Date)
    descricao = Column(Text)
    nom_orgao = Column(String)
    keywords = Column(String)
    dsc_urlamigavel = Column(String)
    relevante = Column(Boolean)
    resumo = Column(String)
    cont_text = Column(Text)
    cont_html = Column(Text)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    def __repr__(self):
        return f"<Publicacao(tipo_pub={self.tipo_pub}, nom_titulo={self.nom_titulo})>"


class DOU(Base):
    __tablename__ = 'dou_items'

    id = Column(Integer, primary_key=True)
    origem = Column(String, nullable=False)
    tipo_pub = Column(String)
    nom_titulo = Column(Text)
    dsc_urlamigavel = Column(String, unique=True, nullable=False)
    data = Column(Date)
    resumo = Column(Text)
    conteudo_html = Column(Text)
    conteudo_texto = Column(Text)
    ementa = Column(Text)
    assina = Column(String)
    identifica = Column(String)
    numero_pagina = Column(String)
    numero_edicao = Column(String)
    tipo_artigo = Column(String)
    ordem_publicacao = Column(String)
    hierarquia = Column(Text)
    nom_subtitulo = Column(Text)
    titulo_alternativo = Column(Text)
    nivel_hierarquico = Column(String)
    lista_hierarquia = Column(JSON)
    url = Column(String)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    termos = relationship("Termo", secondary="dou_items_termos")
 

    def __repr__(self):
        return f"<DOU(origem={self.origem}, nom_titulo={self.nom_titulo})>"


class DOU_AR(Base):
    __tablename__ = 'dou_ar'

    id = Column(Integer, primary_key=True)
    origem = Column(String, nullable=False)
    seccion = Column(String)
    tipo_pub = Column(String)
    nom_titulo = Column(Text)
    dsc_urlamigavel = Column(String, unique=True, nullable=False)
    data = Column(Date)
    cont_html = Column(Text)
    cont_text = Column(Text)
    assina = Column(String)
    identifica = Column(String)
    edicao = Column(String)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    def __repr__(self):
        return f"<BOLETIN OFICIAL DE ARGENTINA(origem={self.origem}, nom_titulo={self.nom_titulo})>"


class DOE(Base):
    __tablename__ = 'doe_items'

    id = Column(Integer, primary_key=True)
    dedup_id = Column(String, nullable=False)
    jornal = Column(String)
    tipo_pub = Column(String)
    data = Column(Date)
    origem = Column(String)
    nom_titulo = Column(String)
    url = Column(String)
    url_api = Column(String)
    resumo = Column(Text)
    hierarquia = Column(String)
    conteudo_html = Column(Text)
    conteudo_texto = Column(Text)
    sessao = Column(String)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    def __repr__(self):
        return f"<DOE(origem={self.origem}, nom_titulo={self.nom_titulo})>"


class AgendaLegis(Base):
    __tablename__ = 'agendas_legis'

    id = Column(Integer, primary_key=True)
    dedup_id = Column(String, nullable=False, unique=True)
    fonte = Column(String, nullable=False)
    data = Column(Date)
    hora = Column(String)
    categoria = Column(String)
    titulo = Column(Text)
    url = Column(String)
    tipo = Column(String)
    local = Column(Text)
    situacao = Column(String)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    def __repr__(self):
        return f"<AgendaLegis(fonte={self.fonte}, categoria={self.categoria}, titulo={self.titulo})>"
