#!/usr/bin/python
# -*- coding: utf-8 -*-

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
# Eliminamos los archivos de losgs anteriores en cada ejecucion
try:
	map(os.remove,glob('./parsedLogs/*/log_*'))
	map(os.remove,glob('./logs/*/log_*'))
	cp = subprocess.Popen(["perl", ".cmd.perl", "7" ], stdout=subprocess.PIPE)
	outputcp, errcp = cp.communicate()
	shutil.copy(glob('Templates/*'),'./')
	print "logs OK (limpios)!"
except:
	print "logs OK!"

f = open("mensaje.txt", 'r+')
f.write("#---------------------------------------------------------------------------------#\n")
f.write("#------------Se econtraron las siguientes lineas con contenido sopechoso----------#\n")
f.write("#---------------------------------------------------------------------------------#\n\n")
f.truncate()
f.close()

f = open("mensaje.txt", 'r+')
f.write("0;0;0;0;0;0;0\n")
f.write("#------------Se econtraron las siguientes lineas con contenido sopechoso----------#\n")

f.truncate()
f.close()
def banner():
	print "\n __    ___     _______     __    __  .__   __.      ___      .___  ___.          ______  _______ .______     .___________."
	print "/_ |  / _ \   /  _____|   |  |  |  | |  \ |  |     /   \     |   \/   |         /      ||   ____||   _  \    |           |"
	print " | | | | | | |  |  __     |  |  |  | |   \|  |    /  ^  \    |  \  /  |  ______|  ,----'|  |__   |  |_)  |   `---|  |----`"
	print " | | | | | | |  | |_ |    |  |  |  | |  . `  |   /  /_\  \   |  |\/|  | |______|  |     |   __|  |      /        |  |     "
	print " | | | |_| | |  |__| |    |  `--'  | |  |\   |  /  _____  \  |  |  |  |        |  `----.|  |____ |  |\  \----.   |  |     "
	print " |_|  \___/   \______|     \______/  |__| \__| /__/     \__\ |__|  |__|         \______||_______|| _| `._____|   |__| 	 "

Origen = "unam.cert.log.send@gmail.com"
Administrador = "juan.as1991@gmail.com"
passwd = "hola123.,"
def sendEmail(user, pwd, recipient, subject, html, text):
	gmail_user = user
	gmail_pwd = pwd
	From = user
	to = recipient

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = From
	msg['To'] = to
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')
	msg.attach(part1)
	msg.attach(part2)
	try:
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_pwd)
		server.sendmail(From, to, msg.as_string())
		server.close()
		print 'Se envio correo electronico!!!'
	except Exception as cadena:
		print "Error al envio del correo" + format(cadena)

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

			   
def getfromPerl(outputL):
	ip=[]
	cont=[]
	allLines=[]
	for str in outputL.split(' '):
		if not (str == ''):
			allLines.append(str.strip())
	cont=allLines[0::2]
	ip=allLines[1::2]
	return cont, ip
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

class SQliThread(threading.Thread):
	def __init__(self, threadID, name, pathWeb, pathWebE, pathWaf, pathPostgres, file_names, flag):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.pathWeb = pathWeb
		self.pathWebE = pathWebE
		self.pathWaf = pathWaf
		self.pathPostgres = pathPostgres
		self.filenames = file_names
		self.flag = flag
	def run(self):
		print "Iniciando: " + self.name
		init_SQli(self.pathWeb, self.pathWebE, self.pathWaf, self.pathPostgres, self.filenames, self.flag)
		print "Saliendo: " + self.name
		
class eviaMail(threading.Thread):
	def __init__(self, threadID, name, mail):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.mail = mail
	def run(self):
		print "Iniciando: " + self.name
		send_mail(self.mail)
		print "Saliendo: " + self.name

