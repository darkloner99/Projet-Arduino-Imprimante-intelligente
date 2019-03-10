'''
Created on 6 janv. 2019

@author: @antoi
'''

# Quelques variables utilsés par page, word et line
# Attention !!!!
# Ces chemins sont périmés et n'existent pas dans le git 
#----------------------------------------------------------------------------------------------#

OUTPUT_PATH = '../data/output'

characters = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L',
                'M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h',
                'i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','autres']

# Le dossier de trie doit etre au même endroit que votre scrit l'utilisant
INPUT_PATH = {
    0:'trie\\0',1:'trie\\1',2:'trie\\2',3:'trie\\3',4:'trie\\4',5:'trie\\5',6:'trie\\6',7:'trie\\7',8:'trie\\8',9:'trie\\9',10:'trie\\A',11:'trie\\B',12:'trie\\C',13:'trie\\D',14:'trie\\E',15:'trie\\F',
    16:'trie\\G',17:'trie\\H',18:'trie\\I',19:'trie\\J',20:'trie\\K',21:'trie\\L',22:'trie\\M',23:'trie\\N',24:'trie\\O',25:'trie\\P',26:'trie\\Q',27:'trie\\R',28:'trie\\S',29:'trie\\T',30:'trie\\U',
    31:'trie\\V',32:'trie\\W',33:'trie\\X',34:'trie\\Y',35:'trie\\Z',36:'trie\\z--a',37:'trie\\z--b',38:'trie\\z--c',39:'trie\\z--d',40:'trie\\z--e',41:'trie\\z--f',42:'trie\\z--g',43:'trie\\z--h',44:'trie\\z--i',45:'trie\\z--j',
    46:'trie\\z--k',47:'trie\\z--l',48:'trie\\z--m',49:'trie\\z--n',50:'trie\\z--o',51:'trie\\z--p',52:'trie\\z--q',53:'trie\\z--r',54:'trie\\z--s',55:'trie\\z--t',56:'trie\\z--u',57:'trie\\z--v',58:'trie\\z--w',59:'trie\\z--x',60:'trie\\z--y',61:'trie\\z--z',
    62:'trie\\autres',
}


#----------------------------------------------------------------------------------------------#

#Chemin pointant vers les characteres isolés(exemple ceux dans trie) 
characters1 = "../data/charac"
#Chemin pointant vers les mots triés par charactères-extrator.py et validé par un humain !
characters2 = "../data/combinaisons"
default_space = 100
max_line_lenght = 35
line_number = 25


#----------------------------------------------------------------------------------------------#


    