#!/bin/bash

# Ruta al proyecto
PROYECTO_DIR="."

# (Opcional) Activar el entorno virtual
# source $PROYECTO_DIR/venv/bin/activate

# Ejecutar cada inserccion uno tras otro con python3
python3 $PROYECTO_DIR/guardar/insert_ahumada.py
python3 $PROYECTO_DIR/guardar/insert_cruz_verde.py
python3 $PROYECTO_DIR/guardar/insert_dr_simi.py
python3 $PROYECTO_DIR/guardar/insert_eco.py
python3 $PROYECTO_DIR/guardar/insert_salcobrand.py
python3 $PROYECTO_DIR/guardar/insert_simi.py

echo "Todos los spiders se han ejecutado correctamente."

