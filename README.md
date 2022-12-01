# MavenPizzaXml
Write Maven Pizza data to a Xml file

Proyecto con la utilización de las librerías de expresiones regulares 're', Dataframe 'pandas' y luego exportamos la información a un archivo xml con 'xml.etree.ElementTree' en el lenguaje Python. Análisis de los datos de la Pizzería Maden y sugerencia para comprar ingredientes por semana

Datos (csv) extraidos de: https://www.kaggle.com/datasets/neethimohan/maven-pizza-challenge-dataset?select=data_dictionary.csv

1. Install a virtual enviroment with venv: python -m pip install virtualenv 
2. Create a virtual enviroment: python -m venv env
3. Activate virtual enviroment:
 - Move to: cd .\env\Scripts\
 - Start: activate
4. Install packages for the python file: pip install -r requirements.txt
 Packages:  Pandas, xml.etree.ElementTree and re
6. Run the python file: python PizzaDatasetToXml.py
7. Deactivate virtual enviroment:
 - Move to: cd .\env\Scripts\
 - Finish: deactivate
