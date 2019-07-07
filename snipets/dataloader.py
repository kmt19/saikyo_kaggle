"""
Note: this snipet is assumed to work on a Jupyter Notebook
"""

!pip install dicom
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import os
import torch
import pandas as pd
from skimage import io
import pydicom

class SIIMDataset(Dataset):
    """
    args:
    - root_dir : parents dir of csv_file
    - phase    : phase of the dataset used (∈{"train", "test"})
    - transform:  
    """
    def __init__(self, root_dir, phase, transform=None):
        self.phase = phase
        self.root_dir = root_dir
        self.cols = 2 if phase == "train" else 1
        self.table = pd.read_csv(f"{root_dir}/{phase}.csv", usecols = [i for i in range(self.cols)])
        self.transform = transform

    def __len__(self):
        return len(self.table)

    def __getitem__(self, idx):
        img_path = train_names[idx]
        image = pydicom.dcmread(self.table["Path"][idx]).pixel_array
        label = self.table["EncodedPixels"][idx] if self.phase == "train" else None
        
        image = Image.fromarray(image)
        image = image.convert("RGB")

        if self.transform:
            image = self.transform(image)   # transform image to tensor

        sample = {'image':image, 'label':label}
        return sample
       

"""
上記クラスのテスト用スクリプト
"""
train_set = SIIMDataset(root_dir="./gdrive/My Drive", phase="train")
count=0

for i,data in enumerate(train_set):
    print(data)
    count += 1
    if count == 5:
      break
      
