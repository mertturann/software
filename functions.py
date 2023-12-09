import os
import pandas as pd, re
from datetime import datetime


def getcurrentime():
    c = datetime.now()
    current_time = c.strftime('%H:%M')
    return str(current_time)


def sort_folders(folders):
    def natural_keys(text):
        def atoi(text):
            return int(text) if text.isdigit() else text

        return [atoi(c) for c in re.split(r'(\d+)', text)]

    return sorted(folders, key=natural_keys)

def validate_layer(string):
    pattern = r"^Layer\s\d+$"
    return re.match(pattern, string) is not None

def list_folders(directory: str):
    #directory = directory.replace("file://","")
    folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
    sorted_folders = sort_folders(folders)  # Klasörleri sırala

    return sorted_folders

def list_files(directory: str):
    #directory = directory.replace("file://","")
     #if f.endswith(".xlsx")
    folders = [f for f in os.listdir(directory)]
    return folders

def get_layers(file_path):
    try:
        sheets = []
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
        for name in sheet_names:
             if validate_layer(name):
                 sheets.append(name)
        return sheets
    except Exception as e:
        print(f"Excel Layer Tespit Edilirken Hata oluştu: {e}")
        return []
    
def check_files(file_name, folder):
    for files in os.walk(folder):
        if file_name in files:
            print ("Dosya Mevcut: {folder} {file_name}")
            return True
        else: 
            return None