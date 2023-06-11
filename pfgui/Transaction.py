class Transaction:

    def __init__(self, transaction_id, statement_id, date, vendor, amount):
        self.transaction_id=transaction_id
        self.statement_id=statement_id
        self.date=date
        self.vendor=vendor
        self.amount=amount

    def __str__(self):
        return 'self.transaction_id: ' + str(self.transaction_id) + '\n' + 'self.statement_id: ' + str(self.statement_id) + '\n' + 'self.date: ' + str(self.date) + '\n'+ 'self.vendor: ' + str(self.vendor) + '\n' + 'self.amount: ' + str(self.amount) + '\n'
