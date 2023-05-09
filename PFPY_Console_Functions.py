import pandas as pd

import PersonalFinancePYData
import PersonalFinancePYData as data
import os
import BudgetLine as bl
import csv
import PersonalFinancePYXML as pfxml
import datetime
def map_import_transactions(i_t, bank, statement_id) -> pd.DataFrame:
    new_transactions = pd.DataFrame(columns=data.transaction_column_map.keys())

    new_transactions['Date'] = i_t[data.transaction_column_map['Date'][bank]]
    new_transactions['Date'] = pd.to_datetime(new_transactions['Date'])
    new_transactions.sort_values(by='Date', inplace=True)
    new_transactions['Vendor'] = i_t[data.transaction_column_map['Vendor'][bank]]
    new_transactions['Amount'] = i_t[data.transaction_column_map['Amount'][bank]]
    if data.transaction_column_map['Amount Sign'][bank] == '-':
        new_transactions['Amount'] = -new_transactions['Amount']
    new_transactions.reset_index(drop=True, inplace=True)
    new_transactions['Transaction ID'] = new_transactions.index
    new_transactions['Transaction ID'] = new_transactions['Transaction ID'].astype(str) + statement_id

    return new_transactions

def import_single_transaction(b_l, bl_file) -> bl.BudgetLine:
    raw_vendor = b_l.vendor  # save raw vendor for saving before it's changed
    autocompleted = autocomplete(b_l)

    os.system('clear')
    if autocompleted is False:
        os.system('clear')
        input_vendor(b_l)
        os.system('clear')

        input_categories=prompt_categories(b_l)

        if input_categories[0] in pfxml.category_dict:
            pfxml.category_dict[input_categories[0]].append(input_categories[1])
        else:
            pfxml.category_dict[input_categories[0]] = [input_categories[1]]
        print(pfxml.category_dict)
        b_l.category=input_categories[0]
        b_l.subcategory=input_categories[1]
        os.system('clear')

    print(b_l)
    b_l.tag = '#' + input("Input Tag: ")
    os.system('clear')

    print(b_l)
    b_l.notes = 'NOTES: ' + input('Notes:' )
    os.system('clear')

    print(b_l)
    print()
    bl_was_saved = save_appropriately(b_l, bl_file, autocompleted)
    os.system('clear')

    # check if the BudgetLine was saved
    if bl_was_saved:
        pfxml.add_new_vendor(raw_vendor, b_l)

def autocomplete(b_l) -> bool:
    matching_vendors = pfxml.vendors_data.find_all('vendor', {'name': b_l.vendor.replace(' ', '').replace(u'\xa0', '')})
    potential_bl = b_l.copy()

    for v in matching_vendors:

        potential_bl.vendor = v.contents[0].strip()
        potential_bl.category = v.find_all('category')[0].contents[0].strip()
        potential_bl.subcategory = v.find_all('subcategory')[0].contents[0].strip()
        print(b_l)
        print(potential_bl)
        complete=input('Complete? y or n? ')

        if complete == 'y':
            b_l.vendor = potential_bl.vendor
            b_l.category = potential_bl.category
            b_l.subcategory = potential_bl.subcategory

            return True

    return False
def input_vendor(b_l):
    vendor_dict = pfxml.get_vendor_dict()
    vendor_set = set(vendor_dict.values())
    while True:
        print(b_l)
        print()
        i = input('Input vendor | ENTER to keep | v for vendor list: ').strip()

        if i == 'v':
            print()
            for index, v in enumerate(vendor_set):
                print(str(index) + '. ' + v)
            print()
        elif i.isdigit():
            print()
            b_l.vendor = list(vendor_set)[int(i)]
            return
        elif i == 'x':
            return
        else:
            b_l.vendor = i
            return
def prompt_categories(budget_line) -> (str,str):

    categories = list(pfxml.category_dict.keys())

    while True:

        valid_input = False
        input_category = ''

        while not valid_input:
            os.system('clear')
            print(budget_line)
            print_categories(8)
            print('99: ADD CATEGORY/SUBCATEGORY')
            print()

            category_index = input('Input category: ')
            if not category_index.isdigit():
                continue
            category_index = int(category_index)
            print()
            if category_index == 99:
                return prompt_custom_category_subcategory()
            if (category_index < len(categories)) and (category_index >= 0):
                input_category = categories[category_index]
                input_subcategory = prompt_subcategory(input_category, budget_line)

                if input_subcategory == '99':
                    continue
                return (input_category,input_subcategory)
                os.system('clear')

def prompt_subcategory(category, budget_line) -> str:
    os.system('clear')
    print(budget_line)
    subcategories = pfxml.category_dict[category]

    for index, s in enumerate(subcategories):
        print(str(index) + ': ' + s)
    print('99: reselect category')
    print()
    while True:
        subcategory_index = input('Input subcategory: ')
        print()
        if subcategory_index.isdigit() is not True:
            continue
        if subcategory_index == '99':
            return '99'
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

def save_appropriately(b_l: bl.BudgetLine, bl_file, auto):

    save_response = ''
    while (save_response != 'y'):# or (save_response != 'n'):
        save_response = input('Save? y or n? ')

    if save_response == 'y':
        write_budget_line(b_l, bl_file)
        return True

    return False

def write_budget_line(b_l, bl_file):
    d = {
        'Transaction ID': b_l.transaction_id,
        'Vendor': b_l.vendor,
        'Category': b_l.category,
        'Subcategory': b_l.subcategory,
        'Amount': b_l.amount,
        'Tag': b_l.tag,
        'Notes': b_l.notes}
    with open(bl_file, 'a') as file:
        dict_obj=csv.DictWriter(file, fieldnames=PersonalFinancePYData.budget_col_names)
        dict_obj.writerow(d)

def print_categories(rows):
    lines =['','','','']
    for r,cat in enumerate(sorted(pfxml.category_dict.keys())):
        lines[r%4]=lines[r%4] + str(r) + ': ' + cat + '\t'

    for l in lines:
        print(l)