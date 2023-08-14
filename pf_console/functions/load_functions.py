from bs4 import BeautifulSoup

def load_categories(data_manager) -> {}:
    with open(data_manager.CATEGORIES_FILE, 'r') as categories_file:
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

