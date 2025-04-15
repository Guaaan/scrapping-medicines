from datetime import datetime
from numpy import append
import requests
import json
import time
from datetime import datetime

archivo = 'Articulos Salcobrand'


def string_to_int(s):
    try:
        temp = int(eval(str(s)))
        if type(temp) == int:
            return temp
    except:
        return


categories = ['Medicamentos',
              'Adulto%20Mayor',
              'Cuidado%20de%20la%20Salud',
              'Infantil%20y%20Mam%C3%A1', 'Belleza',
              'Vitaminas%20y%20Suplementos',
              'Cuidado%20Personal',
              'Clinique',
              'Dermocoaching',
              'Marcas%20Exclusivas'
              ]
# url = "https://gm3rp06hjg-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.8.5)%3B%20Browser%20(lite)&x-algolia-api-key=51f403f1055fee21d9e54d028dc19eba&x-algolia-application-id=GM3RP06HJG"
url = "https://gm3rp06hjg-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.14.3)%3B%20Browser%20(lite)&x-algolia-api-key=0259fe250b3be4b1326eb85e47aa7d81&x-algolia-application-id=GM3RP06HJG"
res = []
try:
    for category in categories:

        for x in range(18):

            time.sleep(0.02)

            payload = "{\"requests\":[{\"indexName\":\"sb_variant_production\",\"params\":\"clickAnalytics=true&facets=%5B%22cyber%22%2C%22brand%22%2C%22normal_price%22%2C%22ribbon_info.promotion_label%22%2C%22drug_patent_type_filter%22%2C%22bioequivalent_filter.label%22%2C%22has_ribbon_misalcobrand%22%2C%22product_categories.lvl0%22%2C%22product_categories.lvl1%22%2C%22product_categories.lvl2%22%2C%22product_categories.lvl3%22%5D&filters=(timestamp_available_on%20%3C%201711030690)%20AND%20(id%3A22768%20OR%20id%3A22772%20OR%20id%3A22769%20OR%20id%3A51718%20OR%20id%3A40149%20OR%20id%3A22767%20OR%20id%3A22754%20OR%20id%3A22760%20OR%20id%3A46919%20OR%20id%3A53888%20OR%20id%3A51720%20OR%20id%3A52978%20OR%20id%3A45068%20OR%20id%3A46301)%20AND%20(is_store_exclusive%3Afalse%20OR%20available_communes%3A357)&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&highlightPreTag=%3Cais-highlight-0000000000%3E&hitsPerPage=24&maxValuesPerFacet=50&page=0&tagFilters=\"}]}"

            headers = {
                'Accept': '*/*',
                'Accept-Language': 'es-AR,es-419;q=0.9,es;q=0.8',
                'Connection': 'keep-alive',
                'Origin': 'https://salcobrand.cl',
                'Referer': 'https://salcobrand.cl/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'content-type': 'application/x-www-form-urlencoded',
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"'
            }

            r = requests.request("POST", url, headers=headers, data=payload)
            # print(r.status_code )
            data = r.json()
            # res.append(data['results'][0]['hits'])
            for p in data['results'][0]['hits']:
                p_oferta = p['direct_discount']
                p_club = p['direct_discount_sbpay']
                res.append({
                    'cod_farm_ext': 'S',
                    'sku': p['sku'],
                    'internal_id': p['id'],
                    'fecha_busq': datetime.now().strftime('%Y-%m-%d'),
                    'tipo_id': 's',
                    'nombre': p['name'],
                    'marca': p['brand'],
                    'precio_normal': p['normal_price'],
                    'precio_oferta': p_oferta,
                    'precio_club': p_club,
                    'cod_id': 'null',
                    'link': 'https://www.salcobrand.cl/products/' + p['slug'],
                    'img': p['catalog_image_url'],
                    'active_principle': p['slug'],
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
    f = open(f"../../logs/{datetime.now().strftime('%Y-%m-%d')}.txt", "a")
    # writing in the file
    f.write(str(Argument))
    # closing the file
    f.close()

finally:
    print(f'resultados salcobrand {str(len(res))}')
