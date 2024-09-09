# -------------------------------------- Importando bibliotecas -----------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.interpolate import interp2d
from statistics import mean

# -------------------------------------- Funções -----------------------------------------------------------------------------------------

def getMean(path,a):
    
    with open(path + a, 'r') as arquivo:
        arquivo = arquivo.read()
        #print(arquivo)
    
        referencia1 = arquivo.index('Média:') + 6
        referencia2 = referencia1 + 6
        
        return((float(arquivo[referencia1:referencia2].replace(",","."))))
    
def getMax(path,a):
    
    with open(path + a, 'r') as arquivo:
        arquivo = arquivo.read()
        #print(arquivo)
    
        referencia1 = arquivo.index('Max:') + 4
        referencia2 = referencia1 + 5
        
        return((float(arquivo[referencia1:referencia2].replace(",","."))))

def reorganize(string):
    number = ''
    for rorg in string[1:string.index('H')]:
        if (rorg.isdigit()):
            number += rorg
    return(int(number))

def excluirPonto(file,P,Pvalue,H):
    for i in range(10):
        for j in file:
            if j[:j.index('_')] == '{}{}H{}'.format(P,Pvalue,H):
                file.pop(file.index(j))
                
# -------------------------------------- Texto de menu -----------------------------------------------------------------------------------------

print( ' ------------------------------ Instruções para plotagem de dados --------------------------------')

triggerMediaMaximo = input('Valores médios(med) ou máximos(max): ').upper()
while((triggerMediaMaximo != ('MED')) and (triggerMediaMaximo != ('MAX'))):
    print('')
    print('Codificaçao não reconehcida, por favor digitar "med" ou "max"')
    triggerMediaMaximo = input('Valores médios(med) ou máximos(max): ').upper()
    
triggerDbaDbc = input('Escolha a ponderação DbA(A) ou DbC(C): ').upper()
while(triggerDbaDbc != ('A')) and (triggerDbaDbc != ('C')):
    print('')
    print('Codificaçao não reconehcida, por favor digitar "A" para DbA, ou "C" para DbC')
    triggerDbaDbc = input('Escolha a ponderação DbA(A) ou DbC(A): ').upper()
 
print('\n ---------------------------------- Codificação para os locais ----------------------------------')  
print('\n As medições foram realizadas nos seguintes locais: \n \n -> Motor Lateral(ML)                       -> Motor Fio(MF)                           -> Torno(T)')
print('\n -> Exaustor(E)                             -> Ventilador(V)                           -> Depósito(D)')
print('\n -> Pátio(P)                                -> Compressor(C)                           -> Rua(R)')
print('\n -> Torre de Resfriamento A(TRA)            -> Torre de Resfriamento B(TRB)            -> Usinagem(U)') 
triggerLocal = input('Escolha o local da medição: ').upper()

while(triggerLocal != ('ML')) and (triggerDbaDbc != ('MF')) and (triggerLocal != ('E')) and (triggerLocal != ('V')) and (triggerLocal != ('D')) and (triggerLocal != ('P')) and (triggerLocal != ('C')) and (triggerLocal != ('R')) and (triggerLocal != ('TRA')) and (triggerLocal != ('TRB')) and (triggerLocal != ('U')) and (triggerLocal != ('I')):
    print('')
    print('Insira uma codificação válida referente aos locais da fábrica')
    triggerLocal = input('Escolha o local da medição: ').upper()
    
if (triggerLocal == 'P'):
    triggerPatio = input('Patio Frontal(F) ou Traseiro(T): ').upper()
    while(triggerPatio != 'F') and (triggerPatio != 'T'):
        print('Escolha um sub local válido')
        triggerPatio = input('Patio Interno(I) ou externo(E): ').upper()
  
if triggerLocal == 'R':
    triggerRua = input('Rua Frontal(F) ou Lateral(L): ').upper()
    while(triggerRua != 'F') and (triggerRua != 'L'):
        print('Escolha um sub local válido')
        triggerRua = input('Rua Frontal(F) ou Lateral(L): ').upper()
    
