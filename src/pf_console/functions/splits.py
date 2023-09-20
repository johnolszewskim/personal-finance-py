def split_bl(console, splits, amount):

    splits.append(splits[console.bl_index].copy())
    splits[len(splits) - 1].amount = -amount

    if amount < 0:
        splits[console.bl_index].amount = splits[console.bl_index].amount + amount

    reindex_splits(splits)
    return


def reindex_splits(splits):

    for index, bl in enumerate(splits):
        bl.transaction_id = bl.transaction_id[0:-2] + '_' + str(index)


def change_active_budget_line(console, splits, bl_index):

    console.bl_index = bl_index
    console.rerun(splits)

