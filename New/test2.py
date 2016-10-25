#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading, time, pysftp, spur, sys, os, subprocess, shutil, os, re
from glob import glob
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Eliminamos los archivos de losgs anteriores en cada ejecucion
try:
	map(os.remove,glob('./parsedLogs/*/*/*'))
	map(os.remove,glob('./logs/*/*/*'))
	cp = subprocess.Popen(["perl", ".cmd.perl", "7" ], stdout=subprocess.PIPE)
	outputcp, errcp = cp.communicate()
	shutil.copy(glob('Templates/*'),'./')
	print "logs OK (limpios)!"
except:
	print "logs OK!"
# Datos del correo electronico
Origen = "unam.cert.log.send@gmail.com"
Administrador = "juan.as1991@gmail.com"
passwd = "hola123.,"

servidor_web = {"ip": " ",
				"usuario": " ", 
				"pass":" ", 
				"logs":[],
				"serverIndex":[],
				"Lineas_inicio_log":[],
				"file_name_list":[],
				"file_name_list2":[],
				"Lineas_inicio_log":[],
				"folder":[],
				"log_type":[],
				"sitios":[]}
servidor_waf = {"ip": " ",
				"usuario": " ",
				"pass":" ",
				"logs":[],
				"serverIndex":[],
				"Lineas_inicio_log":[],
				"file_name_list":[],
				"file_name_list2":[],
				"folder":[],
				"log_type":[],
				"sitios":[]}
servidor_bd = {"ip": " ",
			   "usuario": " ",
			   "pass":" ",
			   "serverIndex":[],
			   "Lineas_inicio_log":[],
			   "file_name_list":[],
			   "file_name_list2":[],
			   "folder":[],
			   "log_type":[],
			   "logs":[]}
servidor_modsec = {"ip": " ",
			   "usuario": " ",
			   "pass":" ",
			   "serverIndex":[],
			   "Lineas_inicio_log":[],
			   "file_name_list":[],
			   "file_name_list2":[],
			   "folder":[],
			   "log_type":[],
			   "logs":[]}
Sitios_listas = {}
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------Funciones-------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
def banner():
	print "\n __    ___     _______     __    __  .__   __.      ___      .___  ___.            ______  _______ .______     .___________."
	print "/_ |  / _ \   /  _____|   |  |  |  | |  \ |  |     /   \     |   \/   |           /      ||   ____||   _  \    |           |"
	print " | | | | | | |  |  __     |  |  |  | |   \|  |    /  ^  \    |  \  /  |  ______  |  ,----'|  |__   |  |_)  |   `---|  |----`"
	print " | | | | | | |  | |_ |    |  |  |  | |  . `  |   /  /_\  \   |  |\/|  | |______| |  |     |   __|  |      /        |  |     "
	print " | | | |_| | |  |__| |    |  `--'  | |  |\   |  /  _____  \  |  |  |  |          |  `----.|  |____ |  |\  \----.   |  |     "
	print " |_|  \___/   \______|     \______/  |__| \__| /__/     \__\ |__|  |__|           \______||_______|| _| `._____|   |__| 	 "

