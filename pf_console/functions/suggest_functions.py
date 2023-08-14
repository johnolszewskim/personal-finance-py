import pf_console.functions.input_functions as ipt
import pf_console.functions.print_functions as prt
import pandas as pd
import os


def did_accept_suggested_vendor(console, splits):
    prt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)

    raw_vendor_to_vendor_df = pd.read_csv(console.dm.RAW_VENDOR_TO_VENDOR_FILENAME)
    matching_vendors = raw_vendor_to_vendor_df.loc[
        raw_vendor_to_vendor_df['raw_vendor'] == splits[0].vendor.replace(' ', '').replace(u'\xa0', '')]
    matching_vendors.reset_index(drop=True, inplace=True)

    if len(matching_vendors) == 0:
        input('No autocomplete')
        return

    os.system('clear')
    prt.print_splits(splits, console.statement_index, console.statement_length, console.bl_index)
    print()
    for i, v in enumerate(matching_vendors['vendor']):
        print(str(i) + ': ' + v)

    print('Input index or ENTER to input new vendor.')
    response_index = ipt.get_input_index(len(matching_vendors))

    if response_index == -1:
        return False

    splits[console.bl_index].vendor = matching_vendors.loc[response_index]['vendor']
    return console.next(splits)


def suggest_category(console, splits, last_index=-1) -> int:
    bl_with_matching_vendor = console.dm.df_budget_lines.loc[
        console.dm.df_budget_lines['Vendor'] == splits[console.bl_index].vendor]
    bl_with_matching_vendor.reset_index(drop=True, inplace=True)

    last_index = last_index + 1
    splits[console.bl_index].category = bl_with_matching_vendor.loc[last_index, 'Category']
    splits[console.bl_index].subcategory = bl_with_matching_vendor.loc[last_index, 'Subcategory']
    splits[console.bl_index].tag = bl_with_matching_vendor.loc[last_index, 'Tag']
    splits[console.bl_index].notes = bl_with_matching_vendor.loc[last_index, 'Notes']

    return last_index

    #case for at end of suggested
def suggest_subcategory(console, splits, last_index=-1) -> int:
    bl_with_matching_vendor_and_category = console.dm.df_budget_lines.loc[
        (console.dm.df_budget_lines['Vendor'] == splits[console.bl_index].vendor)
        & (console.dm.df_budget_lines['Category'] == splits[console.bl_index].category)]
    input("last_index" + str(last_index))
    bl_with_matching_vendor_and_category.reset_index(drop=True, inplace=True)

    last_index = last_index + 1
    splits[console.bl_index].subcategory = bl_with_matching_vendor_and_category.loc[last_index, 'Subcategory']
    splits[console.bl_index].tag = bl_with_matching_vendor_and_category.loc[last_index, 'Tag']
    splits[console.bl_index].notes = bl_with_matching_vendor_and_category.loc[last_index, 'Notes']

    return last_index
#case for at end of suggested
