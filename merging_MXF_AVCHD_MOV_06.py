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
        self.out = "/mnt/rushs_OUT_2"
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
            
            mt = subprocess.Popen("ffmpeg -y -i '%s' -aspect 16:9 -vf 'yadif=0:0:0' -an -vcodec mpeg2video -q:v 0 %s" % (liste_transmise[l], self_m2t_temp1), shell=True)#, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)           
            while mt.poll() == None:
                time.sleep(0.1)
                
            if self.changement :
                
                offset = 0
                self.outpath = "/".join((self.temp, "%s_complet.m2t" % l[:-4]))
                self.outpath_a0 = "/".join((self.out, "%s_00_complet.wav" % l[:-4]))
                self.outpath_a1 = "/".join((self.out, "%s_01_complet.wav" % l[:-4]))
                self.outpath_a2 = "/".join((self.out, "%s_02_complet.wav" % l[:-4]))
                self.outpath_a3 = "/".join((self.out, "%s_03_complet.wav" % l[:-4]))
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
            
            
            origine_audio = "/".join((liste_transmise[l].split("/")[:-2]))
            
            chemin_audio0 = "/".join((origine_audio, "AUDIO", l.split(".")[0] + "00.MXF"))
            self.temp_a0 = "/".join((self.ram, l.split(".")[0] + "00.WAV"))
            m0 = subprocess.Popen("ffmpeg -y -i '%s' -acodec copy '%s'" % (chemin_audio0, self.temp_a0), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)           
            while m0.poll() == None:
                time.sleep(0.1)
            if os.path.exists(self.outpath_a0) and os.stat(self.outpath_a0).st_size > 0:
                self.increment = True
                self.outpath_a0_temp = self.outpath_a0[:-4] + "_temp.wav"
                shutil.copyfile(self.outpath_a0, self.outpath_a0_temp)
                m1 = subprocess.Popen("sox %s %s %s" % (self.outpath_a0_temp, self.temp_a0, self.outpath_a0), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)      
                while m1.poll() == None:
                    time.sleep(0.1)       
            else :
                shutil.copyfile(self.temp_a0, self.outpath_a0)
                self.increment = False
            
            
            chemin_audio1 = "/".join((origine_audio, "AUDIO", l.split(".")[0] + "01.MXF"))
            self.temp_a1 = "/".join((self.ram, l.split(".")[0] + "01.WAV"))
            m2 = subprocess.Popen("ffmpeg -y -i '%s' -acodec copy '%s'" % (chemin_audio1, self.temp_a1), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)           
            while m2.poll() == None:
                time.sleep(0.1)
            if self.increment:
                self.outpath_a1_temp = self.outpath_a1[:-4] + "_temp.wav"
                shutil.copyfile(self.outpath_a1, self.outpath_a1_temp)
                m3 = subprocess.Popen("sox %s %s %s" % (self.outpath_a1_temp, self.temp_a1, self.outpath_a1), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)      
                while m3.poll() == None:
                    time.sleep(0.1)      
            else :
                shutil.copyfile(self.temp_a1, self.outpath_a1)
            
            
            #try :
                #chemin_audio2 = "/".join((origine_audio, "AUDIO", l.split(".")[0] + "02.MXF"))
                #self.temp_a2 = "/".join((self.ram, l.split(".")[0] + "02.WAV"))
                #m4 = subprocess.Popen("ffmpeg -y -i '%s' -acodec copy '%s'" % (chemin_audio2, self.temp_a2), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)           
                #while m4.poll() == None:
                    #time.sleep(0.1)
                #if self.increment:
                    #self.outpath_a2_temp = self.outpath_a2[:-4] + "_temp.wav"
                    #shutil.copyfile(self.outpath_a2, self.outpath_a2_temp)
                    #m5 = subprocess.Popen("sox %s %s %s" % (self.outpath_a2_temp, self.temp_a2, self.outpath_a2), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)      
                    #while m5.poll() == None:
                        #time.sleep(0.1)
                #else :
                    #shutil.copyfile(self.temp_a2, self.outpath_a2)
                    
                #chemin_audio3 = "/".join((origine_audio, "AUDIO", l.split(".")[0] + "03.MXF"))
                #self.temp_a3 = "/".join((self.ram, l.split(".")[0] + "03.WAV"))
                #m6 = subprocess.Popen("ffmpeg -y -i '%s' -acodec copy '%s'" % (chemin_audio3, self.temp_a3), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)           
                #while m6.poll() == None:
                    #time.sleep(0.1)
                #if self.increment:
                    #self.outpath_a3_temp = self.outpath_a3[:-4] + "_temp.wav"
                    #shutil.copyfile(self.outpath_a3, self.outpath_a3_temp)
                    #m7 = subprocess.Popen("sox %s %s %s" % (self.outpath_a3_temp, self.temp_a3, self.outpath_a3), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)      
                    #while m7.poll() == None:
                        #time.sleep(0.1)       
                #else :
                    #shutil.copyfile(self.temp_a3, self.outpath_a3)
            #except :
                #pass
            
            if self.dernier:
                self.suite(self.outpath, self.outpath_a0, self.outpath_a1, self.precedent)
                self.changement = True
                self.dernier = False
           
                
    def suite(self, chemin_in, a0, a1, nom):
        
        m2 = subprocess.Popen("ffmpeg -y -i '%s' -i '%s' -i '%s' -filter_complex '[1:0][2:0] amerge=inputs=2' -acodec pcm_s16le -b:a 256k -ac 2 -aspect 16:9 -vcodec mpeg2video -q:v 0 '%s/%s.mov'" % (chemin_in, a0, a1, self.out, nom), shell=True, stdout = subprocess.PIPE, bufsize = 1 , universal_newlines = True)            
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
        for dirpath, dirnames, filenames in os.walk("/".join((start_path, "CONTENTS", "VIDEO"))):
            for f in filenames:
                if f.split(".")[-1].upper() == "MXF" :
                    fp = os.path.join(dirpath, f)
                    print(fp)
                    liste_des_videos[f] = fp
        return (liste_des_videos, self.numero, self.sous_chemin, self.racine)
                
merge = Merge("/home/david/temp")
liste = Liste()
merge.merger(liste.new_liste(sys.argv[1]))
