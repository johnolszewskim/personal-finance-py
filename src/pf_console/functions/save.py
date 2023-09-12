import src.pf_console.datasets as datasets


def save_splits(data_manager, console, splits):  # keep

    for budget_line in splits:
        save_new_vendor(data_manager, console.importing_tx['Vendor'].replace(' ', '').replace(u'\xa0', ''), budget_line)
        save_category_subcategory(data_manager, console, splits, budget_line.category, budget_line.subcategory)

        data_manager.df_budget_lines.loc[len(data_manager.df_budget_lines.index)] = [budget_line.transaction_id, budget_line.date,
                                                                                     budget_line.vendor, budget_line.category,
                                                                                     budget_line.subcategory, budget_line.amount,
                                                                                     budget_line.tag, budget_line.notes]
        data_manager.df_saved_transactions.loc[len(data_manager.df_saved_transactions.index)] = console.importing_tx

    data_manager.df_budget_lines.to_csv(data_manager.saved_budget_lines_filename)
    data_manager.df_saved_transactions.to_csv(data_manager.saved_transactions_filename)


def save_new_vendor(data_manager, raw_vendor, budget_line):  # keep, validated

    if budget_line.vendor in data_manager.df_raw_vendor_to_vendor['vendor'].values:
        return
    else:
        data_manager.df_raw_vendor_to_vendor.loc[len(data_manager.df_raw_vendor_to_vendor.index)] = [raw_vendor, budget_line.vendor]

    data_manager.df_raw_vendor_to_vendor.to_csv(datasets.get_raw_vendor_to_vendor())
    return


def save_category_subcategory(data_manager, console, splits, category, subcategory):  # keep

    is_new_category = False
    is_new_subcategory = False

    if category not in data_manager.dict_categories_subcategories.keys():
        is_new_category = True
        data_manager.dict_categories_subcategories[category] = []

    if subcategory not in data_manager.dict_categories_subcategories[category]:
        data_manager.dict_categories_subcategories[category] = data_manager.dict_categories_subcategories[category] + [subcategory]
        is_new_subcategory = True

    return data_manager.write_categories_subcategories(console, splits, category, subcategory, is_new_category,
                                                       is_new_subcategory)