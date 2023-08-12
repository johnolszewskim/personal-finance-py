import os
import calendar
import pf_console.functions.print_functions as prt
import pf_console.functions.input_functions as ipt
import pf_console.functions.suggest_functions as suggest


def prompt_account(df_accounts) -> str:
    while True:

        os.system('clear')

        for i, k in df_accounts.iterrows():
            print(f'{str(i):>7}' + ': ' + k.Name)

        # input_acct = input('\nSelect account: ')
        input_acct = '22009'

        if not input_acct.isdigit():
            continue
        if input_acct in df_accounts.index:
            return input_acct
        else:
            continue


def prompt_month(new_statement_filename) -> int:

    filename = new_statement_filename[new_statement_filename.rindex('/'):]
    month = int(filename[1:filename.find('.')])

    while True:

        os.system('clear')
        input_month = input('Closing Date: ' + calendar.month_name[month] + '\nInput month or ENTER to keep: ')

        if input_month == "":
            return month
        if not input_month.isdigit():
            continue
        if int(input_month) < 0:
            continue
        if int(input_month) > 12:
            continue

        return int(input_month)


def prompt_keep(console, splits):

    while True:
        os.system('clear')
        prt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        response = input('Keep? y or n? ')

        if response == 'y':
            console.next(splits)
        elif response == 'n':
            return 0


def prompt_refund(console, splits):

    if console.splitting:
        console.next(splits)

    if splits[console.bl_index].get_amount() < 0:

        while True:
            os.system('clear')
            prt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
            response = input('Is this transaction a refund? y or n? ')

            if response == 'y':
                return prompt_refunded_budget_line(splits)
            if response == 'n':
                return console.next(splits)

    return console.next(splits)

def prompt_refunded_budget_line(console, splits) -> int:
    os.system('clear')
    dict_index_tid = {}
    for index, tid in enumerate(list(console.dict_budget_lines.keys())):
        temp = console.dict_budget_lines[tid]
        print(f'{index:<5}{str(temp[0])}')
        dict_index_tid[index] = tid
    print('99: not listed')

    while True:
        bl_index = input('Input line to refund: ')
        if not bl_index.isdigit():
            continue
        bl_index = int(bl_index)
        if bl_index == 99:
            return console.next()
        elif (bl_index > len(dict_index_tid)) and (bl_index >= 0):
            continue
        else:
            splits[console.bl_index].vendor = console.dict_budget_lines[dict_index_tid[bl_index]][0].vendor
            splits[console.bl_index].category = console.dict_budget_lines[dict_index_tid[bl_index]][0].category
            splits[console.bl_index].subcategory = console.dict_budget_lines[dict_index_tid[bl_index]][0].subcategory
            splits[console.bl_index].tag = 'REFUND'
            splits[console.bl_index].notes = str(console.dict_budget_lines[dict_index_tid[bl_index]][0].transaction_id)

            console.print_splits(splits)
            console.func_index = console.functions.index(console.prompt_save) - 1
            return console.next(splits)

def prompt_autocomplete(console, splits) -> int:

    input("prompt_autocomplete()")





    potential_splits = console.create_potential_budget_lines(splits, matching_vendors)

    for index, bl in enumerate(potential_splits):

        while True:
            os.system('clear')
            console.print_splits(splits)
            console.print_splits(potential_splits, index, False)
            complete = input('Complete? y or n? ')

            if complete == 'y':
                splits[console.bl_index].vendor = bl.vendor
                splits[console.bl_index].category = bl.category
                splits[console.bl_index].subcategory = bl.subcategory
                splits[console.bl_index].tag = bl.tag
                splits[console.bl_index].notes = bl.notes
                console.func_index = console.functions.index(console.prompt_amount) - 1
                return console.next(splits)
            if complete == 'n':
                break

    return console.next(splits)


def prompt_vendor(console, splits) -> int:

    input("prompt_vendor()")

    suggest.suggest_vendor(console, splits)

    input("RETURNED AFTER NO SUGGESTIONS")

    while True:
        os.system('clear')
        prt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)

        i = ipt.input_vendor_name(console,splits)
        splits[console.bl_index].vendor = i

        return console.next(splits)


def prompt_category(console, splits) -> int:

    input("prompt_category()")

    categories = sorted(console.dm.dict_categories.keys())

    while True:

        os.system('clear')
        prt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        prt.print_categories(console.PRINT_CATEGORY_ROWS)

        print('99: ADD CATEGORY/SUBCATEGORY')
        print()

        category_index = input('Input category: ')
        if category_index == '':
            return 2
        if not category_index.isdigit():
            continue
        category_index = int(category_index)
        if category_index == 99:
            return 1
        if (category_index < len(categories)) and (category_index >= 0):
            splits[console.bl_index].category = categories[category_index]
            return 2