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
                self.date + '\t' + \
                str(self.vendor) + '\t' + \
                str(self.category) + '\t' + \
                str(self.subcategory) + '\t' + \
                '$' + str(self.amount) + '\t' + \
                str(self.tag) + '\t' + str(self.notes)

    def copy(self):
        return BudgetLine(self.transaction_id, self.date, self.vendor, self.category, self.subcategory, self.amount, self.tag, self.notes)

