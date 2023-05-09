import datetime
class BudgetLine:

    def __init__(self, transaction_id, date: datetime, vendor, category, subcategory, amount, tag, notes):
        self.transaction_id=transaction_id
        self.date=date
        self.vendor=vendor
        self.category=category
        self.subcategory=subcategory
        self.amount=amount
        self.tag=tag
        self.notes=notes

    def __str__(self):
        return str(self.transaction_id) + '\t' + \
                datetime.datetime.strftime(self.date, '%-d %b %y') + '\t' + \
                str(self.vendor) + '\t' + \
                str(self.category) + '\t' + \
                str(self.subcategory) + '\t' + \
                '$' + str(self.amount) + '\t' + \
                str(self.tag) + '\t' + str(self.notes)

    def copy(self):
        return BudgetLine(self.transaction_id, self.date, self.vendor, self.category, self.subcategory, self.amount, self.tag, self.notes)
    def split(self):
        return BudgetLine(self.transaction_id, self.date, self.vendor, '', '', self.amount, '', '')
    def print_with_splits(self, splits):
        [print(str(bl)) for bl in splits]
        # print(self)
    def print_splits(splits: []):
        [print(bl) for bl in splits]
    def adjust_transaction_ids_for_splits(splits: []):
        for index, bl in enumerate(splits):
            bl.transaction_id = bl.transaction_id[0:-2] + '_' + str(index)
