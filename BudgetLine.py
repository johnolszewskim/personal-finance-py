class BudgetLine:

    def __init__(self, transaction_id, vendor, category, subcategory, amount, tag, notes):
        self.transaction_id=transaction_id
        self.vendor=vendor
        self.category=category
        self.subcategory=subcategory
        self.amount=amount
        self.tag=tag
        self.notes=notes

    def __str__(self):
        return 'transaction_id: ' + str(self.transaction_id) + '\n' + 'self.vendor: ' + str(self.vendor) + '\n' + 'self.category: ' + str(self.category) + '\n' + 'self.subcategory: ' + str(self.subcategory) + '\n' + 'self.amount: ' + str(self.amount) + '\n' + 'self.tag:' + str(self.tag) + '\n' + 'self.notes: ' + str(self.notes)
