#!/usr/bin/env python3
'''
Raport wersja 1.0

'''
import os
import time
from datetime import datetime
from os import popen

IND_START = [0,0,0]
IND_STOP  = [0,0,0]

KOMP = []
SERVIS = []
PLIK = []
sciezka = "/opt/magazyn/pliki_serwis/LOGI/SAMBA/SMB"


def kat_nazwa(sciez_dane_gl):
        gkat = datetime.now().strftime('%Y-%m-%d')
        sciez = sciez_dane_gl + "/" + gkat
        if not os.path.exists(sciez):
                os.makedirs(sciez)
                os.chmod(sciez,0o777)
        return sciez


def PobierzDane():
        tekst = popen('smbstatus').read()

        return tekst

def PodajDate():
	return time.strftime("%Y-%m-%d %H:%M:%S")

def KopmaktujListe(params):
        dane = params
        LISTA = []
        for dana in dane:
            if (len(dana)>0):
                LISTA.append(dana)
        return LISTA



def PodzielDane(params):
         DANE = params.split("\n")

         i=0
         for nr,element in enumerate(DANE):
               if (element.find("---")==0):
                      IND_START[i] = nr
                      i = i + 1
               if (element.find("Service")==0):
                      IND_STOP[0] = nr - 1
               if (element.find("Locked")==0):
                      IND_STOP[1] = nr - 1

         for nr,element in enumerate(DANE):
               if (nr > IND_START[0] and nr < IND_STOP[0]):
                      KOMP.append(element) 

               if (nr > IND_START[1] and nr < IND_STOP[1]):
                      SERVIS.append(element)

               if (nr > IND_START[2]):
                      if len(element)>0:
                             PLIK.append(element)
    
    

def GenerujRap(params):
        wyjscie = params
        lkomp = KopmaktujListe(wyjscie.split(" "))
        komp = lkomp[0]

        wyjscie = "| U:["+lkomp[1]+"]   | G:["+lkomp[2]+"]   | H:["+lkomp[3]+" "+lkomp[4]+"]\r\n"
        wyjscie = wyjscie + "------------------------------------------------------------------------------------------\r\n"
        for nr,element in enumerate(SERVIS):
               if (element.find(komp)>=0):
                      l1 = KopmaktujListe(element.split(" "))
                      wyjscie = wyjscie + "     Start: " + l1[6] + " (" + l1[5] + " " + l1[4] + " " + l1[7] + ")\r\n"

        for nr,element in enumerate(PLIK):
               if (element.find(komp)>=0):
                      kl = KopmaktujListe(element.split(" "))
                      data = " [" + kl[-3] + " " + kl[-4] + " " + kl[-1] + "   " + kl[-2] + "]"
                      sciezka = kl[6]
                      element = " ".join(kl[6:-4]) # -5
                      wyjscie = wyjscie + "          " + data + "/" + element + "\r\n" #  wyjscie + "          " + data + " " + sciezka + "/" + element + "\r\n"
        return wyjscie
    
    
def DoPliku():
        RAP = "\n"
        for host in KOMP:
               RAP = RAP + GenerujRap(host) + "\n\n\n\n"

        plik = open(kat_nazwa(sciezka)+"/"+PodajDate()+" smb.dat", 'w')
        plik.write(RAP)
        plik.close()    
    
'''    
###########################################################################################################################    
'''    

PodzielDane(PobierzDane())
DoPliku()



