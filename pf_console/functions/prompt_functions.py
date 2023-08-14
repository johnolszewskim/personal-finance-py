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

        if ipt.did_input_yes(message='\nKeep?'):
            return console.next(splits)

        return


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

def prompt_refunded_budget_line(console, splits):
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


def prompt_vendor(console, splits):

    # input("prompt_vendor()") # for testing

    if suggest.did_accept_suggested_vendor(console, splits):
        console.next(splits)

    # input("RETURNED AFTER !did_accept_suggested_vendor()") # for testing

    while True:
        os.system('clear')
        prt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)

        i = "Costco" #ipt.input_vendor_name(console,splits)
        splits[console.bl_index].vendor = i
        console.new_raw_vendor = True

        return console.next(splits)


def prompt_category(console, splits):

    # input("prompt_category()") # for testing

    suggestion_index = -1

    while True:

        os.system('clear')
        suggestion_index = suggest.suggest_category(console,splits, last_index=suggestion_index)
        prt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        all_categories = prt.print_categories(console.dm)

        print('99: ADD CATEGORY/SUBCATEGORY')
        print()  # for formatting

        category_index = ipt.get_input_index(len(all_categories),
                                             message='Input category number. ENTER to select suggestion. n for next '
                                                     'suggestion: ',
                                             special_cases=['99','n'])
        if category_index == -1:
            console.next(splits)
        # elif category_index = '99'
        elif category_index == 'n':
            continue
        else:
            splits[console.bl_index].category = all_categories[category_index]
            console.next(splits)


# prompt custom category


def prompt_subcategory(console, splits):

    input('prompt_subcategory()')  # for testing

    suggestion_index = -1
    subcategories = console.dm.dict_categories_subcategories[splits[console.bl_index].category]

    while True:

        os.system('clear')
        suggestion_index = suggest.suggest_subcategory(console, splits, last_index=suggestion_index)
        prt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        print()
        subcategories = prt.print_subcategories(console, splits[console.bl_index].category)
        print('88: ADD CUSTOM SUBCATEGORY')
        print('99: REINPUT CATEGORY')
        print()  # for formatting

        subcategory_index = ipt.get_input_index(len(subcategories),
                                             message='Input subcategory number. ENTER to select suggestion. n for next '
                                                     'suggestion: ',
                                             special_cases=['88','99', 'n'])

        if subcategory_index == -1:
            console.next(splits)
        # elif category_index = '99'
        # elif category_index = '99'
        elif subcategory_index == 'n':
            continue
        else:
            splits[console.bl_index].subcategory = subcategories[subcategory_index]
            console.next(splits)
        # custom = False
        #
        # print()
        # if len(subcategories) == 0:
        #     print('No subcategories.')
        #     print('99: REINPUT CATEGORY')
        #     subcategory = input('\nInput custom subcategory: ')
        #     custom = True
        # else:
        #     for index, subcat in enumerate(subcategories):
        #         print(str(index) + ': ' + subcat)
        #     print('88: ADD CUSTOM SUBCATEGORY')
        #     print('99: REINPUT CATEGORY')
        #     subcategory = input('\nInput subcategory: ')
        # print()
        #
        # if subcategory == "":
        #     return 1
        # elif custom == True:
        #     splits[console.bl_index].subcategory = subcategory
        #     return 1
        # elif subcategory == '99':
        #     console.func_index = console.functions.index(console.prompt_category) - 1
        #     return 1
        # elif subcategory == '88':
        #     splits[console.bl_index].subcategory = input('\nInput custom subcategory: ')
        #     return 1
        # elif subcategory.isdigit() is not True:
        #     continue
        # elif (int(subcategory) < len(subcategories)) and (int(subcategory) >= 0):
        #     splits[console.bl_index].subcategory = subcategories[int(subcategory)]
        #     return 1