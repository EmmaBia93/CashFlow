from datetime import datetime,timedelta

import requests


url = 'https://api.wisphub.net/api/facturas/'
fecha_actual = datetime.now()

# Calcula la fecha del día anterior
dia_anterior = fecha_actual - timedelta(days=1)

fecha_formateada = dia_anterior.strftime('%Y-%m-%d')
        # Define el encabezado con la API key
headers = {
            'Authorization': 'Api-Key ryVTfsEP.wiPj1WcWM8iVT6nE5Mfddy3JvyLj1sG9'
        }

params = {
            'fecha_pago': fecha_formateada,
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
