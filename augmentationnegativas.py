import cv2
import albumentations as A
import os
import shutil

# --- CONFIGURAÇÕES ---
# O nome da sua pasta de entrada, que contém apenas as imagens
PASTA_IMAGENS_ORIGINAIS = 'imagens3'

# O nome da nova pasta onde as imagens aumentadas serão salvas
PASTA_DATASET_AUMENTADO = 'dataset_negativas_aumentado1'

# Altere este número para gerar mais ou menos imagens por original
IMAGENS_POR_ORIGINAL = 10 
# --- FIM DAS CONFIGURAÇÕES ---

# --- Pipeline de Aumento de Dados ---
# Removido o 'bbox_params' pois não há anotações
transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(brightness_limit=0.25, contrast_limit=0.25, p=0.8),
    A.Rotate(limit=20, p=0.5, border_mode=cv2.BORDER_CONSTANT),
    A.Blur(blur_limit=4, p=0.2),
    A.GaussNoise(p=0.2),
    A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.15, rotate_limit=20, p=0.6, border_mode=cv2.BORDER_CONSTANT),
    A.Resize(height=640, width=640) # Redimensiona todas as imagens para um tamanho padrão
])

# --- Lógica Principal ---
# Cria a pasta de destino para as imagens aumentadas
os.makedirs(PASTA_DATASET_AUMENTADO, exist_ok=True)

# Verifica se a pasta de entrada existe
if not os.path.isdir(PASTA_IMAGENS_ORIGINAIS):
    print(f"Erro: A pasta de entrada '{PASTA_IMAGENS_ORIGINAIS}' não foi encontrada.")
    exit()

arquivos_imagem = [f for f in os.listdir(PASTA_IMAGENS_ORIGINAIS) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.jfif'))]
total_imagens = len(arquivos_imagem)

if total_imagens == 0:
    print(f"Nenhuma imagem encontrada na pasta '{PASTA_IMAGENS_ORIGINAIS}'.")
    exit()

print(f"Iniciando augmentation para {total_imagens} imagens...")

for i, nome_imagem in enumerate(arquivos_imagem):
    print(f"Processando imagem {i+1}/{total_imagens}: {nome_imagem}")
    
    caminho_imagem = os.path.join(PASTA_IMAGENS_ORIGINAIS, nome_imagem)
    nome_base, extensao = os.path.splitext(nome_imagem)

    try:
        imagem = cv2.imread(caminho_imagem)
        # Se a imagem não puder ser lida, pula para a próxima
        if imagem is None:
            print(f"  - Aviso: Não foi possível ler a imagem {nome_imagem}. Pulando.")
            continue
        
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    except Exception as e:
        print(f"  - Erro ao carregar a imagem {nome_imagem}: {e}")
        continue

    # Salva uma cópia da imagem original (já redimensionada) no novo dataset
    resized_original = A.Resize(height=640, width=640)(image=imagem)['image']
    cv2.imwrite(os.path.join(PASTA_DATASET_AUMENTADO, nome_imagem), cv2.cvtColor(resized_original, cv2.COLOR_RGB2BGR))
    
    # Gera N novas imagens a partir da original
    for j in range(IMAGENS_POR_ORIGINAL):
        try:
            # Aplica as transformações na imagem
            transformed = transform(image=imagem)
            imagem_transformada = transformed['image']
            
            novo_nome_imagem = f"{nome_base}_aug_{j}{extensao}"

            # Salva a imagem transformada
            caminho_salvar_img = os.path.join(PASTA_DATASET_AUMENTADO, novo_nome_imagem)
            cv2.imwrite(caminho_salvar_img, cv2.cvtColor(imagem_transformada, cv2.COLOR_RGB2BGR))

        except Exception as e:
            print(f"  - Erro ao transformar a imagem {nome_imagem}: {e}")

print(f"\nProcesso de Data Augmentation concluído!")
print(f"Seu novo dataset com aproximadamente {total_imagens * (IMAGENS_POR_ORIGINAL + 1)} imagens está em '{PASTA_DATASET_AUMENTADO}'.")