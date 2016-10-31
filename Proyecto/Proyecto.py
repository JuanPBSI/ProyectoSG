#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading, time, pysftp, spur, sys, os, subprocess, shutil, os, re, smtplib, urllib2
from termcolor import colored
from glob import glob
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import Series
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import utils
from reportlab.lib.units import cm
from reportlab.platypus import Frame, Image
from matplotlib import gridspec
# Eliminamos los archivos de losgs anteriores en cada ejecucion
try:
	map(os.remove,glob('./parsedLogs/*/*/*'))
	map(os.remove,glob('./logs/*/*/*'))
	cp = subprocess.Popen(["perl", ".cmd.perl", "11" ], stdout=subprocess.PIPE)
	outputcp, errcp = cp.communicate()
	clean()
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
			   "logs":[],
			   "rutaWafConfig": " "}
mail = {"from":"unam.cert.log.send@gmail.com",
		"pass":"", 
		"to":"",
		"asunto":"",
		"html":"",
		"text":"",
		"cont-mail":0,
		"flag-mail":0}
mail_report = {"from":"unam.cert.log.send@gmail.com",
		"pass":"", 
		"to":"",
		"asunto":"",
		"html":"",
		"text":"",
		"cont-mail":0,
		"flag-mail":0}
Sitios_listas = {}
logcfg = {"time_log":0,
		"max_size_log":0,
		"tiempoReportes":0}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------Funciones-------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
def banner():
	#os.system("clear")
	print colored("\n __    ___     _______     __    __  .__   __.      ___      .___  ___.            ______  _______ .______     .___________.", 'green')
	print colored("/_ |  / _ \   /  _____|   |  |  |  | |  \ |  |     /   \     |   \/   |           /      ||   ____||   _  \    |           |", 'green')
	print colored(" | | | | | | |  |  __     |  |  |  | |   \|  |    /  ^  \    |  \  /  |  ______  |  ,----'|  |__   |  |_)  |   `---|  |----`", 'green')
	print colored(" | | | | | | |  | |_ |    |  |  |  | |  . `  |   /  /_\  \   |  |\/|  | |______| |  |     |   __|  |      /        |  |     ", 'green')
	print colored(" | | | |_| | |  |__| |    |  `--'  | |  |\   |  /  _____  \  |  |  |  |          |  `----.|  |____ |  |\  \----.   |  |     ", 'green')
	print colored(" |_|  \___/   \______|     \______/  |__| \__| /__/     \__\ |__|  |__|           \______||_______|| _| `._____|   |__| 	   ", 'green')
	fecha = subprocess.Popen(["date"], stdout=subprocess.PIPE)
	outputDate, errDate = fecha.communicate()
	print "\n" + outputDate + "\n"

