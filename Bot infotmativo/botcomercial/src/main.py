import logging
import time
import random
import os
from playwright.sync_api import sync_playwright
# IMPORTANTE: Importar el handler
from handler import ChatHandler

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def limpiar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

class WhatsAppBot:
    def __init__(self):
        self.mensajes_cont = 0
        # Creamos la instancia del handler AQUÍ
        self.handler = ChatHandler()

    def iniciar(self):
        limpiar_terminal()
        print("🚀 INICIANDO NAVEGADOR...")
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch(headless=False, args=["--start-maximized"])
        self.context = self.browser.new_context(no_viewport=True)
        self.page = self.context.new_page()
        self.page.goto("https://web.whatsapp.com")
        print("📱 Escanea el QR para continuar...")
        self.page.wait_for_selector('div[data-tab="3"]', timeout=0)
        limpiar_terminal()
        print("✅ QR ESCANEADO — BOT ACTIVO")

    def escribir_como_humano(self, texto):
        selector = 'div[contenteditable="true"][data-tab="10"]'
        try:
            cuadro = self.page.wait_for_selector(selector, timeout=5000)
            cuadro.click()
            for letra in texto:
                self.page.keyboard.type(letra)
                time.sleep(random.uniform(0.04, 0.10))
            time.sleep(0.4)
            self.page.keyboard.press("Enter")
        except Exception as e:
            logger.error(f"❌ Error al escribir: {e}")

    def bucle_principal(self):
        logger.info("🤖 Bot activo — esperando mensajes nuevos...")
        while True:
            try:
                # Localizamos notificaciones
                notificaciones = self.page.query_selector_all('#pane-side span[aria-label*="unread"], #pane-side span[aria-label*="leído"]')

                for notif in notificaciones:
                    if notif.is_visible():
                        notif.click()
                        time.sleep(1.5)

                        todos_los_mensajes = self.page.query_selector_all(".message-in, .message-out")
                        if not todos_los_mensajes: continue

                        ultimo_msg_div = todos_los_mensajes[-1]
                        clases = ultimo_msg_div.get_attribute("class")

                        # Evitar respondernos a nosotros mismos
                        if "message-out" in clases:
                            self.page.keyboard.press("Escape")
                            continue

                        ultimo_texto_elem = ultimo_msg_div.query_selector(".copyable-text")
                        texto = ultimo_texto_elem.inner_text().split("\n")[0].strip() if ultimo_texto_elem else "Mensaje multimedia"

                        logger.info(f"👤 Usuario: {texto}")

                        # --- AQUÍ ESTABA EL FALLO: Ahora llamamos al handler ---
                        respuesta = self.handler.procesar(texto)
                        
                        if respuesta:
                            self.escribir_como_humano(respuesta)
                            self.mensajes_cont += 1
                            logger.info(f"📨 Respondido. Total: {self.mensajes_cont}")

                        self.page.keyboard.press("Escape")
                        time.sleep(1)
                        break 

                time.sleep(2)
            except Exception as e:
                time.sleep(3)

if __name__ == "__main__":
    bot = WhatsAppBot()
    bot.iniciar()
    bot.bucle_principal()