triggerPeriodo = input('Informe o período, Dia(D) ou Noite(N): ').upper()
while (triggerPeriodo != 'D') and (triggerPeriodo != 'N'):
    print('Insira um período válido da medição')
    triggerPeriodo = input('Informe o período, Dia(D) ou Noite(N): ').upper()

# -------------------------------------- Criando Listas -----------------------------------------------------------------------------------------

path = "C:/Users/thobi/Desktop/Arquivos fundição/Valores Python 3/{}/{}/".format(triggerPeriodo,triggerLocal)

# Criando listas Rua

if triggerLocal == 'R':
    
    filesR = []
    
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path,i)) and ('R' in i) and not ('TR' in i):
            filesR.append(i)
            
    filesR_DbA = []
    filesR_DbC = []
    
    for j in filesR:
        if j[-5] == 'A':
            filesR_DbA.append(j)
        elif j[-5] == 'C':
            filesR_DbC.append(j)
        else:
            raise ValueError("(R) Erro ao separar DbA e DbC")

#########################################################################################
# Criando listas Motor Frio

elif triggerLocal == 'MF':
    
    filesMF = []
    
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path,i)) and ('MF' in i):
            filesMF.append(i)   
            
    filesMF_DbA = []
    filesMF_DbC = []

    for j in filesMF:
        if j[-5] == 'A':
            filesMF_DbA.append(j)
        elif j[-5] == 'C':
            filesMF_DbC.append(j)
        else:
            raise ValueError("(MF) Erro ao separar DbA e DbC")
    
#########################################################################################
# Criando listas Motor Lateral

elif triggerLocal == 'ML':
    
    filesML = []
    
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path,i)) and ('ML' in i):
            filesML.append(i)
            
    filesML_DbA = []
    filesML_DbC = []
    
    for j in filesML:
        if j[-5] == 'A':
            filesML_DbA.append(j)
        elif j[-5] == 'C':
            filesML_DbC.append(j)
        else:
            raise ValueError("(ML) Erro ao separar DbA e DbC")

#########################################################################################
# Criando listas Exaustor

elif triggerLocal == 'E':
    
    filesE = []
    
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path,i)) and ('E' in i):
            filesE.append(i)
            
    filesE_DbA = []
    filesE_DbC = []
    
    for j in filesE:
        if j[-5] == 'A':
            filesE_DbA.append(j)
        elif j[-5] == 'C':
            filesE_DbC.append(j)
        else:
            raise ValueError("(E) Erro ao separar DbA e DbC")
            
#########################################################################################
# Criando listas Torre de resfriamento B

elif triggerLocal == 'TRB':
    
    filesTRB = []
    
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path,i)) and ('TRB' in i):
            filesTRB.append(i)
            
    filesTRB_DbA = []
    filesTRB_DbC = []
    
    for j in filesTRB:
        if j[-5] == 'A':
            filesTRB_DbA.append(j)
        elif j[-5] == 'C':
            filesTRB_DbC.append(j)
        else:
            raise ValueError("(TRB) Erro ao separar DbA e DbC")
            
#########################################################################################
# Criando listas Torre de resfriamento A

elif triggerLocal == 'TRA':
    
    filesTRA = []
    
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path,i)) and ('TRA' in i):
            filesTRA.append(i)
            
    filesTRA_DbA = []
    filesTRA_DbC = []
    
    for j in filesTRA:
        if j[-5] == 'A':
            filesTRA_DbA.append(j)
        elif j[-5] == 'C':
            filesTRA_DbC.append(j)
        else:
            raise ValueError("(TRA) Erro ao separar DbA e DbC")
            
    for i in range(5): ###### RETIRANDO PONTOS PARA A MALHA FINA!!!! ######
        for j in globals()['filesTRA_Db{}'.format(triggerDbaDbc)]:
            if j.find('H6.5') == -1:
                globals()['filesTRA_Db{}'.format(triggerDbaDbc)].remove(j)
    
#########################################################################################
# Criando listas Pátio

