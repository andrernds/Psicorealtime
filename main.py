import json
from datetime import datetime
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from kivy.clock import Clock

ESTADOS = ["Tranquilo", "Ansioso", "Cansado", "Motivado", "Confuso"]
PERGUNTAS = [
    "O que fez você sorrir hoje?",
    "Se pudesse mudar algo na sua rotina, o que seria?",
    "Quais 3 coisas você agradece hoje?",
    "Como seu corpo está se sentindo agora?",
    "Existe algo que você precisa perdoar?"
]

DATA_FILE = "menteclara_dados.json"

def salvar_dado(estado, entrada):
    data = {
        "data": str(datetime.now().date()),
        "estado": estado,
        "entrada": entrada
    }
    try:
        with open(DATA_FILE, "r") as file:
            dados = json.load(file)
    except FileNotFoundError:
        dados = []

    dados.append(data)
    with open(DATA_FILE, "w") as file:
        json.dump(dados, file, indent=4)

def gerar_pdf():
    try:
        with open(DATA_FILE, "r") as file:
            dados = json.load(file)
    except FileNotFoundError:
        return

    pdf = canvas.Canvas("Relatorio_MenteClara.pdf")
    pdf.setTitle("Relatório MenteClara")

    y = 800
    for item in dados:
        pdf.drawString(50, y, f"{item['data']} - {item['estado']}")
        y -= 15
        pdf.drawString(60, y, item['entrada'][:100] + "...")
        y -= 25
        if y < 100:
            pdf.showPage()
            y = 800
    pdf.save()

def gerar_grafico():
    try:
        with open(DATA_FILE, "r") as file:
            dados = json.load(file)
    except FileNotFoundError:
        return

    contagem = {}
    for estado in ESTADOS:
        contagem[estado] = 0
    for item in dados:
        contagem[item["estado"]] += 1

    plt.bar(contagem.keys(), contagem.values(), color='skyblue')
    plt.title("Frequência dos Estados Emocionais")
    plt.ylabel("Ocorrências")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("grafico.png")
    plt.show()


class TelaPrincipal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.spinner = Spinner(text="Tranquilo", values=ESTADOS)
        self.pergunta = Label(text=random.choice(PERGUNTAS), size_hint_y=None, height=40)
        self.textinput = TextInput(hint_text="Escreva aqui...", size_hint_y=0.4)

        layout.add_widget(Label(text="Como está se sentindo hoje?"))
        layout.add_widget(self.spinner)
        layout.add_widget(self.pergunta)
        layout.add_widget(self.textinput)

        salvar_btn = Button(text="Salvar Entrada", on_press=self.salvar)
        grafico_btn = Button(text="Ver Gráfico", on_press=lambda x: gerar_grafico())
        pdf_btn = Button(text="Exportar PDF", on_press=lambda x: gerar_pdf())
        respiracao_btn = Button(text="Respiração Guiada", on_press=self.ir_respirar)

        layout.add_widget(salvar_btn)
        layout.add_widget(grafico_btn)
        layout.add_widget(pdf_btn)
        layout.add_widget(respiracao_btn)

        self.add_widget(layout)

    def salvar(self, instance):
        estado = self.spinner.text
        texto = self.textinput.text
        if texto.strip():
            salvar_dado(estado, texto)
            self.textinput.text = ""
            self.pergunta.text = random.choice(PERGUNTAS)

    def ir_respirar(self, instance):
        self.manager.current = "respiracao"


class TelaRespiracao(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20)
        self.label = Label(text="Respire Fundo...", font_size=32)
        self.layout.add_widget(self.label)
        self.add_widget(self.layout)
        self.respirando = False

    def on_enter(self):
        self.passos = ["Inspire", "Segure", "Expire", "Pausa"]
        self.index = 0
        self.contador = 4
        self.label.text = f"{self.passos[self.index]} ({self.contador})"
        self.evento = Clock.schedule_interval(self.respirar, 1)

    def respirar(self, dt):
        self.contador -= 1
        if self.contador <= 0:
            self.index = (self.index + 1) % len(self.passos)
            self.contador = 4
        self.label.text = f"{self.passos[self.index]} ({self.contador})"

    def on_leave(self):
        Clock.unschedule(self.evento)


class MenteClaraApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TelaPrincipal(name="principal"))
        sm.add_widget(TelaRespiracao(name="respiracao"))
        return sm

if __name__ == '__main__':
    MenteClaraApp().run()