def send_mail(mail):
	parseo = subprocess.Popen(["perl", ".cmd.perl", "0" ], stdout=subprocess.PIPE)
	outputL, errL = parseo.communicate()
	lineas_inicio = int(outputL)
	cont_time = 0
	while 1:
		parseo = subprocess.Popen(["perl", ".cmd.perl" ], stdout=subprocess.PIPE)
		outputL, errL = parseo.communicate()
		lineas_actuales = int(outputL)
		if (lineas_actuales - lineas_inicio) != 0:
			time.sleep(1)
			lastLine = subprocess.Popen(["tail", "-1", "cod_status.txt" ], stdout=subprocess.PIPE)
			outputLast, errLast = lastLine.communicate()
			Values = outputLast.split(';')
			#print $status "$cont_PATH;$cont_XSS;$cont_encuentros;$cont_error;$cont_200;$cont_errores_postgres;$cont_error_en_base\n";
			cont_PATH = int(Values[0])
			cont_XSS = int(Values[1])
			cont_encuentros = int(Values[2])
			cont_error = int(Values[3])
			cont_200 = int(Values[4])
			cont_errores_postgres = int(Values[5])
			cont_error_en_base = int(Values[6])
			lineas_inicio = lineas_actuales;

			# si es una herramienta generará muchas peticiones
			if (cont_PATH > 30 or cont_encuentros > 30 or cont_XSS > 30) and (cont_time == 0):
			
				ipCount = subprocess.Popen(["perl", ".cmd.perl", "1" ], stdout=subprocess.PIPE)
				outputIP1, errIP1 = ipCount.communicate()
				ipCount = subprocess.Popen(["perl", ".cmd.perl", "2" ], stdout=subprocess.PIPE)
				outputIP2, errIP2 = ipCount.communicate()
				ipCount = subprocess.Popen(["perl", ".cmd.perl", "3" ], stdout=subprocess.PIPE)
				outputIP3, errIP3 = ipCount.communicate()

				userCount = subprocess.Popen(["perl", ".cmd.perl", "4" ], stdout=subprocess.PIPE)
				outputU1, errU1 = userCount.communicate()
				userCount = subprocess.Popen(["perl", ".cmd.perl", "5" ], stdout=subprocess.PIPE)
				outputU2, errU1 = userCount.communicate()
				userCount = subprocess.Popen(["perl", ".cmd.perl", "6" ], stdout=subprocess.PIPE)
				outputU3, errU1 = userCount.communicate()
				
				contIP1, ip1 = getfromPerl(outputIP1)
				contIP2, ip2 = getfromPerl(outputIP2)
				contIP3, ip3 = getfromPerl(outputIP3)

				contUser1, agent1 = getfromPerl(outputU1)
				contUser2, agent2 = getfromPerl(outputU2)
				contUser3, agent3 = getfromPerl(outputU3)

				mail["html"] += "\n    <h1>Seccion 1 : Resumen de los hallazgos </h1>\n"
				mail["html"] += "    <br><p>SQL injection: </p><br>\n"
				mail["html"] += "    <p>------> Num. detecciones: " + str(cont_encuentros) + "</p>\n"
				for inx, ip in enumerate(ip1):
					mail["html"] += "    <p>------> IP de origen: <b>" + ip + "</b>  Cantidad: <b>" + contIP1[inx] + "</b></p>\n"
				for inx, agent in enumerate(agent1):
					mail["html"] += "    <p>------> User-Agent: <b>" + agent + "</b>  Cantidad: <b>" + contUser1[inx] + "</b></p>\n"

				mail["html"] += "    <br><p>Cross Site Scripting: </p><br>\n"
				mail["html"] += "    <p>------> Num. detecciones: " + str(cont_XSS) + "</p>\n"
				for inx, ip in enumerate(ip2):
					mail["html"] += "    <p>------> IP de origen: <b>" + ip + "</b>  Cantidad: <b>" + contIP2[inx] + "</b></p>\n"
				for inx, agent in enumerate(agent2):
					mail["html"] += "    <p>------> User-Agent: <b>" + agent + "</b>  Cantidad: <b>" + contUser2[inx] + "</b></p>\n"

				mail["html"] += "    <br><p>Path Transversal: </p><br>\n"
				mail["html"] += "    <p>------> Num. detecciones: " + str(cont_PATH) + "</p><br>\n"
				for inx, ip in enumerate(ip3):
					mail["html"] += "    <p>------> IP de origen: <b>" + ip + "</b>  Cantidad: <b>" + contIP3[inx] + "</b></p>\n"
				for inx, agent in enumerate(agent3):
					mail["html"] += "    <p>------> User-Agent: <b>" + agent + "</b>  Cantidad: <b>" + contUser3[inx] + "</b></p>\n"

				mail["html"] += "    <br><h1>Seccion 2 : Detalles </h1><br>\n"
				f = open("mensajeSQL.html", 'r+')
				sqliHtml = f.read()
				f.close()
				f = open("mensajeXSS.html", 'r+')
				xssHtml = f.read()
				f.close()
				f = open("mensajePATH.html", 'r+')
				pathHtml = f.read()
				f.close()
				mail["html"] += sqliHtml
				mail["html"] += xssHtml
				mail["html"] += pathHtml
				sendEmail(mail["from"], mail["pass"], mail["to"], mail["asunto"], mail["html"], mail["text"])
				print u"Tal ves te esten atacando amiguito ಠ_ಠ !!!!!"
				cont_time = cont_time + 1;
			if (cont_time != 0):
				cont_time = cont_time + 1;

			if (cont_time == 800):
				cont_time = 0;

		#f = open('status_act.txt', 'r')
		#resultados = f.readline()
		#res = resultados.split(";")
		#f.close();

