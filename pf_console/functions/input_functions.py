import os
import pf_console.functions.print_functions as prt
def input_yes_no(console, splits):

    pass

def input_vendor_name(console, splits):

    i = input('Input vendor | ENTER to keep | -v for vendor list: ').strip()

    if i == '':
        return console.next(splits)
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
def check_input_for_commands(response, console, splits):

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

