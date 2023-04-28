import pandas as pd

import PersonalFinancePYData
import PersonalFinancePYData as data
import os
import BudgetLine as bl
import csv
import PersonalFinancePYXML as pfxml
def input_transaction(transaction_id, date, vendor, amount) -> bl.BudgetLine:
    result = get_autocomplete(transaction_id, date, vendor, amount)

    autocompleted=False
    if result != None:
        autocompleted=True

    os.system('clear')
    if result is None:
        result=bl.BudgetLine(transaction_id, date, vendor, "", amount, "", "")
        os.system('clear')
        result.vendor=input_vendor(date,vendor)
        os.system('clear')
        result.category=input_category(date, result.vendor)
        os.system('clear')
        result.subcategory=input_subcategory(date, result.vendor, result.category)
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

    if save == True:
        # check if the vendor value is already in file
        if autocompleted == False:
            pfxml.add_new_vendor(vendor, result)
        return result

def get_autocomplete(transaction_id, date, vendor,amount) -> bl.BudgetLine:
    matching_vendors = pfxml.bs_data.find_all('vendor', {'name': vendor.replace(' ','').replace(u'\xa0','')})

    for v in matching_vendors:
        potential_bl = bl.BudgetLine(transaction_id, vendor, '', "", "", amount, "")
        potential_bl.vendor = v.contents[0].strip()
        potential_bl.category = v.find_all('category')[0].contents[0]
        potential_bl.subcategory = v.find_all('subcategory')[0].contents[0]
        print(potential_bl)
        complete=input('Complete? y or n? ')

        if complete == 'y':
            return potential_bl

    return None
def input_vendor(date, vendor) -> str:
    loop = True
    while loop is True:
        print(date + '\t' + vendor)
        print()
        i = input('Input vendor | ENTER to keep | l for vendor list: ')

        if i == '':
            print()
            return vendor
        elif i == 'l':
            print()
            if vendor in data.vendors:
                print('0. ' + data.vendors[vendor])
            for index, v in enumerate(data.vendors.values()):
                print(v)
        elif i == '0':
            print()
            return data.vendors[vendor]
        elif i == 'x':
            return
        else:
            return i

def input_category(date, vendor) -> str:

    print(date + '\t' + vendor + '\n')
    categories = [key for key in data.category_lookup]

    for index, c in enumerate(categories):
        print(str(index) + ': ' + c)

    print()
    while True:
        category_index = int(input('Input category: '))
        print()
        if category_index < len(categories):
            return categories[int(category_index)]

def input_subcategory(date, vendor, category) -> str:
    print(date + '\t' + vendor + '\t' + category + '\n')
    subcategories = data.category_lookup[category]

    for index, s in enumerate(subcategories):
        print(str(index) + ': ' + s)

    print()
    while True:
        subcategory_index = int(input('Input subcategory: '))
        print()
        if subcategory_index < len(subcategories):
            return subcategories[int(subcategory_index)]

def input_save() -> bool:

    while True:
        save = input('Save? y or n? ')
        if save == 'y':
            return True
        if save == 'n':
            return False

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