import logging
import time
import random
import os
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def limpiar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

class WhatsAppBot:
    def __init__(self):
        self.mensajes_cont = 0
        self.estado = None 

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

    def menu_principal(self):
        return (
            "👋 ¡Hola! soy *botLima*.\n\n"
            "¿En qué puedo ayudarte?\n\n"
            "1️⃣ Ver productos\n"
            "2️⃣ Estado de mi pedido\n"
            "3️⃣ Hablar con un asesor\n"
            "4️⃣ Promociones del día\n\n"
            "👉 *Escribe el número de la opción o escribe MENU para volver a empezar*."
        )

    def bucle_principal(self):
        logger.info("🤖 Bot activo — esperando mensajes nuevos...")
        while True:
            try:
                notificaciones = self.page.query_selector_all('#pane-side span[aria-label*="unread"], #pane-side span[aria-label*="leído"]')

                for notif in notificaciones:
                    if notif.is_visible():
                        notif.click()
                        time.sleep(1.5)

                        todos_los_mensajes = self.page.query_selector_all(".message-in, .message-out")
                        if not todos_los_mensajes:
                            continue

                        ultimo_msg_div = todos_los_mensajes[-1]
                        clases = ultimo_msg_div.get_attribute("class")

                        if "message-out" in clases:
                            self.page.keyboard.press("Escape")
                            continue

                        ultimo_texto_elem = ultimo_msg_div.query_selector(".copyable-text")
                        texto = ultimo_texto_elem.inner_text().split("\n")[0].strip() if ultimo_texto_elem else "Mensaje multimedia"

                        logger.info(f"👤 Usuario: {texto}")

                        respuesta = self.procesar(texto)
                        
                        # Si la respuesta no es None, enviamos mensaje
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

    # ---------------- LÓGICA DE CONVERSACIÓN MEJORADA ----------------
    def procesar(self, texto):
        t = texto.lower()

        # Si el usuario escribe MENU en cualquier momento, reseteamos estado y damos menú
        if "menu" in t or "menú" in t:
            self.estado = None
            return self.menu_principal()

        # Si el bot ya dio los datos de envío, se queda callado hasta que digan MENU
        if self.estado == "atendido":
            return None

        # Lógica de compra y zonas
        if self.estado == "esperando_zona":
            if "lima" in t:
                self.estado = "atendido" # Cambiamos a atendido para que no repita
                return (
                    "🚚 *El Delivery es de 10 soles*\n\n"
                    "Como es *contraentrega*, necesito:\n"
                    "📛 *Nombre completo*\n"
                    "📍 *Dirección exacta*\n\n"
                    "⚠️ *Escribe MENU si deseas volver al inicio.*"
                )
            if "prov" in t:
                self.estado = "atendido" # Cambiamos a atendido
                return (
                    "✈️ *El envío a Provincia es de 15 soles.Pago destino*\n\n"
                    "Necesitamos 50% de adelanto, nesecitamos su: nombre completo,dni,destino exacto.\n"
                    "💳 *BCP:* 111-11111111-1\n"
                    "📲 *Yape:* 111111111\n\n"
                    "⚠️ *Escribe MENU si deseas volver al inicio.*"
                )
            return "❓ ¿El envío es para *Lima* o *Provincia*? (Escribe una opción)"

        # Opciones normales del menú
        if t in ["hola", "buenas"]: return self.menu_principal()
        
        if t == "1": return "🛍️ *Productos:*\n🎒 Urban Pro — S/89\n🎒 Traveler Max — S/120\n👉 Escribe *COMPRAR* para ordenar."
        if t == "2": return "📦 Envíame tu pedido así: *PEDIDO 12345*"
        if t == "3": return "👤 Un asesor te atenderá en breve. Espera un momento..."
        if t == "4": return "🔥 *Promos:* Traveler Max 10% OFF hoy."
        
        if t.startswith("comprar"):
            self.estado = "esperando_zona"
            return "📍 ¿El envío es para *Lima* o *Provincia*?"
            
        if t.startswith("pedido"): 
            return "🔎 Estamos Verificando, en unos minutos un asesor le dira el estado de su pedido... (Escribe MENU para volver)"
        
        # Mensaje de error con instrucción clara de volver al inicio
        return (
            "🤖 No logré entender esa opción.\n\n"
            "🔄 Escribe *MENU* para ver las opciones principales nuevamente."
        )

if __name__ == "__main__":
    bot = WhatsAppBot()
    bot.iniciar()
    bot.bucle_principal()