elif triggerLocal == 'P':
    
    filesP = []
    
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path,i)) and ('P' in i):
            filesP.append(i)
             
    excluirPonto(filesP,'P',30,1.5) # EXCLUINDO PONTOS
    
    filesP_DbA = []
    filesP_DbC = []
    
    for j in filesP:
        if j[-5] == 'A':
            filesP_DbA.append(j)
        elif j[-5] == 'C':
            filesP_DbC.append(j)
        else:
            raise ValueError("(P) Erro ao separar DbA e DbC")
            
    for i in range(5): ###### RETIRANDO PONTOS PARA A MALHA FINA!!!! ######
        for j in globals()['filesP_Db{}'.format(triggerDbaDbc)]:
            if j.find('H1.5') == -1:
                globals()['filesP_Db{}'.format(triggerDbaDbc)].remove(j)
                
#########################################################################################
# Criando listas Pátio

elif triggerLocal == 'C':
    
    filesC = []
    
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path,i)) and ('C' in i):
            filesC.append(i)
            
    filesC_DbA = []
    filesC_DbC = []
    
    for j in filesC:
        if j[-5] == 'A':
            filesC_DbA.append(j)
        elif j[-5] == 'C':
            filesC_DbC.append(j)
        else:
            raise ValueError("(C) Erro ao separar DbA e DbC")
            
    # for i in range(5): ###### RETIRANDO PONTOS PARA A MALHA FINA!!!! ######
    #     for j in globals()['filesC_Db{}'.format(triggerDbaDbc)]:
    #         if j.find('H1.5') == -1:
    #             globals()['filesC_Db{}'.format(triggerDbaDbc)].remove(j)

#########################################################################################
# Criando listas Ventilador

elif triggerLocal == 'V':
    
    filesV = []
    
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path,i)) and ('V' in i):
            filesV.append(i)
            
    filesV_DbA = []
    filesV_DbC = []
    
    for j in filesV:
        if j[-5] == 'A':
            filesV_DbA.append(j)
        elif j[-5] == 'C':
            filesV_DbC.append(j)
        else:
            raise ValueError("(V) Erro ao separar DbA e DbC")   

#########################################################################################
# Criando listas Interno

elif triggerLocal == 'I':
    
    filesI = []
    
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path,i)) and ('I' in i):
            filesI.append(i)
            
    excluirPonto(filesI,'I',31,1.5) # EXCLUINDO PONTOS
    
    filesI_DbA = []
    filesI_DbC = []
    
    for j in filesI:
        if j[-5] == 'A':
            filesI_DbA.append(j)
        elif j[-5] == 'C':
            filesI_DbC.append(j)
        else:
            raise ValueError("(I) Erro ao separar DbA e DbC") 
    
#########################################################################################
# Criando listas Depósito

elif triggerLocal == 'D':
    
    filesD = []
    
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path,i)) and ('D' in i):
            filesD.append(i)
    
    filesD_DbA = []
    filesD_DbC = []
    
    for j in filesD:
        if j[-5] == 'A':
            filesD_DbA.append(j)
        elif j[-5] == 'C':
            filesD_DbC.append(j)
        else:
            raise ValueError("(D) Erro ao separar DbA e DbC") 
    
#########################################################################################
# Criando listas Usinagem

elif triggerLocal == 'U':
    
    filesU = []
    
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path,i)) and ('U' in i):
            filesU.append(i)

    filesU_DbA = []
    filesU_DbC = []
    
    for j in filesU:
        if j[-5] == 'A':
            filesU_DbA.append(j)
        elif j[-5] == 'C':
            filesU_DbC.append(j)
        else:
            raise ValueError("(U) Erro ao separar DbA e DbC")
    
# -------------------------------------------- Organizando ordem das listas ---------------------------------------------------------------

if (triggerMediaMaximo == 'MED'):
    globals()['medias_{}_Db{}'.format(triggerLocal,triggerDbaDbc)] = []
    
if (triggerMediaMaximo == 'MAX'):
    globals()['maximos_{}_Db{}'.format(triggerLocal,triggerDbaDbc)] = []

