import moduloDeteccao
from flask import Flask, make_response, jsonify, request
import base64
import cv2
import os
import tempfile
from flask_cors import CORS

os.environ['LD_LIBRARY_PATH'] = '/usr/lib/x86_64-linux-gnu'

app = Flask(__name__)
CORS(app)

key = "vek8yTvUfktFkf0Ibdp2"
projeto = "cultura-pepino"
versaoModelo = 4

@app.route("/")
def homepage():
    return("Olá, aqui é o assistente virtual da Motusbots.")

@app.route("/wakeup", methods = ['POST'])
def wakeup():
    if request.method == 'POST':
        return jsonify({'status': 'success'})

@app.route("/get_sick_area", methods = ['POST', 'GET'])
def getSickArea():
    
    if request.method == 'POST':
    
        imagemTexto = request.get_json()
        imagem_decodificada = base64.b64decode(imagemTexto['img'])
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            temp_file.write(imagem_decodificada)
            temp_file_path = temp_file.name
            
        porcentagemAfetada = (moduloDeteccao.analisarImagem(temp_file_path, key, projeto, versaoModelo)[1])
        
        # ------------------------------------------------------------------------------------------------
        
        _, imagem_codificada = cv2.imencode('.jpg', (moduloDeteccao.analisarImagem(temp_file_path, key, projeto, versaoModelo)[0]))
        imagem_base64 = base64.b64encode(imagem_codificada).decode('utf-8')
        
        return jsonify({'status': 'success', 'data': {'porcentagem': porcentagemAfetada, 'Imagem_final': imagem_base64}})
    
if __name__ == "__main__":
    app.run()