def clean():
	shutil.copy('./Templates/mensajeSQL.html','./')
	shutil.copy('./Templates/mensajeCRAW.html','./')
	shutil.copy('./Templates/mensajeXSS.html','./')
	shutil.copy('./Templates/mensajePATH.html','./')
	shutil.copy('./Templates/mensajeDEFC.html','./')

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
		
		rutaWafConfig = re.search('".*"', re.search('rutaWafConfig.*', confContent).group(0)).group(0).split('"')[1]
		modSecAuditLog = re.search('".*"', re.search('modSecAuditLog.*', confContent).group(0)).group(0).split('"')[1]
		servidor_modsec["file_name_list"].append("/tmp/" + re.search('(?!\/?.*\/).*', modSecAuditLog).group(0))
		servidor_modsec["file_name_list2"].append(re.search('(?!\/?.*\/).*', modSecAuditLog).group(0))
		servidor_modsec["serverIndex"].append(1)
		servidor_modsec["logs"].append(modSecAuditLog)
		servidor_modsec["folder"].append("ModSec")
		servidor_modsec["log_type"].append(4)
		servidor_modsec["rutaWafConfig"] = rutaWafConfig
		
		
		mail["from"] = re.search('".*"', re.search('mailFROM.*', confContent).group(0)).group(0).split('"')[1]
		mail["pass"] = re.search('".*"', re.search('passMail.*', confContent).group(0)).group(0).split('"')[1]
		mail["to"] = re.search('".*"', re.search('mailTo.*', confContent).group(0)).group(0).split('"')[1]
		mail["asunto"] = re.search('".*"', re.search('subject.*', confContent).group(0)).group(0).split('"')[1]

		logcfg["max_size_log"] = int(re.search('".*"', re.search('maxLinesLog.*', confContent).group(0)).group(0).split('"')[1])
		logcfg["time_log"] = int(re.search('".*"', re.search('tiempoMonitoreo.*', confContent).group(0)).group(0).split('"')[1])
		logcfg["tiempoReportes"] = int(re.search('".*"', re.search('tiempoReportes.*', confContent).group(0)).group(0).split('"')[1])
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
		srv = pysftp.Connection(host=servidor["ip"], username=servidor["usuario"], password=servidor["pass"])
		shell = spur.SshShell(hostname=servidor["ip"], username=servidor["usuario"], password=servidor["pass"],  missing_host_key=spur.ssh.MissingHostKey.accept)
		for log in servidor["logs"]:
			result = shell.run(["sh", "-c", "wc -l " + log + " | cut -d' ' -f1"])
			servidor["Lineas_inicio_log"].append(result.output.rstrip())
		time.sleep(1)
		print "Conexion SSH al servidor: [" + servidor["ip"] + "] " + server + " [Exitosa]"
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
	
		# Creamos el archivo en el servidor actual
		for i,lineas_act in enumerate(lineas_inicio):
			command[i] = 'tail -n +' + str(lineas_inicio[i]) + ' ' + pathSrv[i] + ' > "' + ruta_destino[i] + '"'
		try:
			for i,lineas_act in enumerate(lineas_inicio):
				result_srv2[i] = shell[server_index[i]].run(["sh", "-c", command[i]])
		except Exception as cadena:
			print "Error1: " + format(cadena)
			break;

		# Bajamos el archivo
		try:
			for i,lineas_act in enumerate(lineas_inicio):
				srv[server_index[i]].get(ruta_destino[i])
		except Exception as cadena:
			print "Error2: " + format(cadena)
			break;
		# contamos las nuevas lineas despues de dejar pasar tiempo
		try:
			for i,path in enumerate(pathSrv):
				shell_local = spur.LocalShell()
				result_srv[i] = shell_local.run(["sh", "-c", "wc -l " + "./" + file_name2[i] + str(count_log) + ".txt" + " | cut -d' ' -f1"])
		except Exception as cadena:
			print "Error: " + format(cadena)
			break;
		for i,result in enumerate(result_srv):
			lineas_actuales[i] = int(result.output.rstrip()) + 1
		
		for i,lineas_act in enumerate(lineas_actuales):
			lineas[i] = int(lineas_act)
			
		banner()
		print colored("No log actual: " + str(count_log), 'cyan')
		print colored("eMail enviados: " + str(mail["cont-mail"]), 'cyan')
		print ""
		for i,lineaNueva in enumerate(lineas):
			print colored("Nuevas lineas --> " + file_name2[i] +  ": [" + str(lineaNueva - 1) + "], Sitio: " + sitios[i], 'blue')
		print "Numero maximo de lineas tomadas: " + str(lineas_MAX)

		# Actualizamos el contador para el nombre del archivo
		# Borramos el archivo del servidor actual
		try:
			for i,lineas_act in enumerate(lineas_actuales):
				result_srv2[i] = shell[server_index[i]].run(["sh", "-c", "rm -rf " + ruta_destino[i]])
		except Exception as cadena:
			print "Error3: " + format(cadena)
			break;
		# Actualizamos las lineas de inicio para el nuevo ciclo
		for i,lineas_act in enumerate(lineas_actuales):
			lineas_inicio[i] = lineas_inicio[i] + lineas_actuales[i] - 1
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

