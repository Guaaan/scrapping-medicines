try:
    import insert_ahumada as ahumada
except:
    print("problema importando ahumada") 
# import insert_cruzverde as cruzverde
try:
    import insert_salcobrand as salcobrand
except:
    print("problema importando salcobrand") 
try:
    import insert_eco as eco
except:
    print("problema importando ecofarmacias") 
try:
    import insert_farmex as farmex 
except:
    print("problema importando farmex")
try:
    import insert_simi as simi 
except:
    print("problema importando dr simi")    

import requests
import json

try:
    ahumada
except:
    print("problema en ahumada")
#cruzverde
try:
    salcobrand
except:
    print("problema en salcobrand")
try:
    eco
except:
    print("problema en ecofarmacias")
try:
    farmex
except:
    print("problema en farmex")
try:
    simi
except:
    print("problema en simi")
    
print('terminado todo ')