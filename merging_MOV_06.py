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
        
        
    def merger(self, liste_transmise):
        
        liste_transmise, numero, sous_chemin, racine = liste
        
        if racine :
            self.out = "/".join((self.out, numero))
        else:
            os.makedirs(sous_chemin, mode = 777)
            self.out = "/".join((self.out, sous_chemin))
            
        offset = 0
        for l in sorted(liste_transmise.keys()):
            
                
            if l.split(".")[0].split("_")[1] == "01" :
                if self.precedent != "":
                    self.suite(self.chemin_precedent, self.precedent)
                    #os.remove(self.chemin_precedent)
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
            
        self.suite(self.chemin_precedent, self.precedent)  
        #os.remove(self.chemin_precedent)
        
        
    def versFifo(self, chemin_in, nom):
        nomFifo = "%s/%s.m2t" % (self.ram, nom)
        os.mkfifo(nomFifo)
        m2 = subprocess.Popen("ffmpeg -y -i '%s' -acodec ac3 -b:a 384k -vcodec copy %s" % (chemin_in, nomFifo), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)            
        time.sleep(0.5)
        return nomFifo
        
                
                
    def suite(self, chemin_in, nom):
        m2 = subprocess.Popen("ffmpeg -y -i '%s' -acodec copy -vcodec mpeg2video -q:v 0 %s/%s.m2t" % (chemin_in, self.out, nom), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)            
        while m2.poll() == None:
            time.sleep(0.1)
        os.remove(chemin_in)
            
    def suiteDeint(self, chemin_in, nom):
        m2 = subprocess.Popen("ffmpeg -y -i '%s'  -vf 'yadif=0:0:0' -acodec copy -vcodec mpeg2video -q:v 0 %s/%s.m2t" % (chemin_in, self.out, nom), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)            
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
        
        if self.numero == self.sous_chemin :
            self.racine = True
        else :
            self.racine = False
        
        liste_des_videos = {}
        extension = ""
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                if f.split(".")[-1].upper() == "MOV" :
                    fp = os.path.join(dirpath, f)
   
                    ### correct pour MOV/HDV_1080p/MPEG2/1920x1080/35Mbs/PCM_s16be (RUGGIU) 3474_1
                    print(f)
                    print(fp)
                    liste_des_videos[f] = fp
        return (liste_des_videos, self.numero, self.sous_chemin, self.racine)
                
        
            
builder = Gtk.Builder()     
builder.add_from_file("encodage_01.glade")
window = builder.get_object("window1")
window.connect("delete-event", Gtk.main_quit)

gui = Gui()
window.show_all()
Gtk.main() 


merge = Merge("/home/david/temp")
liste = Liste()
merge.merger(liste.new_liste(liste.new_liste(sys.argv[1]) )




       