def init_SQli(file_name2, tipo_log, folder, sitios, mail):
	count = 1;
	flag = 0;
	file_name = file_name2
	contador_mail = 0
	while 1:
		time.sleep(1)
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
		flagDetectionOnly = 0
		#------Comprueba se ModSecurity esta activado----------#
		# try:
			# srv_list[1].get(servidor_modsec["rutaWafConfig"])
			# f = open("modsecurity.conf")
			# try:
				# for line in f:
					# if re.search('SecRuleEngine DetectionOnly', line):
						# flagDetectionOnly = 1
						# f.close()
						# break;
				# else:
					# flagDetectionOnly = 0
			# except Exception as cadena:
				# print "Error en el archivo de configuracion: " + format(cadena)
		# except Exception as cadena:
			# print "El archivo de configuracion no se puede abrir: " + format(cadena)
		flagDetectionOnly = 1
		#--------------------#
		if flag == 1:
			for site in Sitios_listas:
				#-------Analisis del mod Security----------#
				if flagDetectionOnly == 1:
					print "Mod Security mod: [Detection Only]"
					errorWAF = "./logs/" + site + "/ErrorWaf/" + Sitios_listas[site][3] + str(count) + ".txt"
					auditWAF = "./logs/Audit/ModSec/modsec_audit.log" + str(count) + ".txt"
					proceso = subprocess.Popen(["perl", "./modSecurity.pl",errorWAF, auditWAF], stdout=subprocess.PIPE)
					output, err = proceso.communicate()
					print "Error Script ./modSecurity.pl: " + str(err)
					#print "Salida ModSecurity: " + str(output)
				#------------------------------------------#
				print u"\nAnálisis para el sitio: "+ colored("[" + site + "]", 'yellow')
				accesLog = Sitios_listas[site][2] + str(count) + ".txt"
				errorLog = Sitios_listas[site][1] + str(count) + ".txt"
				postgresLog = "./parsedLogs/bd/postgres/" + servidor_bd["file_name_list2"][0] + str(count) + ".txt"
				proceso = subprocess.Popen(["perl", "./analizador.pl", accesLog, errorLog, postgresLog, str(count), site], stdout=subprocess.PIPE)
				output, err = proceso.communicate()
				print "Error Script analizador.pl: " + str(err)
				print colored(str(output),'green')
				contador_mail = send_mail(mail, site, contador_mail)
			count = count + 1

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


def autolabel(rects,ax):
	for rect in rects:
		height = rect.get_height()
		if not height==0:
			ax.text(rect.get_x() + rect.get_width()/2., 1*height,'%d' % int(height),ha='center', va='bottom', fontsize=12)

def graficar(path):
	today = date.today()
	f = open(path)
	x_axis = [];
	y_PATH = [];
	y_SQLi = [];
	y_Xss = [];
	y_Craw = [];
	y_DEF = [];
	y_std = [];
	max_y = [];
	for line in f:
		values = line.split(';')
		x_axis.append(values[0])
		y_PATH.append(int(values[1]))
		y_Xss.append(int(values[2]))
		y_SQLi.append(int(values[3]) + int(values[4]) + int(values[5]))
		y_DEF.append(int(values[6]))
		y_Craw.append(int(values[7]))
		y_std.append(10);
		max_y.append( max([int(values[1]),int(values[2]),int(values[3]) + int(values[4]) + int(values[5]),int(values[6]),int(values[6])]) )

	ind = np.arange(len(x_axis)) 

	width = 0.5 
	fig1, ax1 = plt.subplots()
	fig2, ax2 = plt.subplots()
	fig3, ax3 = plt.subplots()
	fig4, ax4 = plt.subplots()
	fig5, ax5 = plt.subplots()
	rects1 = ax1.bar(ind, y_PATH, width, color='r')
	rects2 = ax2.bar(ind, y_Xss, width, color='b')
	rects3 = ax3.bar(ind, y_SQLi, width, color='g')
	rects4 = ax4.bar(ind, y_DEF, width, color='y')
	rects5 = ax5.bar(ind, y_Craw, width, color='cyan')

	ax1.set_ylabel('Coincidencias detectadas: Path Traversal')
	ax1.set_xlabel(u'Hora y fecha de detección')
	ax1.set_title(u'No. de detecciones por ataque para el día: ' + format(today))
	ax2.set_ylabel('Coincidencias detectadas: XSS')
	ax2.set_xlabel(u'Hora y fecha de detección')
	ax2.set_title(u'No. de detecciones por ataque para el día: ' + format(today))
	ax3.set_ylabel('Coincidencias detectadas: SQLi')
	ax3.set_xlabel(u'Hora y fecha de detección')
	ax3.set_title(u'No. de detecciones por ataque para el día: ' + format(today))
	ax4.set_ylabel('Coincidencias detectadas: Defacement')
	ax4.set_xlabel(u'Hora y fecha de detección')
	ax4.set_title(u'No. de detecciones por ataque para el día: ' + format(today))
	ax5.set_ylabel('Coincidencias detectadas: Crawler/Spidering')
	ax5.set_xlabel(u'Hora y fecha de detección')
	ax5.set_title(u'No. de detecciones por ataque para el día: ' + format(today))

	ax1.set_xticks(ind + width)
	ax1.set_xticklabels(x_axis, rotation='vertical')
	ax2.set_xticks(ind + width)
	ax2.set_xticklabels(x_axis, rotation='vertical')
	ax3.set_xticks(ind + width)
	ax3.set_xticklabels(x_axis, rotation='vertical')
	ax4.set_xticks(ind + width)
	ax4.set_xticklabels(x_axis, rotation='vertical')
	ax5.set_xticks(ind + width)
	ax5.set_xticklabels(x_axis, rotation='vertical')
	
	ax1.set_ybound(lower=0, upper=(max(y_PATH)+50))
	ax2.set_ybound(lower=0, upper=(max(y_Xss)+50))
	ax3.set_ybound(lower=0, upper=(max(y_SQLi)+50))
	ax4.set_ybound(lower=0, upper=(max(y_DEF)+50))
	ax5.set_ybound(lower=0, upper=(max(y_Craw)+50))
	
	autolabel(rects1,ax1)
	autolabel(rects2,ax2)
	autolabel(rects3,ax3)
	autolabel(rects4,ax4)
	autolabel(rects5,ax5)

	fig1.subplots_adjust(bottom=0.3)
	fig2.subplots_adjust(bottom=0.3)
	fig3.subplots_adjust(bottom=0.3)
	fig4.subplots_adjust(bottom=0.3)
	fig5.subplots_adjust(bottom=0.3)
	
	fig1.set_figheight(8)
	fig1.set_figwidth(15)
	fig2.set_figheight(8)
	fig2.set_figwidth(15)
	fig3.set_figheight(8)
	fig3.set_figwidth(15)
	fig4.set_figheight(8)
	fig4.set_figwidth(15)
	fig5.set_figheight(8)
	fig5.set_figwidth(15)

	fig1.savefig('img/report1.png')
	fig2.savefig('img/report2.png')
	fig3.savefig('img/report3.png')
	fig4.savefig('img/report4.png')
	fig5.savefig('img/report5.png')
	plt.close(fig1)
	plt.close(fig2)
	plt.close(fig3)
	plt.close(fig4)
	plt.close(fig5)

