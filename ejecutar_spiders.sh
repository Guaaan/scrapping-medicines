#!/bin/bash

# Ruta al proyecto
PROYECTO_DIR="."

# (Opcional) Activar el entorno virtual
# source $PROYECTO_DIR/venv/bin/activate

# Ejecutar cada spider uno tras otro con python3
python3 $PROYECTO_DIR/spiders/ahumada.py
python3 $PROYECTO_DIR/spiders/cruz_verde.py
python3 $PROYECTO_DIR/spiders/dr_simi.py
python3 $PROYECTO_DIR/spiders/eco.py
python3 $PROYECTO_DIR/spiders/salcobrand.py
python3 $PROYECTO_DIR/spiders/simi_bioequivalentes.py
python3 $PROYECTO_DIR/spiders/simi_dispositivos.py
python3 $PROYECTO_DIR/spiders/simi_medicamento.py
python3 $PROYECTO_DIR/spiders/simi_salud_femenina.py
python3 $PROYECTO_DIR/spiders/simi_suplementos.py

echo "Todos los spiders se han ejecutado correctamente."

