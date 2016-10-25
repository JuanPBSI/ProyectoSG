import threading
import time
import pysftp
import spur
import sys
import os
import subprocess
import shutil
import os
from glob import glob
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Definimos los datos de los servidores a monitoear
servidor_web = {"ip": "192.168.36.130",
				"usuario": "root", 
				"pass":"ola123", 
				"log_access":"/var/log/apache2/access.log", 
				"log_error":"/var/log/apache2/error.log"}
servidor_waf = {"ip": "192.168.36.128",
				"usuario": "root",
				"pass":"ola123",
				"log_access":"/var/log/apache2/access.log",
				"log_waf":"/var/log/modsec_audit.log",
				"log_error":"/var/log/apache2/error.log"}
servidor_bd = {"ip": "192.168.36.131", "usuario": "root",
			   "pass":"ola123",
			   "log_postgres_error":"/var/log/postgresql/postgresql-9.1-main.log"}


def get_log_servidor(srv, shell, pathSrv, lineas_inicio, tiempo_logs, file_name, server_index, lineas_MAX, file_name2, sitios):
	count_log = 1
	ruta_destino = [''] * len(lineas_inicio)
	result_srv = [''] * len(lineas_inicio)
	result_srv2 = [''] * len(lineas_inicio)
	result_srv3 = [''] * len(lineas_inicio)
	lineas_actuales = [''] * len(lineas_inicio)
	lineas = [''] * len(lineas_inicio)
	command = [''] * len(lineas_inicio)
	path = [''] * len(lineas_inicio)
	while 1:
		for i, fileName in enumerate(file_name):
			ruta_destino[i] = fileName + str(count_log) + ".txt";
		# Dejamos pasar el tiempo para obtener los archivos
		time.sleep(tiempo_logs)
		# contamos las nuevas lineas despues de dejar pasar tiempo
		try:
			for i,path in enumerate(pathSrv):
				result_srv[i] = shell[server_index[i]].run(["sh", "-c", "wc -l " + path + " | cut -d' ' -f1"])
		except Exception as cadena:
			print "Error: " + format(cadena)
			break;
		for i,result in enumerate(result_srv):
			lineas_actuales[i] = int(result.output.rstrip()) + 1		
		
		# Ponemos como limite 2000 lineas a transferir
		for i,lineas_actuales in enumerate(lineas_actuales):
			lineas.append( int(lineas_actuales) - int(lineas_inicio[i]) )
		
		#print "Nuevas lineas --> " + "Web_access: " + str(lineas) + ", Web_error: " + str(lineas_1) + ", Waf_access: " + str(lineas_2) + ", Waf_error: " + str(lineas_3) + ", postgres: " + str(lineas_4) + ", mod_security: " + str(lineas_5)
		#print "Numero maximo de lineas tomadas: " + str(lineas_MAX)
		
		for i,line in enumerate(lineas_actuales):
			if lineas[i] >= lineas_MAX:
				lineas_actuales[i] = int(lineas_inicio[i]) + lineas_MAX
			
		# Creamos el archivo en el servidor actual
		for i,lineas_actuales in enumerate(lineas_actuales):
			command[i] = 'awk "NR >= ' + str(lineas_inicio[i]) + ' && NR <=' + str(lineas_actuales[i]) + ' " ' + pathSrv[i] + ' > "' + ruta_destino[i] + '"'
		try:
			for i,lineas_actuales in enumerate(lineas_actuales):
				result_srv2[i] = shell[server_index[i]].run(["sh", "-c", command[i]])
		except Exception as cadena:
			print "Error: " + format(cadena)
			break;
		# Actualizamos el contador para el nombre del archivo
		# Bajamos el archivo
		try:
			for i,lineas_actuales in enumerate(lineas_actuales):
				srv[server_index[i]].get(ruta_destino[i])
		except Exception as cadena:
			print "Error: " + format(cadena)
			break;
		# Borramos el archivo del servidor actual
		try:
			for i,lineas_actuales in enumerate(lineas_actuales):
				result_srv2[i] = shell[server_index[i]].run(["sh", "-c", "rm -rf " + ruta_destino[i]])
		except Exception as cadena:
			print "Error: " + format(cadena)
			break;
		
		for i,lineas_actuales in enumerate(lineas_actuales):
			lineas_inicio[i] = lineas_actuales[i]
		try:
			for i,lineas_actuales in enumerate(lineas_actuales):
				if not os.path.exists("./logs/" + sitios[i]):
					os.makedirs("./logs/" + sitios[i])
				shutil.move("./" + file_name2[i] + str(count_log) + ".txt", "./logs/" + sitios[i] + file_name2[i] + str(count_log) + ".txt")
		except Exception as cadena:
			print "Error: " + format(cadena)
			break;
		count_log = count_log + 1
		


		
