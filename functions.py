import os
import pandas as pd
from datetime import datetime


def list_folders(directory: str):
    #directory = directory.replace("file://","")
    folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
    return folders

def list_files(directory: str):
    #directory = directory.replace("file://","")
     #if f.endswith(".xlsx")
    folders = [f for f in os.listdir(directory)]
    return folders
