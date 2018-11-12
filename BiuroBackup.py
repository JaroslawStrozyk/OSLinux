#!/usr/bin/python3
from subprocess import Popen, PIPE
import time

cmd = "rsync -avz /opt/magazyn/pliki_ogolne/BIURO/ /opt/magazyn/pliki_chronione/BIURO_KOPIA/"
sciezka = "/opt/magazyn/pliki_serwis/LOGI/RSYNC/"


def PodajDate():
	return time.strftime("%Y-%m-%d %H:%M")
	
def PodajDateS():
	return time.strftime("%Y-%m-%d %H:%M:%S")



def KopiaZasobow():
	data_start = PodajDateS()
	p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
	out, err = p.communicate()

	if p.returncode == 0:
		status = "OK"
	else:
		status = "BŁĄD"
 
	wyjscie = out.rstrip().decode("utf-8").splitlines()
	ilosc   = len(wyjscie)
	bledy   = err.decode("utf-8")
	data_koniec = PodajDateS()
	
	return "<tr><td colspan='2'>Katalog dokumentów [BIURO]</td></tr>\n<tr><td>DATA START:</td><td>%s</td></tr>\n<tr><td>DATA KONIEC:</td><td>%s</td></tr>\n<tr><td>ILOŚĆ ARCHIWIZOWANYCH ELEMENTÓW:</td><td>%i</td></tr>\n<tr><td>STATUS:</td><td>%s</dt></tr>\n<tr><td>OPIS BŁĘDU:</td><td>%s</td><tr>\n" % (data_start, data_koniec, ilosc, status, bledy)	
	
def ZapiszRap(opis):
	zasob = sciezka + PodajDate()+" biuro.txt"
	plik = open(zasob, 'w')
	plik.write(opis)
	plik.close()


ZapiszRap(KopiaZasobow())
