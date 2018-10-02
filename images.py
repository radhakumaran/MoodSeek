from __future__ import print_function
import json
from os.path import join, dirname
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud.tone_analyzer_v3 import ToneInput
import json
from os.path import abspath
import os
import os.path
import pandas as pd
from constants import Constants
from watson_developer_cloud import VisualRecognitionV3, WatsonApiException

const = Constants()

def ProcessImage(image_path):
    """
    Identifies the emotion of an image, using the Watson Visual Recognition API

    Args:

    image_path: the path to the image file

    Returns:

    The emotion of the image
    """
    service = VisualRecognitionV3('2018-03-19',url='https://gateway.watsonplatform.net/visual-recognition/api',iam_apikey='dnckUYEa5ip8jnJvWFdeFA7aMsRCXx9agFgEiGO3NBpu')
    path = abspath(image_path)
    text = " "
    try:
        with open(path, 'rb') as images_file:
            results = service.classify(images_file=images_file,threshold='0.1',classifier_ids=['default']).get_result()
            #print()
            for value in results["images"][0]["classifiers"][0]["classes"]:
                text= text +" "+value["class"]
            print(text)
            text+="."
            puncs1=['@','#','$','%','^','&','*','(',')','-','_','+','=','{','}','[',']','|','\\','"',"'",';',':','<','>','/']
            for punc in puncs1:
                text=text.replace(punc,'')
    except WatsonApiException as ex:
        print(ex)
    

    service = ToneAnalyzerV3(username='07b26723-e879-447e-9323-15659e44f3fa',password='c4FKFPlpHo5K',version='2017-09-21')
    service.set_detailed_response(True)
    tone_input = ToneInput(text)
    tone = service.tone(tone_input=tone_input, content_type="application/json")

    emo_score=[]
    for emotion in tone.result["document_tone"]["tones"]:
        print(emotion["score"])
        print(emotion["tone_name"])
        emo_score.append(emotion["score"])
    if not emo_score:
        return 'Neutral'
    else:
        return(tone.result["document_tone"]["tones"][emo_score.index(max(emo_score))]["tone_name"])   
    #service.set_detailed_response(False)

def ImageDatasetProcessing():
    """
    Processes the images in the dataset and associates each image to one of
    the emotions.
    """
    list_df=[]
    if not os.path.exists(const.clustered_images):
        for dirpath, dirnames, filenames in os.walk(const.image_dataset):
            for filename in [f for f in filenames if f.endswith(".png") or f.endswith(".jpg")]:
                i = os.path.join(dirpath, filename)
                print(i)
                emotion = ProcessImage(i)
                print(emotion)
                list_df.append([i, emotion])
        df = pd.DataFrame(list_df,columns=['Filepath','Emotion'])
        df.to_csv(const.clustered_images, sep=',', encoding='utf-8', index = False)

def get_images(emotion):
    """
    Returns a set of emotions for a given emotion.

    Args:

    emotion: The emotion for which you want images to be fetched.

    Returns:

    The set of images for the particular emotion
    """
    df = pd.read_csv(const.clustered_images)
    df = df.loc[df.Emotion == emotion]
    return df.sample(const.image_num)


