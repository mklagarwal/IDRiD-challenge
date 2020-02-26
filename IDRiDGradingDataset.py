from __future__ import print_function, division
import os
import torch
import pandas as pd
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
from bengraham_preprocessing import preprocess

class IDRiDGradingDataset(Dataset):
    """IDRiD grading dataset."""

    def __init__(self, csv_file, root_dir, transform, bengraham=False):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.labels = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform
        self.bengraham = bengraham

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        # labels
        lbls = self.labels.iloc[idx, :]
        img_name = lbls['Image name']
        target = lbls['Retinopathy grade']

        # image
        # get img path
        img_path = os.path.join(self.root_dir,
                                img_name+'.jpg')

        # Bengraham preprocessing if necessary
        if self.bengraham:
            image = preprocess(img_name+'.jpg', self.root_dir, img_name)
            image = Image.fromarray(np.uint8(image))
        else:
            image = Image.open(img_path)

        sample = {'image': image, 'labels': target}

        if self.transform:
            sample['image'] = self.transform(sample['image'])
            #sample['label'] = torch.from_numpy(np.array(sample['labels']))

        return sample
