# Scraper de Farmacias

Este proyecto es un scraper que recopila información de farmacias en línea y la guarda en un archivos json que luego lee para insertar en una base de datos SQL. Está dividido en cuatro carpetas principales: `guardar`, `obtener`, `outputs` y `logs`.

## instrucciones
La mejor manera de correr este programa es desde un entrono virtual en la terminal del sistema. Cómo hacerlo depende del sistema operativo que se vaya a utilizar (instrucciones más adelante). Pero se deben agendar tareas en el programador de tareas (Windows) o el crontanb (linux).

También se deben instalar via `pip install` requirements.txt

## Windows

### Crear el entorno virtual

1. Abre una ventana de comando en la ubicación donde deseas crear el entorno virtual.
2. Ejecuta el siguiente comando para crear el entorno virtual: `python -m venv nombre_del_entorno_virtual`

### Activar el entorno virtual

1. Abre una ventana de comando en la ubicación donde se encuentra el entorno virtual.
2. Ejecuta el siguiente comando para activar el entorno virtual: `nombre_del_entorno_virtual\Scripts\activate.bat`
3. Una vez que el entorno virtual se active, el nombre del entorno virtual aparecerá en la línea de comandos antes del cursor, indicando que estás trabajando dentro del entorno virtual.

### Desactivar el entorno virtual

Para desactivar el entorno virtual, simplemente ejecuta el comando `deactivate` en la línea de comandos.

## Linux

### Crear el entorno virtual

1. Abre una terminal en la ubicación donde deseas crear el entorno virtual.
2. Ejecuta el siguiente comando para crear el entorno virtual: `python3 -m venv nombre_del_entorno_virtual`

### Activar el entorno virtual

1. Abre una terminal en la ubicación donde se encuentra el entorno virtual.
2. Ejecuta el siguiente comando para activar el entorno virtual: `source nombre_del_entorno_virtual/bin/activate`
3. Una vez que el entorno virtual se active, el nombre del entorno virtual aparecerá en la línea de comandos antes del cursor, indicando que estás trabajando dentro del entorno virtual.

### Desactivar el entorno virtual

Para desactivar el entorno virtual, simplemente ejecuta el comando `deactivate` en la línea de comandos.

## Carpetas

### guardar

Esta carpeta contiene los scripts que insertan en la base de datos la información del los JSON. cada farmacia cuenta con su propio insert. y hay un archivo llamado `insert_all.py` que se encarga de hacer la inserción de cada farmacia y avisar si alguna falla.

### obtener

En esta carpeta se encuentran las arañas que consiguen los links de cada producto por farmacia y las que en base a esos links obtienen toda la información de articulos. el archivo `scraper.py`, que contiene el código del scraper. Este archivo utiliza la librería Beautiful Soup para extraer información de las páginas web de las farmacias y guardarla en un archivo CSV ubicado en la carpeta `outputs`.

### outputs

En esta carpeta se guardan los archivos JSON generados por el scraper. Cada archivo tiene por nombre sucodigo de farmacia + items. Un ejemplo sería `Aitems.json` (para los items de ahumada) y contiene la información de los items de la farmacia correspondiente 

### logs

Esta carpeta contiene los archivos de registro de errores generados por el scraper. El archivo se llama como la fecha en la que se encontró el error y contiene información sobre el lugar donde falló y qué revisar para solucionarlo.

## Uso

Para utilizar este scraper existen dos maneras publicación y debug pero siempre se debe seguir un orden por cada farmacia:

`farmacia_links.py`--> `detailed_farmacia.py`--> `insert_farmacia`

este orden asegura que al ejecutar cada araña ya existan los datos necesarios para hacerlo.

Publicación

## Publicación 

1. Abre el Programador de Tareas de Windows Server: Puedes hacerlo a través del panel de control o escribiendo "Task Scheduler" en el menú de inicio.

2. Crea una nueva tarea: Haz clic en "Crear tarea" en la sección Acciones de la barra lateral derecha. Asigna un nombre a la tarea y asegúrate de seleccionar la opción "Ejecutar con los mayores privilegios".

3. Configura los desencadenantes: En la pestaña "Disparadores", selecciona el intervalo de tiempo y la frecuencia en la que quieres que se ejecute el script de Python. También puedes seleccionar otros tipos de desencadenantes, como un archivo .bat en ocasiones es más comodo esto pero ambas funcionan.

4. Configura la acción: En la pestaña "Acciones", selecciona "Iniciar un programa" como tipo de acción y luego escribe la ubicación del archivo de Python que deseas ejecutar en el campo "Programa o script". Si el archivo de Python requiere argumentos, asegúrate de agregarlos en el campo "Argumentos".

5. Guarda la tarea: Haz clic en "Aceptar" para guardar la tarea y cerrar el Programador de Tareas. La tarea se ejecutará automáticamente según la configuración que hayas establecido.

## Debug

- Desde el entorno virtual (venv) ejecuta el comando `python nombre_araña.py`y espera a que termine de ejecutarse
- si la araña parece fallar o encontrarse muchos errores hay una manera de ejecutar solo una página 
- abre una ventana del terminal y escribe `scrapy shell`.
- Luego escribe `fetch('url de la página que hay que debuggear')`.
- eso genera un `response`donde podremos acceder a sus atributos css o xpath
- un ejemplo sería `response.css('div.clase-div::text').get()` y con eso obtendríamos el texto dentro de la etiqueta div con clase "clase-div".

