import json
import os
import shutil
import cv2

# --- CONFIGURAÇÕES ADAPTADAS PARA SEUS ARQUIVOS ---
# Nomes exatos dos arquivos JSON que você enviou
ARQUIVOS_JSON = ['via_project_12Sep2025_8h23m.json'] 

# Pasta onde TODAS as suas imagens originais (Eclipse e Triton) estão
PASTA_IMAGENS_ORIGINAIS = 'pajero' 

# Pasta onde o dataset formatado será salvo (não precisa criar, o script cria)
PASTA_SAIDA_FORMATADA = 'dataset_formatado_yolo_paj' 

# Mapeamento de suas classes para um ID numérico (YOLO precisa de números)
# 0 para Eclipse, 1 para Triton
classes_map = {
    'Eclipse':0,
    'Triton':1,
    'Outlander PHEV': 2,
    'Jimny': 3,
    'Pajero': 4
}
# --- FIM DAS CONFIGURAÇÕES ---

# Cria os diretórios de saída, se não existirem
os.makedirs(PASTA_SAIDA_FORMATADA, exist_ok=True)
os.makedirs(os.path.join(PASTA_SAIDA_FORMATADA, 'images'), exist_ok=True)
os.makedirs(os.path.join(PASTA_SAIDA_FORMATADA, 'labels'), exist_ok=True)

print("Iniciando a conversão do formato VIA JSON para o formato YOLO...")

for arquivo_json in ARQUIVOS_JSON:
    if not os.path.exists(arquivo_json):
        print(f"AVISO: Arquivo '{arquivo_json}' não foi encontrado. Verifique o nome e o local.")
        continue

    with open(arquivo_json) as f:
        dados = json.load(f)

    anotacoes = dados.get('_via_img_metadata', {})

    for key, value in anotacoes.items():
        nome_arquivo = value.get('filename')
        regioes = value.get('regions', [])
        
        if not regioes or not nome_arquivo:
            continue

        caminho_original = os.path.join(PASTA_IMAGENS_ORIGINAIS, nome_arquivo)
        
        if not os.path.exists(caminho_original):
            print(f"  - Aviso: Imagem '{nome_arquivo}' não encontrada na pasta '{PASTA_IMAGENS_ORIGINAIS}'. Pulando anotação.")
            continue

        # Copia a imagem original para a nova pasta 'images'
        shutil.copy(caminho_original, os.path.join(PASTA_SAIDA_FORMATADA, 'images', nome_arquivo))
        
        # Lê as dimensões da imagem para normalizar as coordenadas
        img = cv2.imread(caminho_original)
        if img is None:
            print(f"  - Aviso: Não foi possível ler a imagem '{nome_arquivo}'.")
            continue
        altura_img, largura_img, _ = img.shape

        # Cria o arquivo de anotação correspondente
        nome_base, _ = os.path.splitext(nome_arquivo)
        caminho_label = os.path.join(PASTA_SAIDA_FORMATADA, 'labels', f'{nome_base}.txt')
        
        with open(caminho_label, 'w') as f_label:
            for regiao in regioes:
                # O nome do atributo que você criou no VIA foi "Modelo_Carro"
                nome_classe = regiao.get('region_attributes', {}).get('Modelo_Carro', '') 
                
                if not nome_classe:
                    print(f"  - Aviso: Região em '{nome_arquivo}' sem o atributo 'Modelo_Carro'. Pulando.")
                    continue
                
                id_classe = classes_map.get(nome_classe)
                if id_classe is None:
                    print(f"  - Aviso: Classe '{nome_classe}' não definida no 'classes_map'. Pulando.")
                    continue
                
                shape = regiao.get('shape_attributes', {})
                if shape.get('name') == 'rect':
                    x, y = shape.get('x', 0), shape.get('y', 0)
                    largura, altura = shape.get('width', 0), shape.get('height', 0)
                    
                    # Converte para o formato YOLO (centro_x, centro_y, largura, altura) normalizado
                    x_centro = (x + largura / 2) / largura_img
                    y_centro = (y + altura / 2) / altura_img
                    largura_norm = largura / largura_img
                    altura_norm = altura / altura_img
                    
                    f_label.write(f'{id_classe} {x_centro:.6f} {y_centro:.6f} {largura_norm:.6f} {altura_norm:.6f}\n')

print("\nConversão concluída!")
print(f"Seu novo dataset está pronto em '{PASTA_SAIDA_FORMATADA}' com as subpastas 'images' e 'labels'.")