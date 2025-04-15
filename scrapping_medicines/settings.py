# Archivo: settings.py (dentro de la carpeta scrapping_medicines)

# Configuración básica del bot
BOT_NAME = 'scrapping_medicines'

SPIDER_MODULES = ['scrapping_medicines.spiders']
NEWSPIDER_MODULE = 'scrapping_medicines.spiders'

# Obedecer robots.txt (mejor desactivar para scraping de prueba)
ROBOTSTXT_OBEY = False  # True = respeta reglas, False = ignora

# User-Agent personalizado (evitar bloqueos)
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Configuración de pipelines (si usas items.py)
ITEM_PIPELINES = {
    # 'scrapping_medicines.pipelines.ExamplePipeline': 300,
}

# Configuración de descargas
CONCURRENT_REQUESTS = 16  # Número de solicitudes simultáneas
DOWNLOAD_DELAY = 1  # Retardo entre solicitudes (segundos)
AUTOTHROTTLE_ENABLED = True  # Autoajuste dinámico de velocidad

# Configuración de headers
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
}