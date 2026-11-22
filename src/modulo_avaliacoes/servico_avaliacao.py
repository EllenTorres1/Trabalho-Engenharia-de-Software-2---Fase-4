from datetime import datetime
from typing import Dict, List, Optional

from .models import Avaliacao, ConteudoMusical, TipoConteudo, Usuario


class ErroAvaliacao(ValueError):
    """Erro de regra de negócio no módulo de avaliações musicais."""


class ServicoAvaliacao:
    """Serviço responsável por registrar e consultar avaliações musicais.

    Rastreabilidade (REQ 4): F5, F6, F7, NF5.1-NF5.5, NF6.1-NF6.4, NF7.1-NF7.3, SE01-SE03.
    """

    def __init__(self) -> None:
        self._avaliacoes: List[Avaliacao] = []

    def _validar_nota(self, nota: float) -> None:
        if not isinstance(nota, (int, float)) or isinstance(nota, bool):
            raise ErroAvaliacao("A nota deve ser numérica.")
        if nota < 0.5 or nota > 5.0:
            raise ErroAvaliacao("A nota deve estar entre 0,5 e 5,0 estrelas.")
        if round(nota * 2) != nota * 2:
            raise ErroAvaliacao("A nota deve utilizar intervalos de 0,5 estrela.")

    def registrar_avaliacao(
        self,
        usuario: Optional[Usuario],
        conteudo: Optional[ConteudoMusical],
        nota: float,
        titulo_resenha: Optional[str] = None,
        texto_resenha: Optional[str] = None,
        data_avaliacao: Optional[datetime] = None,
    ) -> Dict[str, object]:
        if usuario is None or not usuario.autenticado:
            raise ErroAvaliacao("Somente usuários autenticados podem publicar avaliações.")

        if conteudo is None or not conteudo.id_externo.strip() or not conteudo.nome.strip():
            raise ErroAvaliacao("Conteúdo musical inválido para avaliação.")

        self._validar_nota(nota)

        titulo_limpo = titulo_resenha.strip() if titulo_resenha else None
        texto_limpo = texto_resenha.strip() if texto_resenha else None
        if titulo_limpo == "":
            titulo_limpo = None
        if texto_limpo == "":
            texto_limpo = None

        avaliacao = Avaliacao(
            id_usuario=usuario.id_usuario,
            id_conteudo_musical=conteudo.id_externo,
            tipo_conteudo=conteudo.tipo,
            nota=float(nota),
            titulo_resenha=titulo_limpo,
            texto_resenha=texto_limpo,
            data_avaliacao=data_avaliacao or datetime.utcnow(),
        )
        self._avaliacoes.append(avaliacao)

        avaliacoes_conteudo = [
            item
            for item in self._avaliacoes
            if item.id_conteudo_musical == conteudo.id_externo
            and item.tipo_conteudo == conteudo.tipo
        ]
        soma = sum(item.nota for item in avaliacoes_conteudo)
        media = round(soma / len(avaliacoes_conteudo), 2)

        return {
            "avaliacao": avaliacao,
            "media": media,
            "total_avaliacoes": len(avaliacoes_conteudo),
            "tipo": conteudo.tipo.value,
        }

    def calcular_media_conteudo(
        self, id_conteudo_musical: str, tipo_conteudo: TipoConteudo
    ) -> float:
        if not id_conteudo_musical or not id_conteudo_musical.strip():
            raise ErroAvaliacao("Identificador do conteúdo musical é obrigatório.")

        avaliacoes_conteudo = [
            item
            for item in self._avaliacoes
            if item.id_conteudo_musical == id_conteudo_musical
            and item.tipo_conteudo == tipo_conteudo
        ]
        if not avaliacoes_conteudo:
            return 0.0

        soma = sum(item.nota for item in avaliacoes_conteudo)
        return round(soma / len(avaliacoes_conteudo), 2)

    def listar_avaliacoes_usuario(self, id_usuario: int) -> List[Avaliacao]:
        return [item for item in self._avaliacoes if item.id_usuario == id_usuario]