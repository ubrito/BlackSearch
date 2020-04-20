# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from bs4 import BeautifulSoup

import json
import requests
import sys


def carregar_dados():
    try:
        return json.load(open('./dados.json', 'r'))
    except FileNotFoundError:
        return []


def sincronizar_dados():
    pagina = requests.get("https://blackarch.org/tools.html")
    tabela = BeautifulSoup(pagina.content, 'html.parser').find(id="tbl-minimalist")

    nomes = [n.get_text() for n in tabela.find_all_next(itemprop="name")]
    versoes = [v.get_text() for v in tabela.find_all_next(itemprop="version")]
    descricoes = [d.get_text() for d in tabela.find_all_next(itemprop="description")]
    categorias = [c.get_text().strip() for c in tabela.find_all_next(itemprop="genre")]
    links = [l.a.get('href') for l in tabela.find_all_next(itemprop="mainEntityOfPage")]

    dados = []

    for i in range(len(nomes)):
        dados.append(
            {
                "nome": nomes[i],
                "versao": versoes[i],
                "descricao": descricoes[i],
                "categoria": categorias[i],
                "link": links[i]
            }
        )

    with open('dados.json', 'w') as d:
        json.dump(dados, d)

    return dados


class Tela(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Tela, self).__init__(*args, **kwargs)
        self.dados = carregar_dados()

        self.categorias = [d["categoria"] for d in self.dados]
        self.categorias = sorted(set(self.categorias))
        self.categorias[0] = "Todas"
        # print(self.categorias)

        self.combo = QComboBox(self)  # Combo para selecionar a categoria
        self.categorias[0] = "Todas"
        self.combo.addItems(self.categorias)
        self.combo.move(10, 120)
        self.combo.resize(280, 30)
        self.combo.currentIndexChanged.connect(self.relistar_pacotes)

        self.imagem = QLabel(self)
        self.imagem.setPixmap(QPixmap("./banner.png"))
        self.imagem.resize(400, 100)
        self.imagem.move(0, 0)

        self.bt_sinc = QPushButton("Sync", self)
        self.bt_sinc.resize(80, 30)
        self.bt_sinc.move(310, 120)

        self.layout = QVBoxLayout(self)
        self.widget = QWidget(self)
        self.area = QScrollArea(self)

        self.widget.setLayout(self.layout)
        self.area.setWidget(self.widget)

        self.area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.area.setWidgetResizable(True)
        self.area.move(10, 170)
        self.area.setFixedSize(380, 420)
        self.area.setStyleSheet("Background-Color: #143B69;")

        self.listar_pacotes(self.dados)

    def relistar_pacotes(self):
        # Limpar área para listar os pacotes da pesquisa
        for i in range(self.layout.count()):
            self.layout.itemAt(i).widget().close()

        dados2 = []
        if self.combo.currentText() != "Todas":
            for i in range(len(self.dados)):
                if self.dados[i]["categoria"] == self.combo.currentText().strip():
                    dados2.append(self.dados[i])
        else:
            dados2 = json.load(open('./dados.json', 'r'))

        self.listar_pacotes(dados2)

    def listar_pacotes(self, dados):

        for i in range(len(dados)):
            frame = QFrame()
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setFrameShadow(QFrame.Sunken)
            frame.setMaximumWidth(345)
            frame.setStyleSheet("Background-Color: #BBBBBB;")
            # frame.setFrameStyle(12)

            nome = QLabel(dados[i]["nome"])
            nome.setFixedHeight(30)
            nome.setAlignment(Qt.AlignCenter)
            nome.setStyleSheet(
                "Background-color: #333333;"
                "color: white;"
                "Font-size: 15px;"
                "Font-family: Verdana"
            )

            grupo = QLabel(dados[i]["categoria"])
            grupo.setFixedHeight(20)
            grupo.setAlignment(Qt.AlignCenter)
            grupo.setStyleSheet(
                "Background-color: #9ECFFF;"
                "font: 12px;"
                "font-family: 'Lucida Console'"
            )

            desc = QLabel(dados[i]["descricao"])
            desc.setWordWrap(True)
            desc.setMaximumWidth(350)
            desc.setAlignment(Qt.AlignJustify)

            hlay = QHBoxLayout()
            vlay = QVBoxLayout()

            hlay.addWidget(nome)
            vlay.addLayout(hlay)
            vlay.addWidget(grupo)
            vlay.addWidget(desc)
            frame.setLayout(vlay)

            self.layout.addWidget(frame)

            print("listando")
        print("Listou!!!!!!!!!!!!!!")


def main():
    app = QApplication(sys.argv)

    tela = Tela()
    tela.setStyleSheet("Background-Color: #333333;")
    tela.setGeometry(60, 60, 400, 600)
    tela.setFixedSize(400, 600)
    tela.setWindowTitle('Busca de pacotes do BlackArch')
    tela.setWindowIcon(QIcon("./logo.png"))
    tela.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