def init_SQli(pathWeb, pathWebE, pathWaf, pathPostgres, filenames, flag):
	count = 1;
	file_log_web = pathWeb + str(count) + ".txt"
	file_log_webE = pathWebE + str(count) + ".txt"
	file_log_waf = pathWaf + str(count) + ".txt"
	file_log_postgres = pathPostgres + str(count) + ".txt"
	while 1:
		if os.path.isfile(file_log_web) and os.path.isfile(file_log_waf) and os.path.isfile(file_log_postgres):
			try:
				parseo = subprocess.Popen(["perl", "Mod_parseo.pl", filenames[0] + str(count) + ".txt", filenames[1] + str(count) + ".txt", filenames[4] + str(count) + ".txt" ], stdout=subprocess.PIPE)
				outputP, errP = parseo.communicate()

				proceso = subprocess.Popen(["perl", "analizador.pl", filenames[0] + str(count) + ".txt", filenames[1] + str(count) + ".txt", filenames[4] + str(count) + ".txt", str(count) ], stdout=subprocess.PIPE)
				output, err = proceso.communicate()
			except Exception as cadena:
				print "Error: " + format(cadena)
				break;
			print "No log actual: " + str(count)
			print filenames[0] + str(count) + ".txt"
			print "Salida PATH, XSS, SQLi: " + str(output)
			print "Error Scirpt analizador.pl: " + str(err)
			count = count + 1
			file_log_web = pathWeb + str(count) + ".txt"
			file_log_waf = pathWaf + str(count) + ".txt"
			file_log_postgres = pathPostgres + str(count) + ".txt"

class logThread(threading.Thread):
	def __init__(self, threadID, name, srv, shell, path, lineas_inicio, tiempo_logs, file_name, log_name, lineas_MAX, file_name2):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.srv = srv
		self.shell = shell
		self.path = path
		self.lineas_inicio = lineas_inicio
		self.tiempo_logs = tiempo_logs
		self.file_name = file_name
		self.log_name = log_name
		self.lineas_MAX = lineas_MAX
		self.file_name2 = file_name2
	def run(self):
		print "Iniciando: " + self.name
		get_log_servidor(self.srv, self.shell, self.path, self.lineas_inicio, self.tiempo_logs, self.file_name, self.log_name, self.lineas_MAX, self.file_name2)
		print "Saliendo: " + self.name
		