def loadConfig(conFilesPath):
	try:
		f = open("config.conf",'r')
	except Exception as cadena:
		print "El archivo de configuracion no se puede abrir: " + format(cadena)
	try:
		confContent = f.read()
		usuarioWeb = re.search('".*"', re.search('usuarioWeb.*', confContent).group(0)).group(0).split('"')[1]
		passWeb = re.search('".*"', re.search('passWeb.*', confContent).group(0)).group(0).split('"')[1]
		usuarioWaf = re.search('".*"', re.search('usuarioWaf.*', confContent).group(0)).group(0).split('"')[1]
		passWaf = re.search('".*"', re.search('passWaf.*', confContent).group(0)).group(0).split('"')[1]
		usuarioBD = re.search('".*"', re.search('usuarioBD.*', confContent).group(0)).group(0).split('"')[1]
		passBD = re.search('".*"', re.search('passBD.*', confContent).group(0)).group(0).split('"')[1]
		ipApache = re.search('".*"', re.search('ipApache.*', confContent).group(0)).group(0).split('"')[1]
		ipPostgres = re.search('".*"', re.search('ipPostgres.*', confContent).group(0)).group(0).split('"')[1]
		ipWaf = re.search('".*"', re.search('ipWaf.*', confContent).group(0)).group(0).split('"')[1]
		servidor_bd["logs"].append(re.search('".*"', re.search('postgresErrorLog.*', confContent).group(0)).group(0).split('"')[1])
		servidor_bd["serverIndex"].append(2)
		servidor_bd["file_name_list"].append("/tmp/" + re.search('(?!\/?.*\/).*', servidor_bd["logs"][0]).group(0))
		servidor_bd["file_name_list2"].append(re.search('(?!\/?.*\/).*', servidor_bd["logs"][0]).group(0))
		servidor_bd["folder"].append("postgres")
		servidor_bd["log_type"].append(3)
		
		modSecAuditLog = re.search('".*"', re.search('modSecAuditLog.*', confContent).group(0)).group(0).split('"')[1]
		servidor_modsec["file_name_list"].append("/tmp/" + re.search('(?!\/?.*\/).*', modSecAuditLog).group(0))
		servidor_modsec["file_name_list2"].append(re.search('(?!\/?.*\/).*', modSecAuditLog).group(0))
		servidor_modsec["serverIndex"].append(1)
		servidor_modsec["logs"].append(modSecAuditLog)
		servidor_modsec["folder"].append("ModSec")
		servidor_modsec["log_type"].append(4)
		f.close()
	except Exception as cadena:
		print "Error en el archivo de configuracion: " + format(cadena)
	conFiles = glob(conFilesPath)
	for file in conFiles:
		f = open(file,'r')
		confContent = f.read()
		Site_name = re.search('".*"', re.search('Site_name = ".*"', confContent).group(0)).group(0).split('"')[1]
		webApacheAccess = re.search('".*"', re.search('webApacheAccess.*', confContent).group(0)).group(0).split('"')[1]
		webApacheError = re.search('".*"', re.search('webApacheError.*', confContent).group(0)).group(0).split('"')[1]
		wafApacheAccess = re.search('".*"', re.search('wafApacheAccess.*', confContent).group(0)).group(0).split('"')[1]
		wafApacheError = re.search('".*"', re.search('wafApacheError.*', confContent).group(0)).group(0).split('"')[1]

		servidor_web["ip"] = ipApache
		servidor_web["usuario"] = usuarioWeb
		servidor_web["pass"] = passWeb

		servidor_waf["ip"] = ipWaf
		servidor_waf["usuario"] = usuarioWaf
		servidor_waf["pass"] = passWaf

		servidor_modsec["ip"] = ipWaf
		servidor_modsec["usuario"] = usuarioWaf
		servidor_modsec["pass"] = passWaf

		servidor_bd["ip"] = ipPostgres
		servidor_bd["usuario"] = usuarioBD
		servidor_bd["pass"] = passBD

		servidor_web["sitios"].append(Site_name)
		servidor_web["sitios"].append(Site_name)
		servidor_waf["sitios"].append(Site_name)
		servidor_waf["sitios"].append(Site_name)

		servidor_web["serverIndex"].append(0)
		servidor_web["serverIndex"].append(0)
		servidor_waf["serverIndex"].append(1)
		servidor_waf["serverIndex"].append(1)
		
		servidor_web["log_type"].append(1)
		servidor_web["log_type"].append(2)
		servidor_waf["log_type"].append(1)
		servidor_waf["log_type"].append(2)
		
		servidor_web["logs"].append(webApacheAccess)
		servidor_web["folder"].append("AccessWeb")
		servidor_web["logs"].append(webApacheError)
		servidor_web["folder"].append("ErrorWeb")
		servidor_waf["logs"].append(wafApacheAccess)
		servidor_waf["folder"].append("AccessWaf")
		servidor_waf["logs"].append(wafApacheError)
		servidor_waf["folder"].append("ErrorWaf")
		
		servidor_web["file_name_list"].append("/tmp/" + re.search('(?!\/?.*\/).*', webApacheAccess).group(0))
		servidor_web["file_name_list2"].append(re.search('(?!\/?.*\/).*', webApacheAccess).group(0))
		servidor_web["file_name_list"].append("/tmp/" + re.search('(?!\/?.*\/).*', webApacheError).group(0))
		servidor_web["file_name_list2"].append(re.search('(?!\/?.*\/).*', webApacheError).group(0))
		servidor_waf["file_name_list"].append("/tmp/" + re.search('(?!\/?.*\/).*', wafApacheAccess).group(0))
		servidor_waf["file_name_list2"].append(re.search('(?!\/?.*\/).*', wafApacheAccess).group(0))
		servidor_waf["file_name_list"].append("/tmp/" + re.search('(?!\/?.*\/).*', wafApacheError).group(0))
		servidor_waf["file_name_list2"].append(re.search('(?!\/?.*\/).*', wafApacheError).group(0))
		
		Sitios_listas[Site_name] = [servidor_web["file_name_list2"][-2],servidor_web["file_name_list2"][-1],servidor_waf["file_name_list2"][-2],servidor_waf["file_name_list2"][-1]]
		f.close()	

