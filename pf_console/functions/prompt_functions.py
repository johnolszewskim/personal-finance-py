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

        if ipt.did_input_yes(console, splits, message='\nKeep?'):
            return console.next(splits)

        return


def prompt_refund(console, splits):
    if console.splitting:
        console.next(splits)

    if splits[console.bl_index].input_amount() < 0:

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


def prompt_vendor(console, splits):
    # input("prompt_vendor()") # for testing

    if suggest.did_accept_suggested_vendor(console, splits):
        console.next(splits)

    # input("RETURNED AFTER !did_accept_suggested_vendor()") # for testing

    while True:
        os.system('clear')
        prt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)

        i = "Costco"  # ipt.input_vendor_name(console,splits)
        splits[console.bl_index].vendor = i
        console.new_raw_vendor = True

        return console.next(splits)


def prompt_category(console, splits):
    # input("prompt_category()") # for testing

    suggestion_index = -1
    will_suggest = True

    while True:

        os.system('clear')
        suggestion_index = suggest.suggest_category(console, splits, last_index=suggestion_index)
        if suggestion_index == -1:  # if there are no suggestions
            will_suggest = False

        prt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        all_categories = prt.print_categories(console.dm)

        print('99: ADD CATEGORY/SUBCATEGORY\n')

        if will_suggest:
            category_index = ipt.input_index(console, splits, len(all_categories),
                                             message='Input category number. ENTER to select suggestion. \'n\' for next suggestion: ',
                                             special_cases=['99', 'n'])
        else:
            category_index = ipt.input_index(console, splits, len(all_categories),
                                             message='No suggestions. Input category number: ',
                                             special_cases=['99'])
        if not category_index:  # user hit enter
            console.next(splits, to_func_index=console.functions.index(prompt_subcategory))
        elif category_index == '99':  # add new category
            console.next(splits, to_func_index=console.functions.index(prompt_add_category))
        elif category_index == 'n':  # n is returned as input
            continue
        else:  # if category is selected by index
            splits[console.bl_index].category = all_categories[category_index]
            console.next(splits)


def prompt_add_category(console, splits):
    while True:

        os.system('clear')
        prt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        all_categories = prt.print_categories(console.dm)
        print('99: RETURN TO CHOOSE CATEGORY\n')

        new_category_name = ipt.get_custom_input(console, splits, message='Input new category name: ',
                                                 special_cases=['99'])

        #if not new_category name # user hit enter
        # check to make sure theres a category before accepting enter
        if new_category_name == '99':
            console.next(splits, to_func_index=console.functions.index(prompt_category))
        splits[console.bl_index].category = new_category_name
        console.next(splits, to_func_index=console.functions.index(prompt_subcategory))


def prompt_subcategory(console, splits):
    # input('prompt_subcategory()')  # for testing

    suggestion_index = -1
    will_suggest = True

    while True:

        os.system('clear')
        suggestion_index = suggest.suggest_subcategory(console, splits, last_index=suggestion_index)
        if suggestion_index == -1:  # if there are no suggestions
            will_suggest = False

        prt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        print()

        subcategories = prt.print_subcategories(console, splits[console.bl_index].category)

        if not subcategories:
            console.next(splits, to_func_index=console.functions.index(prompt_add_subcategory))

        print('88: ADD SUBCATEGORY')
        print('99: REINPUT CATEGORY')
        print()  # for formatting

        if will_suggest:
            subcategory_index = ipt.input_index(console, splits, len(subcategories),
                                                message='Input subcategory number. ENTER to select suggestion. n for next suggestion: ',
                                                special_cases=['88', '99', 'n'])
        else:
            subcategory_index = ipt.input_index(console, splits, len(subcategories),
                                                message='No suggestions. Input subcategory index: ',
                                                special_cases=['88', '99'])

        if not subcategory_index:
            console.next(splits, to_func_index=console.functions.index(prompt_amount))
        elif subcategory_index == '88':
            console.next(splits, to_func_index=console.functions.index(prompt_add_subcategory))
        elif subcategory_index == '99':
            console.next(splits, to_func_index=console.functions.index(prompt_category))
        elif subcategory_index == 'n':
            continue
        else:
            splits[console.bl_index].subcategory = subcategories[subcategory_index]
            console.next(splits)


def prompt_add_subcategory(console, splits):
    while True:

        os.system('clear')
        prt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        print('99: RETURN TO CHOOSE CATEGORY')
        print()  # for formatting

        new_subcategory_name = ipt.get_custom_input(console, splits, message='Input new subcategory name: ',
                                                    special_cases=['99'])

        #if not new_category name # user hit enter
        # check to make sure theres a category before accepting enter
        if new_subcategory_name == '99':
            console.next(splits, to_func_index=console.functions.index(prompt_category))
        splits[console.bl_index].subcategory = new_subcategory_name
        console.next(splits, to_func_index=console.functions.index(prompt_amount))


def prompt_amount(console, splits):
    while True:
        os.system('clear')
        prt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        print()
        input_amount = ipt.input_amount(console, splits, special_cases=['-', '+'])
        console.next(splits, to_func_index=console.functions.index(prompt_tag))


def prompt_tag(console, splits):
    while True:
        os.system('clear')
        prt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        print()

        input_tag = ipt.get_custom_input(console, splits, message='Input tag. -tag to see tags: #',
                                         special_cases=['-tag'])
        if not input_tag:
            console.next(splits, to_func_index=console.functions.index(prompt_notes))
        if input_tag == '-tag':
            prt.print_all_element(console, splits, 'Tag')
            console.rerun(splits)
        if input_tag:
            splits[console.bl_index].tag = input_tag
            console.next(splits, to_func_index=console.functions.index(prompt_notes))


def prompt_notes(console, splits):
    while True:
        os.system('clear')
        prt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        print()

        input_notes = ipt.get_custom_input(console, splits, message='Input notes. -notes to see notes: ',
                                         special_cases=['-notes'])
        if not input_notes:
            console.next(splits, to_func_index=console.functions.index(prompt_save))
        if input_notes == '-notes':
            prt.print_all_element(console, splits, 'Notes')
            console.rerun(splits)
        if input_notes:
            splits[console.bl_index].notes = input_notes


def prompt_save(console, splits):

    while True:
        os.system('clear')
        prt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        print()

        if ipt.did_input_yes(console, splits, 'Save?'):
            console.dm.save_splits(splits)