def send_mail_reporte(mail_report):
	while 1:
		tiempo = logcfg["tiempoReportes"]
		#time.sleep(tiempo*3600)
		#time.sleep(tiempo*60)
		time.sleep(1)
		ipCount = subprocess.Popen(["perl", ".cmd.perl", "1" ], stdout=subprocess.PIPE)
		outputIP1, errIP1 = ipCount.communicate()
		ipCount = subprocess.Popen(["perl", ".cmd.perl", "2" ], stdout=subprocess.PIPE)
		outputIP2, errIP2 = ipCount.communicate()
		ipCount = subprocess.Popen(["perl", ".cmd.perl", "3" ], stdout=subprocess.PIPE)
		outputIP3, errIP3 = ipCount.communicate()
		ipCount = subprocess.Popen(["perl", ".cmd.perl", "4" ], stdout=subprocess.PIPE)
		outputIP4, errIP4 = ipCount.communicate()
		ipCount = subprocess.Popen(["perl", ".cmd.perl", "5" ], stdout=subprocess.PIPE)
		outputIP5, errIP5 = ipCount.communicate()
		userCount = subprocess.Popen(["perl", ".cmd.perl", "6" ], stdout=subprocess.PIPE)
		outputU1, errU1 = userCount.communicate()
		userCount = subprocess.Popen(["perl", ".cmd.perl", "7" ], stdout=subprocess.PIPE)
		outputU2, errU1 = userCount.communicate()
		userCount = subprocess.Popen(["perl", ".cmd.perl", "8" ], stdout=subprocess.PIPE)
		outputU3, errU1 = userCount.communicate()
		userCount = subprocess.Popen(["perl", ".cmd.perl", "10" ], stdout=subprocess.PIPE)
		outputU5, errU5 = userCount.communicate()
		
		contIP1, ip1 = getfromPerl(outputIP1)
		contIP2, ip2 = getfromPerl(outputIP2)
		contIP3, ip3 = getfromPerl(outputIP3)
		contIP4, ip4 = getfromPerl(outputIP4)
		contIP5, ip5 = getfromPerl(outputIP5)
		contUser1, agent1 = getfromPerl(outputU1)
		contUser2, agent2 = getfromPerl(outputU2)
		contUser3, agent3 = getfromPerl(outputU3)
		contUser5, agent5 = getfromPerl(outputU5)
		
		today = date.today()
		mail_report["html"] += "\n    <h1>Reporte de actividad maliciosa [" + format(today) + "].</h1>\n"
		mail_report["html"] += "\n    <h1>Secci&oacuten 1 : Resumen de los hallazgos </h1>\n"
		mail_report["html"] += "    <br><p>SQL injection: </p><br>\n"
		for inx, ip in enumerate(ip1):
			mail_report["html"] += "    <p>------> IP de origen: <b>" + ip + "</b>  Cantidad: <b>" + contIP1[inx] + "</b></p>\n"
		mail_report["html"] += "    <br><p>Cross Site Scripting: </p><br>\n"
		for inx, ip in enumerate(ip2):
			mail_report["html"] += "    <p>------> IP de origen: <b>" + ip + "</b>  Cantidad: <b>" + contIP2[inx] + "</b></p>\n"
		mail_report["html"] += "    <br><p>Path Traversal: </p><br>\n"
		for inx, ip in enumerate(ip3):
			mail_report["html"] += "    <p>------> IP de origen: <b>" + ip + "</b>  Cantidad: <b>" + contIP3[inx] + "</b></p>\n"
		mail_report["html"] += "    <br><p>Crawler: </p><br>\n"
		for inx, ip in enumerate(ip4):
			mail_report["html"] += "    <p>------> IP de origen: <b>" + ip + "</b>  Cantidad: <b>" + contIP4[inx] + "</b></p>\n"
		mail_report["html"] += "    <br><p>Defacement: </p><br>\n"
		for inx, ip in enumerate(ip5):
			mail_report["html"] += "    <p>------> IP de origen: <b>" + ip + "</b>  Cantidad: <b>" + contIP5[inx] + "</b></p>\n"
		mail_report["html"] += "    <br><h1>Seccion 2 : Gr&aacuteficas </h1><br>\n"
		mail_report["html"] += "    <br><p>SQL injection: </p><br>\n"
		mail_report["html"] += '    <br><img src="cid:image1"><br>' + "\n"
		mail_report["html"] += "    <br><p>Cross Site Scripting: </p><br>\n"
		mail_report["html"] += '    <br><img src="cid:image2"><br>' + "\n"
		mail_report["html"] += "    <br><p>Path Traversal: </p><br>\n"
		mail_report["html"] += '    <br><img src="cid:image3"><br>' + "\n"
		mail_report["html"] += "    <br><p>Crawler: </p><br>\n"
		mail_report["html"] += '    <br><img src="cid:image4"><br>' + "\n"
		mail_report["html"] += "    <br><p>Defacement: </p><br>\n"
		mail_report["html"] += '    <br><img src="cid:image5"><br>' + "\n"
		graficar('cod_status.txt')
		print colored(u"Se envio correo de reporte diario",'red')
		report = ['img/report1.png','img/report2.png','img/report3.png','img/report4.png','img/report5.png']
		sendEmailMIME(mail_report["from"], mail_report["pass"], mail_report["to"], "Reporte de actividad maliciosa [" + format(today) + "]", mail_report["html"], report)

