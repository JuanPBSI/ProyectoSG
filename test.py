import os
import subprocess
from glob import glob


map(os.remove,glob('./parsedLogs/*/log_*'))
map(os.remove,glob('./logs/*/log_*'))


parseo = subprocess.Popen(["perl", ".cmd.perl", "1" ], stdout=subprocess.PIPE)
outputL, errL = parseo.communicate()
	
print outputL


f = open("mensajeSQL.html", 'r+')
sqliHtml = f.read()
f.close()

print sqliHtml