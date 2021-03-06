# -*- coding: utf-8 -*-

import os, os.path, sys
import subprocess
import time

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
        
        if racine :
            self.out = "/".join((self.out, numero))
        else:
            os.makedirs(sous_chemin, mode = 777)
            self.out = "/".join((self.out, sous_chemin))
        
        offset = 0
        for l in sorted(liste_transmise.keys()):     
            
            if str(os.stat(liste_transmise[l]).st_size)[:-7] == "204" and self.precedent == "":
            #if str(os.stat(liste_transmise[l]).st_size)[:-7] == "429" and self.precedent == "":
                
                offset = 0
                self.outpath = "/".join((self.temp, "%s_complet.m2t" % l[:-4]))
                self.precedent = l
                self.chemin_precedent = self.outpath
                
                m1 = subprocess.Popen("dd if='%s' of='%s' seek=%d" % (self.versFifo(liste_transmise[l], l), self.outpath, offset), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)
            
                while m1.poll() == None:
                    time.sleep(0.1)
                reste_div = os.stat(self.outpath).st_size % 512
                if reste_div != 0:
                    offset = (os.stat(self.outpath).st_size / 512) + 1
                else :
                    offset = os.stat(self.outpath).st_size / 512
                print(offset)
                
            #if str(os.stat(liste_transmise[l]).st_size)[:-7] != "212" :
            elif str(os.stat(liste_transmise[l]).st_size)[:-7] != "204":
            #elif str(os.stat(liste_transmise[l]).st_size)[:-7] != "429" :
                if self.precedent != "":
                    m1 = subprocess.Popen("dd if='%s' of='%s' seek=%d" % (self.versFifo(liste_transmise[l], l), self.outpath, offset), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)
                    while m1.poll() == None:
                        time.sleep(0.1)
                    
                    offset = 0
                    self.suite(self.chemin_precedent, self.precedent)
                    #self.suiteDeint(self.chemin_precedent, self.precedent)
                    self.chemin_precedent = ""
                    self.precedent = ""

                else :
                    
                        
                    offset = 0
                    self.outpath = "/".join((self.temp, "%s_complet.m2t" % l[:-4]))
                    self.precedent = l
                    self.chemin_precedent = "/".join((self.temp, "%s_complet.m2t" % l[:-4]))
                    m1 = subprocess.Popen("dd if='%s' of='%s' seek=%d" % (self.versFifo(liste_transmise[l], l), self.outpath, offset), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)
                    while m1.poll() == None:
                        time.sleep(0.1)
                    self.suite(self.chemin_precedent, self.precedent)
                    #self.suiteDeint(self.chemin_precedent, self.precedent)
                    self.chemin_precedent = ""
                    self.precedent = ""
                
            else :
                m1 = subprocess.Popen("dd if='%s' of='%s' seek=%d" % (self.versFifo(liste_transmise[l], l), self.outpath, offset), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)
            
                while m1.poll() == None:
                    time.sleep(0.1)
                reste_div = os.stat(self.outpath).st_size % 512
                if reste_div != 0:
                    offset = (os.stat(self.outpath).st_size / 512) + 1
                else :
                    offset = os.stat(self.outpath).st_size / 512
                print(offset)
            
        #self.suite(self.chemin_precedent, self.precedent)  
        #self.suiteDeint(self.chemin_precedent, self.precedent)  
        
            
    def versFifo(self, chemin_in, nom):
        nomFifo = "%s/%s.m2t" % (self.ram, nom)
        os.mkfifo(nomFifo)
        #m2 = subprocess.Popen("ffmpeg -y -i '%s' -acodec pcm_s16le -vcodec copy %s" % (chemin_in, nomFifo), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)            
        m2 = subprocess.Popen("ffmpeg -y -i '%s' -acodec ac3 -b:a 384k -vcodec copy '%s'" % (chemin_in, nomFifo), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)            
        time.sleep(0.5)
        return nomFifo
        
                
                
    def suite(self, chemin_in, nom):
        #m2 = subprocess.Popen("ffmpeg -y -i '%s' -acodec copy -vcodec mpeg2video -q:v 0 -f vob %s/%s.mpg" % (chemin_in, self.out, nom), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)            
        m2 = subprocess.Popen("ffmpeg -y -i '%s' -acodec copy -vcodec mpeg2video -q:v 0 '%s/%s.m2t'" % (chemin_in, self.out, nom), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)            
        while m2.poll() == None:
            time.sleep(0.1)

            
    def suiteDeint(self, chemin_in, nom):
        #m2 = subprocess.Popen("ffmpeg -y -i '%s'  -vf 'yadif=0:0:0' -acodec copy -vcodec mpeg2video -q:v 0 -f vob %s/%s.mpg" % (chemin_in, self.out, nom), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)            
        m2 = subprocess.Popen("ffmpeg -y -i '%s'  -vf 'yadif=0:0:0' -acodec copy -vcodec mpeg2video -q:v 0 '%s/%s.m2t'" % (chemin_in, self.out, nom), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)            
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
        extension = ""
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                if f.split(".")[-1].upper() == "MTS" :
                    fp = os.path.join(dirpath, f)
                    nom = f.split(".")[0]
   
                    ### correct pour MTS/HDV_1080i/MPEG2/1440x1080/25Mbs/PCM_s16be (lopacki) 748_doublon
                    
                    print(f)
                    print(fp)
                    liste_des_videos[f] = fp
        return (liste_des_videos, self.numero, self.sous_chemin, self.racine)
  
        
     
merge = Merge("/home/david/temp")
liste = Liste()
merge.merger(liste.new_liste(sys.argv[1]))

