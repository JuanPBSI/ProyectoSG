import os
import subprocess
from glob import glob


map(os.remove,glob('./parsedLogs/*/log_*'))
map(os.remove,glob('./logs/*/log_*'))


parseo = subprocess.Popen(["perl", ".cmd.perl", "1" ], stdout=subprocess.PIPE)
outputL, errL = parseo.communicate()
	
#print outputL.split(' ')


def getIPfromLog(outputL):
	ip=[]
	cont=[]
	allLines=[]
	for str in outputL.split(' '):
		if not (str == ''):
			allLines.append(str.strip())
	cont=allLines[0::2]
	ip=allLines[1::2]
	return cont, ip

cont, ip1 = getIPfromLog(outputL)
print cont
print ip1

for indx,ip in enumerate(ip1):
	mail = "    <p>------> IP de origen: <b>" + ip + "</b>  Cantidad: <b>" + cont[indx] +  "</b></p>\n"
	print mail

#f = open("mensajeSQL.html", 'r+')
#sqliHtml = f.read()
#f.close()

#print sqliHtml