# Definimos la funcion que extraeran y generaran los logs
def get_log_servidor(srv, shell, path, lineas_inicio, tiempo_logs, file_name, log_name, lineas_MAX, file_name2):
	count_log = 1
	ruta_destino = []
	while 1:
		ruta_destino = file_name[0] + str(count_log) + ".txt";
		ruta_destino_1 = file_name[1] + str(count_log) + ".txt";
		ruta_destino_2 = file_name[2] + str(count_log) + ".txt";
		ruta_destino_3 = file_name[3] + str(count_log) + ".txt";
		ruta_destino_4 = file_name[4] + str(count_log) + ".txt";
		ruta_destino_5 = file_name[5] + str(count_log) + ".txt";
		# Dejamos pasar el tiempo para obtener los archivos
		# print "inicio: " + log_name
		time.sleep(tiempo_logs)
		#print "inicio2"
		# contamos las nuevas lineas despues de dejar pasar tiempo
		try:
			result = shell[0].run(["sh", "-c", "wc -l " + path[0] + " | cut -d' ' -f1"])
			result_1 = shell[0].run(["sh", "-c", "wc -l " + path[1] + " | cut -d' ' -f1"])
			result_2 = shell[1].run(["sh", "-c", "wc -l " + path[2] + " | cut -d' ' -f1"])
			result_3 = shell[1].run(["sh", "-c", "wc -l " + path[3] + " | cut -d' ' -f1"])
			result_4 = shell[2].run(["sh", "-c", "wc -l " + path[4] + " | cut -d' ' -f1"])
			result_5 = shell[1].run(["sh", "-c", "wc -l " + path[5] + " | cut -d' ' -f1"])
		except Exception as cadena:
			print "Error: " + format(cadena)
			break;
		lineas_actuales = int(result.output.rstrip()) + 1
		lineas_actuales_1 = int(result_1.output.rstrip()) + 1
		lineas_actuales_2 = int(result_2.output.rstrip()) + 1
		lineas_actuales_3 = int(result_3.output.rstrip()) + 1
		lineas_actuales_4 = int(result_4.output.rstrip()) + 1
		lineas_actuales_5 = int(result_5.output.rstrip()) + 1
		
		# Ponemos como limite 2000 lineas a transferir
		lineas = int(lineas_actuales) - int(lineas_inicio[0])
		lineas_1 = int(lineas_actuales_1) - int(lineas_inicio[1])
		lineas_2 = int(lineas_actuales_2) - int(lineas_inicio[2])
		lineas_3 = int(lineas_actuales_3) - int(lineas_inicio[3])
		lineas_4 = int(lineas_actuales_4) - int(lineas_inicio[4])
		lineas_5 = int(lineas_actuales_5) - int(lineas_inicio[5])
		
		print "Nuevas lineas --> " + "Web_access: " + str(lineas) + ", Web_error: " + str(lineas_1) + ", Waf_access: " + str(lineas_2) + ", Waf_error: " + str(lineas_3) + ", postgres: " + str(lineas_4) + ", mod_security: " + str(lineas_5)
		print "Numero maximo de lineas tomadas: " + str(lineas_MAX)
		
		if lineas >= lineas_MAX:
			lineas_actuales = int(lineas_inicio[0]) + lineas_MAX
		if lineas_1 >= lineas_MAX:
			lineas_actuales_1 = int(lineas_inicio[1]) + lineas_MAX
		if lineas_2 >= lineas_MAX:
			lineas_actuales_2 = int(lineas_inicio[2]) + lineas_MAX
		if lineas_3 >= lineas_MAX:
			lineas_actuales_3 = int(lineas_inicio[3]) + lineas_MAX
		if lineas_4 >= lineas_MAX:
			lineas_actuales_4 = int(lineas_inicio[4]) + lineas_MAX
		if lineas_5 >= lineas_MAX:
			lineas_actuales_5 = int(lineas_inicio[5]) + lineas_MAX
			
		# Creamos el archivo en el servidor actual
		command = 'awk "NR >= ' + str(lineas_inicio[0]) + ' && NR <=' + str(lineas_actuales) + ' " ' + path[0] + ' > "' + ruta_destino + '"'
		command_1 = 'awk "NR >= ' + str(lineas_inicio[1]) + ' && NR <=' + str(lineas_actuales_1) + ' " ' + path[1] + ' > "' + ruta_destino_1 + '"'
		command_2 = 'awk "NR >= ' + str(lineas_inicio[2]) + ' && NR <=' + str(lineas_actuales_2) + ' " ' + path[2] + ' > "' + ruta_destino_2 + '"'
		command_3 = 'awk "NR >= ' + str(lineas_inicio[3]) + ' && NR <=' + str(lineas_actuales_3) + ' " ' + path[3] + ' > "' + ruta_destino_3 + '"'
		command_4 = 'awk "NR >= ' + str(lineas_inicio[4]) + ' && NR <=' + str(lineas_actuales_4) + ' " ' + path[4] + ' > "' + ruta_destino_4 + '"'
		command_5 = 'awk "NR >= ' + str(lineas_inicio[5]) + ' && NR <=' + str(lineas_actuales_5) + ' " ' + path[5] + ' > "' + ruta_destino_5 + '"'
		try:
			result2 = shell[0].run(["sh", "-c", command])
			result2_1 = shell[0].run(["sh", "-c", command_1])
			result2_2 = shell[1].run(["sh", "-c", command_2])
			result2_3 = shell[1].run(["sh", "-c", command_3])
			result2_4 = shell[2].run(["sh", "-c", command_4])
			result2_5 = shell[1].run(["sh", "-c", command_5])
		except Exception as cadena:
			print "Error: " + format(cadena)
			break;
		# Actualizamos el contador para el nombre del archivo
		# Bajamos el archivo
		try:
			srv[0].get(ruta_destino)
			srv[0].get(ruta_destino_1)
			srv[1].get(ruta_destino_2)
			srv[1].get(ruta_destino_3)
			srv[2].get(ruta_destino_4)
			srv[1].get(ruta_destino_5)
		except Exception as cadena:
			print "Error: " + format(cadena)
			break;
		# Borramos el archivo del servidor actual
		try:
			result3 = shell[0].run(["sh", "-c", "rm -rf " + ruta_destino])
			result3_1 = shell[0].run(["sh", "-c", "rm -rf " + ruta_destino_1])
			result3_2 = shell[1].run(["sh", "-c", "rm -rf " + ruta_destino_2])
			result3_3 = shell[1].run(["sh", "-c", "rm -rf " + ruta_destino_3])
			result3_4 = shell[2].run(["sh", "-c", "rm -rf " + ruta_destino_4])
			result3_5 = shell[1].run(["sh", "-c", "rm -rf " + ruta_destino_5])
		except Exception as cadena:
			print "Error: " + format(cadena)
			break;
		#print log_name + ": " + "lineas nuevas: " + str(lineas)

		lineas_inicio[0] = lineas_actuales
		lineas_inicio[1] = lineas_actuales_1
		lineas_inicio[2] = lineas_actuales_2
		lineas_inicio[3] = lineas_actuales_3
		lineas_inicio[4] = lineas_actuales_4
		lineas_inicio[5] = lineas_actuales_5
		try:
			shutil.move("./" + file_name2[0] + str(count_log) + ".txt", "./logs/accessApache/" + file_name2[0] + str(count_log) + ".txt")
			shutil.move("./" + file_name2[1] + str(count_log) + ".txt", "./logs/errorApache/" + file_name2[1] + str(count_log) + ".txt")
			shutil.move("./" + file_name2[2] + str(count_log) + ".txt", "./logs/waf/" + file_name2[2] + str(count_log) + ".txt")
			shutil.move("./" + file_name2[3] + str(count_log) + ".txt", "./logs/waf/" + file_name2[3] + str(count_log) + ".txt")
			shutil.move("./" + file_name2[4] + str(count_log) + ".txt", "./logs/postgres/" + file_name2[4] + str(count_log) + ".txt")
			shutil.move("./" + file_name2[5] + str(count_log) + ".txt", "./logs/waf/" + file_name2[5] + str(count_log) + ".txt")
		except Exception as cadena:
			print "Error: " + format(cadena)
			break;
		count_log = count_log + 1
		#print command
		#print result2
		#print "inicio3"
 
