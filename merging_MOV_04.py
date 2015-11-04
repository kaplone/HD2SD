# -*- coding: utf-8 -*-

import os, os.path, sys
import subprocess
import time
from gi.repository import Gtk




class Merge():
    
    def __init__(self, liste_root):
        self.liste_root = liste_root
        self.chemin_precedent = ""
        self.precedent = ""
        
        
    def merger(self, liste_transmise):
        offset = 0
        for l in sorted(liste_transmise.keys()):
            
                
            if l.split(".")[0].split("_")[1] == "01" :
                if self.precedent != "":
                    self.suite(self.chemin_precedent, self.precedent)
                offset = 0
                self.outpath = "/".join((self.liste_root, "%s_complet.MOV" % l[:-4]))
                self.precedent = l
                self.chemin_precedent = self.outpath
            m1 = subprocess.Popen("dd if='%s' of='%s' seek=%d" % (liste_transmise[l], self.outpath, offset), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)
            
            while m1.poll() == None:
                time.sleep(0.1)
            reste_div = os.stat(self.outpath).st_size % 512
            if reste_div != 0:
                offset = (os.stat(self.outpath).st_size / 512) + 1
            else :
                offset = os.stat(self.outpath).st_size / 512
            print(offset)
            
        self.suite(self.chemin_precedent, self.precedent)   
                
                
    def suite(self, chemin_in, nom):
        m2 = subprocess.Popen("ffmpeg -y -i '%s' -acodec ac3 -b:a 384k -vcodec mpeg2video -q:v 0 /mnt/rushs_OUT_2/3474_1/%s.m2t" % (chemin_in, nom), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)            
        while m2.poll() == None:
            time.sleep(0.1)
            

class Gui(): 
    def __init__(self):
        pass
    
class Liste():
    def __init__(self):
        pass
        
    def new_liste(self, start_path):
        
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
        return liste_des_videos
                
        
            
builder = Gtk.Builder()     
builder.add_from_file("encodage_01.glade")
window = builder.get_object("window1")
window.connect("delete-event", Gtk.main_quit)

gui = Gui()
merge = Merge("/mnt/SSD_TEMP")
liste = Liste()
merge.merger(liste.new_liste("/mnt/cartes_IN_2/3474_1/cartes"))



window.show_all()

Gtk.main()        