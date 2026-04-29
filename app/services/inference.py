import torch
import torch.nn as nn
import cv2
import numpy as np
from io import BytesIO
from app.core.logger import logger
import time

import os
# import shutil
import uuid
from app.core.config import settings


class SRCNN(nn.Module):
    def __init__(self, scale_factor=4):
        super(SRCNN, self).__init__()
        self.upsample = nn.Upsample(scale_factor=scale_factor, mode='bicubic', align_corners=False)
        self.conv1 = nn.Conv2d(3, 128, kernel_size=9, padding=4)
        self.leaky_relu1 = nn.LeakyReLU()
        self.conv2 = nn.Conv2d(128, 64, kernel_size=1)
        self.leaky_relu2 = nn.LeakyReLU()
        self.conv3 = nn.Conv2d(64, 32, kernel_size=1)
        self.leaky_relu3 = nn.LeakyReLU()
        self.conv4 = nn.Conv2d(32, 3, kernel_size=5, padding=2)

    def forward(self, x):
        x=self.upsample(x)
        x = self.leaky_relu1(self.conv1(x))
        x = self.leaky_relu2(self.conv2(x))
        x = self.leaky_relu3(self.conv3(x))
        x = self.conv4(x)
        return x
    
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


OUTPUT_DIR = settings.output_dir
MODEL_PATH = "model_weights/model_weights.pth"

os.makedirs(OUTPUT_DIR,exist_ok = True)


model = SRCNN().to(device)
model.load_state_dict(torch.load(MODEL_PATH, map_location = device))
model.eval()

def preprocessing(img):
    if isinstance(img, BytesIO):
        img.seek(0)
        img_array = np.frombuffer(img.read(), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    elif isinstance(img, np.ndarray):
        pass
    else:
        raise ValueError("Invalid input image format.")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype('float32') / 255.0

    img = torch.from_numpy(img.transpose(2,0,1)).unsqueeze(0)
    
    return img.to(device)


def enhance_image(upload_file):
    logger.info(f"Enhancement started for {upload_file.filename}")
    start = time.time()


    file_bytes = upload_file.file.read()

    tensor = preprocessing(BytesIO(file_bytes))

    infer_start = time.time()

    with torch.no_grad():
        output = model(tensor)

    infer_ms = round((time.time() - infer_start) * 1000, 2)

    logger.info(f"Model imferemce completed in {infer_ms}ms")

    output = output.squeeze(0).permute(1,2,0).cpu().numpy()
    output = np.clip(output * 255.0,0,255).astype(np.uint8)

    output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)


    output_name = f"enchance_{uuid.uuid4()}_{upload_file.filename}"
    output_path = os.path.join(OUTPUT_DIR,output_name)


    # with open(output_path, "wb") as buffer:
    #     shutil.copyfileobj(upload_file.file, buffer)

    cv2.imwrite(output_path,output)

    total_ms = round((time.time() - start) * 1000, 2)

    logger.info(
        f"Enhancement completed for {upload_file.filename} "
        f"Output={output_name} Total={total_ms}ms"
    )

    return output_name