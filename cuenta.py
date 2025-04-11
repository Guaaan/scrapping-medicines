import json

archivo = 'outputs/itemsSimi'

# Carga el archivo JSON
with open(f'{archivo}.json', 'r') as f:
    data = json.load(f)

# Crea un diccionario para almacenar los recuentos
counts = {}
# Variable para contar los elementos repetidos
repeated_count = 0

# Itera sobre los elementos del archivo JSON y actualiza los recuentos
for item in data:
    item_key = tuple(item.items())
    if item_key in counts:
        counts[item_key] += 1
        repeated_count += 1  # Incrementa el contador de elementos repetidos
    else:
        counts[item_key] = 1

# Imprime los recuentos de los elementos repetidos
for item, count in counts.items():
    if count > 1:
        print(f"{dict(item)}: {count}")
print(f"Total de elementos repetidos: {repeated_count}")

# Pide al usuario que elimine los duplicados
remove_duplicates = input("¿Desea eliminar los elementos duplicados? (y/n): ")

# Si el usuario ingresa "y", crea una nueva lista con elementos únicos
if remove_duplicates.lower() == "y":
    unique_data = [dict(item) for item in counts.keys()]
    print(f"Se encontraron {repeated_count} elementos duplicados. Se eliminaron {len(data) - len(unique_data)} elementos.")
    # Sobrescribe el archivo JSON original con los elementos únicos
    with open(f'{archivo}.json', 'w') as f:
        json.dump(unique_data, f)
    print("Se eliminaron los elementos duplicados.")
else:
    print("No se eliminaron los elementos duplicados.")
    # Puedes seguir usando la lista original data que contiene los elementos duplicados