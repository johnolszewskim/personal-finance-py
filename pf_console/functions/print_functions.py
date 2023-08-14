from colorama import Fore, Style

def print_splits(splits, statement_index, statement_length, bl_index, mark_index=None, print_statement_index=True):
    if print_statement_index:
        print('(' + str(statement_index + 1) + ',' + str(statement_length) + ')')

    if len(splits) == 1:
        print(' ' + str(splits[0]))
        return

    if mark_index != None:
        for i, b_l in enumerate(splits):
            if i == mark_index:
                print('-' + str(b_l))
            else:
                print(Fore.WHITE + ' ' + str(b_l) + Style.RESET_ALL)

    else:
        for i, b_l in enumerate(splits):
            if i == bl_index:
                print('-' + str(b_l))
            else:
                print(' ' + str(b_l))


def print_categories(console) -> []:

    lines = ['','','','','','','','','','']
    categories = []

    print()
    for b in console.dict_budget_categories.keys():
        lines[0] = lines[0] + "\033[1m" + f'{b:20}\t' + "\033[0m"
        for i,c in enumerate(console.dict_budget_categories[b]):
            categories = categories + [c]
            lines[i+1] = lines[i+1] + str(len(categories)-1) + '. ' + f'{c:19}\t'

    for l in lines:
        print(l)

    return categories

def print_subcategories(console, category) -> []:

    subcategories = []

    for index, subcategory in enumerate(console.dm.dict_categories_subcategories[category]):
        subcategories = subcategories + [subcategory]
        print(str(index) + ': ' + subcategory)

    return subcategories