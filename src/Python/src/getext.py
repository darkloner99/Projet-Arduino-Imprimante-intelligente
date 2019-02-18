import os

# Simple read line fonction
# Return a single line of an entire file

def read_file(filename):
    text =""
    if(os.path.exists(filename)):

        if(os.path.isfile(filename)):

            file = open(filename,'r')
            for line in file :
                text +=line

            return text

    return None 