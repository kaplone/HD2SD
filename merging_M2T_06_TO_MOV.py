#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, os.path, sys
import subprocess
import time
from gi.repository import Gtk




class Merge():
    
    def __init__(self, liste_root):
        self.liste_root = liste_root
        self.ram = "/mnt/ramdisk"
        self.temp = "/home/david/temp"
        self.out = "/mnt/rushs_OUT_1"
        self.chemin_precedent = ""
        self.precedent = ""
        
    def merger(self, liste):
        liste_transmise, numero, sous_chemin, racine = liste
        print(liste_transmise)
        print(racine)
        print(numero)
        print(sous_chemin)
        
        if racine :
            self.out = "/".join((self.out, numero))
        else:
            #os.makedirs(sous_chemin, mode = 777)
            self.out = "/".join((self.out, sous_chemin))  
            
        offset = 0
        for l in sorted(liste_transmise.keys()):
            print("_" + l)
            if l[-3:] == "IDX" :
                if self.precedent != "":
                    #self.suite(self.chemin_precedent, self.precedent)
                    self.suiteDeint(self.chemin_precedent, self.precedent)
                offset = 0
                self.outpath = "/".join((self.temp, "%s_complet.m2t" % l[:-4]))
                self.precedent = l
                self.chemin_precedent = self.outpath
            elif l[-3:] == "M2T" :
            #elif l[-3:] == "AVI" :
                m1 = subprocess.Popen("dd if='%s' of='%s' seek=%d" % (liste_transmise[l], self.outpath, offset), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)            
                while m1.poll() == None:
                    time.sleep(0.1)
                reste_div = os.stat(self.outpath).st_size % 512
                if reste_div != 0:
                    offset = (os.stat(self.outpath).st_size / 512) + 1
                else :
                    offset = os.stat(self.outpath).st_size / 512
                print(offset)
                
        #self.suite(self.chemin_precedent, self.precedent)  
        self.suiteDeint(self.chemin_precedent, self.precedent) 
       
    def suite(self, chemin_in, nom):
        m2 = subprocess.Popen("ffmpeg -y -i '%s' -acodec pcm_s16be -vcodec mpeg2video -q:v 0 '%s/%s.mov'" % (chemin_in, self.out, nom), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)            
        while m2.poll() == None:
            time.sleep(0.1)
            
    def suiteDeint(self, chemin_in, nom):
        print(chemin_in)
        print(self.out)
        print(nom)
        m2 = subprocess.Popen("ffmpeg -y -i '%s'  -vf 'yadif=0:0:0' -acodec pcm_s16be  -vcodec mpeg2video -q:v 0 '%s/%s.mov'" % (chemin_in, self.out, nom), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)            
        while m2.poll() == None:
            time.sleep(0.1)
        

   
class Liste():
    def __init__(self):
        pass
        
    def new_liste(self, start_path):
        
        print(start_path)
        if start_path[-1] == "/" :
            start_path = start_path[:-1]
        
        self.numero = start_path.split("/")[4]
        print(self.numero)
        self.sous_chemin = "/".join(start_path.split("/")[4:])
        print(self.sous_chemin)
        
        if self.numero == self.sous_chemin :
            self.racine = True
        else :
            self.racine = False
        
        liste_des_videos = {}
        extension = ""
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                print(f.split(".")[-1].upper())
                if f.split(".")[-1].upper() in ["M2T", "IDX"] :
                #if f.split(".")[-1].upper() in ["AVI", "IDX"] :
                    fp = os.path.join(dirpath, f)
                    print(fp)
   
                    ### correct pour M2T/IDX/HDV_1080p/MPEG2/1440x1080/25Mbs/MP2A/TS (bensemhoun)(paradis) = 5280
                    
                    liste_des_videos["_".join(f.split("_")[2:])] = fp
                    print("$$" + "_".join(f.split("_")[2:]))
        return (liste_des_videos, self.numero, self.sous_chemin, self.racine)
                
merge = Merge("/home/david/temp")
liste = Liste()
merge.merger(liste.new_liste(sys.argv[1]))
