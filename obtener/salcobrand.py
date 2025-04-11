from datetime import datetime
from numpy import append
import requests
import json
import time
from datetime import datetime

archivo = 'Articulos Salcobrand'

def envio():
    url_notif = "https://api.cdr.cl/notificar/v0.1?topico=recolector.inicio.ejecucion"

    payload = json.dumps({
    "farmacia": f"Parte 1 recolectando: {archivo}"
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url_notif, headers=headers, data=payload)

def termino():
    url = "https://api.cdr.cl/notificar/v0.1?topico=recolector.termino.ejecucion"

    payload = json.dumps({
    "farmacia": f"Parte 1 recolectando: {archivo}"
    })
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    
def error():
    url = "https://api.cdr.cl/notificar/v0.1?topico=recolector.error.ejecucion"

    payload = json.dumps({
    "archivo": f"{archivo}.py",
    "log": f"{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
def string_to_int(s):
    try:
        temp = int(eval(str(s)))
        if type(temp) == int:
            return temp
    except:
        return
    
envio()
categories = ['Medicamentos',
            'Adulto%20Mayor',
            'Cuidado%20de%20la%20Salud',
            'Infantil%20y%20Mam%C3%A1','Belleza',
            'Vitaminas%20y%20Suplementos',
            'Cuidado%20Personal',
            'Clinique',
            'Dermocoaching',
            'Marcas%20Exclusivas'
]
url = "https://gm3rp06hjg-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.8.5)%3B%20Browser%20(lite)&x-algolia-api-key=51f403f1055fee21d9e54d028dc19eba&x-algolia-application-id=GM3RP06HJG"
res = []
try:
    for category in categories:

        for x in range(18):
            
            time.sleep(0.02)


            payload = json.dumps({
                "requests": [
                    {
                        "indexName": "sb_variant_production",
                        "params": f"highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&filters=(timestamp_available_on%20%3C%201646663674)&hitsPerPage=96&page={x}&maxValuesPerFacet=50&clickAnalytics=true&facets=%5B%22cyber%22%2C%22brand%22%2C%22normal_price%22%2C%22ribbon_info.promotion_label%22%2C%22drug_patent_type_filter%22%2C%22bioequivalent_filter.label%22%2C%22has_ribbon_misalcobrand%22%2C%22product_categories.lvl0%22%2C%22product_categories.lvl1%22%2C%22product_categories.lvl2%22%2C%22product_categories.lvl3%22%5D&tagFilters=&facetFilters=%5B%5B%22product_categories.lvl0%3A{category}%22%5D%5D"
                    },
                    # {
                    #     "indexName": "sb_variant_production",
                    #     "params": "highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&filters=(timestamp_available_on%20%3C%201646663674)&hitsPerPage=1&page=0&maxValuesPerFacet=50&clickAnalytics=false&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&analytics=false&facets=%5B%22product_categories.lvl0%22%5D"
                    # }
                ]
            })
            headers = {
                'Content-Type': 'application/json'
            }

            r = requests.request("POST", url, headers=headers, data=payload)
            #print(r.status_code )
            data = r.json()
            # res.append(data['results'][0]['hits'])
            for p in data['results'][0]['hits']:
                p_oferta = p['direct_discount']
                p_club = p['direct_discount_sbpay']
                res.append({
                    'CodFarmExt': 'S',
                    'sku': p['sku'],
                    'FechaBusq': datetime.now().strftime('%Y-%m-%d'),
                    'TipoID': 's',
                    'nombre': p['name'],
                    'marca': p['brand'],
                    'precio_normal': p['normal_price'],
                    'precio_oferta': p_oferta,
                    'precio_club': p_club, 
                    'CodId': p['id'], 
                    'link': 'https://www.salcobrand.cl/products/' + p['slug'],
                    'img': p['catalog_image_url'],
                    'category': p['product_categories']['lvl0'][0],
                })

        

        for i in res:
            i['precio_oferta'] = str(i['precio_oferta']).replace('.0', '')
            i['precio_club'] = str(i['precio_club']).replace('.0', '')
            if i['precio_oferta'] != "None":
                i['precio_oferta'] = int(i['precio_oferta'])
            else:
                i['precio_oferta'] = 0
            if i['precio_club'] != "None":
                i['precio_club'] = int(i['precio_club'])
            else:
                i['precio_club'] = 0

            


        
        # for i in res:
        #     i['precio_oferta'] = int(float(i['precio_oferta']))
        #     i['precio_club'] = int(float(i['precio_club']))
            
            


        with open('../outputs/Sitems.json', 'w') as outfile:
            json.dump(res, outfile)
        print(f'{category.replace("%20", "")} terminado')

except Exception as Argument:
    print('Error mientras se obtenían datos de salcobrand')
    f = open(f"../logs/{datetime.now().strftime('%Y-%m-%d')}.txt", "a")
    # writing in the file
    f.write(str(Argument))
    # closing the file
    f.close()  
    error()
finally:
    print(f'resultados salcobrand {str(len(res))}')
    
    termino()