def connectSSH(server, servidor):
	shell = ''
	srv = ''
	try:
		shell = spur.SshShell(hostname=servidor["ip"], username=servidor["usuario"], password=servidor["pass"],  missing_host_key=spur.ssh.MissingHostKey.accept)
		for log in servidor["logs"]:
			result = shell.run(["sh", "-c", "wc -l " + log + " | cut -d' ' -f1"])
			servidor["Lineas_inicio_log"].append(result.output.rstrip())
		srv = pysftp.Connection(host=servidor["ip"], username=servidor["usuario"], password=servidor["pass"])
		print "Conexion SSH al servidor: [" + servidor["ip"] + "] " + server + " [Exitosa]"
	except Exception as cadena:
		print "Error en la conexion SHH: " + format(cadena)
	return shell, srv

def connectSSH2(server, servidor):
	shell = ''
	srv = ''
	try:
		shell = spur.SshShell(hostname=servidor["ip"], username=servidor["usuario"], password=servidor["pass"],  missing_host_key=spur.ssh.MissingHostKey.accept)
		for log in servidor["logs"]:
			result = shell.run(["sh", "-c", "wc -l " + log + " | cut -d' ' -f1"])
			servidor["Lineas_inicio_log"].append(result.output.rstrip())
		srv = pysftp.Connection(host=servidor["ip"], username=servidor["usuario"], password=servidor["pass"])
	except Exception as cadena:
		print "Error en la conexion SHH: " + format(cadena)
	return shell, srv

def get_log_servidor(srv, shell, pathSrv, lineas_inicio, tiempo_logs, file_name, server_index, lineas_MAX, file_name2, sitios, folder):
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
		for i,lineas_act in enumerate(lineas_actuales):
			lineas[i] = int(lineas_act) - int(lineas_inicio[i])

		print ""
		for i,lineaNueva in enumerate(lineas):
			print"Nuevas lineas --> " + file_name2[i] +  ": [" + str(lineaNueva) + "], Sitio: " + sitios[i]
		print "Numero maximo de lineas tomadas: " + str(lineas_MAX)

		for i,line in enumerate(lineas_actuales):
			if lineas[i] >= lineas_MAX:
				lineas_actuales[i] = int(lineas_inicio[i]) + lineas_MAX
			
		# Creamos el archivo en el servidor actual
		for i,lineas_act in enumerate(lineas_actuales):
			command[i] = 'awk "NR >= ' + str(lineas_inicio[i]) + ' && NR <=' + str(lineas_actuales[i]) + ' " ' + pathSrv[i] + ' > "' + ruta_destino[i] + '"'
		try:
			for i,lineas_act in enumerate(lineas_actuales):
				result_srv2[i] = shell[server_index[i]].run(["sh", "-c", command[i]])
		except Exception as cadena:
			print "Error1: " + format(cadena)
			break;
		# Actualizamos el contador para el nombre del archivo
		# Bajamos el archivo
		try:
			for i,lineas_act in enumerate(lineas_actuales):
				srv[server_index[i]].get(ruta_destino[i])
		except Exception as cadena:
			print "Error2: " + format(cadena)
			break;
		# Borramos el archivo del servidor actual
		try:
			for i,lineas_act in enumerate(lineas_actuales):
				result_srv2[i] = shell[server_index[i]].run(["sh", "-c", "rm -rf " + ruta_destino[i]])
		except Exception as cadena:
			print "Error3: " + format(cadena)
			break;
		# Actualizamos las lineas de inicio para el nuevo ciclo
		for i,lineas_act in enumerate(lineas_actuales):
			lineas_inicio[i] = lineas_actuales[i]
		# Movemos los archivos a las carpetas que les corresponden
		try:
			for i,lineas_act in enumerate(lineas_actuales):
				if not os.path.exists("./logs/" + sitios[i]):
					os.makedirs("./logs/" + sitios[i])
				if not os.path.exists("./logs/" + sitios[i] + "/" + folder[i]):
						os.makedirs("./logs/" + sitios[i] + "/" + folder[i])
				shutil.move("./" + file_name2[i] + str(count_log) + ".txt", "./logs/" + sitios[i] + "/" + folder[i] + "/" + file_name2[i] + str(count_log) + ".txt")
		except Exception as cadena:
			print "Error4: " + format(cadena)
			break;
		count_log = count_log + 1

