"""
Preprocessing:
BraTS 2021
BraTS 2020
BraTS 2019

"""
from glob import glob
from os import getenv, makedirs, path

import nibabel as nib
import numpy as np
from sklearn.preprocessing import MinMaxScaler

try:
    path_dataset = getenv("PATH_DATASET")
    path_preprocess = getenv("PATH_PREPROCESS")
    input_exists = path.exists(path_dataset)
    output_exists = path.exists(path_preprocess)
except Exception as err:
    print("Error in parsing environment variables: ", repr(err))
    exit()

if not input_exists:
    raise Exception("Dataset does't exist.")
if not output_exists:
    makedirs(path_preprocess)

flair_list = sorted(glob(rf"{path_dataset}/*/*flair.nii.gz"))
t1ce_list = sorted(glob(rf"{path_dataset}/*/*t1ce.nii.gz"))
t2_list = sorted(glob(rf"{path_dataset}/*/*t2.nii.gz"))
mask_list = sorted(glob(rf"{path_dataset}/*/*seg.nii.gz"))

scaler = MinMaxScaler()


def load_transform(img):
    img_raw = nib.load(img).get_fdata()
    img_norm = scaler.fit_transform(img_raw.reshape(-1, img_raw.shape[-1])).reshape(
        img_raw.shape
    )
    return img_norm


def dataset_len():
    if not len(flair_list) == len(t1ce_list) == len(t2_list) == len(mask_list):
        print("error")
        exit()
    else:
        return len(flair_list)


def preprocess(
    x_start=55, x_end=185, y_start=55, y_end=185, slice_start=15, slice_end=140
):
    if x_end - x_start != y_end - y_start:
        print("ALERT: the output will not be square.")

    for img_idx in range(dataset_len()):
        load_transform(flair_list[img_idx])

        img_stack = np.stack(
            [
                load_transform(flair_list[img_idx]),
                load_transform(t1ce_list[img_idx]),
                load_transform(t2_list[img_idx]),
            ],
            axis=3,
        )
        img_stack_cropped = img_stack[
            x_start:x_end, y_start:y_end, slice_start:slice_end
        ]

        img_mask_raw = nib.load(mask_list[img_idx]).get_fdata()
        img_mask_norm = img_mask_raw.astype(np.uint8)
        img_mask_norm[img_mask_norm == 4] = 3
        img_mask_cropped = img_mask_norm[56:184, 56:184, slice_start:slice_end]

        _, counts = np.unique(img_mask_cropped, return_counts=True)

        if (1 - (counts[0] / counts.sum())) > 0.01:

            img_mask_cat = np.eye(4, dtype="uint8")[img_mask_cropped]
            np.save(rf"{path_preprocess}/{img_idx}.npy", img_stack_cropped)
            np.save(rf"{path_preprocess}/m{img_idx}.npy", img_mask_cat)
            print(f"Data {img_idx} was saved.")

        else:
            print(f"Useless Segmentation {img_idx}.")
            with open("./log/useless_segmentation.log", "a") as f:
                f.write(f"{img_idx} \n")


preprocess()
