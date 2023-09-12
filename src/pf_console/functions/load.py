from bs4 import BeautifulSoup
import src.pf_console.datasets as datasets
import pandas as pd


def load_categories(data_manager) -> {}:

    with open(datasets.get_categories(), 'r') as categories_file:
        categories_str = categories_file.read()

    data_manager.data_categories = BeautifulSoup(categories_str, 'xml')
    categories = data_manager.data_categories.find_all('category')

    for c in categories:
        cat = c['name']
        data_manager.dict_categories_subcategories[cat] = []
        subcategories = c.find_all('subcategory')
        for sc in subcategories:
            data_manager.dict_categories_subcategories[cat] = data_manager.dict_categories_subcategories[cat] + [sc['name']]

        b = c['budget']
        b = b.replace('_', ' ')
        if b not in data_manager.dict_budget_categories:
            data_manager.dict_budget_categories.update({b: [cat]})
        else:
            data_manager.dict_budget_categories[b] = data_manager.dict_budget_categories[b] + [cat]

def load_raw_vendor_to_vendor() -> pd.DataFrame:

    try:
        result = pd.read_csv(datasets.get_raw_vendor_to_vendor(), index_col=['index'])

    except Exception:

        result = pd.DataFrame(columns=['raw_vendor', 'vendor'])

    return result


def load_csv(file_name, new_columns) -> pd.DataFrame:
    try:
        result = pd.read_csv(file_name, header=0, index_col=['index'])
        result = result.fillna('')

    except Exception:

        result = pd.DataFrame(columns=new_columns)

    return result
