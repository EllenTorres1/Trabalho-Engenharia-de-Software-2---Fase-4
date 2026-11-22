import unittest
from datetime import datetime

from src.modulo_avaliacoes import (
    ConteudoMusical,
    ServicoAvaliacao,
    TipoConteudo,
    Usuario,
)
from src.modulo_avaliacoes.servico_avaliacao import ErroAvaliacao


class TestServicoAvaliacao(unittest.TestCase):
    def setUp(self) -> None:
        self.servico = ServicoAvaliacao()
        self.usuario_valido = Usuario(id_usuario=1, nome_usuario="ellen", autenticado=True)
        self.musica = ConteudoMusical(
            id_externo="trk_001", nome="Infiel", tipo=TipoConteudo.MUSICA
        )
        self.album = ConteudoMusical(
            id_externo="alb_001", nome="Só Toca Top", tipo=TipoConteudo.ALBUM
        )
        self.artista = ConteudoMusical(
            id_externo="art_001", nome="Marília Mendonça", tipo=TipoConteudo.ARTISTA
        )

    def test_deve_registrar_avaliacao_valida_de_musica_com_resenha_opcional(self) -> None:
        data = datetime(2026, 11, 20, 15, 0, 0)
        resultado = self.servico.registrar_avaliacao(
            usuario=self.usuario_valido,
            conteudo=self.musica,
            nota=4.5,
            data_avaliacao=data,
        )

        self.assertEqual(resultado["media"], 4.5)
        self.assertEqual(resultado["total_avaliacoes"], 1)
        self.assertIsNone(resultado["avaliacao"].texto_resenha)
        self.assertEqual(resultado["avaliacao"].data_avaliacao, data)

    def test_deve_bloquear_usuario_nao_autenticado(self) -> None:
        visitante = Usuario(id_usuario=2, nome_usuario="convidado", autenticado=False)

        with self.assertRaises(ErroAvaliacao):
            self.servico.registrar_avaliacao(
                usuario=visitante, conteudo=self.musica, nota=4.0
            )

    def test_deve_rejeitar_nota_fora_do_intervalo_ou_sem_passo_de_meia_estrela(self) -> None:
        for nota_invalida in [0.0, 5.5, -1.0, 3.3, True]:
            with self.subTest(nota=nota_invalida):
                with self.assertRaises(ErroAvaliacao):
                    self.servico.registrar_avaliacao(
                        usuario=self.usuario_valido,
                        conteudo=self.album,
                        nota=nota_invalida,
                    )

    def test_deve_calcular_media_separada_para_musica_album_e_artista(self) -> None:
        usuario_dois = Usuario(id_usuario=2, nome_usuario="maryana", autenticado=True)

        self.servico.registrar_avaliacao(self.usuario_valido, self.musica, 5.0)
        self.servico.registrar_avaliacao(usuario_dois, self.musica, 4.0)
        self.servico.registrar_avaliacao(self.usuario_valido, self.album, 3.5)
        self.servico.registrar_avaliacao(self.usuario_valido, self.artista, 5.0)

        self.assertEqual(
            self.servico.calcular_media_conteudo("trk_001", TipoConteudo.MUSICA), 4.5
        )
        self.assertEqual(
            self.servico.calcular_media_conteudo("alb_001", TipoConteudo.ALBUM), 3.5
        )
        self.assertEqual(
            self.servico.calcular_media_conteudo("art_001", TipoConteudo.ARTISTA), 5.0
        )

    def test_deve_retornar_media_zero_quando_nao_houver_avaliacoes(self) -> None:
        media = self.servico.calcular_media_conteudo("trk_999", TipoConteudo.MUSICA)
        self.assertEqual(media, 0.0)


if __name__ == "__main__":
    unittest.main()