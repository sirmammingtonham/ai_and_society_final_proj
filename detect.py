import sys
import glob
sys.path.append('./classification')
sys.path.append('..')

from classification.detection import test_full_image_network, detect_from_image
from classification.network import models
import torch
from compression_detection import compression_detection
import os
import re

from scraper import *
from text_detection import *

import warnings
warnings.filterwarnings("ignore")


ALLOWED_EXTENSIONS = set(['html', '/'])
MODEL_PATH = './classification/weights/full/xception/full_c23.p'
OUTPUT_PATH = './classification/data_dir/results'

cuda = False

base_weights_path = 'classification/weights/face_detection/xception'
model_full_path = f'{base_weights_path}/all_raw.p'
model_77_path = f'{base_weights_path}/all_c23.p'
model_60_path = f'{base_weights_path}/all_c40.p'

model_full = torch.load(model_full_path, map_location=lambda storage, loc: storage)
model_77 = torch.load(model_77_path, map_location=lambda storage, loc: storage)
model_60 = torch.load(model_60_path, map_location=lambda storage, loc: storage)

gpt = LM()

def get_word_index(s, idx):
    words = re.findall(r'\s*\S+\s*', s)
    try:
        limit = sum(map(len, words[:idx])) + len(words[idx]) - len(words[idx].lstrip())
        return limit
    except IndexError:
        return len(s)

def check_if_fake(url):
    try:
        text_preds = []
        image_preds = []
        fakes = []

        scraped = get_elements(url)
        if scraped[0]:
            raw_text = ''.join([''.join(x[1]) for x in scraped[0]]).encode('ascii', 'replace').decode()
            limit = get_word_index(raw_text, 740)
            result_percentage = get_generated_analysis(raw_text[:limit], gpt)
            if result_percentage >= 0.3:
                text_preds.append('very low likelihood')
            if result_percentage >= 0.15:
                text_preds.append('low likelihood')
            elif result_percentage >= 0.12:
                text_preds.append('reasonable chance')
            else:
                text_preds.append('high likelihood')
            text_preds.append(result_percentage)

        if scraped[1]:
            print('found images, running detection')
            for image in scraped[1]:
                image_preds.append((detect_from_image(image[1], model_full, cuda=cuda), image))
            # print(image_preds)
            fakes = [i for i in image_preds if i[0] == 0]
            if os.path.exists("temp.jpg"):
                os.remove("temp.jpg")


        if scraped[2]:
            print('found videos, running detection')
            predicted_class = compression_detection.classify_video(scraped[2])

            if predicted_class == '0.6':
                fake_prediction = test_full_image_network(scraped[2], model=model_60, output_path=OUTPUT_PATH,
                                        start_frame=0, end_frame=None, cuda=cuda)
            elif predicted_class == '0.77':
                fake_prediction = test_full_image_network(scraped[2], model=model_77, output_path=OUTPUT_PATH,
                                        start_frame=0, end_frame=None, cuda=cuda)
            elif predicted_class == 'original':
                fake_prediction = test_full_image_network(scraped[2], model=model_full, output_path=OUTPUT_PATH,
                                        start_frame=0, end_frame=None, cuda=cuda)
            else:
                fake_prediction = None

            print(f'fake_prediction: {fake_prediction}')

            if fake_prediction == 1:
                a = False
            elif fake_prediction == 0:
                a = True
            else:
                print('ERROR! Something went wrong. Please try again.')
                return None
            return {'paragraphs': None, 'images': None, 'videos': a, 'length': 1}
        return {'paragraphs': text_preds, 'images': fakes, 'videos': None, 'length' : len(scraped[0])+len(fakes)}
    except Exception as e:
        raise e
        print(e)
        print('ERROR! Something went wrong. Please try again.')
        # return redirect(url_for('index'))
        return None

# if __name__ == "__main__":
    # check_if_fake('https://www.youtube.com/watch?v=cQ54GDm1eL0')
    # print(check_if_fake('https://medium.com/futuremag/fortnite-creative-mode-isn-t-for-everybody-9551c47d2de3'))
    # print(check_if_fake('https://medium.com/futuremag/why-people-buy-30-power-cords-against-all-reason-8d01b837ce4e'))
    # print(check_if_fake('https://www.cnn.com/2019/12/08/politics/north-korea-donald-trump-test-kim-jong-un/index.html'))