import joblib
import csv
import numpy as np
def returnDiseaseName(input_param):
    if(len(input_param)!=1):
        return "It seems like we couldn't identify the disease, please try again or try contacting one of our doctors"
    elif(len(input_param[0])!=17):
        while(len(input_param[0])!=17):
            input_param[0].append(0)
    count=0
    for i in range(0,17):
        if(input_param[0][i]==0):
            count=count+1
    if(count==17):
        return "You seem to be okay! Good job"
    loaded_model = joblib.load(r"C:\Users\devra\Desktop\projects\project codeforge ml\Robo-Hackathon\ML Models\DiseaseM.joblib")
    prediction = loaded_model.predict(input_param)
    return prediction[0]

def get_row_by_value(csv_file, column_name, target_value):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row[column_name] == target_value:
                return row
def returnDiseaseDescription(disease_name):
    dir_descip =(r"C:\Users\devra\Desktop\projects\project codeforge ml\Robo-Hackathon\Data\symptom_Description.csv")
    descip = get_row_by_value(dir_descip,"Disease",disease_name)

    return descip["Description"]
def returnDiseasePrecaution(disease_name):
    dir_precau = (r"C:\Users\devra\Desktop\projects\project codeforge ml\Robo-Hackathon\Data\symptom_precaution.csv")
    precau = get_row_by_value(dir_precau,"Disease",disease_name)
    precau_list = []
    for i in range(1,5):
        key_val = "Precaution_"+str(i)
        if(precau[key_val]!=''):
            precau_list.append(precau[key_val]) 
    return precau_list
print(returnDiseaseName([[6, 4, 5, 4]]))