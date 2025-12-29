import logging
import time
import random
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

# --- CONFIGURACIÓN ---
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def limpiar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

class WhatsAppBot:
    def __init__(self):
        self.session_path = "./session"
        self.mensajes_cont = 0

    def iniciar(self):
        limpiar_terminal()
        print("🚀 INICIANDO NAVEGADOR...")
        
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch_persistent_context(
            user_data_dir=self.session_path,
            headless=False,
            no_viewport=True,
            args=["--start-maximized"]
        )
        self.page = self.browser.pages[0]
        self.page.goto("https://web.whatsapp.com")

        try:
            logger.info("⏳ Esperando WhatsApp Web (Escanea el QR si es necesario)...")
            self.page.wait_for_selector('div[data-tab="3"]', timeout=120000)
            limpiar_terminal()
            print("✅ CONECTADO EXITOSAMENTE")
        except:
            input("⚠️  Presiona ENTER cuando ya veas tus chats en la pantalla...")
            limpiar_terminal()

    def escribir_como_humano(self, texto):
        selector = 'div[contenteditable="true"][data-tab="10"]'
        try:
            cuadro = self.page.wait_for_selector(selector, timeout=5000)
            cuadro.click()
            for letra in texto:
                self.page.keyboard.type(letra)
                time.sleep(random.uniform(0.04, 0.10))
            time.sleep(0.5)
            self.page.keyboard.press("Enter")
        except Exception as e:
            logger.error(f"❌ Error al intentar escribir: {e}")

    def bucle_principal(self):
        logger.info("🤖 Bot en patrulla... (Esperando mensajes no leídos)")
        
        while True:
            try:
                notificaciones = self.page.query_selector_all(
                    '#pane-side span[aria-label*="leído"], #pane-side span[aria-label*="unread"]'
                )
                
                for notif in notificaciones:
                    if notif.is_visible():
                        logger.info("📩 Nuevo mensaje detectado!")
                        notif.click()
                        time.sleep(1.5)

                        mensajes_in = self.page.query_selector_all(".message-in")
                        if mensajes_in:
                            ultimo_contenedor = mensajes_in[-1].query_selector(".copyable-text")
                            if ultimo_contenedor:
                                texto_recibido = ultimo_contenedor.inner_text().split('\n')[0]
                            else:
                                texto_recibido = "Mensaje multimedia o sin texto"

                            logger.info(f"👤 Usuario dice: {texto_recibido}")

                            # 🔹 RESPUESTA ACTUALIZADA
                            respuesta = (
                                "¡Hola! soy botLima. El titular no se encuentra disponible en este momento.\n"
                                "Gracias por escribir 👤"
                            )
                            
                            self.escribir_como_humano(respuesta)
                            self.mensajes_cont += 1
                            logger.info(f"✅ Respondido. Total: {self.mensajes_cont}")

                            time.sleep(1)
                            self.page.keyboard.press("Escape")
                            time.sleep(1)
                            break

                time.sleep(2)

            except Exception as e:
                time.sleep(3)

if __name__ == "__main__":
    bot = WhatsAppBot()
    try:
        bot.iniciar()
        bot.bucle_principal()
    except KeyboardInterrupt:
        print("\n🛑 Bot apagado por el usuario.")
    finally:
        pass
