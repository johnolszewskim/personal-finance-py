import pandas as pd

import PersonalFinancePYData
import PersonalFinancePYData as data
import os
import BudgetLine as bl
import csv
import PersonalFinancePYXML as pfxml
import datetime
def map_import_transactions(import_transactions, bank, statement_id) -> pd.DataFrame:
    new_transactions = pd.DataFrame(columns=data.transaction_column_map.keys())

    new_transactions['Date'] = import_transactions[data.transaction_column_map['Date'][bank]]
    new_transactions['Vendor'] = import_transactions[data.transaction_column_map['Vendor'][bank]]
    new_transactions['Amount'] = import_transactions[data.transaction_column_map['Amount'][bank]]
    new_transactions['Transaction ID'] = new_transactions.index

    new_transactions.set_index('Transaction ID')

    return new_transactions
def import_single_transaction(budget_line) -> bl.BudgetLine:
    result = get_autocomplete(budget_line)
    raw_vendor = budget_line.vendor

    autocompleted=True
    if result is None:
        autocompleted=False

    os.system('clear')
    if result is None:
        result=budget_line
        os.system('clear')
        result.vendor=input_vendor(result)
        os.system('clear')
        input_categories=prompt_categories(result)

        if input_categories[0] in pfxml.category_dict:
            pfxml.category_dict[input_categories[0]].append(input_categories[1])
        else:
            pfxml.category_dict[input_categories[0]] = [input_categories[1]]
        print(pfxml.category_dict)
        result.category=input_categories[0]
        result.subcategory=input_categories[1]
        os.system('clear')

    print(result)
    result.tag = '#' + input("Input Tag: ")
    os.system('clear')

    print(result)
    result.notes = input('Notes:' )
    os.system('clear')

    print(result)
    print()
    save = input_save()
    os.system('clear')

    if save == 'y':
        write_budget_line(result)
        # check if the vendor value is already in file
        if autocompleted is False:
            pfxml.add_new_vendor(raw_vendor, result)
        return result

    return None

def get_autocomplete(budget_line) -> bl.BudgetLine:
    matching_vendors = pfxml.vendors_data.find_all('vendor', {'name': budget_line.vendor.replace(' ', '').replace(u'\xa0', '')})
    potential_bl = budget_line.copy()

    for v in matching_vendors:

        potential_bl.vendor = v.contents[0].strip()
        potential_bl.category = v.find_all('category')[0].contents[0].strip()
        potential_bl.subcategory = v.find_all('subcategory')[0].contents[0].strip()
        print(potential_bl)
        complete=input('Complete? y or n? ')

        if complete == 'y':
            return potential_bl

    return None
def input_vendor(budget_line) -> str:
    loop = True
    while loop is True:
        print(budget_line)
        print()
        i = input('Input vendor | ENTER to keep | l for vendor list: ')

        if i == '':
            print()
            return budget_line.vendor
        elif i == 'l':
            print()
            if budget_line.vendor in data.vendors:
                print('0. ' + data.vendors[budget_line.vendor])
            for index, v in enumerate(data.vendors.values()):
                print(v)
        elif i == '0':
            print()
            return data.vendors[budget_line.vendor]
        elif i == 'x':
            return
        else:
            return i

def prompt_categories(budget_line) -> (str,str):

    categories = list(pfxml.category_dict.keys())

    while True:
        print(budget_line)
        print_categories(8)
        print('99: ADD CATEGORY/SUBCATEGORY')
        print()

        valid_input = False
        input_category = ''

        while not valid_input:
            category_index = input('Input category: ')
            if not category_index.isdigit():
                continue
            category_index = int(category_index)
            print()
            if category_index == 99:
                return prompt_custom_category_subcategory()
            if (category_index < len(categories)) and (category_index >= 0):
                input_category = categories[category_index]
                valid_input = True

        input_subcategory = prompt_subcategory(input_category, budget_line)
        if input_subcategory != '':
            return (input_category,input_subcategory)
        os.system('clear')

def prompt_subcategory(category, budget_line) -> str:
    os.system('clear')
    print(budget_line)
    subcategories = pfxml.category_dict[category]

    for index, s in enumerate(subcategories):
        print(str(index) + ': ' + s)
    print('ENTER: reselect category')
    print()
    while True:
        subcategory_index = input('Input subcategory: ')
        print()
        if subcategory_index == '':
            return ''
        if (int(subcategory_index) < len(subcategories)) and (int(subcategory_index) >= 0):
            return subcategories[int(subcategory_index)]

def prompt_custom_category_subcategory() -> (str,str):
    os.system('clear')
    while True:
        custom_category=input('Input custom category: ')
        custom_subcategory=input('Input custom subcategory: ')
        print(custom_category + ',' + custom_subcategory)

        valid_response = False
        while not valid_response:
            keep = input('Keep? y or n? ')
            if keep == 'y':
                return (custom_category, custom_subcategory)
            if keep == 'n':
                valid_response = True


def input_save() -> str:

    while True:
        return input('Save? y or n? ')

def write_budget_line(b_l):
    d = {
        'Transaction ID': b_l.transaction_id,
        'Vendor': b_l.vendor,
        'Category': b_l.category,
        'Subcategory': b_l.subcategory,
        'Amount': b_l.amount,
        'Tag': b_l.tag,
        'Notes': b_l.notes}
    FILENAME='/Users/johnmatthew/Documents/Personal Finance/0. PersonalFinancePY/BUDGET_TRANSACTIONS_PersonalFinancePY.csv'
    with open(FILENAME, 'a') as file:
        dict_obj=csv.DictWriter(file, fieldnames=PersonalFinancePYData.budget_col_names)
        dict_obj.writerow(d)

def print_categories(rows):
    lines =['','','','']
    for r,cat in enumerate(pfxml.category_dict.keys()):
        lines[r%4]=lines[r%4] + str(r) + ': ' + cat + '\t'

    for l in lines:
        print(l)