for i in ['A','C']:
    globals()['files{}_Db{}'.format(triggerLocal,i)].sort(key = reorganize)
 
# -------------------------------------------- Manejando itens duplicados ---------------------------------------------------------------

file = globals()['files{}_Db{}'.format(triggerLocal,triggerDbaDbc)]
fileSemRepeticoes = {}
for i in range (3):
    if (triggerMediaMaximo == 'MED'):
        for i in file:
            nomeAtual = i[:i.index('_')]
            
            horarioAtual = i[i.index('')+6:i.index('')+10]
            
            mediaAtual = getMean(path, i)
            
            if nomeAtual not in fileSemRepeticoes:
                fileSemRepeticoes[nomeAtual] = mediaAtual
            else:
                fileSemRepeticoes[nomeAtual] = (mediaAtual + fileSemRepeticoes[nomeAtual])/2     
                
    if (triggerMediaMaximo == 'MAX'):
        
        for i in file:
            
            nomeAtual = i[:i.index('_')]
            
            horarioAtual = i[i.index('')+6:i.index('')+10]
            
            maximoAtual = getMax(path, i)
            
            if nomeAtual not in fileSemRepeticoes:
                fileSemRepeticoes[nomeAtual] = maximoAtual
                
            else:
                fileSemRepeticoes[nomeAtual] = (maximoAtual + fileSemRepeticoes[nomeAtual])/2
                
if triggerLocal == 'P':
    if triggerPatio == 'T':
        for i in range(28):
            del fileSemRepeticoes[next(iter(fileSemRepeticoes))]
    
if (triggerMediaMaximo == 'MED'):
    
    for i in fileSemRepeticoes:    
        globals()['medias_{}_Db{}'.format(triggerLocal,triggerDbaDbc)].append(fileSemRepeticoes.get(i))
        
    if (triggerLocal == 'R'):
        if triggerRua == 'F':
            globals()['medias_{}Db{}'.format(triggerLocal,triggerDbaDbc)] = np.roll(globals()['medias{}_Db{}'.format(triggerLocal,triggerDbaDbc)],5*7)
                
    
if (triggerMediaMaximo == 'MAX'):
    
    for i in fileSemRepeticoes:    
        globals()['maximos_{}_Db{}'.format(triggerLocal,triggerDbaDbc)].append(fileSemRepeticoes.get(i))
        
    if (triggerLocal == 'R'):
        if triggerRua == 'F':
            globals()['maximos_{}Db{}'.format(triggerLocal,triggerDbaDbc)] = np.roll(globals()['maximos{}_Db{}'.format(triggerLocal,triggerDbaDbc)],5*7)
        


                         
# ------------------------------------------- valor médio global -----------------------------------------------------------------------------------------------------------------

if triggerMediaMaximo == 'MED':
    medioGlobal = mean(globals()['medias_{}_Db{}'.format(triggerLocal,triggerDbaDbc)])
    maximoGlobal = max(globals()['medias_{}_Db{}'.format(triggerLocal,triggerDbaDbc)])

elif triggerMediaMaximo == 'MAX':
    medioGlobal = mean(globals()['maximos_{}_Db{}'.format(triggerLocal,triggerDbaDbc)])
    maximoGlobal = max(globals()['maximos_{}_Db{}'.format(triggerLocal,triggerDbaDbc)])
    
    
print('Valor máximo global: {}'.format(maximoGlobal) + 'Db{}'.format(triggerDbaDbc))
print('Valor médio global: {}'.format(medioGlobal) + 'Db{}'.format(triggerDbaDbc))
               
# ------------------------------------------- Criando variavel de valor -----------------------------------------------------------------------------------------------------------------

if triggerMediaMaximo == 'MED':
    valores = globals()['medias_{}_Db{}'.format(triggerLocal,triggerDbaDbc)]
    
if triggerMediaMaximo == 'MAX':
    valores = globals()['maximos_{}_Db{}'.format(triggerLocal,triggerDbaDbc)]
    
