# -*- coding: utf-8 -*-

import os, os.path, sys
import subprocess
import time
from gi.repository import Gtk




class Merge():
    
    def __init__(self, liste_root):
        self.liste_root = liste_root
        
    def merger(self, liste_transmise):
        offset = 0
        for l in sorted(liste_transmise.keys()):
            if l.split(".")[0].split("_")[-1] == "01" :
                offset = 0
                self.outpath = "/".join((self.liste_root, "%s_complet.MP4" % "_".join(l.split("_")[:-1])))
            else :
                m1 = subprocess.Popen("dd if='%s' of='%s' seek=%d" % (liste_transmise[l], self.outpath, offset), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)             
                while m1.poll() == None:
                    time.sleep(0.1)
                reste_div = os.stat(self.outpath).st_size % 512
                if reste_div != 0:
                    offset = (os.stat(self.outpath).st_size / 512) + 1
                else :
                    offset = os.stat(self.outpath).st_size / 512
                print(offset)


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
                if f.split(".")[-1].upper() in ["MP4",] :
                    fp = os.path.join(dirpath, f)
   
                    ### correct pour MP4/XML/HDV_1080p/MPEG2/1440x1080/25Mbs/PCM_s16be (Morel) 991_1
                    print f
                    print fp
                    liste_des_videos[f] = fp
        return liste_des_videos
                
        
            
builder = Gtk.Builder()     
builder.add_from_file("/home/autor/Desktop/auto-ring/CHECK_2014/encodage/encodage_01.glade")
window = builder.get_object("window1")
window.connect("delete-event", Gtk.main_quit)

gui = Gui()
merge = Merge("/mnt/isos_archives/debut_2014/temp/1000-2000/1052")
liste = Liste()
merge.merger(liste.new_liste("/mnt/isos_archives/debut_2014/temp/1000-2000/1052"))



window.show_all()

Gtk.main()        
        

def main():
	
	
    return 0

if __name__ == '__main__':
	main()

