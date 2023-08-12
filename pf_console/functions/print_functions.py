from colorama import Fore, Style

def print_splits(splits, statement_index, statement_length, bl_index, mark_index=None, print_statement_index=True):
    if print_statement_index:
        print('(' + str(statement_index + 1) + ',' + str(statement_length) + ')')

    if len(splits) == 1:
        print(' ' + str(splits[0]))
        return

    if mark_index != None:
        for i, b_l in enumerate(splits):
            if i == mark_index:
                print('-' + str(b_l))
            else:
                print(Fore.WHITE + ' ' + str(b_l) + Style.RESET_ALL)

    else:
        for i, b_l in enumerate(splits):
            if i == bl_index:
                print('-' + str(b_l))
            else:
                print(' ' + str(b_l))


def print_categories(console, rows):
    lines = [[], [], [], []]
    for r, cat in enumerate(sorted(console.dm.dict_categories.keys())):
        lines[r % rows].append(str(r) + ': ' + cat)

    print()
    for l in lines:
        row = ''
        for c in l:
            row = row + (f'{c:20}\t')
        print(row)