# Remoção de Fundo com OpenCV

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv&logoColor=white)
![Status](https://img.shields.io/badge/status-concluído-brightgreen)

## Dataset Utilizado
- [Orange Fruit Dataset - Kaggle](https://www.kaggle.com/datasets/mohammedarfathr/orange-fruit-daatset)

## Sobre
Trabalho desenvolvido para a disciplina de Computação Gráfica – La Salle, semestre 2025/01.

## Integrantes
- Ana Julia Ribeiro  
- Eduarda Mariotti  
- Ernesto Terra dos Santos  
- Nathan Schranck  
- Pedro Mendonça  

## Mini-problema
Remover o fundo das imagens e posicionar os objetos (frutas) de forma centralizada sobre um fundo branco padronizado.

---

## Solução com OpenCV

Utilizamos o OpenCV em conjunto com NumPy para segmentar o objeto principal da imagem e aplicar um fundo branco com centralização.

### Etapas do processamento:

#### 1. Importações
```python
import cv2
import numpy as np
```

#### 2. Inicialização do GrabCut
```python
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)
```

#### 3. Segmentação
```python
cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
```

#### 4. Refinamento da máscara
```python
cv2.findContours
cv2.drawContours
```

#### 5. Suavização (Feathering)
```python
cv2.GaussianBlur
```

#### 6. Recorte e Centralização
```python
cv2.findNonZero
cv2.boundingRect
```

---

## Como Usar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Instale as dependências
Recomendado: use um ambiente virtual.

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip3 install -r requirements.txt
```

**`requirements.txt`:**
```
opencv-python
numpy
```

### 3. Estrutura de pastas
Crie as seguintes pastas (ou ajuste no código):
```
unprocessed_images/
└── imagem1.jpg
processed_images/
```

### 4. Execute o script
```bash
python remover_fundo.py
```

As imagens processadas aparecerão na pasta `processed_images/`.

---

## 📸 Exemplo de Resultado

| Original | Processada |
|----------|------------|
| ![Exemplo1](![antes](https://github.com/user-attachments/assets/f1e030b6-05eb-4810-a44b-97300e321392)) | ![Exemplo2](![depois](https://github.com/user-attachments/assets/9aa9c4ae-1288-45a1-bd0b-842a66280145)) |

---

