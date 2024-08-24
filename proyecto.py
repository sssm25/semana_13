# Importar las librerías
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Hacemos la petición a la página y a BeautifulSoup
url = 'https://www.scrapethissite.com/pages/simple/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Encuentra todos los divs que contienen la información de los países
countries = soup.find_all('div', class_='country')

data = []
for country in countries:
    name = country.find('h3', class_='country-name').text.strip()
    capital = country.find('span', class_='country-capital').text.strip()
    population = country.find('span', class_='country-population').text.strip()
    area = country.find('span', class_='country-area').text.strip()

    data.append([name, capital, population, area])

# Convierte a DataFrame
df = pd.DataFrame(data, columns=['Nombre', 'Capital', 'Población', 'Área (km²)'])

# Guardar los datos en un CSV
df.to_csv('datos_scrapeados.csv', index=False)


#2 Importar librerías para crear el API con flask
from flask import Flask, jsonify, request

app = Flask(__name__)

# Cargar los datos
df = pd.read_csv('datos_scrapeados.csv')
# Convertir a tipos numéricos nuevamente por seguridad
df['Población'] = pd.to_numeric(df['Población'], errors='coerce')
df['Área (km²)'] = pd.to_numeric(df['Área (km²)'], errors='coerce')

#Edpoint para obtener datos filtrados
@app.route('/api/datos', methods=['GET'])
def get_data():
    nombre_pais = request.args.get('nombre')
    min_area = request.args.get('min_area', default=0, type=int)

    # Filtrar los datos
    filtered_data = df
    if nombre_pais:
        filtered_data = filtered_data[filtered_data['Nombre'].str.contains(nombre_pais, case=False)]
    if min_area > 0:
        filtered_data = filtered_data[filtered_data['Área (km²)'] > min_area]

    return jsonify(filtered_data.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)

---
title: "Análisis de Datos de Países"
author: "Sisney"
format: 
 pdf:
   code-fold: true
   toc: true
   toc-depth: 2
   number-sections: true
   fig-cap: true
jupyter: python3
---
# Gráfico Categórico
```{python}
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('datos_scrapeados.csv')
df.head()
```
```{python}
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Área (km²)')
plt.title('Número de Países por Área')
plt.show()
```
```{python}
#Grafico relaccional
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Población', y='Área (km²)')
plt.title('Población vs Área')
plt.show()
```
```{python}
#Grafico de distribucion
plt.figure(figsize=(10, 6))
sns.histplot(df['Población'], bins=10, kde=True)
plt.title('Distribución de Población')
plt.show()
```
