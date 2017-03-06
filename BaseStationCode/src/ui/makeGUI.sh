# arg 1: path vers le fichier .ui a convertir
# arg 2: path du fichier python a generer
python -m PyQt5.uic.pyuic -x $1 -o $2