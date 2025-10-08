import os
import random
import shutil

# --- CONFIGURAÇÕES ---
# Pasta com o dataset final aumentado
PASTA_FONTE = 'meu_dataset_final_aumentado_paj'

# Pasta onde o dataset dividido será criado
PASTA_DESTINO = 'dataset_yolo_paj'

# Proporção da divisão (soma deve ser 1.0)
PERCENTUAL_TREINO = 0.8
PERCENTUAL_VALIDACAO = 0.1
PERCENTUAL_TESTE = 0.1
# --- FIM DAS CONFIGURAÇÕES ---

def dividir_dataset():
    print("Iniciando a divisão do dataset...")
    
    # Caminhos para imagens e labels da fonte
    pasta_imagens_fonte = os.path.join(PASTA_FONTE, 'images')
    pasta_labels_fonte = os.path.join(PASTA_FONTE, 'labels')

    # Pega a lista de todos os arquivos de imagem
    imagens = [f for f in os.listdir(pasta_imagens_fonte) if f.endswith(('.jpg', '.jpeg', '.png'))]
    random.shuffle(imagens) # Embaralha a lista para garantir aleatoriedade

    # Calcula os pontos de corte para a divisão
    total_imagens = len(imagens)
    ponto_corte_treino = int(total_imagens * PERCENTUAL_TREINO)
    ponto_corte_validacao = int(total_imagens * (PERCENTUAL_TREINO + PERCENTUAL_VALIDACAO))

    # Divide a lista de arquivos
    imagens_treino = imagens[:ponto_corte_treino]
    imagens_validacao = imagens[ponto_corte_treino:ponto_corte_validacao]
    imagens_teste = imagens[ponto_corte_validacao:]
    
    listas = {
        'train': imagens_treino,
        'val': imagens_validacao,
        'test': imagens_teste
    }
    
    # Cria a estrutura de pastas de destino
    if os.path.exists(PASTA_DESTINO):
        shutil.rmtree(PASTA_DESTINO) # Remove a pasta se já existir para começar do zero
        
    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(PASTA_DESTINO, 'images', split), exist_ok=True)
        os.makedirs(os.path.join(PASTA_DESTINO, 'labels', split), exist_ok=True)

    # Copia os arquivos para as pastas de destino
    for split, lista_imagens in listas.items():
        print(f"Copiando {len(lista_imagens)} arquivos para o conjunto de {split}...")
        for nome_imagem in lista_imagens:
            nome_base, _ = os.path.splitext(nome_imagem)
            nome_label = f"{nome_base}.txt"
            
            # Caminhos de origem
            caminho_imagem_origem = os.path.join(pasta_imagens_fonte, nome_imagem)
            caminho_label_origem = os.path.join(pasta_labels_fonte, nome_label)
            
            # Caminhos de destino
            caminho_imagem_destino = os.path.join(PASTA_DESTINO, 'images', split, nome_imagem)
            caminho_label_destino = os.path.join(PASTA_DESTINO, 'labels', split, nome_label)
            
            # Copia os arquivos
            shutil.copy(caminho_imagem_origem, caminho_imagem_destino)
            if os.path.exists(caminho_label_origem):
                shutil.copy(caminho_label_origem, caminho_label_destino)

    print(f"\nDivisão concluída! Dataset pronto para o YOLO em '{PASTA_DESTINO}'.")

if __name__ == '__main__':
    dividir_dataset()