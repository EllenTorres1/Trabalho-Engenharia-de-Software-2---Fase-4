from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class TipoConteudo(str, Enum):
    MUSICA = "musica"
    ALBUM = "album"
    ARTISTA = "artista"


@dataclass(frozen=True)
class Usuario:
    id_usuario: int
    nome_usuario: str
    autenticado: bool = True


@dataclass(frozen=True)
class ConteudoMusical:
    id_externo: str
    nome: str
    tipo: TipoConteudo


@dataclass
class Avaliacao:
    id_usuario: int
    id_conteudo_musical: str
    tipo_conteudo: TipoConteudo
    nota: float
    titulo_resenha: Optional[str] = None
    texto_resenha: Optional[str] = None
    data_avaliacao: datetime = field(default_factory=datetime.utcnow)