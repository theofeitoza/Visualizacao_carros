<div id="top"></div>

<div align="center">

# 🚗 Detecção de Veículos com Visão Computacional
*Um modelo de visão computacional, baseado na arquitetura YOLO, treinado para identificar e localizar veículos em imagens.*

<br>

<img alt="last-commit" src="https://img.shields.io/github/last-commit/theofeitoza/Visualizacao_carros?style=flat&logo=git&logoColor=white&color=0080ff">
<img alt="repo-top-language" src="https://img.shields.io/github/languages/top/theofeitoza/Visualizacao_carros?style=flat&color=0080ff">

<p><em>Tecnologias e Frameworks Utilizados:</em></p>
<img alt="Python" src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white">
<img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-EE4C2C.svg?style=flat&logo=PyTorch&logoColor=white">
<img alt="YOLO" src="https://img.shields.io/badge/YOLO-00FFFF.svg?style=flat&logo=yolo&logoColor=black">
<img alt="OpenCV" src="https://img.shields.io/badge/OpenCV-5C3EE8.svg?style=flat&logo=OpenCV&logoColor=white">

</div>

---

## 📜 Índice
- [Visão Geral](#-visão-geral)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Como Usar](#-como-usar)
  - [Pré-requisitos](#pré-requisitos)
  - [Instalação](#instalação)
  - [Executando a Detecção](#executando-a-detecção)
- [Exemplos de Detecção](#-exemplos-de-detecção)

---

## 🚀 Visão Geral
Este repositório contém um projeto completo de detecção de objetos focado na identificação de veículos. Utilizando o framework Ultralytics YOLO e PyTorch, o modelo foi treinado para desenhar caixas delimitadoras (bounding boxes) ao redor de carros em imagens.

O projeto não inclui apenas o modelo treinado (`best.pt`), mas também todos os scripts de apoio utilizados no processo de MLOps, como:

-   Pré-processamento e divisão do dataset.
-   Aumento de dados (Data Augmentation) para melhorar a robustez do modelo.
-   Conversão de formatos de anotação.
-   Script de inferência para testar o modelo em novas imagens.

---

## 🤖 Estrutura do Projeto
O repositório está organizado com os seguintes scripts e arquivos principais:

-   `deteccao.py`: Script principal de inferência. Utiliza o modelo treinado para detectar veículos em uma imagem fornecida.
-   `best.pt` / `last.pt`: Pesos do modelo treinado. O arquivo `best.pt` contém os pesos com o melhor desempenho de validação.
-   `dividir_dataset.py`: Script para separar o conjunto de dados em pastas de treino, validação e teste.
-   `aumentar_dataset.py`: Aplica técnicas de aumento de dados (rotação, zoom, etc.) nas imagens de treino.
-   `augmentationnegativas.py`: Script específico para aumentar o dataset de imagens negativas (sem veículos).
-   `converter_dados.py`: Utilitário para converter anotações de um formato para outro (ex: XML para formato YOLO `.txt`).
-   `*.jpg`: Imagens de teste e exemplos de saídas do treinamento.

---

## 🏁 Como Usar
Siga os passos abaixo para configurar o ambiente e executar o modelo.

### Pré-requisitos
-   Python 3.8 ou superior.
-   Gerenciador de pacotes `pip`.

### Instalação
1.  **Clone o repositório:**
    ```sh
    git clone [https://github.com/theofeitoza/Visualizacao_carros.git](https://github.com/theofeitoza/Visualizacao_carros.git)
    ```
2.  **Navegue até o diretório do projeto:**
    ```sh
    cd Visualizacao_carros
    ```
3.  **Crie um ambiente virtual (recomendado):**
    ```sh
    # Para macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```
4.  **Instale as dependências necessárias:**
    ```sh
    pip install ultralytics opencv-python
    ```

### Executando a Detecção
Para executar a detecção em uma das imagens de teste ou em uma imagem sua, utilize o script `deteccao.py`.

1.  **Execute o script de detecção:**
    ```sh
    # Exemplo utilizando uma das imagens do repositório
    python deteccao.py --image_path teste5.jpg
    ```
    *Nota: Pode ser necessário ajustar o nome do argumento (ex: `--image_path`, `--source`) dentro do script `deteccao.py`.*

2.  **Verifique o resultado:** O script salvará uma nova imagem com as detecções desenhadas nela, geralmente em uma pasta como `runs/detect/predict/`.

---

## 🖼️ Exemplos de Detecção
Abaixo, um exemplo do resultado esperado após a execução do modelo sobre uma imagem de validação.

*(Você pode adicionar a imagem val_batch2_pred.jpg aqui)*

---

<div align="left">
  <a href="#top">⬆ Voltar ao topo</a>
</div>
