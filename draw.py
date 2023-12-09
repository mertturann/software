import pandas as pd, os
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.chart import (
    ScatterChart,
    Reference,
    Series,
)

def getperiod():
    try:
        excel_data = pd.read_excel("period.xlsx", sheet_name="Sayfa1")
        selected_column = excel_data["Period (sec)"].dropna().tolist()
        return selected_column
    except FileNotFoundError:
        return f"Period dosyası bulunamadı."
    except Exception as e:
        return f"Hata oluştu: {e}"


def multi_analysis(folders, deprem, layer, column):
    all_y_values = []
    for folder in folders:
        file_path = os.path.join(folder, deprem)

        if os.path.exists(folder):
                try:
                    excel_data = pd.read_excel(file_path, sheet_name=layer)
                    y_values = excel_data[column].dropna().tolist()
                    all_y_values.append(y_values)
                    input_data = pd.read_excel(file_path, sheet_name="Input Motion",header=1)
                    input_motion = input_data["PSA (g)"].dropna().tolist()
                
                except Exception as e:
                    print(f"{deprem} dosyasını okuma sırasında hata oluştu: {e}")
        else:
            print(f"{deprem} dosyası bulunamadı: {folder}")
       
    return all_y_values, input_motion


def draw_combined_graph(y_values,graphname: str, title: str,dirname: str,input_motion):
    x_values = getperiod()
    plt.figure(figsize=(15, 9))
    plt.xlim(0,3)
    plt.tight_layout()
    #plt.ylim(bottom=0,top=1.75)

    index = 1

    for idx, y_data in enumerate(y_values):
        plt.plot(x_values, y_data,linestyle='--' ,marker='.' ,label=f"A{index+idx}")
    plt.plot(x_values,input_motion,marker='*',label = "Input Motion")    


    plt.xlabel("Periyot (X)")
    plt.ylabel("PSA (g) (y)")
    plt.title(str(title))
    plt.tight_layout()
    plt.legend()
    plt.savefig(f"sonuclar/{dirname}/{graphname}")
    plt.close()

    

def draw_test(y_values,graphname: str, title: str,dirname: str,input_motion,labels):
    label = labels
    x_values = getperiod()
    plt.figure(figsize=(15, 9))
    plt.xlim(0,3)
    plt.tight_layout()
    #plt.ylim(bottom=0,top=1.75)
    for idx, y_data in enumerate(y_values,start=0):
        plt.plot(x_values, y_data,linestyle='--',marker='.',label=labels[idx])
    plt.plot(x_values,input_motion,marker='*',label = "Input Motion")    

    plt.xlabel("Periyot (X)")
    plt.ylabel("PSA (g) (y)")
    plt.title(str(title))
    plt.tight_layout()
    plt.legend()
    plt.savefig(f"sonuclar/{dirname}/{graphname}")
    plt.close()

    