def init_SQli(file_name2, tipo_log, folder, sitios):
	count = 1;
	flag = 0;
	file_name = file_name2
	while 1:
		time.sleep(2)
		for i,file in enumerate(file_name):
			file_log = "./logs/" + sitios[i] + "/" + folder[i] + "/" + file_name2[i] + str(count) + ".txt"
			if os.path.isfile(file_log):
				try:
					if not os.path.exists("./parsedLogs/" + sitios[i]):
						os.makedirs("./parsedLogs/" + sitios[i])
					if not os.path.exists("./parsedLogs/" + sitios[i] + "/" + folder[i]):
						os.makedirs("./parsedLogs/" + sitios[i] + "/" + folder[i])
					file_parsedlog = "./parsedLogs/" + sitios[i] + "/" + folder[i] + "/" + file_name2[i] + str(count) + ".txt"
					parseo = subprocess.Popen(["perl", "Mod_parseo.pl", str(tipo_log[i]), file_log, file_parsedlog], stdout=subprocess.PIPE)
					outputP, errP = parseo.communicate()
				except Exception as cadena:
					print "Error: " + format(cadena)
					break;
				flag = 1
				#print file_parsedlog
			else:
				flag = 0
		if flag == 1:
			for site in Sitios_listas:
				print "No log actual: " + str(count)
				print u"\nAnálisis para el sitio" + site
				accesLog = Sitios_listas[site][2] + str(count) + ".txt"
				errorLog = Sitios_listas[site][1] + str(count) + ".txt"
				postgresLog = "./parsedLogs/bd/postgres/" + servidor_bd["file_name_list2"][0] + str(count) + ".txt"
				proceso = subprocess.Popen(["perl", "./analizador.pl", accesLog, errorLog, postgresLog, str(count), site], stdout=subprocess.PIPE)
				output, err = proceso.communicate()
				print "Error Script analizador.pl: " + str(err)
				print "Salida PATH, XSS, SQLi: " + str(output)
			count = count + 1
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------Hilos--------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
class SQliThread(threading.Thread):
	def __init__(self, threadID, name, file_name2, tipo_log, folder, sitios):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.file_name2 = file_name2
		self.tipo_log = tipo_log
		self.folder = folder
		self.sitios = sitios
	def run(self):
		print "Iniciando: " + self.name
		init_SQli(self.file_name2, self.tipo_log, self.folder, self.sitios)
		print "Saliendo: " + self.name