# ------------------------------------------- Criando mapa sonoro rua frontal -----------------------------------------------------------------------------------------------------------------

if (triggerLocal == 'D'):
    plt.figure(figsize=(20, 10))
    matriz = pd.DataFrame(np.zeros((3, 3)))
    dimensaoX = 3
    dimensaoY = 3
    
elif (triggerLocal == 'R'): 
    plt.figure(figsize=(50, 10))
    
    if triggerRua == 'F':
        matriz = pd.DataFrame(np.zeros((7, 24)))
        dimensaoX = 24
        dimensaoY = 7
    if triggerRua == 'L':
        matriz = pd.DataFrame(np.zeros((7, 24)))
        dimensaoX = 24
        dimensaoY = 7
        
elif (triggerLocal == 'TRB'):
    plt.figure(figsize=(20, 80))
    matriz = pd.DataFrame(np.zeros((9, 2)))
    dimensaoX = 1
    dimensaoY = 9
    
elif (triggerLocal == 'TRA'):
    plt.figure(figsize=(30, 60))
    matriz = pd.DataFrame(np.zeros((6, 3)))
    dimensaoX = 3
    dimensaoY = 6
    
    matriz[0][5] = valores[0]
    matriz[1][5] = valores[1]
    matriz[2][5] = valores[2]
    
    matriz[1][4] = valores[3]
    matriz[2][4] = valores[4]
    
    matriz[0][3] = valores[5]
    
    matriz[0][2] = valores[6]
    matriz[1][2] = valores[7]
    matriz[2][2] = valores[8]
    
    matriz[2][1] = valores[9]
    
    matriz[2][1] = valores[10]
    
    for ix in range(dimensaoX):
        for iy in range(dimensaoY):
            if matriz[ix][iy] == 0:
                matriz[ix][iy] = medioGlobal 
    
            
elif (triggerLocal == 'P'):
    
    if triggerPatio == 'F':
        plt.figure(figsize=(50, 10))
        matriz = pd.DataFrame(np.zeros((3, 15)))
        dimensaoX = 15
        dimensaoY = 3
        
        matriz[0][2] = valores[2]
        matriz[1][2] = valores[5]
        matriz[2][2] = valores[8]
        matriz[3][2] = valores[11]
        matriz[4][2] = valores[14]
        
        matriz[0][1] = valores[1]
        matriz[1][1] = valores[4]
        matriz[2][1] = valores[7]
        matriz[3][1] = valores[10]
        matriz[4][1] = valores[13]
        matriz[5][1] = valores[16]
        matriz[6][1] = valores[18]
        matriz[7][1] = valores[20]
        matriz[8][1] = valores[22]
        
        matriz[0][0] = valores[0]
        matriz[1][0] = valores[3]
        matriz[2][0] = valores[6]
        matriz[3][0] = valores[9]
        matriz[4][0] = valores[12]
        matriz[5][0] = valores[15]
        matriz[6][0] = valores[17]
        matriz[7][0] = valores[19]
        matriz[8][0] = valores[21]
        matriz[10][0] = valores[23]
        matriz[11][0] = valores[24]
        matriz[12][0] = valores[25]
        matriz[13][0] = valores[26]
        matriz[14][0] = valores[27]
        
    elif triggerPatio == 'T':
        plt.figure(figsize=(50, 10))
        matriz = pd.DataFrame(np.zeros((3, 10)))
        dimensaoX = 10
        dimensaoY = 3
        
        matriz[0][2] = valores[10]
        matriz[1][2] = valores[8]
        
        matriz[0][1] = valores[11]
        matriz[1][1] = valores[9]
        matriz[2][1] = valores[7]
        matriz[3][1] = valores[6]
        matriz[4][1] = valores[5]
        matriz[5][1] = valores[4]
        matriz[7][1] = valores[3]
        matriz[8][1] = valores[0]
        
        matriz[8][0] = valores[2]
        matriz[9][0] = medioGlobal
        
    
    for ix in range(dimensaoX):
        for iy in range(dimensaoY):
            if matriz[ix][iy] == 0:
                matriz[ix][iy] = medioGlobal
  
