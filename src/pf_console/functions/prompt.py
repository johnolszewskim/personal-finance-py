import os
import calendar
import src.pf_console.functions.prnt as prnt
import src.pf_console.functions.input as inpt
import src.pf_console.functions.suggest as sggst
import src.pf_console.functions.save as sv


def prompt_account(df_accounts) -> str:
    while True:

        os.system('clear')

        for i, k in df_accounts.iterrows():
            print(f'{str(i):>7}' + ': ' + k.Name)

        input_acct = input('\nSelect account: ')
        # input_acct = '22009'

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


def prompt_import(console, splits):
    while True:
        os.system('clear')
        prnt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)

        if inpt.did_input_yes(console, splits, message='\nKeep?'):
            return console.next(splits)

        return


def prompt_refund(console, splits): # need to migrate
    if console.splitting:
        return console.next(splits)

    if splits[console.bl_index].input_amount() < 0:

        while True:
            os.system('clear')
            prnt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
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

    if sggst.did_accept_suggested_vendor(console, splits):
        return prompt_category

    while True:
        os.system('clear')
        prnt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)

        did_assign_vendor = inpt.input_vendor_name(console, splits)
        if not did_assign_vendor:
            continue

        return prompt_category


def prompt_category(console, splits):
    # input("prompt_category()") # for testing

    suggestion_index = -1
    will_suggest = True

    while True:

        #  TODO//rework suggestion to be more like vendor, hiding in prnt.py

        os.system('clear')
        suggestion_index = sggst.suggest_category(console, splits, last_index=suggestion_index)
        if suggestion_index == -1:  # if there are no suggestions
            will_suggest = False

        prnt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        all_categories = prnt.print_categories(console.dm)

        print('99: ADD CATEGORY/SUBCATEGORY\n')

        if will_suggest:
            category_index = inpt.input_index(console, splits, len(all_categories),
                                              message='Input category number. ENTER to select suggestion. \'n\' for next suggestion: ',
                                              special_cases=['99', 'n'])
        else:
            category_index = inpt.input_index(console, splits, len(all_categories),
                                              message='No suggestions. Input category number: ',
                                              special_cases=['99'])

        if category_index is None:  # user hit enter
            if splits[console.bl_index].category == '':
                continue
            return prompt_subcategory
        elif category_index == '99':  # add new category
            return prompt_add_category
        elif category_index == 'n':  # n is returned as input
            continue
        else:  # if category is selected by index
            splits[console.bl_index].category = all_categories[category_index]
            return prompt_subcategory


def prompt_add_category(console, splits):
    while True:

        os.system('clear')
        prnt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        all_categories = prnt.print_categories(console.dm) # value unused
        print('99: RETURN TO CHOOSE CATEGORY\n')

        new_category_name = inpt.get_custom_input(console, splits, message='Input new category name: ',
                                                  special_cases=['99'])

        #if not new_category name # user hit enter

        if new_category_name is None:
            continue
        if new_category_name == '99':
            splits[console.bl_index].category = ''
            return prompt_category
        splits[console.bl_index].category = new_category_name
        return prompt_subcategory


def prompt_subcategory(console, splits):
    # input('prompt_subcategory()')  # for testing

    suggestion_index = -1
    will_suggest = True

    while True:

        os.system('clear')
        suggestion_index = sggst.suggest_subcategory(console, splits, last_index=suggestion_index)
        if suggestion_index == -1:  # if there are no suggestions
            will_suggest = False

        prnt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        print()

        subcategories = prnt.print_subcategories(console, splits[console.bl_index].category)

        if not subcategories:
            return prompt_add_subcategory

        print('88: ADD SUBCATEGORY')
        print('99: REINPUT CATEGORY')
        print()  # for formatting

        if will_suggest:
            subcategory_index = inpt.input_index(console, splits, len(subcategories),
                                                 message='Input subcategory number. ENTER to select suggestion. n for next suggestion: ',
                                                 special_cases=['88', '99', 'n'])
        else:
            subcategory_index = inpt.input_index(console, splits, len(subcategories),
                                                 message='No suggestions. Input subcategory index: ',
                                                 special_cases=['88', '99'])

        if subcategory_index is None:
            if splits[console.bl_index].subcategory == '':
                continue
            return prompt_amount
        elif subcategory_index == '88':
            return prompt_add_subcategory
        elif subcategory_index == '99':
            splits[console.bl_index].category = ''
            return prompt_category
        elif subcategory_index == 'n':
            continue
        else:
            splits[console.bl_index].subcategory = subcategories[subcategory_index]
            return prompt_amount


def prompt_add_subcategory(console, splits):
    while True:

        os.system('clear')
        prnt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        print('\n99: RETURN TO CHOOSE CATEGORY')
        print()  # for formatting

        new_subcategory_name = inpt.get_custom_input(console, splits, message='Input new subcategory name: ',
                                                     special_cases=['99'])

        if new_subcategory_name is None:
            continue
        if new_subcategory_name == '99':
            splits[console.bl_index].category = ''
            return prompt_category
        splits[console.bl_index].subcategory = new_subcategory_name
        return prompt_amount


def prompt_amount(console, splits):
    while True:
        os.system('clear')
        prnt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        print()
        didSplit = inpt.input_amount(console, splits, special_cases=['-', '+'])
        if didSplit:
            continue
        else:
            return prompt_tag


def prompt_tag(console, splits):
    while True:
        os.system('clear')
        prnt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        print()

        input_tag = inpt.get_custom_input(console, splits, message='Input tag. -tag to see tags: #',
                                          special_cases=['-tag'])
        if input_tag is None:
            return console.next(splits, to_func_index=console.functions.index(prompt_notes))
        if input_tag == '-tag':
            prnt.print_all_element(console, splits, 'Tag')
            return console.rerun(splits)
        if input_tag:
            splits[console.bl_index].tag = input_tag
            return console.next(splits, to_func_index=console.functions.index(prompt_notes))


def prompt_notes(console, splits):
    while True:
        os.system('clear')
        prnt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        print()

        input_notes = inpt.get_custom_input(console, splits, message='Input notes. -notes to see notes: ',
                                            special_cases=['-notes'])
        if input_notes is None:
            return console.next(splits, to_func_index=console.functions.index(prompt_save))
        if input_notes == '-notes':
            prnt.print_all_element(console, splits, 'Notes')
            return console.rerun(splits)
        if input_notes:
            splits[console.bl_index].notes = input_notes
            return console.next(splits, to_func_index=console.functions.index(prompt_save))


def prompt_save(console, splits):

    os.system('clear')
    prnt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
    print()

    if inpt.did_input_yes(console, splits, 'Save?'):
        sv.save_splits(console.dm, console, splits)

    return

    # console.finish(splits)


def prompt_budget(console, splits) -> str:

    while True:
        os.system('clear')
        prnt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
        print()

        prnt.print_budgets(console, splits)

        budget_index = inpt.input_index(console, splits, max_index=len(console.dm.dict_budget_categories.keys()),
                                        message='Input index of budget for new category: ')

        if budget_index is None:
            continue
        else:
            budget_index = int(budget_index)
            return list(console.dm.dict_budget_categories.keys())[budget_index]

