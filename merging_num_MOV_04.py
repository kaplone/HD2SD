# -*- coding: utf-8 -*-

import os, os.path, sys
import subprocess
import time

class Liste():
    def __init__(self, start_path):
        self.start_path = start_path
        print(start_path)
        
    def new_liste(self):

        for dirpath, dirnames, filenames in os.walk(self.start_path):
            for f in filenames:
                if f.split(".")[-1].upper() == "MOV" :
                    print(f)
                    fp = os.path.join(dirpath, f)
                    nom = f.split(".")[0]
                    index = 1
                    while os.path.exists("/mnt/rushs_OUT_2/778/%s.m2t" % nom) :
                        nom += "_1"
   
                    ### correct pour MTS/HDV_1080i/MPEG2/1440x1080/25Mbs/PCM_s16be (lopacki) 748_doublon
                    
                    m2 = subprocess.Popen("ffmpeg -i '%s'  -vf 'yadif=0:0:0' -acodec ac3 -b:a 384k -vcodec mpeg2video -q:v 0 '/mnt/rushs_OUT_2/778/%s.m2t'" % (fp, nom), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)            
                    while m2.poll() == None:
                        time.sleep(0.1)
  
        
     

liste = Liste("/mnt/cartes_IN_2/500-1000/778/doublon/")
liste.new_liste()
