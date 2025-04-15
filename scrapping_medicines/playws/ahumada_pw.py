#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import json
from datetime import datetime
import re

def clean_string(texto):
    """Limpia cadenas de texto eliminando saltos de línea, tabulaciones y espacios innecesarios."""
    return texto.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()

def limpiar_precio(price):
    """Extrae y convierte el precio a un número entero."""
    numbers = re.findall(r'\d+', price)
    number_string = ''.join(map(str, numbers))
    return int(number_string)

def extract_gtin13(json_string):
    """Extrae el código GTIN13 de un JSON en formato de cadena."""
    pattern = r'"gtin13"\s*:\s*"(\d+)"'
    match = re.search(pattern, json_string)
    return match.group(1) if match else None

def get_date():
    """Obtiene la fecha actual en formato YYYY-MM-DD."""
    return datetime.today().strftime('%Y-%m-%d')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=5)
    context = browser.new_context()
    page = context.new_page()
    
    # Navegar a la página principal
    page.goto('https://www.farmaciasahumada.cl/medicamentos')
    page.wait_for_load_state('load')
    
    # Hacer clic en el botón de "decline" si aparece
    try:
        page.wait_for_selector('button.decline.btn.btn-primary', timeout=5000)
        page.click('button.decline.btn.btn-primary')
    except:
        print("Botón 'decline' no encontrado, continuando...")
    
    # Selector del botón para cargar más productos
    button_selector = 'button.btn.btn-primary.col-8.col-sm-4.more'
    
    # Hacer clic en el botón mientras esté disponible
    while True:
        try:
            page.wait_for_selector(button_selector, timeout=5000)
            page.click(button_selector)
            print("Botón encontrado y clickeado.")
        except:
            print("No se encontró más el botón, saliendo del bucle.")
            break
    
    # Extraer enlaces de los productos
    product_links = page.locator('a.link').all()
    product_urls = [f"https://www.farmaciasahumada.cl{link.get_attribute('href')}" for link in product_links]
    print(f"Se encontraron {len(product_urls)} productos.")
    
    # Guardar las URLs en un archivo JSON
    with open('../outputs/product_urls.json', 'w') as f:
        json.dump(product_urls, f, indent=4, ensure_ascii=False)
    
    print(f"Se guardaron {len(product_urls)} URLs en product_urls.json.")
    browser.close()
