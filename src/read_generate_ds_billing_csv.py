import csv
import pandas as pd
import os
from itertools import groupby

class ReadGenerateDsBillingCsv : 

    CURRENT_FILE_DIR = 'csvs'
    CSV_HEADER = ['total_amount', 'gst', 'end_date', 'running_hour', 'amount_without_tax', 'start_date','description']

    def __init__(self) : 
        self.final_output = []
        self.temp_output = []
    

    def read_file(self) :
        fileDir = os.chdir(self.CURRENT_FILE_DIR)
        files = os.listdir(os.getcwd())
        for file in files :
            data = pd.read_csv(file,usecols=[2,3,4,5,6], skipfooter=1,engine='python')
            for i,description in enumerate(data['description']) : 
                usd_amount = data['USD'][i].replace('$','')
                usd_amount = float(usd_amount)
                gst_amount = (usd_amount / 100) * 10
                prepare_object = {
                    "description" : description,
                    "running_hour" : data['hours'][i],
                    "amount_without_tax" : data['USD'][i],
                    "start_date" : data['start'][i],
                    "end_date" :  data['end'][i],
                    "gst":gst_amount,
                    "total_amount":(gst_amount + usd_amount)  
                }
                self.temp_output.append(prepare_object) 


    def sort_by_key(self,args) :
        return args['description']
    


    def sort_by_desc(self) :
        self.temp_output = sorted(self.temp_output,key=self.sort_by_key)
        for key,response in groupby(self.temp_output,self.sort_by_key):
            self.final_output.append(list(response))

    
    def read_and_sort_csv(self) :
        self.read_file()
        self.sort_by_desc()
        self.generate_csv_from_output()
        return 'CSV file successfully generated in the output directory'


    def generate_csv_from_output(self):
        for output in self.final_output:
            output_dir_file_name = "../outputs/" + output[0]['description'] + '.csv'
            with open(output_dir_file_name, 'w+') as f :
                writer = csv.DictWriter(f,fieldnames=self.CSV_HEADER,delimiter=',')
                writer.writeheader()
                writer.writerows(output)
                f.close()