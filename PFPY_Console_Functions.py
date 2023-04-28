import pandas as pd

import PersonalFinancePYData
import PersonalFinancePYData as data
import os
import BudgetLine as bl
import csv
def input_transaction(transaction_id, date, vendor, amount) -> bl.BudgetLine:
    # os.system('clear')
    new_vendor=input_vendor(date, vendor)
    os.system('clear')
    new_category=input_category(date, vendor)
    os.system('clear')
    new_subcategory=input_subcategory(date, new_vendor, new_category)
    os.system('clear')

    print(date + '\t' + vendor + '\t' + new_category + '\t' + new_subcategory + '\t$' + str(amount) + '\n')
    new_tag = '#' + input("Input Tag: ")
    os.system('clear')

    print(date + '\t' + vendor + '\t' + new_category + '\t' + new_subcategory + '\t$' + str(amount) + '\t' + new_tag + '\n')
    new_notes = input('Notes:' )
    os.system('clear')

    print(date + '\t' + vendor + '\t' + new_category + '\t' + new_subcategory + '\t$' + str(amount) + '\t' + new_tag + '\t' + new_notes + '\n')
    print()
    save = input_save()
    os.system('clear')

    if save == True:
        return bl.BudgetLine(transaction_id, new_vendor, new_category, new_subcategory, amount, new_tag, new_notes)

def input_vendor(date, vendor) -> str:
    for v in data.bs_vendors:
        print(v.attrs)
    loop = True
    while loop is True:
        print()
        print(date + '\t' + vendor)
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

    # data = [{
    #
    #     'Transaction ID': b_l.transaction_id,
    #     'Vendor': b_l.vendor,
    #     'Category': b_l.category,
    #     'Subcategory': b_l.subcategory,
    #     'Amount': b_l.amount,
    #     'Tag': b_l.tag,
    #     'Notes': b_l.notes}]
    # df = pd.DataFrame(data)
    # df.to_csv('/Users/johnmatthew/Documents/Personal Finance/0. PersonalFinancePY/BUDGET_TRANSACTIONS_PersonalFinancePY.csv')
