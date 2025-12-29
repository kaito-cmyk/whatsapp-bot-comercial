class ChatHandler:
    def __init__(self):
        # Mantenemos el estado aquí dentro
        self.estado = None 

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

    def procesar(self, texto):
        t = texto.lower()

        if "menu" in t or "menú" in t:
            self.estado = None
            return self.menu_principal()

        if self.estado == "atendido":
            return None

        if self.estado == "esperando_zona":
            if "lima" in t:
                self.estado = "atendido"
                return (
                    "🚚 *El Delivery es de 10 soles*\n\n"
                    "Como es *contraentrega*, necesito:\n"
                    "📛 *Nombre completo*\n"
                    "📍 *Dirección exacta*\n\n"
                    "⚠️ *Escribe MENU si deseas volver al inicio.*"
                )
            if "prov" in t:
                self.estado = "atendido"
                return (
                    "✈️ *El envío a Provincia es de 15 soles.Pago destino*\n\n"
                    "Necesitamos 50% de adelanto, nesecitamos su: nombre completo,dni,destino exacto.\n"
                    "💳 *BCP:* 111-11111111-1\n"
                    "📲 *Yape:* 111111111\n\n"
                    "⚠️ *Escribe MENU si deseas volver al inicio.*"
                )
            return "❓ ¿El envío es para *Lima* o *Provincia*? (Escribe una opción)"

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
        
        return "🤖 No logré entender esa opción.\n\n🔄 Escribe *MENU* para volver a las opciones."