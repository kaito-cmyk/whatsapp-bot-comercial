import time
import random
from playwright.sync_api import sync_playwright
from bot.configuracion import logger, limpiar_terminal

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
            logger.info("⏳ Esperando WhatsApp Web...")
            self.page.wait_for_selector('div[data-tab="3"]', timeout=120000)
            limpiar_terminal()
            print("✅ CONECTADO EXITOSAMENTE")
        except:
            input("⚠️ Presiona ENTER cuando ya veas tus chats...")
            limpiar_terminal()

    def escribir_como_humano(self, texto):
        selector = 'div[contenteditable="true"][data-tab="10"]'
        try:
            cuadro = self.page.wait_for_selector(selector, timeout=5000)
            cuadro.click()
            for letra in texto:
                self.page.keyboard.type(letra)
                time.sleep(random.uniform(0.04, 0.10))
            self.page.keyboard.press("Enter")
        except Exception as e:
            logger.error(f"❌ Error: {e}")

    def bucle_principal(self):
        logger.info("🤖 Bot en patrulla...")
        while True:
            try:
                notif = self.page.query_selector('#pane-side span[aria-label*="leído"], #pane-side span[aria-label*="unread"]')
                if notif and notif.is_visible():
                    notif.click()
                    time.sleep(1.5)
                    respuesta = "¡Hola! soy botLima. El titular no se encuentra disponible.\nGracias por escribir 👤"
                    self.escribir_como_humano(respuesta)
                    self.mensajes_cont += 1
                    logger.info(f"✅ Respondido. Total: {self.mensajes_cont}")
                    time.sleep(1)
                    self.page.keyboard.press("Escape")
                time.sleep(2)
            except:
                time.sleep(3)