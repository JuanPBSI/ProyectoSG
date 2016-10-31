#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import os
from pandas import Series
import time
from datetime import date
from matplotlib import gridspec

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

report = ['img/report1.png','img/report2.png','img/report3.png','img/report4.png','img/report5.png']
graficar('cod_status.txt')


	

	
#np.random.seed(23)
#sample = Series(np.random.randn(1,100).ravel())
#x = np.array([[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3]])
#sample = Series(x.ravel())
#sample.head()
#print sample
#sample2={[1,2,3,4,5],[2,2,2,2,2]}
#fig = plt.figure()
#ax = fig.add_subplot(1,1,1)
#ax.hist(sample,30, color='y', alpha=0.5)
#fig.savefig('to.png')
#plt.close(fig)
