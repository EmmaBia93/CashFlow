import requests
from dotenv import load_dotenv
import os

load_dotenv()
headers = {'Authorization': os.getenv("API")}
url = os.getenv("URL_FACTURAS")


params = {
                    'fecha_pago__range_0':'2024-09-10',
                    'fecha_pago__range_1':'2024-09-10',
                    'estado': 2,
                    'limit': 300,
                    'offset':0
                }


results=[]
total_cobrado=0    
     
while True:
                                
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                results.extend(data.get('results', []))
                
                if not len(results)==300:
                    break
                    
                params['offset']+=300
                 
            else:
                results=[]

if results:
    for result in results:
          total_cobrado+=int(result.get('total_cobrado',0))

print(total_cobrado)