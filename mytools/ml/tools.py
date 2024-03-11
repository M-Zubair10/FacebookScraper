import os
from itertools import combinations
import cv2
from skimage.metrics import structural_similarity
from collections import Counter
from mytools.common.generator import username as random_name
from mytools.pre_processing import plist
import shutil
import numpy as np


def detect_and_remove_duplicates(dataset):
    folder_names = os.listdir(dataset)
    for folder_name in folder_names:
        img_paths = [f"{dataset}/{folder_name}/" + x for x in os.listdir(f"{dataset}/{folder_name}")]
        combs = (combinations(img_paths, 2))
        pending_removal = []
        for c in combs:
            if int(os.stat(c[0]).st_size/1000) == int(os.stat(c[1]).st_size/1000):
                print(f"Validating {c[0]} -> {c[1]}")
                img1 = cv2.imread(c[0])
                img2 = cv2.imread(c[1])
                if img1.shape == img2.shape:
                    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
                    score, diff = structural_similarity(gray1, gray2, full=True)
                    if score > 0.8:
                        print(f"Matched {score}% -> Removed!")
                        pending_removal.append(c[1])
                    else:
                        print(f"Matched {score}% -> Keep")
            else:
                print(f"Size not same i.e, {c[0]} != {c[1]}")

        print("Before: ", len(img_paths))
        print("Total combinations: ", len(list(combs)))
        print("Duplicate images: ", len(pending_removal))
        for p in set(pending_removal):
            os.remove(p)
        print("After: ", len([f"Dataset/{folder_name}" + x for x in os.listdir(f"Dataset/{folder_name}")]))


def remove_blank_images(dataset):
    folder_names = os.listdir(dataset)
    for folder_name in folder_names:
        img_paths = [f"{dataset}/{folder_name}/" + x for x in os.listdir(f"{dataset}/{folder_name}")]
        for img_path in img_paths:
            img = cv2.imread(img_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            pixels = [gray[i, j] for i in range(gray.shape[0]) for j in range(gray.shape[1])]
            if len(Counter(pixels)) < 10:
                os.remove(img_path)
                print(f"Removed {img_path}")


def nms(boxes, scores, nms_thresh):
    # Convert to numpy arrays
    boxes = np.array(boxes)
    scores = np.array(scores)
    scores = scores.astype(np.float64)

    # Apply NMS
    indices = cv2.dnn.NMSBoxes(boxes, scores, score_threshold=0.0, nms_threshold=nms_thresh)

    # Return the selected boxes
    return [boxes[i] for i in indices]



def extract_dir(src_folder, dest_folder):
    """
    Recursively copies all image files from src_folder to dest_folder.
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_folder, file)
                shutil.copy2(src_path, dest_path)

def get_classes(filename):
    return File(filename).read()


def make_classes(dataset, filename):
    classes = get_classes(filename)
    for c in classes:
        os.mkdir(f"{dataset}/{c}")


def split_dataset(src_dataset, dst_dataset):
    folder_names = os.listdir(src_dataset)
    os.mkdir(dst_dataset + "/train")
    os.mkdir(dst_dataset + "/test")
    os.mkdir(dst_dataset + "/val")
    for folder_name in folder_names:
        img_paths = [f"{src_dataset}/{folder_name}/" + x for x in os.listdir(f"{src_dataset}/{folder_name}")]
        train_set, test_set = plist.split(img_paths, int(len(img_paths) * 0.8))
        train_set, val_set = plist.split(train_set, int(len(train_set) * 0.8))
        print(len(train_set), len(test_set), len(val_set), folder_name, len(img_paths))

        train_path = dst_dataset + f"/train/{folder_name}"
        test_path = dst_dataset + f"/test/{folder_name}"
        val_path = dst_dataset + f"/val/{folder_name}"
        os.mkdir(train_path)
        os.mkdir(test_path)
        os.mkdir(val_path)

        for im in train_set:
            shutil.copy(im, train_path)
        for im in test_set:
            shutil.copy(im, test_path)
        for im in val_set:
            shutil.copy(im, val_path)


if __name__ == '__main__':
    pass