# Creamos los hilos que se encargaran de extraer los logs de los servidores
#print lineas_inicio_web_access
#print lineas_inicio_web_error
#print lineas_inicio_waf_access
#print lineas_inicio_waf_error
#print lineas_inicio_waf
#print lineas_inicio_bd
# Creamos las listas que van como argumentos en la funcion del hilo
srv_list = [srv_web, srv_waf, srv_BD]
shell_list = [shell_web, shell_waf, shell_bd]
path_list = [servidor_web["log_access"], servidor_web["log_error"], servidor_waf["log_access"], servidor_waf["log_error"], servidor_bd["log_postgres_error"], servidor_waf["log_waf"]]
lineas_inicio_list = [int(lineas_inicio_web_access) + 1, int(lineas_inicio_web_error) + 1, int(lineas_inicio_waf_access) + 1, int(lineas_inicio_waf_error) + 1, int(lineas_inicio_bd) + 1, int(lineas_inicio_waf) + 1]
file_name_list = ["/root/log_web_apache_access", "/root/log_web_apache_error", "/root/log_waf_apache_access", "/root/log_waf_apache_error", "/root/log_postgres_error", "/root/log_modsec_audit"]
file_name_list2 = ["log_web_apache_access", "log_web_apache_error", "log_waf_apache_access", "log_waf_apache_error", "log_postgres_error", "log_modsec_audit"]

