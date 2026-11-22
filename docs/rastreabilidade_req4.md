# Rastreabilidade Bidirecional — REQ 4 (F4)

| Requisito / Função | Artefato / Componente | Teste Unitário |
| :--- | :--- | :--- |
| F5 - Avaliar música (NF5.1–NF5.5) | `src/modulo_avaliacoes/servico_avaliacao.py` (`registrar_avaliacao`) | `test_deve_registrar_avaliacao_valida_de_musica_com_resenha_opcional`, `test_deve_bloquear_usuario_nao_autenticado`, `test_deve_rejeitar_nota_fora_do_intervalo_ou_sem_passo_de_meia_estrela` |
| F6 - Avaliar álbum (NF6.1–NF6.4) | `src/modulo_avaliacoes/servico_avaliacao.py` (`registrar_avaliacao`) | `test_deve_rejeitar_nota_fora_do_intervalo_ou_sem_passo_de_meia_estrela`, `test_deve_calcular_media_separada_para_musica_album_e_artista` |
| F7 - Avaliar artista (NF7.1–NF7.3) | `src/modulo_avaliacoes/servico_avaliacao.py` (`registrar_avaliacao`) | `test_deve_calcular_media_separada_para_musica_album_e_artista` |
| SE01–SE03 - Médias de música, álbum e artista | `src/modulo_avaliacoes/servico_avaliacao.py` (`calcular_media_conteudo`) | `test_deve_calcular_media_separada_para_musica_album_e_artista`, `test_deve_retornar_media_zero_quando_nao_houver_avaliacoes` |