import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MESSAGES_FILE = os.path.join(BASE_DIR, 'lang', 'es.json')

MESSAGES = {}

def load_messages():
    """Carga el contenido del archivo JSON definido en la variable global
    """
    global MESSAGES
    try:
        with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
            MESSAGES = json.load(f)
        print("mensajes cargados")
    except FileNotFoundError:
        print(f"ERROR: Archivo de mensajes no encontrado en {MESSAGES_FILE}")
    except json.JSONDecodeError:
        print("ERROR: Archivo de mensajes JSON con formato incorrecto")

def get_message(category: str, key: str, **kwargs) ->str:
    """busca un mensaje en el archivo cargado y le apliica el formato (sustitucion dde variables)

    Args:
        category (str): Categoria del mensaje
        key (str): Nombre del mensaje
        kwargs -> argumentos de sustitucon de variables (ej: usuario=Bastian)

    Returns:
        str: Retorna el mensaje en el formato definido
    """
    try:
        template = MESSAGES[category][key]

        return template.format(**kwargs)
    except KeyError:
        return f"ERROR de clave: {category}.{key} no encontrado"