def send_mail(mail, sitio, cont_time):
	file = open('status_act.txt', 'r')
	resultados = file.readline()
	res = resultados.split(";")

	cont_PATH = int(res[0])
	cont_XSS = int(res[1])
	cont_encuentros = int(res[2])
	cont_encuentros_ref = int(res[3])
	cont_encuentros_user = int(res[4])
	cont_DEF = int(res[5])
	cont_CRAW = int(res[6])
	cont_encuentros_mail = int(res[7])	
	#if ( (cont_PATH > 1) or (cont_encuentros > 30) or (cont_XSS > 30) or (cont_encuentros_user > 30) or (cont_encuentros_ref > 30) or (cont_encuentros_mail > 1) or (cont_DEF > 1) or (cont_CRAW > 1) ):
	if ( (cont_PATH > 1) or (cont_encuentros > 30) or (cont_XSS > 30) or (cont_encuentros_user > 30) or (cont_encuentros_ref > 30) or (cont_encuentros_mail > 1) or (cont_DEF > 1) or (cont_CRAW > 1) ) and (cont_time <= len(Sitios_listas)):
		ipCount = subprocess.Popen(["perl", ".cmd.perl", "1" ], stdout=subprocess.PIPE)
		outputIP1, errIP1 = ipCount.communicate()
		ipCount = subprocess.Popen(["perl", ".cmd.perl", "2" ], stdout=subprocess.PIPE)
		outputIP2, errIP2 = ipCount.communicate()
		ipCount = subprocess.Popen(["perl", ".cmd.perl", "3" ], stdout=subprocess.PIPE)
		outputIP3, errIP3 = ipCount.communicate()
		ipCount = subprocess.Popen(["perl", ".cmd.perl", "4" ], stdout=subprocess.PIPE)
		outputIP4, errIP4 = ipCount.communicate()
		ipCount = subprocess.Popen(["perl", ".cmd.perl", "5" ], stdout=subprocess.PIPE)
		outputIP5, errIP5 = ipCount.communicate()
		userCount = subprocess.Popen(["perl", ".cmd.perl", "6" ], stdout=subprocess.PIPE)
		outputU1, errU1 = userCount.communicate()
		userCount = subprocess.Popen(["perl", ".cmd.perl", "7" ], stdout=subprocess.PIPE)
		outputU2, errU1 = userCount.communicate()
		userCount = subprocess.Popen(["perl", ".cmd.perl", "8" ], stdout=subprocess.PIPE)
		outputU3, errU1 = userCount.communicate()
		userCount = subprocess.Popen(["perl", ".cmd.perl", "10" ], stdout=subprocess.PIPE)
		outputU5, errU5 = userCount.communicate()
		
		contIP1, ip1 = getfromPerl(outputIP1)
		contIP2, ip2 = getfromPerl(outputIP2)
		contIP3, ip3 = getfromPerl(outputIP3)
		contIP4, ip4 = getfromPerl(outputIP4)
		contIP5, ip5 = getfromPerl(outputIP5)
		contUser1, agent1 = getfromPerl(outputU1)
		contUser2, agent2 = getfromPerl(outputU2)
		contUser3, agent3 = getfromPerl(outputU3)
		contUser5, agent5 = getfromPerl(outputU5)
			
		mail["html"] += "\n    <h1>Sitio: " + sitio + " </h1>\n"
		mail["html"] += "\n    <h1>Seccion 1 : Resumen de los hallazgos </h1>\n"
		mail["html"] += "    <br><p>SQL injection: </p><br>\n"
		sum = cont_encuentros + cont_encuentros_ref + cont_encuentros_user
		mail["html"] += "    <p>------> Num. detecciones: <b>" + str(sum) + "</b></p>\n"
		for inx, ip in enumerate(ip1):
			mail["html"] += "    <p>------> IP de origen: <b>" + ip + "</b>  Cantidad: <b>" + contIP1[inx] + "</b></p>\n"
		#if int(cont_encuentros_user) >= 1:
		#	mail["html"] += "    <p>------> User-Agent: <b>Se encontraron peticiones SQL en el User-Argent</b>  Cantidad: <b>" + contUser1[inx] + "</b></p>\n"
		#else:
		#	for inx, agent in enumerate(agent1):
		#		mail["html"] += "    <p>------> User-Agent: <b>" + agent + "</b>  Cantidad: <b>" + contUser1[inx] + "</b></p>\n"
		mail["html"] += "    <br><p>Cross Site Scripting: </p><br>\n"
		mail["html"] += "    <p>------> Num. detecciones: " + str(cont_XSS) + "</p>\n"
		for inx, ip in enumerate(ip2):
			mail["html"] += "    <p>------> IP de origen: <b>" + ip + "</b>  Cantidad: <b>" + contIP2[inx] + "</b></p>\n"
		#for inx, agent in enumerate(agent2):
		#	mail["html"] += "    <p>------> User-Agent: <b>" + agent + "</b>  Cantidad: <b>" + contUser2[inx] + "</b></p>\n"
		mail["html"] += "    <br><p>Path Traversal: </p><br>\n"
		mail["html"] += "    <p>------> Num. detecciones: " + str(cont_PATH) + "</p><br>\n"
		for inx, ip in enumerate(ip3):
			mail["html"] += "    <p>------> IP de origen: <b>" + ip + "</b>  Cantidad: <b>" + contIP3[inx] + "</b></p>\n"
		#for inx, agent in enumerate(agent3):
		#	mail["html"] += "    <p>------> User-Agent: <b>" + agent + "</b>  Cantidad: <b>" + contUser3[inx] + "</b></p>\n"
		mail["html"] += "    <br><p>Crawler: </p><br>\n"
		mail["html"] += "    <p>------> Num. detecciones: " + str(cont_CRAW) + "</p><br>\n"
		for inx, ip in enumerate(ip4):
			mail["html"] += "    <p>------> IP de origen: <b>" + ip + "</b>  Cantidad: <b>" + contIP4[inx] + "</b></p>\n"
		mail["html"] += "    <br><p>Defacement: </p><br>\n"
		mail["html"] += "    <p>------> Num. detecciones: " + str(cont_DEF) + "</p><br>\n"
		for inx, ip in enumerate(ip5):
			mail["html"] += "    <p>------> IP de origen: <b>" + ip + "</b>  Cantidad: <b>" + contIP5[inx] + "</b></p>\n"
		#for inx, agent in enumerate(agent5):
		#	mail["html"] += "    <p>------> User-Agent: <b>" + agent + "</b>  Cantidad: <b>" + contUser5[inx] + "</b></p>\n"
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
		f = open("mensajeCRAW.html", 'r+')
		pathCraw = f.read()
		f.close()
		f = open("mensajeDEFC.html", 'r+')
		pathDEFC = f.read()
		f.close()
		mail["html"] += sqliHtml
		mail["html"] += xssHtml
		mail["html"] += pathHtml
		mail["html"] += pathCraw
		mail["html"] += pathDEFC
		print colored(u"-------------------------->[ ¡¡¡¡¡Tal véz te esten atacando: ಠ_ಠ  !!!!!]<-----------------------------------------------------------",'red')
		mail["cont-mail"] = mail["cont-mail"] + 1
		cont_time = cont_time + 1;
		sendEmail(mail["from"], mail["pass"], mail["to"], mail["asunto"], mail["html"], mail["text"])
		clean()
	if (cont_time != 0):
		cont_time = cont_time + 1;
	if (cont_time == 700):
		cont_time = 0;
	return cont_time