elif (triggerLocal == 'U'):
    plt.figure(figsize=(30, 30))
    matriz = pd.DataFrame(np.zeros((4, 4)))
    dimensaoX = 4
    dimensaoY = 4
    
    matriz[0][3] = valores[2]
    matriz[1][3] = valores[5]
    matriz[2][3] = valores[8]
    matriz[3][3] = valores[10]
    
    
    matriz[0][2] = valores[1]
    matriz[1][2] = valores[4]
    matriz[2][2] = valores[7]
    matriz[3][2] = valores[9]
    
    matriz[0][0] = valores[0]
    matriz[1][0] = valores[3]
    matriz[2][0] = valores[6]
    
    for ix in range(dimensaoX):
        for iy in range(dimensaoY):
            if matriz[ix][iy] == 0:
                matriz[ix][iy] = medioGlobal    
    
elif (triggerLocal == 'I'):
    

    plt.figure(figsize=(50, 70))
    matriz = pd.DataFrame(np.zeros((19, 15)))
    dimensaoX = 15
    dimensaoY = 19
    
    matriz[7][18] = valores[0]
    matriz[12][18] = 87
    matriz[13][18] = 87
    
    matriz[7][17] = valores[1]
    matriz[8][17] = valores[3]
    matriz[9][17] = valores[4]
    matriz[10][17] = valores[23]
    matriz[11][17] = valores[22]
    matriz[12][17] = valores[20]
    matriz[13][17] = valores[21]
    
    matriz[0][16] = valores[60]
    matriz[7][16] = valores[2]
    matriz[12][16] = valores[19]
    matriz[13][16] = valores[74]

    matriz[0][15] = valores[59]
    matriz[1][15] = valores[61]
    matriz[2][15] = valores[62]
    matriz[3][15] = valores[63]
    matriz[7][15] = valores[81]
    matriz[11][15] = valores[24]
    matriz[12][15] = valores[17]
    matriz[13][15] = valores[18]
    
    matriz[0][14] = valores[58]
    matriz[1][14] = valores[82]
    matriz[2][14] = valores[65]
    matriz[3][14] = valores[64]
    matriz[4][14] = valores[69]
    matriz[5][14] = valores[70]
    matriz[7][14] = valores[5]
    matriz[12][14] = valores[16]
    matriz[13][14] = valores[75]
    
    matriz[0][13] = valores[57]
    matriz[1][13] = valores[66]
    matriz[2][13] = valores[67]
    matriz[3][13] = valores[68]
    matriz[4][13] = valores[71]
    matriz[5][13] = valores[72]
    matriz[6][13] = valores[73]
    matriz[7][13] = valores[6]
    matriz[12][13] = valores[15]
    matriz[13][13] = valores[76]
    
    matriz[8][12] = valores[7]
    matriz[12][12] = valores[14]
    matriz[13][12] = valores[77]
    matriz[14][12] = valores[80]
    
    matriz[9][11] = valores[8]
    matriz[12][11] = valores[12]
    matriz[13][11] = valores[13]
    
    matriz[10][10] = valores[9]
    
    matriz[11][9] = valores[10]
    matriz[13][9] = valores[11]
    
    matriz[3][8] = valores[40]
    matriz[4][8] = valores[39]    
    matriz[9][8] = valores[78]
    matriz[10][8] = valores[79]
    matriz[11][8] = valores[31]
    matriz[13][8] = valores[25]
    
    matriz[0][7] = valores[42]
    matriz[3][7] = valores[41]    
    matriz[4][7] = valores[38]
    matriz[5][7] = valores[37]
    matriz[6][7] = valores[36]
    matriz[7][7] = valores[35]
    matriz[8][7] = valores[34]
    matriz[9][7] = valores[33]    
    matriz[10][7] = valores[32]
    matriz[11][7] = valores[30]
    matriz[13][7] = valores[26]
    
    matriz[11][6] = valores[29]
    matriz[13][6] = valores[27]
    
    matriz[1][4] = valores[83]
    matriz[12][4] = valores[28]
    
    matriz[2][3] = valores[43]
    matriz[3][3] = valores[44]
    matriz[4][3] = valores[45]
    matriz[5][3] = valores[46]
    matriz[6][3] = valores[47]
    matriz[7][3] = valores[48]    
    matriz[8][3] = valores[49]
    matriz[9][3] = valores[50]
    matriz[10][3] = valores[51]
    
    matriz[9][1] = valores[52]
    
    matriz[6][0] = valores[56]    
    matriz[7][0] = valores[55]
    matriz[8][0] = valores[54]
    matriz[9][0] = valores[53]
    
    for ix in range(dimensaoX):
        for iy in range(dimensaoY):
            if matriz[ix][iy] == 0:
                matriz[ix][iy] = medioGlobal
                
