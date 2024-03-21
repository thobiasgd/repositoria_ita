from roboflow import Roboflow
import cv2
import numpy as np
from copy import copy

def analisarImagem(img, key, projeto, versaoModelo):    

    rf = Roboflow(api_key=key)
    project = rf.workspace().project(projeto)
    model = project.version(versaoModelo).model

    # -------------------------------------------------------------------

    imagem = cv2.imread(img) #cv2.imread(imagemOriginal) 
    imagemOriginal = copy(imagem)
    dim = (640,480)

    resized = cv2.resize(imagem, dim)
    cv2.imwrite('redimensionada.jpg', resized)

    imagemCV2 = 'redimensionada.jpg'

    model.predict(imagemCV2, confidence=10).save("resultadoRoboflow.jpg")

    # -------------------------------------------------------------------

    img = cv2.imread('resultadoRoboflow.jpg')
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (105, 25, 25), (130, 255,255))
    imask = mask>0
    blue = np.zeros_like(img, np.uint8)
    blue[imask] = img[imask]

    # -------------------------------------------------------------------

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(mask, contours, -1, color=(255, 255, 255), thickness=cv2.FILLED)
    area_threshold = 1000
    filtredContours = [contour for contour in contours if cv2.contourArea(contour) <= area_threshold]
    cv2.drawContours(mask, filtredContours, -1, color=(0, 0, 255), thickness=cv2.FILLED)

    # -------------------------------------------------------------------

    contoursMask, hierarchyMask = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    img = imagemOriginal #cv2.imread(imagemOriginal)
    dimension = (640, 480)
    img = cv2.resize(img, dimension)
    cv2.drawContours(img, contoursMask, -1, color=(0, 0, 255), thickness = 4)

    # -------------------------------------------------------------------

    maskedAreaInteresse = cv2.bitwise_and(img, img, mask=mask)
    cv2.imwrite('mascaraFiltrada.jpg', maskedAreaInteresse)################################
    hsvMasked = cv2.cvtColor(maskedAreaInteresse, cv2.COLOR_BGR2HSV)
    maskYellow = cv2.inRange(hsvMasked, (5, 25, 25), (30, 255,255))
    imaskYellow = maskYellow>0
    yellow = np.zeros_like(img, np.uint8)
    yellow[imaskYellow] = img[imaskYellow]

    # -------------------------------------------------------------------

    contoursSick, _ = cv2.findContours(maskYellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(yellow, contoursSick, -1, color=(0, 0, 255), thickness = cv2.FILLED)
    areaDoente = 0
    for contourSick in contoursSick:
        areaDoente += (cv2.contourArea(contourSick))
        x, y, largura, altura = cv2.boundingRect(contourSick)
        imagem_com_retangulo = cv2.rectangle(img, (x, y), (x + largura, y + altura), (255,0,0), 2)
    #print(f'Área Doente: {areaDoente}')
    areaTotal = 0
    for contour in contours:
        areaTotal += (cv2.contourArea(contour))
    #print(f'Área Total: {areaTotal}')    

    # -------------------------------------------------------------------
    cv2.rectangle(img, (0, 0), (185, 30), (255,0,0), -1)
    cv2.rectangle(img, (0, 0), (186, 31), (100,100,100), 2)
    texto = f'Area Afetada: {round((areaDoente/areaTotal)*100, 2)}%'
    fonte = cv2.FONT_HERSHEY_SIMPLEX
    posicaoLetras = (5, 20)  # Coordenadas (x, y) onde o texto será colocado
    tamanho_fonte = 0.5
    espessura_linha = 1
    corLetras = (0, 255, 255)  # Vermelho no formato BGR
    imagem_com_texto = cv2.putText(img, texto, posicaoLetras, fonte, tamanho_fonte, corLetras, espessura_linha)
    cv2.imwrite('produtoFinal.jpg', imagem_com_texto)


    cv2.imwrite('redimensionadaVerde.png', cv2.resize(imagem_com_texto, (320, 200)))

    return([imagem_com_texto,round((areaDoente/areaTotal)*100, 2)])

# -------------------------------------------------------------------


