# Se define una lista de precios que contiene listas de cadenas de caracteres
prec_arr = [['12', '990'], ['790', '12', '990'],
            ['10', '790', '12', '990'], ['130'], None]

# Se define una variable contador para imprimir los resultados de cada conjunto de precios
i = 1

# Se itera sobre la lista de precios
for arr in prec_arr:

    # Se determina la cantidad de elementos en la sublista actual
    cantidad_strings = len(arr)

    # Se inicializan los precios normal y de descuento
    precio_normal = 0
    precio_descuento = 0

    # Se define un diccionario de funciones para determinar los precios
    # El diccionario utiliza la cantidad de elementos en la sublista como clave
    switcher = {
        None: (0,0),  # Si no hay elementos, se devuelven 0 para ambos precios
        4: lambda: (int(arr[0] + arr[1]), int(arr[2] + arr[3])),  # Si hay 4 elementos, se concatenan pares para formar los precios
        3: lambda: (int(arr[0]) if len(arr[0]) == 3 else int(arr[0] + arr[1]), int(arr[1] + arr[2])),  # Si hay 3 elementos, se concatenan pares si es necesario y se asignan a los precios
        2: lambda: (int(arr[0]) if len(arr[0]) == 3 else int(arr[0]), int(arr[1]) if len(arr[1]) > 0 else 0),  # Si hay 2 elementos, se concatenan si es necesario y se asignan a los precios
        1: lambda: (int(arr[0]), 0),  # Si hay 1 elemento, se asigna al precio normal y el descuento es 0
    }

    # Se obtienen los precios normal y de descuento del diccionario usando la cantidad de elementos como clave
    precio_normal, precio_descuento = switcher.get(
        cantidad_strings, lambda: (0, 0))()

    # Se imprimen los resultados de los precios
    print(f'{i} cant_s:{cantidad_strings} precio normal:{precio_normal} precio descuento:{precio_descuento}')

    # Se incrementa el contador
    i += 1
