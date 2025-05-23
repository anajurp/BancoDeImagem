import os
import cv2
import numpy as np


class BackgroundRemover:
    """
    Classe para remover o fundo de imagens utilizando o algoritmo GrabCut,
    centralizando o objeto principal sobre um fundo branco.
    """

    def __init__(self, input_folder: str, output_folder: str):
        """
        Inicializa a classe com as pastas de entrada e saída.

        Args:
            input_folder (str): Caminho para a pasta contendo as imagens originais.
            output_folder (str): Caminho para a pasta onde as imagens processadas serão salvas.
        """
        self.input_folder = os.path.abspath(input_folder)
        self.output_folder = os.path.abspath(output_folder)
        os.makedirs(self.output_folder, exist_ok=True)

    def process_images(self):
        """
        Processa todas as imagens da pasta de entrada e salva as versões
        com fundo branco centralizado na pasta de saída.
        """
        for filename in os.listdir(self.input_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_path = os.path.join(self.input_folder, filename)
                output_path = os.path.join(self.output_folder, filename)
                print(f"🖼️ Processando {filename}")
                self._process_single_image(input_path, output_path)

    def _process_single_image(self, input_path: str, output_path: str):
        """
        Processa uma única imagem, removendo o fundo e centralizando o objeto.

        Args:
            input_path (str): Caminho da imagem original.
            output_path (str): Caminho para salvar a imagem processada.
        """
        image = cv2.imread(input_path)
        if image is None:
            return

        mask = self._create_mask_grabcut(image)
        result = self._apply_white_background_centered(image, mask)

        cv2.imwrite(output_path, result)
        print(f"✅ Salvo em: {output_path}")

    def _create_mask_grabcut(self, image: np.ndarray) -> np.ndarray:
        """
        Cria uma máscara binária usando o algoritmo GrabCut para segmentar o objeto principal.

        Args:
            image (np.ndarray): Imagem original.

        Returns:
            np.ndarray: Máscara com o objeto principal segmentado.
        """
        mask = np.zeros(image.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        height, width = image.shape[:2]
        margin_w = int(width * 0.08)
        margin_h = int(height * 0.08)
        rect = (margin_w, margin_h, width - 2 * margin_w, height - 2 * margin_h)

        # Aplica o algoritmo GrabCut
        cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        mask = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)

        # Mantém apenas o maior contorno (o objeto principal)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            clean_mask = np.zeros_like(mask)
            cv2.drawContours(clean_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
            mask = clean_mask

        # Suavização da máscara (feathering)
        mask = cv2.GaussianBlur(mask, (7, 7), 0)

        return mask

    def _apply_white_background_centered(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """
        Aplica fundo branco e centraliza o objeto com base na máscara fornecida.

        Args:
            image (np.ndarray): Imagem original.
            mask (np.ndarray): Máscara binária do objeto principal.

        Returns:
            np.ndarray: Imagem resultante com fundo branco e objeto centralizado.
        """
        coords = cv2.findNonZero(mask)
        if coords is None:
            return image

        x, y, w, h = cv2.boundingRect(coords)
        fruit = image[y:y+h, x:x+w]
        fruit_mask = mask[y:y+h, x:x+w]

        h_img, w_img = image.shape[:2]
        background = np.ones((h_img, w_img, 3), dtype=np.uint8) * 255

        center_x = (w_img - w) // 2
        center_y = (h_img - h) // 2

        roi = background[center_y:center_y+h, center_x:center_x+w]
        fruit_mask_bool = fruit_mask > 0
        for c in range(3):
            roi[..., c][fruit_mask_bool] = fruit[..., c][fruit_mask_bool]

        return background


input_folder = "unprocessed_images"
output_folder = "processed_images"

processor = BackgroundRemover(input_folder, output_folder)
processor.process_images()
