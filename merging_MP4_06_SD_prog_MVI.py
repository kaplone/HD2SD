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
            os.makedirs(sous_chemin, mode = 777)
            self.out = "/".join((self.out, sous_chemin))
        
        offset = 0
        for l in sorted(liste_transmise.keys()):
            
                
            if self.changement :
                
                if self.precedent != "":
		    #######################################
                    self.suite(self.chemin_precedent, self.precedent)
                    #self.suiteDeint(self.chemin_precedent, self.precedent)
		    #######################################
                    
                offset = 0
                self.outpath = "/".join((self.temp, "%s_complet.m2t" % l[:-4]))
                self.precedent = l
                self.chemin_precedent = self.outpath
		
            #######################################
            #if False :  
            #if os.stat(liste_transmise[l]).st_size > 2040000000:
	    #if os.stat(liste_transmise[l]).st_size > 2120000000:
            if os.stat(liste_transmise[l]).st_size >  4240000000:
            #if os.stat(liste_transmise[l]).st_size >  4250000000:
            #if os.stat(liste_transmise[l]).st_size > 4260000000:
            #f os.stat(liste_transmise[l]).st_size > 4280000000:
            #if os.stat(liste_transmise[l]).st_size > 4100000000:
            #if os.stat(liste_transmise[l]).st_size >= 261310464 and os.stat(liste_transmise[l]).st_size != 656947200 :
	    #######################################
	    # ls -la '/mnt/2015_cartes/5000-6000/5379/contrat 5379 - 270515 arabesque/HVR'
	    #
                self.changement = False           
                self.dernier = False
            
            else:
                self.dernier = True
                
            m1 = subprocess.Popen("dd if='%s' of='%s' seek=%d" % (self.versFifo(liste_transmise[l], l), self.outpath, offset), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)
            
            while m1.poll() == None:
                time.sleep(0.1)
            reste_div = os.stat(self.outpath).st_size % 512
            if reste_div != 0:
                offset = (os.stat(self.outpath).st_size / 512) + 1
            else :
                offset = os.stat(self.outpath).st_size / 512
            print(offset)
        
        if self.dernier:
	    #######################################
            self.suite(self.chemin_precedent, self.precedent) 
            #self.suiteDeint(self.chemin_precedent, self.precedent) 
	    #######################################
            self.changement = True
            self.dernier = False
        
    def versFifo(self, chemin_in, nom):
        nomFifo = "%s/%s.m2t" % (self.ram, nom)
        os.mkfifo(nomFifo)
        m2 = subprocess.Popen("ffmpeg -y -i '%s' -acodec ac3 -b:a 384k -vcodec copy -bsf:v h264_mp4toannexb %s" % (chemin_in, nomFifo), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)            
        time.sleep(0.5)
        return nomFifo
        
        
                
    def suite(self, chemin_in, nom):
        print "in : ", chemin_in
        print "out :" ,self.out   
        m2 = subprocess.Popen("ffmpeg -y -i '%s' -s 720x576 -sws_flags lanczos -pix_fmt yuv420p -b:a 384k -vcodec mpeg2video -q:v 0 %s/%s.mpg" % (chemin_in, self.out, nom), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)            
        while m2.poll() == None:
            time.sleep(0.1)
        os.remove(chemin_in)
            
    def suiteDeint(self, chemin_in, nom):
        m2 = subprocess.Popen("ffmpeg -y -i '%s'  -vf 'yadif=0:0:0' -s 720x576 -sws_flags lanczos -pix_fmt yuv420p -b:a 384k -vcodec mpeg2video -q:v 0 %s/%s.mpg" % (chemin_in, self.out, nom), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)            
        while m2.poll() == None:
            time.sleep(0.1)
        os.remove(chemin_in)
        
          

class Gui(): 
    def __init__(self):
        pass
    
class Liste():
    def __init__(self):
        pass
        
    def new_liste(self, start_path):
        
        self.numero = start_path.split("/")[4]
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
                if f.split(".")[-1].upper() == "MP4" :
                    fp = os.path.join(dirpath, f)
   
                    ### correct pour MP4/XML/HDV_1080p/MPEG2/1440x1080/25Mbs/PCM_s16be (Morel)(baudon) 991_1
                    print(f)
                    print(fp)
                    liste_des_videos[f] = fp
        return (liste_des_videos, self.numero, self.sous_chemin, self.racine)
                
        



merge = Merge("/home/david/temp")
liste = Liste()
merge.merger(liste.new_liste(sys.argv[1]))




