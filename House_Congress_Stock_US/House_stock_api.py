import requests 
import json
import pandas as pd
from os import getcwd


end_point = "https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json"

# data = []
try:
    response = requests.get(end_point)
    obj = response.json()
    text = json.dumps(obj,sort_keys=True, indent=4)
    data = json.loads(text)

    #normalize data into dataframe for analysis
    df2 = pd.json_normalize(data) 

    #write file to csv 
    df2.to_csv(getcwd()+"\\USA_Congress_Transactions_data.csv",index=False)

except ConnectionError:
    print("Error! Connection has failed ... ")
except NameError:
    print("Name Error detected! ")
# else:
    #clean json data 
    # print(data[:20])
