import os
from glob import glob


map(os.remove,glob('./parsedLogs/*/log_*'))
map(os.remove,glob('./logs/*/log_*'))

html = """\
hola
culeros
"""
html2="hola\nculeros"

html2 += "\nmierda"



print html2
