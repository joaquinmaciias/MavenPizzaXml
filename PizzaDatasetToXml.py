import pandas as pd
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom


def extract(csv_file:str) -> pd.DataFrame: # Extraemos los datos de los csv

    df = pd.read_csv(csv_file)

    return df

def transform_orders(df:pd.DataFrame): # Transformamos los datos de los dataframes

    pizza_rep = dict()
    df_pizza_quantity = df.loc[:,['pizza_id','quantity']] # Nos guardamos las columnas que nos interesan del dataframe
    list_pizza_quantity = df_pizza_quantity.values.tolist() # Pasamos el dataframe a una lista

    # Eliminamos con expresiones regulares el tamaño de la pizza que acompaña al nombre de la pizza

    for i in range(len(list_pizza_quantity)):
        list_pizza_quantity[i][0] = re.sub('_[a-z]$','',list_pizza_quantity[i][0])

    # Creamos un diccionario con claves los nombres de las pizzas y sus valores el número de veces que fueron pedidas.

    for i in range(len(list_pizza_quantity)):
        try:
            pizza_rep[list_pizza_quantity[i][0]] += 1
        except:
            pizza_rep[list_pizza_quantity[i][0]] = 1
    
    return pizza_rep
        
def transform_ingredients(df:pd.DataFrame,dict_orders:dict):

    dict_ingredients = dict()
    df_pizza_ingredients = df.loc[:,['pizza_type_id','ingredients']]
    list_pizza_ingredients = df_pizza_ingredients.values.tolist()

    for i in range(len(list_pizza_ingredients)):
        list_pizza_ingredients[i][1] = list_pizza_ingredients[i][1].replace(', ',',')
        list_pizza_ingredients[i][1] = re.findall(r'([^,]+)(?:,|$)', list_pizza_ingredients[i][1])
        # list_pizza_ingredients[i] = [nombre pizza,[ingrediente(1),...,ingrediente(k)]]

    for typepizza in range(len(list_pizza_ingredients)):

        for ingredients in range(len(list_pizza_ingredients[typepizza][1])):

            number_order_pizza = dict_orders[list_pizza_ingredients[typepizza][0]] # Numero de veces que se pedio la pizza con dicho ingrerdiente

            try:
                dict_ingredients[list_pizza_ingredients[typepizza][1][ingredients]] = number_order_pizza + dict_ingredients[list_pizza_ingredients[typepizza][1][ingredients]]
            except:
                dict_ingredients[list_pizza_ingredients[typepizza][1][ingredients]] = number_order_pizza

    # Ingredients semanales

    dict_ingredients_weekly = dict()

    for key in dict_ingredients:
  
        dict_ingredients_weekly[key] = dict_ingredients[key] / (365 / 7) # 365 dias entre 7, cada semana

    return dict_ingredients_weekly

def load(dictionary: dict): # Load on screen

    for key in dictionary:
        print(f'{key}: {int(dictionary[key])}')


def create_xml_tree(tree: ET.SubElement, dict_tree: dict, type:str):

    counter = 1

    if type == 'Pizza':

        for key in dict_tree:

            str_type = type + str(counter) + '\n'

            ET.SubElement(tree, str_type, Pizza = str(key)).text = str(dict_tree[key]) + '\n'

            counter += 1

    elif type == 'Ingredient':

        for key in dict_tree:

            str_type = type + ' ' + str(counter) + '\n'

            ET.SubElement(tree, str_type, Ingredients = str(key)).text = str(int(dict_tree[key])) + '\n'

            counter += 1


if __name__  == '__main__':

    # Seguiremos el preceso ETL

    # Extract
    order_details = extract('order_details.csv')
    pizzas = extract('pizzas.csv')
    pizza_types = extract('pizza_types.csv')

    # Transform
    dict_pizza_orders = transform_orders(order_details)
    dict_ingredients_weekly = transform_ingredients(pizza_types,dict_pizza_orders)

    # Load data on the screen

    print('\n')
    print('Número de pizzas pedidos --> \n')

    load(dict_pizza_orders)

    print('\n')
    print('Para stock de ingredientes deberian comprar a la semana -->')
    print('El consumo de cada ingredientes medio por semana es de: \n')

    load(dict_ingredients_weekly)

    # Create Xml file

    root = ET.Element("Maven Pizza") # Main tree


    pizzas = ET.SubElement(root,'Pizzas') # Pizza subtree
    ingredients = ET.SubElement(root,'Ingredientes') # Ingredients subtree

    
    create_xml_tree(pizzas, dict_pizza_orders, 'Pizza')
    create_xml_tree(ingredients, dict_ingredients_weekly, 'Ingredient')


    ET.ElementTree(root).write("MavenPizzaXml.xml")