srv_list = [srv_web, srv_waf, srv_BD]
shell_list = [shell_web, shell_waf, shell_bd]
path_list = [servidor_web["log_access"], servidor_web["log_error"], servidor_waf["log_access"], servidor_waf["log_error"], servidor_bd["log_postgres_error"], servidor_waf["log_waf"]]
lineas_inicio_list = [int(lineas_inicio_web_access) + 1, int(lineas_inicio_web_error) + 1, int(lineas_inicio_waf_access) + 1, int(lineas_inicio_waf_error) + 1, int(lineas_inicio_bd) + 1, int(lineas_inicio_waf) + 1]
file_name_list = ["/root/log_web_apache_access", "/root/log_web_apache_error", "/root/log_waf_apache_access", "/root/log_waf_apache_error", "/root/log_postgres_error", "/root/log_modsec_audit"]
file_name_list2 = ["log_web_apache_access", "log_web_apache_error", "log_waf_apache_access", "log_waf_apache_error", "log_postgres_error", "log_modsec_audit"]

# Creamos los acceso por SSH para la extraccion de archvios de los servidores y definimos las lineas de inicio para cada log de cada servidor
# Servidor WEB
try:
	shell_web = spur.SshShell(hostname=servidor_web["ip"], username=servidor_web["usuario"], password=servidor_web["pass"],  missing_host_key=spur.ssh.MissingHostKey.accept)
	result = shell_web.run(["sh", "-c", "wc -l " + servidor_web["log_access"] + " | cut -d' ' -f1"])
	lineas_inicio_web_access = result.output.rstrip()
	result = shell_web.run(["sh", "-c", "wc -l " + servidor_web["log_error"] + " | cut -d' ' -f1"])
	lineas_inicio_web_error = result.output.rstrip()
	
	srv_web = pysftp.Connection(host=servidor_web["ip"], username=servidor_web["usuario"], password=servidor_web["pass"])
	print "Conexion SSH al servidor: [" + servidor_web["ip"] + "] WEB [Exitosa]"
except Exception as cadena:
	print "Error en la conexion SHH: " + format(cadena)
# Servidor: WAF
try:
	shell_waf = spur.SshShell(hostname=servidor_waf["ip"], username=servidor_waf["usuario"], password=servidor_waf["pass"],  missing_host_key=spur.ssh.MissingHostKey.accept)
	result = shell_waf.run(["sh", "-c", "wc -l " + servidor_waf["log_access"] + " | cut -d' ' -f1"])
	lineas_inicio_waf_access = result.output.rstrip()
	result = shell_waf.run(["sh", "-c", "wc -l " + servidor_waf["log_error"] + " | cut -d' ' -f1"])
	lineas_inicio_waf_error = result.output.rstrip()
	result = shell_waf.run(["sh", "-c", "wc -l " + servidor_waf["log_waf"] + " | cut -d' ' -f1"])
	lineas_inicio_waf = result.output.rstrip()
	
	srv_waf = pysftp.Connection(host=servidor_waf["ip"], username=servidor_waf["usuario"], password=servidor_waf["pass"])
	print "Conexion SSH al servidor: [" + servidor_waf["ip"] + "] WAF [Exitosa]"
except Exception as cadena:
	print "Error en la conexion SHH: " + format(cadena)
# Servidor: BD
try:
	shell_bd = spur.SshShell(hostname=servidor_bd["ip"], username=servidor_bd["usuario"], password=servidor_bd["pass"],  missing_host_key=spur.ssh.MissingHostKey.accept)
	result = shell_bd.run(["sh", "-c", "wc -l " + servidor_bd["log_postgres_error"] + " | cut -d' ' -f1"])
	lineas_inicio_bd = result.output.rstrip()
	
	srv_BD = pysftp.Connection(host=servidor_bd["ip"], username=servidor_bd["usuario"], password=servidor_bd["pass"])
	print "Conexion SSH al servidor: [" + servidor_bd["ip"] + "] BD [Exitosa]"
except Exception as cadena:
	print "Error en la conexion SHH: " + format(cadena)

flag = 0

try:
	#srv_list, shell_list, path_list, lineas_inicio_list, 10, file_name_list, "web", 2000, file_name_list2)
	pass
except Exception as cadena:
	print "Error: " + format(cadena)