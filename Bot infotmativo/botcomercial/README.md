Entendido. Si el comando python tampoco funciona directamente en tu terminal, el prefijo estándar en Windows para llamar al intérprete es py.

Aquí tienes el README.md final con todas las correcciones de rutas (src/), el prefijo py para evitar errores de comandos, y las dependencias actualizadas.

🤖 WhatsApp Business Bot - botLima
Este es un bot de automatización para WhatsApp Web desarrollado con Python y Playwright. Está diseñado para gestionar consultas comerciales, mostrar catálogos de productos y organizar flujos de pedidos (Lima/Provincias) de forma automatizada, simulando el comportamiento humano para reducir riesgos de detección.

🚀 Características
Detección de Mensajes: Escanea automáticamente la lista de chats en busca de notificaciones no leídas.

Gestión de Estados: Implementa una lógica de conversación que recuerda en qué etapa del proceso de compra se encuentra el cliente mediante una máquina de estados.

Comportamiento Humano: Utiliza tiempos de espera aleatorios y simulación de escritura tecla por tecla.

Arquitectura Modular: Separación de responsabilidades entre el motor del navegador (main.py) y la lógica de negocio (handler.py).

Filtro de Seguridad: Evita responder a mensajes propios (message-out) para prevenir bucles infinitos.

📂 Estructura del Proyecto
El código está organizado de manera modular siguiendo el principio de Responsabilidad Única:

src/main.py: El motor del bot. Controla la instancia de Playwright, la navegación y el bucle de escaneo.

src/handler.py: El cerebro del bot. Contiene la clase ChatHandler que define las respuestas según el flujo.

requirements.txt: Dependencias del proyecto.

dockerfile: Configuración para despliegue en contenedores.

🛠️ Instalación y Uso
Requisitos previos
Python 3.9 o superior.

Navegador Chromium (instalado vía Playwright).

Configuración (Uso del prefijo py)
Si los comandos pip o python no son reconocidos, utiliza el lanzador py:

Instalar dependencias:

Bash

py -m pip install -r requirements.txt
Instalar navegadores de Playwright:

Bash

py -m playwright install chromium
Ejecutar el bot
Desde la raíz del proyecto, ejecuta el motor principal ubicado en la carpeta src:

Bash

py src/main.py
🤖 Flujo de Conversación
El bot guía al usuario a través de los siguientes disparadores:

Inicio / Reset: Al escribir "hola", "buenas" o "MENU", el bot despliega el panel principal con 4 opciones.

Opciones del Menú:

"1": Muestra productos (Urban Pro y Traveler Max) e invita a escribir COMPRAR.

"2": Solicita el ID del pedido (formato: PEDIDO 12345).

"3": Deriva con un asesor humano.

"4": Muestra promociones del día.

Flujo de Compra (esperando_zona):

Si el usuario escribe "comprar", el bot solicita elegir entre Lima o Provincia.

Cierre de Venta (atendido):

Lima: Informa costo de delivery contraentrega (S/10) y solicita datos de dirección.

Provincia: Informa costo de envío (S/15), solicita adelanto y proporciona datos bancarios.

Silencio Automático: Una vez entregados los datos, el bot entra en estado atendido y deja de responder para no interrumpir al usuario.