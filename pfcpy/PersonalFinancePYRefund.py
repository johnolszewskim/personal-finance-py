import os
import BudgetLine as bl
def prompt_refund(b_l):
    if b_l.get_amount() < 0:
        while True:
            print(b_l)
            response = input('Is this transaction a refund? y or n? ')

            if response == 'y':
                return True
            elif response == 'n':
                return False
    return False
def prompt_refunded_budget_line(dict_b_l) -> bl.BudgetLine:
    os.system('clear')
    dict_index_tid = {}
    for index, tid in enumerate(list(dict_b_l.keys())):
        temp = dict_b_l[tid]
        print(f'{index:<5}{str(temp)}')
        dict_index_tid[index] = tid
    print('99: not listed')

    while True:
        bl_index = input('Input line to refund: ')
        if not bl_index.isdigit():
            continue
        bl_index = int(bl_index)
        if bl_index == 99:
            return None
        if (bl_index > len(dict_index_tid)) and (bl_index >= 0):
            continue
        return dict_b_l[dict_index_tid[bl_index]]