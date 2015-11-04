# -*- coding: utf-8 -*-

import os, os.path, sys
import subprocess
import time
import shutil
from gi.repository import Gtk




class Merge():
    
    def __init__(self, liste_root):
        
        self.liste_root = liste_root
        self.ram = "/mnt/ramdisk"
        self.temp = "/home/david/temp"
        self.out = "/mnt/2015_rushs"
        self.chemin_precedent = ""
        self.precedent = ""
        self.changement = True
        self.dernier = True
        
    def merger(self, liste):
        
        liste_transmise, numero, sous_chemin, racine = liste
        
        if racine :
            self.out = "/".join((self.out, numero))
        else:
            os.makedirs("/".join((self.out, sous_chemin)), 777)
            self.out = "/".join((self.out, sous_chemin))
        
        offset = 0
        
        for l in sorted(liste_transmise.keys()):
            
            self_m2t_temp1 = "/".join((self.temp, l + ".m2t"))
            
            mt = subprocess.Popen("ffmpeg -y -i '%s' -acodec ac3 -b:a 256k -ac 2 -vcodec mpeg2video -q:v 0 %s" % (liste_transmise[l], self_m2t_temp1), shell=True)#, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)           
            #mt = subprocess.Popen("ffmpeg -y -i '%s' -acodec ac3 -b:a 256k -ac 2 -vcodec copy -q:v 0 %s" % (liste_transmise[l], self_m2t_temp1), shell=True)#, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)           
            while mt.poll() == None:
                time.sleep(0.1)
                
            if self.changement :
                
                offset = 0
                self.outpath = "/".join((self.temp, "%s_complet.m2t" % l[:-4]))
                self.precedent = l
                
            if os.stat(liste_transmise[l]).st_size > 2040000000:
                self.changement = False           
                self.dernier = False
            
            else:
                self.dernier = True

            mv = subprocess.Popen("dd if='%s' of='%s' seek=%d" % (self_m2t_temp1, self.outpath, offset), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)           
            while mv.poll() == None:
                time.sleep(0.1)
            reste_div = os.stat(self.outpath).st_size % 512
            if reste_div != 0:
                offset = (os.stat(self.outpath).st_size / 512) + 1
            else :
                offset = os.stat(self.outpath).st_size / 512
            print(offset)
            
            if self.dernier:
                self.suite(self.outpath, self.precedent)
                self.changement = True
                self.dernier = False
           
                
    def suite(self, chemin_in, nom):
        
        m2 = subprocess.Popen("ffmpeg -y -i '%s'  -s 720x576 -sws_flags lanczos -pix_fmt yuv420p  -b:a 384k -ac 2 -vcodec mpeg2video -q:v 0 '%s/%s.mpg'" % (chemin_in, self.out, nom), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)            
        while m2.poll() == None:
            time.sleep(0.1)

   
class Liste():
    def __init__(self):
        pass
        
    def new_liste(self, start_path):
        
        self.numero = start_path.split("/")[4]
        self.sous_chemin = "/".join(start_path.split("/")[4:])
        
        if self.numero == self.sous_chemin :
            self.racine = True
        else :
            self.racine = False
        
        liste_des_videos = {}
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                if f.split(".")[-1].upper() == "MXF" :
                    fp = os.path.join(dirpath, f)
                    print(fp)
                    liste_des_videos[f] = fp
        return (liste_des_videos, self.numero, self.sous_chemin, self.racine)
                
merge = Merge("/home/david/temp")
liste = Liste()
merge.merger(liste.new_liste(sys.argv[1]))