def sendEmail(user, pwd, recipient, subject, html, text):
	print "adentro"
	mail["flag-mail"] = 0
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
		print u'¡¡¡¡¡Se envió correo electrónico!!!'
	except Exception as cadena:
		print "Error al envio del correo" + format(cadena)

def sendEmailMIME(user, pwd, recipient, subject, html, images):
	print "adentro"
	mail["flag-mail"] = 0
	gmail_user = user
	gmail_pwd = pwd
	From = user
	to = recipient
	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = subject
	msgRoot['From'] = From
	msgRoot['To'] = to
	msgRoot.preamble = 'This is a multi-part message in MIME format.'
	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)

	msgText = MIMEText('This is the alternative plain text message.')
	msgAlternative.attach(msgText)

	msgText = MIMEText(html, 'html')
	msgAlternative.attach(msgText)

	for i,image in enumerate(images):
		fp = open(image, 'rb')
		msgImage = MIMEImage(fp.read())
		fp.close()

		msgImage.add_header('Content-ID', '<image' + str(i+1) + '>')
		msgRoot.attach(msgImage)
	try:
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_pwd)
		server.sendmail(From, to, msgRoot.as_string())
		server.close()
		print u'¡¡¡¡¡Se envió correo electrónico!!!'
	except Exception as cadena:
		print "Error al envio del correo" + format(cadena)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------Hilos--------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------#
