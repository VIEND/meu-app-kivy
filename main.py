import os
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from plyer import filechooser

class TelegramUploaderApp(App):
    def build(self):
        self.caminho_foto = None

        # Credenciais extraídas do seu fluxo
        self.token = "8202593317:AAFKMFyV6RFGV7PrtozVd8Wve8c5Z8aviXU"
        self.chat_id = "-1002656784772"

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        layout.add_widget(Label(
            text="Backup de Fotos para o Telegram", 
            font_size='18sp', 
            size_hint_y=None, 
            height=40
        ))

        # Botão para escolher foto da câmera/galeria
        btn_selecionar = Button(
            text="1. Selecionar Foto", 
            size_hint_y=None, 
            height=50
        )
        btn_selecionar.bind(on_press=self.abrir_seletor)
        layout.add_widget(btn_selecionar)

        # Status do arquivo selecionado
        self.lbl_status = Label(text="Nenhuma foto selecionada", font_size='14sp')
        layout.add_widget(self.lbl_status)

        # Botão de envio
        btn_enviar = Button(
            text="2. Enviar para o Telegram", 
            size_hint_y=None, 
            height=50,
            background_color=(0.1, 0.7, 0.3, 1)
        )
        btn_enviar.bind(on_press=self.enviar_foto)
        layout.add_widget(btn_enviar)

        return layout

    def abrir_seletor(self, instance):
        filechooser.open_file(on_selection=self.foto_selecionada, filters=['*.jpg', '*.jpeg', '*.png'])

    def foto_selecionada(self, selection):
        if selection:
            self.caminho_foto = selection[0]
            nome = os.path.basename(self.caminho_foto)
            self.lbl_status.text = f"Selecionado: {nome}"

    def enviar_foto(self, instance):
        if not self.caminho_foto:
            self.lbl_status.text = "⚠️ Selecione uma foto primeiro!"
            return

        self.lbl_status.text = "Enviando para o Telegram..."
        url = f"https://api.telegram.org/bot{self.token}/sendPhoto"

        try:
            with open(self.caminho_foto, 'rb') as foto:
                payload = {'chat_id': self.chat_id}
                files = {'photo': foto}
                resposta = requests.post(url, data=payload, files=files)

            if resposta.status_code == 200:
                self.lbl_status.text = "✅ Foto enviada com sucesso!"
            else:
                self.lbl_status.text = f"❌ Erro {resposta.status_code}: {resposta.text}"
        except Exception as e:
            self.lbl_status.text = f"⚠️ Falha: {str(e)}"

if __name__ == '__main__':
    TelegramUploaderApp().run()
