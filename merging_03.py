# -*- coding: utf-8 -*-

import os, os.path, sys
import subprocess
import time
from gi.repository import Gtk




class Merge():
    
    def __init__(self, liste_root):
        self.outpath = "/".join((liste_root, "film_%s_complet." % liste_root.split("/")[-1]))
        
    def merger(self, liste_transmise):
        offset = 0
        for l in sorted(liste_transmise.keys()):
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
                if f.split(".")[-1].upper() in ["MTS", "MOV", "MP4", "M2T"] :
                    fp = os.path.join(dirpath, f)
                    
                    ###### trier suivant le type de carte ...
                    
                    ### correct pour M2T/IDX/HDV_1080p/MPEG2/1440x1080/25Mbs/MP2A/TS (bensemhoun) = 5280
                    liste_des_videos["_".join(f.split("_")[2:])] = fp
                    ### correct pour MTS/BDAV/AVC/H264/1920x1080/20Mbs/AC3 (vernier) = 880
                    #liste_des_videos[f] = fp
                    if extension == "":
                        extension = f.split(".")[-1] 
        merge.outpath += extension           
                    
        return sorted(liste_des_videos)
                
        
            
builder = Gtk.Builder()     
builder.add_from_file("/home/autor/Desktop/auto-ring/CHECK_2014/encodage/encodage_01.glade")
window = builder.get_object("window1")
window.connect("delete-event", Gtk.main_quit)

gui = Gui()
merge = Merge("/mnt/isos_archives/debut_2014/temp/100-1000/880")
liste = Liste()
merge.merger(liste.new_liste("/mnt/isos_archives/debut_2014/temp/100-1000/880"))



window.show_all()

Gtk.main()        
        

def main():
	
	
    return 0

if __name__ == '__main__':
	main()