class analiticThread(threading.Thread):
	def __init__(self, threadID, name, file_name2, tipo_log, folder, sitios, mail):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.file_name2 = file_name2
		self.tipo_log = tipo_log
		self.folder = folder
		self.sitios = sitios
		self.mail = mail
	def run(self):
		print "Iniciando: " + self.name
		init_SQli(self.file_name2, self.tipo_log, self.folder, self.sitios, self.mail)
		print "Saliendo: " + self.name

class mailReportThread(threading.Thread):
	def __init__(self, threadID, name, mail):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.mail = mail
	def run(self):
		print "Iniciando: " + self.name
		send_mail_reporte(mail)
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
	lineas_inicio.append(int(servidor_web["Lineas_inicio_log"][i]) + 1)
	site_list.append(servidor_web["sitios"][i])
	file_name_list.append(servidor_web["file_name_list"][i])
	file_name_list2.append(servidor_web["file_name_list2"][i])
	folder_list.append(servidor_web["folder"][i])
	log_type_list.append(servidor_web["log_type"][i])
	
	path_list.append(servidor_waf["logs"][i])
	server_index.append(servidor_waf["serverIndex"][i])
	lineas_inicio.append(int(servidor_waf["Lineas_inicio_log"][i]) + 1)
	site_list.append(servidor_waf["sitios"][i])
	file_name_list.append(servidor_waf["file_name_list"][i])
	file_name_list2.append(servidor_waf["file_name_list2"][i])
	folder_list.append(servidor_waf["folder"][i])
	log_type_list.append(servidor_waf["log_type"][i])

