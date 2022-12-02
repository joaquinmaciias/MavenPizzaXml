import pandas as pd
import re, operator
import xml.etree.ElementTree as ET

def details_csv(df_name:str,df: pd.DataFrame):

    # Analisis calidad de los datos

    print(f'CSV name is: {df_name} -->\n')

    print(df.info())
    print('\n')

    print(df.head(10))
    print('\n')

    print('Dimensiones del Csv\n')

    print(df.shape)
    print('\n')

    print('Columnas del Csv\n')

    print(df.columns)
    print('\n')

    print('Datos nulos del Csv\n')

    print(df.isnull().sum())

    print('\n')

    print('----------------------------------------------------------')


def extract(csv_file: str, sep: str) -> pd.DataFrame:  # Extraemos los datos de los csv

    df = pd.read_csv(csv_file, sep = sep)

    return df

def clear_data(df:pd.DataFrame):

    df = df.dropna()

    return df

def transform_orders(df: pd.DataFrame):  # Transformamos los datos de los dataframes

    pizza_rep = dict()
    df_pizza_quantity = df.loc[:, ['pizza_id', 'quantity']]  # Nos guardamos las columnas que nos interesan del dataframe
    list_pizza_quantity = df_pizza_quantity.values.tolist()  # Pasamos el dataframe a una lista

    # Eliminamos con expresiones regulares el tamaño de la pizza que acompaña al nombre de la pizza


    for i in range(len(list_pizza_quantity)):

        list_pizza_quantity[i][1] = re.sub("One","1",list_pizza_quantity[i][1])
        list_pizza_quantity[i][1] = re.sub("one","1",list_pizza_quantity[i][1])
        list_pizza_quantity[i][1] = re.sub("-1","1",list_pizza_quantity[i][1])
        list_pizza_quantity[i][1] = re.sub("two","2",list_pizza_quantity[i][1])
        list_pizza_quantity[i][1] = re.sub("Two","2",list_pizza_quantity[i][1])

        list_pizza_quantity[i][0] = re.sub("[ -]","_", list_pizza_quantity[i][0])
        list_pizza_quantity[i][0] = re.sub("@","a", list_pizza_quantity[i][0])
        list_pizza_quantity[i][0] = re.sub("0","o", list_pizza_quantity[i][0])
        list_pizza_quantity[i][0] = re.sub(" ","_", list_pizza_quantity[i][0])
        list_pizza_quantity[i][0] = re.sub("3","e", list_pizza_quantity[i][0])
        list_pizza_quantity[i][0] = re.sub('_[a-z]$', '', list_pizza_quantity[i][0])


    # Creamos un diccionario con claves los nombres de las pizzas y sus valores el número de veces que fueron pedidas.

    for i in range(len(list_pizza_quantity)):
        try:
            pizza_rep[list_pizza_quantity[i][0]] += 1
        except:
            pizza_rep[list_pizza_quantity[i][0]] = 1

    return pizza_rep


def transform_ingredients(df: pd.DataFrame, dict_orders:dict):

    dict_ingredients = dict()
    df_pizza_ingredients = df.loc[:, ['pizza_type_id','ingredients']]
    list_pizza_ingredients = df_pizza_ingredients.values.tolist()

    for i in range(len(list_pizza_ingredients)):
        list_pizza_ingredients[i][1] = list_pizza_ingredients[i][1].replace(', ', ',')
        list_pizza_ingredients[i][1] = re.findall(r'([^,]+)(?:,|$)', list_pizza_ingredients[i][1])
        # list_pizza_ingredients[i] = [nombre pizza,[ingrediente(1),...,ingrediente(k)]]

    for typepizza in range(len(list_pizza_ingredients)):

        for ingredients in range(len(list_pizza_ingredients[typepizza][1])):

            number_order_pizza = dict_orders[list_pizza_ingredients[typepizza][0]]  # Numero de veces que se pedio la pizza con dicho ingrerdiente

            try:
                dict_ingredients[list_pizza_ingredients[typepizza][1][ingredients]] = number_order_pizza + dict_ingredients[list_pizza_ingredients[typepizza][1][ingredients]]
            except:
                dict_ingredients[list_pizza_ingredients[typepizza][1][ingredients]] = number_order_pizza

    return dict_ingredients

def load(dictionary: dict):

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

    date_orders = extract('orders.csv',';')
    order_details = extract('order_details.csv',';')
    pizzas = extract('pizzas.csv',',')
    pizza_types = extract('pizza_types.csv',',')

    # Analisis

    details_csv('orders.csv',date_orders)
    details_csv('order_details.csv',order_details)
    details_csv('pizzas.csv',pizzas)
    details_csv('pizza_types.csv',pizza_types)

    # Clear data

    date_orders_clean = clear_data(date_orders)
    order_details_clean = clear_data(order_details)
    pizzas_clean = clear_data(pizzas)
    pizza_types_clean = clear_data(pizza_types)

    
    # Transform
    
    dict_pizza_orders = transform_orders(order_details_clean)
    dict_ingredients_anual = transform_ingredients(pizza_types_clean,dict_pizza_orders)
    
    # Ingredients semanales

    dict_ingredients_weekly = dict()

    for key in dict_ingredients_anual:

        dict_ingredients_weekly[key] = dict_ingredients_anual[key] / 12 * 4

    # Load data on the screen

    print('\n')
    print('Número de pizzas pedidos --> \n')

    load(dict_pizza_orders)

    print('\n')
    print('Top 5 pizzas pedidas -->\n')

    top_pizzas = sorted(dict_pizza_orders.items(), key=operator.itemgetter(1), reverse=True) # Sorted diccionary

    for i in range(1,6):

        print(f'Top {i} pizza: Pizza {top_pizzas[i - 1][0]} {int(top_pizzas[i - 1][1])}')

    print('\n')
    print('Para stock de ingredientes deberian comprar a la semana -->')
    print('El consumo de cada ingredientes medio por semana es de: \n')

    load(dict_ingredients_weekly)

    print('\n')
    print('Top 5 ingredientes utilizados -->\n')

    top_ingredients = sorted(dict_ingredients_weekly.items(), key=operator.itemgetter(1), reverse=True) # Sorted diccionary

    for i in range(1,6):

        print(f'Top {i} Ingrediente: {top_ingredients[i - 1][0]} {int(top_ingredients[i - 1][1])}')

    print('\n')

    # Create Xml file

    root = ET.Element("Maven Pizza") # Main tree


    pizzas = ET.SubElement(root,'Pizzas') # Pizza subtree
    ingredients = ET.SubElement(root,'Ingredientes') # Ingredients subtree

    
    create_xml_tree(pizzas, dict_pizza_orders, 'Pizza')
    create_xml_tree(ingredients, dict_ingredients_weekly, 'Ingredient')


    ET.ElementTree(root).write("MavenPizzaXml.xml")
