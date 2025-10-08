# deteccao_camera.py

import cv2
from ultralytics import YOLO

# --- CONFIGURAÇÕES ---
# Carrega o modelo treinado que está na mesma pasta do script
model = YOLO('best (1).pt')

# Inicia a captura de vídeo da webcam. 
# O número 0 geralmente se refere à webcam padrão.
# Se tiver mais de uma, pode ser 1, 2, etc.
# Para usar um arquivo de vídeo, coloque o caminho: cv2.VideoCapture("caminho/para/video.mp4")
cap = cv2.VideoCapture(0) 

# Verifica se a câmera foi aberta com sucesso
if not cap.isOpened():
    print("Erro: Não foi possível abrir a câmera.")
    exit()

# --- LOOP PRINCIPAL ---
while True:
    # Captura um frame da câmera
    # success é um booleano (True/False) se a captura foi bem-sucedida
    # frame é a imagem (array NumPy) capturada
    success, frame = cap.read()

    # Se a captura não foi bem-sucedida (ex: câmera desconectada), encerra o loop
    if not success:
        print("Fim do stream de vídeo ou erro de captura.")
        break

    # Executa a predição do YOLOv8 no frame capturado
    # stream=True é mais eficiente para processamento de vídeo
    results = model(frame, stream=True)

    # Itera sobre os resultados da detecção
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Converte as coordenadas da caixa para inteiros
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Pega a confiança e a classe da detecção
            conf = box.conf[0]
            cls = int(box.cls[0])
            nome_classe = model.names[cls]

            # Define a cor do retângulo (em BGR - Azul, Verde, Vermelho)
            cor = (255, 0, 255) # Magenta

            # Desenha o retângulo ao redor do objeto detectado
            cv2.rectangle(frame, (x1, y1), (x2, y2), cor, 2)

            # Cria o texto do rótulo (ex: "Triton 0.85")
            rotulo = f'{nome_classe} {conf:.2f}'

            # Coloca o rótulo acima da caixa
            cv2.putText(frame, rotulo, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor, 2)
            
    # Mostra o frame com as detecções em uma janela
    cv2.imshow("Deteccao em Tempo Real - Pressione 'q' para sair", frame)

    # Verifica se a tecla 'q' foi pressionada para sair do loop
    # cv2.waitKey(1) espera por 1 milissegundo por uma tecla
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- LIMPEZA ---
# Libera o objeto de captura da câmera
cap.release()
# Fecha todas as janelas abertas pelo OpenCV
cv2.destroyAllWindows()

print("Aplicação encerrada.")