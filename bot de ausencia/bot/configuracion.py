import logging
import os

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)
def limpiar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')