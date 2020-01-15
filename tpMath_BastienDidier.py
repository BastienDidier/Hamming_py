import copy
import random

def decodeSequenceHammling(sequence,matriceG,l,tabAllEncoded,dicWord):
    tailleword=2**l-1
    tabSquence=[]
    mot = []
#on separe la sequence de hamming en mot de taille 2^l-1
    for number in sequence:
       if tailleword==0:
           tabSquence.append(mot)
           mot=[]
           tailleword=2**l-1
       else:
           mot.append(number)
           tailleword=tailleword-1
#on affiche la sequence decoder mot par mot
    print("Décodage de la sequence (1 mot par ligne)")
    print(sequence)
    for word in tabSquence:
        print(decodeCode(word,tabAllEncoded,dicWord))


#decode un mot selectionnant le mot ayant la difference minimale entre les mots encodés et le mot a decoder
def decodeCode(modifyedcode,tabAllEncoded,dicWord):
    tabDif=[]
    index=0
    for word in tabAllEncoded:
        tabDif.append(diff2Code(modifyedcode,word))
        index=index+1
    return dicWord[tabDif.index((min(tabDif)))]

def diff2Code(code1,code2):
    nbDif=0
    index=0
    for nb in code1:
        if(nb!=code2[index]):
            nbDif+=1
        index+=1
    return nbDif

def encodeAll(tab_all_possible_word,matriceG):
    dic={}
    tabEncoded=[]
    index=0
    for word in tab_possible_word:
        dic[index] = word
        tabEncoded.append(encode([word],matriceG))
        index=index+1
    result=[tabEncoded,dic]
    return  result
#modifie un bit random dans le mot encoder
def bruitage(encodedWord):
    modifyedWord=copy.deepcopy(encodedWord)
    base2 = lambda x:x%2
    nb=random.randint(0,len(encodedWord)-1)
    if modifyedWord[nb]%2 == 0:
        modifyedWord[nb] = 1
    else:
        modifyedWord[nb] = 0
    return modifyedWord


def encode(toEncode,matriceG):
    #matrice multiplication
    resultNonBinary=[[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*matriceG)] for X_row in toEncode]
    resultNonBinary = resultNonBinary[0]
    base2 = lambda x: x%2
    #set the result in base 2
    resultBinary = list(map(base2,resultNonBinary))
    return resultBinary
#genere une matrice identité de taille n
def identity(n):
    m=[[0 for x in range(n)] for y in range(n)]
    for i in range(0,n):
        m[i][i] = 1
    return m

#generate for all n plet in base 2 for an n given
def per(n):
    tabCol=[]
    for i in range(1 << n):
        s=bin(i)[2:]
        s='0'*(n-len(s))+s
        tabCol.append(list(map(int,list(s))))
    return tabCol

#genere la matrice h pour un l donner
def getMatriceH(l):
    tabLines   = []
    tabColones = per(l)
    del tabColones[0]
    toremove = []
    identityMatrix = []
    index = 0
    for col in tabColones:
        if(col.count(1) == 1):
            identityMatrix.append(col)
            toremove.append(index)
        index-=-1
    identityMatrix.reverse()
    index = 0
    for remover in sorted(toremove,reverse=True):
        del tabColones[remover]
    tabColonnesWithoutIdentity = copy.deepcopy(tabColones)
    for col in identityMatrix:
        tabColones.append(col)
    while index<l:
        line=[]
        for col in tabColones:
            line.append(col[index])
        tabLines.append(line)
        index=index+1
    objectReturn=[tabLines,tabColonnesWithoutIdentity,identityMatrix]
    return objectReturn
#genere une matrice G d'apres une matrice H
def getMatriceG(matriceH):
    nbLine=len(matriceH[1])
    matriceG=identity(nbLine)
    index=0
    for col in matriceH[1]:
        matriceG[index] = matriceG[index]+col
        index = index+1
    return  matriceG
#Main programme
saisie = False
while(saisie == False):
    try:
        l = int(input("saisissez la valeur l (entier obligatoire > 0) : "))
        if(l>0):
            saisie = True
        else:
            print("error not positive")
    except ValueError:
        print("error")

print("display matrice H")
obj_return = getMatriceH(l)
print(obj_return[0])
matriceH=obj_return[0]
matriceG=getMatriceG(obj_return)
print("display matrice G")
print(matriceG)
toEncode=[[1,0,1,1]]
encodedWord=encode(toEncode,matriceG)
modifyedWord=bruitage(encodedWord)
taille_word=2**l-l-1
tab_possible_word=per(taille_word)
dicAllEncoded=encodeAll(tab_possible_word,matriceG)
print("encoded word for 1;0;1;1")
print(encodedWord)
print("after bruitage")
print(modifyedWord)
print("decoded code after alteration")
print(decodeCode(modifyedWord,dicAllEncoded[0],dicAllEncoded[1]))


sequenceHammling=[0, 0, 0, 0, 0, 0, 0,0, 0, 0, 1, 1, 1, 1,0, 0, 1, 0, 1, 1, 0,0, 0, 1, 1, 0, 0, 1]
decodeSequenceHammling(sequenceHammling,matriceG,l,dicAllEncoded[0],dicAllEncoded[1])
