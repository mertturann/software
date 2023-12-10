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
    input_motion = []
    for folder in folders:
        file_path = os.path.join(folder, deprem)

        if os.path.exists(folder):
                try:
                    excel_data = pd.read_excel(file_path, sheet_name=layer)
                    y_values = excel_data[column].dropna().tolist()
                    all_y_values.append(y_values)
                    input_data = pd.read_excel(file_path, sheet_name="Input Motion",header=1)
                    input = input_data["PSA (g)"].dropna().tolist()
                    input_motion.append(input)
                
                except Exception as e:
                    print(f"{deprem} dosyasını okuma sırasında hata oluştu: {e}")
        else:
            print(f"{deprem} dosyası bulunamadı: {folder}")
       
    return all_y_values, input_motion[0]


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

    

def draw_test(y_values,graphname: str, title: str,input_motion,labels):
    label = labels
    x_values = getperiod()
    plt.figure(figsize=(15, 9))
    plt.xscale('log')  # Y eksenini logaritmik ölçekte gösterme
    plt.tight_layout()
    #plt.ylim(bottom=0,top=1.75)
    for idx, y_data in enumerate(y_values,start=0):
        plt.plot(x_values, y_data,label=labels[idx])
        
    print(input_motion)    
    plt.plot(x_values,input_motion,label="Input Motion")    
    plt.xlabel("Periyot (X)")
    plt.ylabel("PSA (g) (y)")
    plt.title(str(title))
    plt.tight_layout()
    plt.legend()
    plt.savefig(f"sonuclar/{graphname}")
    plt.close()



def multi_deprem(folder_path, file_names, sheet_name, column_name):
    all_values = []

    # Verilen klasördeki her dosya için işlem yap
    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)

        # Excel dosyasını oku
        try:
            excel_data = pd.read_excel(file_path, sheet_name=sheet_name)
            if column_name in excel_data.columns:
                values = excel_data[column_name].dropna().tolist()
                all_values.append(values)
        except Exception as e:
            print(f"Hata: {file_name} dosyasında okuma sırasında bir hata oluştu - {e}")
    print ("başarılı")
    return all_values

 
 
def draw_deprem(y_values,graphname: str, title: str,labels):
    label = labels
    x_values = getperiod()
    plt.figure(figsize=(15, 9))
    plt.xscale('log')  # Y eksenini logaritmik ölçekte gösterme
    plt.tight_layout()
    #plt.ylim(bottom=0,top=1.75)
    for idx, y_data in enumerate(y_values,start=0):
        plt.plot(x_values, y_data,label=labels[idx])
        
    plt.xlabel("Periyot (X)")
    plt.ylabel("PSA (g) (y)")
    plt.title(str(title))
    plt.tight_layout()
    plt.legend()
    plt.savefig(f"sonuclar/{graphname}")
    plt.close()   