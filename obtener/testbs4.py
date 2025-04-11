from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urlparse


bc_url = 'https://farmex.cl/collections/antibioticos-y-antivirales/products/cotrimoxazol-forte-comprimidos-cotrimoxazol'
u = urlparse(bc_url)
category = u.path.split('/')[3]
req = requests.get(bc_url)
soup = BeautifulSoup(req.text, 'html.parser')
script = soup.find_all('script')[2].text
script_tag = json.loads(script)
print(script_tag)

# print(barcode)
