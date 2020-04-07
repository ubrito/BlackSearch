# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from bs4 import BeautifulSoup
import requests
import json
import sys


class Tela(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Tela, self).__init__(*args, **kwargs)
        self.categorias = []
        self.dados = self.dados_salvos() #self.coleta_dados()
        self.qtd_linhas = len(self.dados)
        #self.coleta_dados()

        self.cria_widgets()

        self.inicia_tela()

    def inicia_tela(self):
        self.setStyleSheet("Background-Color: #333333;") ##801e00
        self.setGeometry(60, 60, 400, 600)
        self.setFixedSize(400, 600)
        self.setWindowTitle('Busca de pacotes do BlackArch')
        self.setWindowIcon(QIcon("./logo.png"))
        self.show()

    def cria_widgets(self):
        self.combo = QComboBox(self)  # Combo para selecionar a categoria
        self.combo.addItems(self.categorias)
        self.combo.move(10, 120)
        self.combo.resize(280, 30)

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

        for i in range(self.qtd_linhas):
            frame = QFrame()
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setFrameShadow(QFrame.Sunken)
            frame.setMaximumWidth(345)
            frame.setStyleSheet("Background-Color: #BBBBBB;")
            #frame.setFrameStyle(12)

            nome = QLabel(self.dados[i]["name"])
            nome.setAlignment(Qt.AlignCenter)
            nome.setStyleSheet(
                "Background-color: #333333;"
                "color: white;"
                "Font-size: 15px;"
                "Font-family: Verdana"
            )

            grupo = QLabel(self.dados[i]["category"])
            grupo.setAlignment(Qt.AlignCenter)
            grupo.setStyleSheet(
                "Background-color: #9ECFFF;"
                "font: 12px;"
                "font-family: 'Lucida Console'"
            )

            desc = QLabel(self.dados[i]["description"])
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

        self.widget.setLayout(self.layout)
        self.area.setWidget(self.widget)

        self.area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.area.setWidgetResizable(True)
        self.area.move(10, 170)
        self.area.setFixedSize(380, 420)
        self.area.setStyleSheet("Background-Color: #143B69;")

    def coleta_dados(self):
        page = requests.get("https://blackarch.org/tools.html")
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find(id="tbl-minimalist")

        names = [ n.get_text() for n in table.find_all_next(itemprop="name") ]
        versions = [ t.get_text() for t in table.find_all_next(itemprop="version") ]
        descriptions = [ d.get_text() for d in table.find_all_next(itemprop="description") ]
        categories = [ c.get_text() for c in table.find_all_next(itemprop="genre") ]
        links = [ l.a.get('href') for l in table.find_all_next(itemprop="mainEntityOfPage") ]

        self.categorias = sorted(set(categories))

        dados = []

        for i in range(len(names)):
            dados.append(
                {
                    "name": names[i].strip(),
                    "version": versions[i].strip(),
                    "description": descriptions[i].strip(),
                    "category": categories[i].strip(),
                    "link": links[i].strip()
                }
            )

        with open('dados.json', 'w') as d:
            json.dump(dados, d)

        return dados


    def dados_salvos(self):
        try:
            return json.load(open('./dados.json', 'r'))
        except:
            return False

    def compara_dados(self):
        if self.dados_salvos() == self.coleta_dados:
            return True
        else:
            return False

def main():

    '''
    if compara_dados():
        dados = dados_salvos()
    else:
        dados = coleta_dados()
    '''
    app = QApplication(sys.argv)
    main = Tela()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()