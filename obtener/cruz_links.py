import csv
import json

def csv_to_json(csv_file1, csv_file2, json_file):
    data = []

    # Leer el primer archivo CSV
    with open(csv_file1, 'r') as file1:
        csv_reader = csv.DictReader(file1, delimiter=';')
        for row in csv_reader:
            data.append({
                "sku": row["sku"],
                "nombre": row["nombre"],
                "cod_barra": row["cod_barra"]
            })

    # Leer el segundo archivo CSV
    with open(csv_file2, 'r') as file2:
        csv_reader = csv.DictReader(file2, delimiter=';')
        for row in csv_reader:
            data.append({
                "sku": row["sku"],
                "nombre": row["nombre"],
                "cod_barra": row["cod_barra"]
            })

    # Escribir los datos en un archivo JSON
    with open(json_file, 'w') as json_output:
        json.dump(data, json_output, indent=4, ensure_ascii=False)

# Nombres de los archivos de entrada y salida
csv_file1 = 'skus1.csv'
csv_file2 = 'skus2.csv'
json_file = 'cruz_links.json'

# Llamar a la función para realizar la conversión
csv_to_json(csv_file1, csv_file2, json_file)

print("Conversión completada.")