elif (triggerLocal == 'C'):
    plt.figure(figsize=(50, 25))
    matriz = pd.DataFrame(np.zeros((3, 7)))
    dimensaoX = 7
    dimensaoY = 3
    
    matriz[0][2] = valores[2]
    matriz[3][2] = valores[4]
    matriz[5][2] = valores[9]
    
    matriz[0][1] = valores[1]
    matriz[3][1] = valores[3]
    matriz[5][1] = valores[8]
    
    matriz[0][0] = valores[0]
    matriz[4][0] = valores[5]
    matriz[5][0] = valores[6]
    matriz[6][0] = valores[7]
    
    for ix in range(dimensaoX):
        for iy in range(dimensaoY):
            if matriz[ix][iy] == 0:
                matriz[ix][iy] = medioGlobal
                  
if (triggerLocal == 'R') or (triggerLocal == 'D') or (triggerLocal == 'TRB'):    
    
    point = 0
    if triggerLocal == 'R':
        if triggerRua == 'L':
            point += 133
            
    for x in range(dimensaoX):
        for y in range(dimensaoY):
            if triggerMediaMaximo == 'MED':
                if triggerDbaDbc == 'A':
                    matriz[x][y] = valores[point]
                if triggerDbaDbc == 'C':
                    matriz[x][y] = valores[point]
                point += 1
            elif triggerMediaMaximo == 'MAX':
                if triggerDbaDbc == 'A':
                    matriz[x][y] = valores[point]
                if triggerDbaDbc == 'C':
                    matriz[x][y] = valores[point]
                point += 1    
                
if (triggerLocal == 'TRB'):
    matriz[1][:] = matriz[0][:]

# ------------------------------------------- Reajustando a escala dos mapas -----------------------------------------------------------------------------------------------------------------

if (triggerLocal == 'C'):
    valorAxial = 0
    xAxis = []
    for Y in range(dimensaoX):
        xAxis.append(valorAxial)
        valorAxial += 1
        
    valorAxial = 0
    yAxis = []
    for Y in range(dimensaoY):
        yAxis.append(valorAxial)
        valorAxial += 1.333
        
elif (triggerLocal == 'R'):
    valorAxial = 0.5
    yAxis = []
    for Y in range(dimensaoY):
        yAxis.append(valorAxial)
        valorAxial += 1
        
    xAxis = []
    valorAxial = 0
    for X in range(dimensaoX):
        xAxis.append(valorAxial)
        valorAxial += 5
        
elif (triggerLocal == 'TRB'):
    valorAxial = 0
    yAxis = []
    for Y in range(dimensaoY):
        yAxis.append(valorAxial)
        valorAxial += 1
        
    xAxis = []
    valorAxial = 0
    for X in range(dimensaoX+1):
        xAxis.append(valorAxial)
        valorAxial += 5
        
elif (triggerLocal == 'TRA'):
    valorAxial = 0
    yAxis = []
    for Y in range(dimensaoY):
        yAxis.append(valorAxial)
        valorAxial += 1
        
    xAxis = []
    valorAxial = 0
    for X in range(dimensaoX):
        xAxis.append(valorAxial)
        valorAxial += 2
        