class logThread(threading.Thread):
	def __init__(self, threadID, name,srv, shell, path, lineas_inicio, tiempo_logs, file_name, server_index, lineas_MAX, file_name2, site, folder):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.srv = srv
		self.shell = shell
		self.path = path
		self.lineas_inicio = lineas_inicio
		self.tiempo_logs = tiempo_logs
		self.file_name = file_name
		self.server_index = server_index
		self.lineas_MAX = lineas_MAX
		self.file_name2 = file_name2
		self.site = site
		self.folder = folder
	def run(self):
		print "Iniciando: " + self.name
		get_log_servidor(self.srv, self.shell, self.path, self.lineas_inicio, self.tiempo_logs, self.file_name, self.server_index, self.lineas_MAX, self.file_name2, self.site, self.folder)
		print "Saliendo: " + self.name
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
# cargamos el archivo de configuracion en las variables de los servidores
loadConfig('./sites/*')

# creamos las conexiones SSH
shell_web, srv_web = connectSSH("WEB", servidor_web)
shell_waf, srv_waf = connectSSH("WAF", servidor_waf)
shell_mod, srv_mod = connectSSH("MODsec", servidor_modsec)
shell_bd, srv_bd = connectSSH("BD", servidor_bd)

path_list = []
server_index = []
lineas_inicio = []
site_list = []
file_name_list = []
file_name_list2 = []
folder_list = []
log_type_list = []

for i, path in enumerate(servidor_web["logs"]):
	path_list.append(path)
	server_index.append(servidor_web["serverIndex"][i])
	lineas_inicio.append(int(servidor_web["Lineas_inicio_log"][i]))
	site_list.append(servidor_web["sitios"][i])
	file_name_list.append(servidor_web["file_name_list"][i])
	file_name_list2.append(servidor_web["file_name_list2"][i])
	folder_list.append(servidor_web["folder"][i])
	log_type_list.append(servidor_web["log_type"][i])
	
	path_list.append(servidor_waf["logs"][i])
	server_index.append(servidor_waf["serverIndex"][i])
	lineas_inicio.append(int(servidor_waf["Lineas_inicio_log"][i]))
	site_list.append(servidor_waf["sitios"][i])
	file_name_list.append(servidor_waf["file_name_list"][i])
	file_name_list2.append(servidor_waf["file_name_list2"][i])
	folder_list.append(servidor_waf["folder"][i])
	log_type_list.append(servidor_waf["log_type"][i])

path_list.append(servidor_bd["logs"][0])
server_index.append(servidor_bd["serverIndex"][0])
lineas_inicio.append(int(servidor_bd["Lineas_inicio_log"][0]))
site_list.append("bd")
file_name_list.append(servidor_bd["file_name_list"][0])
file_name_list2.append(servidor_bd["file_name_list2"][0])
folder_list.append(servidor_bd["folder"][0])
log_type_list.append(servidor_bd["log_type"][0])

path_list.append(servidor_modsec["logs"][0])
server_index.append(servidor_modsec["serverIndex"][0])
lineas_inicio.append(int(servidor_modsec["Lineas_inicio_log"][0]))
site_list.append("Audit")
file_name_list.append(servidor_modsec["file_name_list"][0])
file_name_list2.append(servidor_modsec["file_name_list2"][0])
folder_list.append(servidor_modsec["folder"][0])
log_type_list.append(servidor_modsec["log_type"][0])

srv_list = [srv_web, srv_waf, srv_bd]
shell_list = [shell_web, shell_waf, shell_bd]

# Creacion de los hilos
try:
	log_thread = logThread(1,"Hilo: Obtencion logs", srv_list, shell_list, path_list, lineas_inicio, 10, file_name_list, server_index, 2000, file_name_list2, site_list, folder_list)
	log_thread.start()
	pass
except Exception as cadena:
	print "Error: " + format(cadena)
	
try:
	sqli_thread = SQliThread(2,"hilo SQLi",file_name_list2, log_type_list, folder_list, site_list)
	sqli_thread.start();
except Exception as cadena:
	print "Error: " + format(cadena)
	
#Creamos un lock para que corran de manera sincronizada
threadLock = threading.Lock()
threads = []
threads.append(log_thread)
threads.append(sqli_thread)
	
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
	#os.system("clear")

#get_log_servidor(srv_list, shell_list, path_list, lineas_inicio, 10, file_name_list, server_index, 2000, file_name_list2, site_list, folder_list)

#init_SQli(file_name_list2, log_type_list, folder_list, site_list)