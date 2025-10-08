import cv2
import albumentations as A
import os
import shutil

# --- CONFIGURAÇÕES ---
PASTA_DATASET_FORMATADO = 'dataset_formatado_yolo_paj'
PASTA_DATASET_AUMENTADO = 'meu_dataset_final_aumentado_paj'
# Altere este número para gerar mais ou menos imagens por original
IMAGENS_POR_ORIGINAL = 20
# --- FIM DAS CONFIGURAÇÕES ---

# --- Pipeline de Aumento de Dados ---
transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(brightness_limit=0.25, contrast_limit=0.25, p=0.8),
    A.Rotate(limit=20, p=0.5, border_mode=cv2.BORDER_CONSTANT),
    A.Blur(blur_limit=4, p=0.2),
    A.GaussNoise(p=0.2),
    A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.15, rotate_limit=20, p=0.6, border_mode=cv2.BORDER_CONSTANT),
    A.Resize(height=640, width=640) # Redimensiona todas as imagens para um tamanho padrão
], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels'], min_visibility=0.2))

# --- Lógica Principal ---
os.makedirs(os.path.join(PASTA_DATASET_AUMENTADO, 'images'), exist_ok=True)
os.makedirs(os.path.join(PASTA_DATASET_AUMENTADO, 'labels'), exist_ok=True)

pasta_imagens_originais = os.path.join(PASTA_DATASET_FORMATADO, 'images')
pasta_labels_originais = os.path.join(PASTA_DATASET_FORMATADO, 'labels')

arquivos_imagem = os.listdir(pasta_imagens_originais)
total_imagens = len(arquivos_imagem)

print(f"Iniciando augmentation para {total_imagens} imagens...")

for i, nome_imagem in enumerate(arquivos_imagem):
    print(f"Processando imagem {i+1}/{total_imagens}: {nome_imagem}")
    
    caminho_imagem = os.path.join(pasta_imagens_originais, nome_imagem)
    nome_base, _ = os.path.splitext(nome_imagem)
    caminho_label = os.path.join(pasta_labels_originais, f'{nome_base}.txt')

    imagem = cv2.imread(caminho_imagem)
    imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)

    bboxes, class_labels = [], []
    if os.path.exists(caminho_label):
        with open(caminho_label, 'r') as f:
            for line in f:
                parts = list(map(float, line.strip().split()))
                class_labels.append(int(parts[0]))
                bboxes.append(parts[1:])
    
    # Salva uma cópia da imagem original (redimensionada) e seu label no novo dataset
    resized_original = A.Resize(height=640, width=640)(image=imagem)
    cv2.imwrite(os.path.join(PASTA_DATASET_AUMENTADO, 'images', nome_imagem), cv2.cvtColor(resized_original['image'], cv2.COLOR_RGB2BGR))
    if os.path.exists(caminho_label):
      shutil.copy(caminho_label, os.path.join(PASTA_DATASET_AUMENTADO, 'labels', f'{nome_base}.txt'))
    
    for j in range(IMAGENS_POR_ORIGINAL):
        try:
            transformed = transform(image=imagem, bboxes=bboxes, class_labels=class_labels)
            
            if not transformed['bboxes']: continue

            novo_nome_imagem = f"{nome_base}_aug_{j}.jpg"
            novo_nome_label = f"{nome_base}_aug_{j}.txt"

            cv2.imwrite(os.path.join(PASTA_DATASET_AUMENTADO, 'images', novo_nome_imagem), cv2.cvtColor(transformed['image'], cv2.COLOR_RGB2BGR))

            with open(os.path.join(PASTA_DATASET_AUMENTADO, 'labels', novo_nome_label), 'w') as f_out:
                for bbox, label in zip(transformed['bboxes'], transformed['class_labels']):
                    f_out.write(f'{label} {" ".join(map(str, bbox))}\n')
        except Exception as e:
            print(f"  - Erro ao transformar {nome_imagem}: {e}")

print(f"\nProcesso de Data Augmentation concluído! Seu dataset com {total_imagens * (IMAGENS_POR_ORIGINAL + 1)} imagens está em '{PASTA_DATASET_AUMENTADO}'.")