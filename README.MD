# scrapping-medicines
Una app que busca todos los medicamentos de la página de la Farmacia Ahumada y los devuelve como objetos en un archivo .json (puedes ver un ejemplo de como se ve después de correr por menos de 4 minutos en **example_output.json**).
Usa la librería scrapy y está programado en Python 3.10.1.

para correr el programa es recomendable crear un entorno virtual con [virtualenv](https://virtualenv.pypa.io/en/latest/) ejecutando:

```
$ python -m venv venv

$ source venv/bin/activate
```	
instalar las librerias de *requirements.txt*
y luego ejecutar:
```
$ scrapy crawl medicine -O medicine.json
>si se quiere sobreescribir el archivo existente:
scrapy crawl medicine -o medicine.json
>si se quieren agregar sumar los datos al archivo existente:
```
