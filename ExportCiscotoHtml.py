#!/usr/bin/env python3
'''
###############################################################################################################
#                                             ExportCiscoHtml                                                 #
#                                         ver. 1.00 [03.02.2018]                                              #
#                                               Autor: J.S.                                                   #
#    Program ten na podstawie plików archiwizacyjnych dla switchy (/opt/magazyn/pliki_serwis/SIEC/<miesiąc>)  #
# generyje statyczne raporty w formie html na ścieżce podanej w zmiennej dpath. Skrypt odczytuje z pliku      #
# wszystkie możliwe dane przez co, zachowane zostało nazewnictwo. Skrypt jest automatycznie uruchamiany przez #
# mechanizm Crona każdego 13 dnia miesiąca.                                                                   #
# Skrypt jest częścią projektu pulpitu technika (choć pewnie będę musuiał zmienić nazwę bo prędzej uda mi się #
# zarobić na nim niż przekonać moich "koserwatywnych" kolegów).                                               #
###############################################################################################################
'''

import time
import os

dpath = "/opt/magazyn/pliki_serwis/KATALOGI/S7330/01 SIEĆ Poznań/Switche/"
hpath = "/opt/magazyn/pliki_serwis/POLECENIA/export_plk/"


def PobierzKatalog(path):
	return os.listdir(path)


def CzytajPlik(spath,nazwa):
	file = open(spath+"/"+nazwa,"r")
	str = file.read()
	file.close()
	return str


def ZapiszPlik(dpath, nazwa, wyj):
	file = open(dpath+nazwa+".html", 'w')
	file.write(wyj)
	file.close()


def CzyscStr(str):             # Wstepne czyszczenie z formatowania odczytanego pliku - wynik lista
	tab_1 = str.split("!")
	i = 0
	for tab in tab_1:
		tab_1[i] = tab.strip()
		i = i+1
	return tab_1


def CzyscTab(tablica):
	i = 0
	for tab in tablica:
		tablica[i] = tab.strip()
		i = i+1
	return tablica


def SelekcjaInt(tablica):
	gniazda = list(filter(lambda x: 'interface Giga' in x, tablica))
	if len(gniazda) < 5:
		gniazda = list(filter(lambda x: 'interface Fast' in x, tablica)) 
	return gniazda


def TrunkDecode(listt):
	out = ""
	fili = list(filter(lambda x: 'switchport trunk allowed' in x, listt))
	
	if len(fili) > 0: 
		out = fili[0]
		out = out[29:]
	if len(fili) > 1:
		out = out + "," + "".join( filter(lambda x: 'switchport trunk allowed vlan add' in x, listt))[33:]
	return out


def Dekoder(gniazda):
	out = ""
	for linia in gniazda:
		lista = linia.split("\n")
		lista = CzyscTab(lista)
		str1 = "".join( filter(lambda x: 'interface Giga' in x, lista))[25:]
		str1 = str1 + "".join( filter(lambda x: 'interface Fast' in x, lista))[22:]
		str2 = "".join( filter(lambda x: 'description' in x, lista))[11:]
		str3 = "".join( filter(lambda x: 'switchport mode' in x, lista))[15:]
		str4 = "".join( filter(lambda x: 'switchport access' in x, lista))[22:]
		str4 = str4 + TrunkDecode(lista) # "".join( filter(lambda x: 'switchport trunk allowed' in x, lista))[29:]
		str5 = "".join( filter(lambda x: 'switchport voice' in x, lista))[22:]
		out = out + "<tr class='success'><td>"+str1+"</td><td>"+str2+"</td><td>"+str3+"</td><td>"+str4+"</td><td>"+str5+"</td></tr>\n"
		
	return out



naj_kat = PobierzKatalog("/opt/magazyn/pliki_serwis/SIEC/")
naj_kat.sort(reverse=True)

spath = "/opt/magazyn/pliki_serwis/SIEC/"+naj_kat[0]
pliki_cfg = PobierzKatalog("/opt/magazyn/pliki_serwis/SIEC/"+naj_kat[0])

naglowek = CzytajPlik(hpath,"naglowek.txt")
stopka = CzytajPlik(hpath, "stopka.txt")



for splik in pliki_cfg:
	tab = CzyscStr(CzytajPlik(spath,splik))
	HOST = "".join(list(filter(lambda x: 'hostname' in x, tab)))[9:]
	BKP = naj_kat[0]
	IPADR = "".join(list(filter(lambda x: 'interface Vlan98\n ip address' in x, tab)))[29:]
	IPADR = IPADR[:13]
	DATA = time.strftime("%Y-%m-%d")
	tresc = "<p><h1><b>Switch: </b>"+HOST+"</h1></p><p><b>Data backup: </b>"+BKP+"</p><p><b>Data dokumentu: </b>"+DATA+"</p><p><b>IP Adres: </b>"+IPADR+"</p>"
	tresc = tresc + '<table class="table table-bordered table-condensed"><thead><tr class="active"><th>Nr portu</th><th>Opis</th><th>Typ portu</th><th>Vlan/Vlany</th><th>Voice</th></tr></thead><tbody>'
	outdata = naglowek + tresc + Dekoder(SelekcjaInt(tab)) + stopka 
	ZapiszPlik(dpath,HOST,outdata)

