#Author: Jhoel Perez
#Date: 10/10/2022 
#Objective: Fetch info from last fm api to obtain dataset for data analysis
#Notes: 


from dotenv import load_dotenv
from os import getcwd, environ

#load environment variables 
load_dotenv(f"{getcwd()}\API_key.env")

API_key = environ.get("API_key")
API_secret = environ.get("API_Shared_secret")