elif (triggerLocal == 'U'):
    valorAxial = 0
    yAxis = []
    for Y in range(dimensaoY):
        yAxis.append(valorAxial)
        valorAxial += 2
        
    xAxis = []
    valorAxial = 0
    for X in range(dimensaoX):
        xAxis.append(valorAxial)
        valorAxial += 2
        
elif (triggerLocal == 'D'):
    valorAxial = 0
    yAxis = []
    for Y in range(dimensaoY):
        yAxis.append(valorAxial)
        valorAxial += 5
        
    xAxis = []
    valorAxial = 0
    for X in range(dimensaoX):
        xAxis.append(valorAxial)
        valorAxial += 10
        
# elif (triggerLocal == 'R') and (triggerRua == 'F'):
#     valorAxial = 0
#     yAxis = []
#     for Y in range(dimensaoY):
#         yAxis.append(valorAxial)
#         valorAxial += 5
        
#     xAxis = []
#     valorAxial = 0
#     for X in range(dimensaoX):
#         xAxis.append(valorAxial)
#         valorAxial += 5
    
        
else:
    valorAxial = 0
    yAxis = []
    for Y in range(dimensaoY):
        yAxis.append(valorAxial)
        valorAxial += 5
        
    xAxis = []
    valorAxial = 0
    for X in range(dimensaoX):
        xAxis.append(valorAxial)
        valorAxial += 5

# ------------------------------------------- Plotando os mapas ----------------------------------------------------------------------------------------------------------------

x_list = np.array(xAxis)
y_list = np.array(yAxis)
z_list = np.array(matriz.values.tolist())
#z_list[:][3] = z_list.min()

df3_smooth = interp2d(x_list, y_list, z_list, kind="linear")
x_coords = np.arange(min(x_list), max(x_list) + 1)
y_coords = np.arange(min(y_list), max(y_list) + 1)
z_i = df3_smooth(x_coords, y_coords)


fig = plt.imshow(
    z_i,
    extent=[min(x_list), max(x_list), min(y_list), max(y_list)],
    origin="lower",
    interpolation='bicubic',
    aspect='auto',
    cmap='jet')

plt.xticks(fontsize=35)
plt.yticks(fontsize=35)
plt.text()
plt.xlabel('Eixo (X)',fontsize=35)
plt.ylabel('Eixo (Y)',fontsize=35)
plt.colorbar(label='Intensidade Sonora dB({})'.format(triggerDbaDbc), location='right')
fig.figure.axes[1].tick_params(axis="both", labelsize=35)

#plt.text(0.5*x_list[0] + 0.1*x_list[1],          0.3*y_list[1], 'Valor máximo: %.2f' % maximoGlobal + 'db', fontsize = max(x_list))
#plt.text(x_list[0] + 0.1*x_list[1],              y_list[1]-0.2*y_list[2], 'Valor médio: %.2f' % medioGlobal + 'db',  fontsize = max(x_list))


if (triggerLocal == 'I') or (triggerLocal == 'U') or (triggerLocal == 'P') or (triggerLocal == 'C') or (triggerLocal == 'TRB') or (triggerLocal == 'TRA'): 
    plt.gca().invert_yaxis()

plt.show()


# ------------------------------------------ Testar filtros ------------------------------------------------------------------------------------------------------------------

# filtros = ['bilinear', 'bicubic', 'spline16', 'spline36', 'hanning', 'hamming', 
#             'hermite', 'kaiser', 'quadric', 'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos', 'blackman']

# for filt in filtros:
#     plt.figure(figsize=(50, 10))
#     fig = plt.imshow(
#         z_i,
#         extent=[min(x_list), max(x_list), min(y_list), max(y_list)],
#         origin="lower",
#         interpolation=filt,
#         aspect='auto',
#         cmap='jet'
#     )
#     plt.xlabel('Comprimento da Rua (m)')
#     plt.ylabel('Altura das Medições (m)')
#     plt.colorbar(label='Intensidade Sonora dB(A)', location='right')
    
#     plt.show()


# ------------------------------------------------------------------------------------------------------------------------------------------------------------
