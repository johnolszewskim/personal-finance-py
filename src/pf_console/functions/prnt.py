import os
import pandas as pd
from colorama import Fore, Style
import src.pf_console.functions.input as inpt

pd.options.display.max_rows = 1000


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

    lines = ['','','','','','','','','','','']
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

    if category not in console.dm.dict_categories_subcategories:
        return subcategories

    for index, subcategory in enumerate(console.dm.dict_categories_subcategories[category]):
        subcategories = subcategories + [subcategory]
        print(str(index) + ': ' + subcategory)

    return subcategories

def print_all_element(console, splits, element):

    os.system('clear')
    print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
    print()

    if element not in console.dm.df_budget_lines.columns:
        return

    df_element = console.dm.df_budget_lines[element]
    df_element = df_element.drop_duplicates()
    df_element.reset_index(drop=True, inplace=True)

    for i,e in enumerate(df_element):
        print(f"{str(i):>3}: {e:10}")
    print()

    element_to_see_index = inpt.input_index(console, splits, len(df_element),
                                            message='*(text) to search for ' + element + ' containing or input index to see all transactions with ' + element + ': ',
                                            special_cases=['*'],
                                            special_cases_just_starts_with=True)

    if not element_to_see_index:
        return
    if str(element_to_see_index).startswith('*'):
        print_all_with_element_value(console, splits, element, element_to_see_index, contains=True)  # element_to_see_index is a '*asdfjk'
    else:
        print_all_with_element_value(console, splits, element, df_element[int(element_to_see_index)])


def print_all_with_element_value(console, splits, element, value, contains=False):

    os.system('clear')
    print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
    print()
    if contains:
        value_str = str(value)
        value_str = value_str[1:]

        print(console.dm.df_budget_lines[console.dm.df_budget_lines[element].str.contains(value_str)])
    else:
        print(console.dm.df_budget_lines.loc[console.dm.df_budget_lines[element] == value])

    input('\nENTER to return.')


def print_budgets(console, splits):

    for i,b in enumerate(console.dm.dict_budget_categories.keys()):
        print(f"{str(i):>3}: {b:10}")
    print()