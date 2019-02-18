'''
Created on 30 dec. 2018

@author: @antoi
This code transform an input text in image of Raphael's handwritting 
'''

import os
import sys
import argparse
from PIL import Image
import getext
from page import Page


#Get arguments 
parser = argparse.ArgumentParser(description="Generate some text...")
parser.add_argument('--file',dest="input_file",type=str,help="absolute path to input file to generate",default=None) # soit l'un soit l'autre
parser.add_argument('--text',dest="input_text",type=str,help="input text to generate",default=None)
parser.add_argument('--dir',dest="output_folder",type=str,help="absolute path to output folder",required=True)
parser.add_argument('--name',dest="output_name",type=str,help="name of output file (without extension !!!) ",required=True)
parser.print_help()
args = parser.parse_args()


# Si un fichier et donné en argument et qu'il existe.
# On va alors recupérer son contenu et construire la page avec.
if (args.input_file is not None and os.path.exists(args.output_folder)):
    print("\nGenerating text .... please be patient\n")
    text = getext.read_file(args.input_file)
    print(text +"\n\n")
    page =  Page(text)
    print("Text succesfully generated ! Please have a look in your save directories path.\n")
    page.image.save(args.output_folder +"\\"+ args.output_name +".jpg", "jpeg")


# Si un texte est donné en argument.
#On va alors recupérer son contenu et construire la page avec.
elif(args.input_text is not None and os.path.exists(args.output_folder)):
    print("\nGenerating text .... please be patient\n")
    print(text +"\n\n")
    text = args.input_text
    page =  Page(text) 
    print("Text succesfully generated ! Please have a look in your save directories path.\n")
    page.image.save(args.output_folder +"\\"+ args.output_name+".jpg", "jpeg")


else:
    print("Aucune instruction trouvé !!\nFin du programme\n")
    sys.exit(0)





