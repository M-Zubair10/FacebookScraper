import time

import cv2
from PIL import Image
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('clip-ViT-B-32')


class Inference:
    def __init__(self, img1, img2):
        self.img1 = img1
        self.img2 = img2
    
    @staticmethod
    def DenseVectorRepresentation(img1, img2) -> float:
        encoded_image = model.encode([img1, img2], batch_size=128, convert_to_tensor=True,
                                     show_progress_bar=False)
        processed_images = util.paraphrase_mining_embeddings(encoded_image)
        return processed_images[0][0]
    
    def on_pil(self):
        return self.DenseVectorRepresentation(self.img1, self.img2)
