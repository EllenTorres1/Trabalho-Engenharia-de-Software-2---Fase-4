from flask import Flask, flash, redirect, render_template, request, url_for

from src.modulo_avaliacoes import (
    ConteudoMusical,
    ServicoAvaliacao,
    TipoConteudo,
    Usuario,
)
from src.modulo_avaliacoes.servico_avaliacao import ErroAvaliacao

app = Flask(__name__)
app.secret_key = "chave-dev-avaliacoes-musicais"

servico = ServicoAvaliacao()

USUARIO_ATUAL = Usuario(id_usuario=1, nome_usuario="ellen_rocha", autenticado=True)

CATALOGO_INICIAL = [
    ConteudoMusical(id_externo="trk_001", nome="Infiel — Marília Mendonça", tipo=TipoConteudo.MUSICA),
    ConteudoMusical(id_externo="alb_001", nome="Só Toca Top — Ana Lima", tipo=TipoConteudo.ALBUM),
    ConteudoMusical(id_externo="trk_002", nome="Hoje — Bruno & Marrone", tipo=TipoConteudo.MUSICA),
    ConteudoMusical(id_externo="art_001", nome="Marília Mendonça", tipo=TipoConteudo.ARTISTA),
]


@app.route("/", methods=["GET"])
def index():
    itens_com_media = []
    for item in CATALOGO_INICIAL:
        media = servico.calcular_media_conteudo(item.id_externo, item.tipo)
        itens_com_media.append(
            {
                "id_externo": item.id_externo,
                "nome": item.nome,
                "tipo": item.tipo.value,
                "media": media,
            }
        )

    avaliacoes = servico.listar_avaliacoes_usuario(USUARIO_ATUAL.id_usuario)
    nomes_por_id = {item.id_externo: item.nome for item in CATALOGO_INICIAL}

    return render_template(
        "index.html",
        usuario=USUARIO_ATUAL,
        catalogo=itens_com_media,
        avaliacoes=list(reversed(avaliacoes)),
        nomes_por_id=nomes_por_id,
    )


@app.route("/avaliar", methods=["POST"])
def avaliar():
    id_conteudo = request.form.get("id_conteudo", "")
    nota_raw = request.form.get("nota", "")
    titulo_resenha = request.form.get("titulo_resenha", "")
    texto_resenha = request.form.get("texto_resenha", "")

    conteudo_selecionado = next(
        (item for item in CATALOGO_INICIAL if item.id_externo == id_conteudo),
        None,
    )

    try:
        nota = float(nota_raw)
        servico.registrar_avaliacao(
            usuario=USUARIO_ATUAL,
            conteudo=conteudo_selecionado,
            nota=nota,
            titulo_resenha=titulo_resenha,
            texto_resenha=texto_resenha,
        )
        flash("Avaliação registrada com sucesso!", "sucesso")
    except ValueError:
        flash("Selecione uma nota válida entre 0,5 e 5,0.", "erro")
    except ErroAvaliacao as erro:
        flash(str(erro), "erro")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)