flag = 0

try:
	log_thread = logThread(1,"Hilo para los logs", srv_list, shell_list, path_list, lineas_inicio_list, 10, file_name_list, "web", 2000, file_name_list2)
	log_thread.start()
	pass
except Exception as cadena:
	print "Error: " + format(cadena)
	
try:
	sqli_thread = SQliThread(2,"hilo SQLi","logs/accessApache/log_web_apache_access", "logs/errorApache/log_web_apache_error", "logs/waf/log_waf_apache_access", "logs/postgres/log_postgres_error", file_name_list2, flag)
	sqli_thread.start();
except Exception as cadena:
	print "Error: " + format(cadena)


text = "Enviamos el siguiente correo por que se cree que su servidor esta bajo ataque:\nRecomendamos realizar las modificaciones pertinentes\n"
html = """\
<html>
  <head></head>
  <body>
    <h1>Se registro un aumento en la actividad maliciosa</h1>
"""

mail = {"from":"unam.cert.log.send@gmail.com", "pass":"hola123.,", "to":"juan_as1991@hotmail.com", "asunto":"Envio de reporte de posbles ataques", "html":html, "text":text}

try:
	Mail = eviaMail(3,"hilo mail",mail)
	Mail.start();
	pass
except Exception as cadena:
	print "Error: " + format(cadena)	
#Creamos un lock para que corran de manera sincronizada
threadLock = threading.Lock()
threads = []
threads.append(log_thread)
threads.append(sqli_thread)
# threads.append(waf_acces_thread)
# threads.append(waf_error_thread)
# threads.append(bd_thread)

while 1:
	banner()
	fecha = subprocess.Popen(["date"], stdout=subprocess.PIPE)
	outputDate, errDate = fecha.communicate()
	print "\n" + outputDate + "\n"
	time.sleep(45)
	if not log_thread.isAlive():
		print "Hilo log: die"
		print "El programa se detendra ya que el hilo es crucial para la operacion..."
		print "ejecute [rm ./logs/*/log_* && rm ./parsedLogs/*/log_*] en la carpeta de proyecto"
		break;
	if not sqli_thread.isAlive():
		print "Hilo analizador: die"
		print "El programa se detendra ya que el hilo es crucial para la operacion..."
		print "ejecute [rm ./logs/*/log_* && rm ./parsedLogs/*/log_*] en la carpeta de proyecto"
		break;
	# if not web_acces_thread.isAlive():
		# print "Hilo access wweb: die"
	# if not web_error_thread.isAlive():
		# print "Hilo error web: die"
	# if not waf_acces_thread.isAlive():
		# print "Hilo access waf: die"
	# if not waf_error_thread.isAlive():
		# print "Hilo waf_error: die"
	# if not bd_thread.isAlive():
		# print "Hilo BD: die"
	# pass
	os.system("clear")

#srv_BD = pysftp.Connection(host="your_FTP_server", username="your_username",password="your_password")
#srv_WAF = pysftp.Connection(host="your_FTP_server", username="your_username",password="your_password")


# Obtener los archivos de los logs
#data = srv_web.listdir()

# Closes the connection
#srv_web.close()
# Prints out the directories and files, line by line

#for i in data:
#    print i