path_list.append(servidor_bd["logs"][0])
server_index.append(servidor_bd["serverIndex"][0])
lineas_inicio.append(int(servidor_bd["Lineas_inicio_log"][0]) + 1)
site_list.append("bd")
file_name_list.append(servidor_bd["file_name_list"][0])
file_name_list2.append(servidor_bd["file_name_list2"][0])
folder_list.append(servidor_bd["folder"][0])
log_type_list.append(servidor_bd["log_type"][0])

path_list.append(servidor_modsec["logs"][0])
server_index.append(servidor_modsec["serverIndex"][0])
lineas_inicio.append(int(servidor_modsec["Lineas_inicio_log"][0]) + 1)
site_list.append("Audit")
file_name_list.append(servidor_modsec["file_name_list"][0])
file_name_list2.append(servidor_modsec["file_name_list2"][0])
folder_list.append(servidor_modsec["folder"][0])
log_type_list.append(servidor_modsec["log_type"][0])

srv_list = [srv_web, srv_waf, srv_bd]
shell_list = [shell_web, shell_waf, shell_bd]

text = "Enviamos el siguiente correo por que se cree que su servidor esta bajo ataque:\nRecomendamos realizar las modificaciones pertinentes\n"
html = """\
<html>
  <head></head>
  <body>
    <h1>Se registro un aumento en la actividad maliciosa</h1>
"""

mail["html"] = html
mail["text"] = text

mail_report = mail
#mail = {"from":"unam.cert.log.send@gmail.com", "pass":"hola123.,", "to":"juan_as1991@hotmail.com", "asunto":"Envio de reporte de posbles ataques", "html":html, "text":text}
#sendEmailMIME(mail_report["from"], mail_report["pass"], mail_report["to"], mail_report["asunto"], mail_report["html"], 'img/report.png')
# Creacion de los hilos
try:
	log_thread = logThread(1,"Hilo: Obtencion logs", srv_list, shell_list, path_list, lineas_inicio, logcfg["time_log"], file_name_list, server_index, logcfg["max_size_log"], file_name_list2, site_list, folder_list)
	log_thread.daemon = True
	log_thread.start()
	pass
except Exception as cadena:
	print "Error: " + format(cadena)
	exit()
	
try:
	analisis_thread = analiticThread(2,"Hilo: analisis",file_name_list2, log_type_list, folder_list, site_list, mail)
	analisis_thread.daemon = True
	analisis_thread.start();
except Exception as cadena:
	print "Error: " + format(cadena)
	exit()

try:
	mail_thread = mailReportThread(2,"Hilo: Envio de email",mail_report)
	mail_thread.daemon = True
	mail_thread.start();
	pass
except Exception as cadena:
	print "Error: " + format(cadena)
	exit()


#Creamos un lock para que corran de manera sincronizada
threadLock = threading.Lock()
threads = []
threads.append(log_thread)
threads.append(analisis_thread)


banner()
while 1:
	if not log_thread.isAlive():
		print "Hilo log: die"
		print "El programa se detendra ya que el hilo es crucial para la operacion..."
		print "ejecute [rm ./logs/*/log_* && rm ./parsedLogs/*/log_*] en la carpeta de proyecto"
		break;
	if not analisis_thread.isAlive():
		print "Hilo analizador: die"
		print "El programa se detendra ya que el hilo es crucial para la operacion..."
		print "ejecute [rm ./logs/*/log_* && rm ./parsedLogs/*/log_*] en la carpeta de proyecto"
		break;
#print "Escriba [q] para salir"
	#salir = raw_input()
	#if salir == 'q':
	#	print "Saliendo...."
	#	Mail.stop()
	#	log_thread.stop()
	#	sqli_thread.stop()
	#	break;
		
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
