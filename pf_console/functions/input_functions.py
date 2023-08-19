import os
import pf_console.functions.splits_functions as splt
import pf_console.functions.print_functions  as prt


def did_input_yes(console, splits, message='') -> bool:

    while True:
        response = input(message + ' y or n? ')

        if str.startswith(response, '-'):
            check_input_for_commands(response, console, splits)
        elif response == 'y' or response == '':
            return True
        elif response == 'n':
            return False


def input_vendor_name(console, splits):

    i = input('\nInput vendor. ENTER to keep. -v for vendor list: ').strip()

    if i == '':
        i = splits[console.bl_index].vendor
    if i == '-v':
        input_vendor_from_list(console, splits)
    elif str.startswith(i, '-'):
        check_input_for_commands(i, console, splits)
    return i


def input_vendor_from_list(console, splits):

    os.system('clear')
    vendor_dict = console.dm.get_vendor_dict()
    vendor_set = sorted(set(vendor_dict.values()))

    print()
    for index, v in enumerate(vendor_set):
        print(str(index) + '. ' + v)
    response = input('ENTER to input vendor.')
    if response == '':
        return console.rerun(splits)
    elif response.isdigit():  # pick vendor from list
        splits[console.bl_index].vendor = list(vendor_set)[int(response)]
        return console.next(splits)


def check_input_for_commands(response, console, splits): # new

    if response.startswith('-bl'):
        try:
            input('starts with -bl')
            splt.change_active_budget_line(console, splits, int(response[3:4]))
        except Exception as e:
            input(e)
            pass
    if response == "-back":
        return console.previous(splits)
    elif response == "-next":
        return console.next(splits)
    elif response == "-help":
        os.system('clear')
        input("SOME HELP")
        return console.rerun(splits)
    elif response == "-show":
        pass


def input_index(console, splits, max_index, min_index=0, message='Select index: ', special_cases=[], special_cases_just_starts_with=False): # new

    while True:
        response = input(message)

        if str.startswith(response, '-'):
            check_input_for_commands(response, console, splits)
        elif response == '':
            return None
        elif special_cases_just_starts_with and (response.startswith(special_cases[0])):
            return response
        elif response in special_cases:
            return response
        elif response.isdigit():
            response_int = int(response)
            if max_index > response_int >= 0:
                return response_int


def get_custom_input(console, splits, message='Input: ', special_cases=[]) -> str:

    while True:

        response = input(message)

        if response == '':
            return None
        if str.startswith(response, '-'):
            check_input_for_commands(response, console, splits)
        elif response in special_cases:
            return response

        return response


def input_amount(console, splits, message='ENTER to accept, \'-\'(item amount), \'+\'(credit amount): $ ', special_cases=[]):

    while True:
        response_str = input(message)

        if response_str == '':
            return
        if str.startswith(response_str, '-'):
            check_input_for_commands(response_str, console, splits)
        try:
            response_flt = float(response_str)
        except:
            input('not a float')
            os.system('clear')
            prt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
            print()
            continue

        if response_str.startswith(('-','+')):
            splt.split_bl(console, splits, response_flt)
        else:
            splits[console.bl_index].amount = response_flt
            return

def input1():
    input('in input1()')
    input2()
    input('input1() after input2() call')

def input2():
    input('in input2')