# Usamos la imagen oficial de Playwright compatible con tu versión de requirements
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los requisitos primero para aprovechar la caché de capas de Docker
COPY requirements.txt .

# Instalamos dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalamos solo el navegador Chromium y sus dependencias de sistema
RUN playwright install chromium
RUN playwright install-deps chromium

# Copiamos todo el contenido del proyecto (incluyendo la carpeta src)
COPY . .

# Comando para arrancar el bot apuntando a la ruta correcta
# Nota: En Linux/Docker se usa 'python3' o 'python', el prefijo 'py' es exclusivo de Windows
CMD ["python", "src/main.py"]
