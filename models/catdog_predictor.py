import sys
import torch
import torchvision 

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from PIL import Image
from torch.nn import functional as F
from utils.logger import Logger
from config.catdog_clg import CatDogDataConfig
from .catdog_model import CatDogModel

LOGGER = Logger(__file__, log_file='predictor.log')
LOGGER.log.info('Start Model Serving')

class Predictor:
    def __init__(self, model_name: str, model_weight: str, device: str='cpu'):
        self.model_name = model_name
        self.model_weight = model_weight
        self.device = device
        self.load_mode()
        self.create_transform()

    async def predict(self, image):
        pil_img = Image.open(image)
        
        if pil_img.mode == 'RGBA':
            pil_img=pil_img.convert('RGB')

        transformed_image = self.transforms_(pil_img).unsqueeze(0)
        output = await self.mode_inference(transformed_image)
        probs, best_prob, predicted_id, predicted_class = self.output2pred(output)

        LOGGER.log_model(self.model_name)
        LOGGER.log_response(best_prob, predicted_id, predicted_class)

        torch.cuda.empty_cache()

        resp_dict = {
            'probs': probs,
            'best_prob': best_prob,
            'predict_id': predicted_id,
            'predict_class': predicted_class,
            'predict_name': self.model_name
        }
        return resp_dict