'''
Created on 30 dec. 2018

'''

import os
import argparse


parser = argparse.ArgumentParser(description="Generate some text...")
parser.add_argument('--file',dest="input_file",type=str,help="input file to generate",default=None) # soit l'un soit l'autre
parser.add_argument('--text',dest="input_text",type=str,help="input text to generate",default=None)
args = parser.parse_args()




