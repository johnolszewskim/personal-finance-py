from datetime import date as dt
from colorama import Fore, Style

class BudgetLine:

    field_names = ["Transaction ID", "Date", "Vendor", "Category", "Subcategory", "Amount", "Tag", "Notes"]
    def __init__(self, transaction_id, date: dt , vendor, category, subcategory, amount, tag, notes):
        self.transaction_id=transaction_id
        self.date=date
        self.vendor=vendor
        self.category=category
        self.subcategory=subcategory
        self.amount=float(amount)
        self.tag=tag
        self.notes=notes

        self.invalid_amount=False

        # print(self)
    def __str__(self):

        date = dt.strftime(self.date, '%-d %b %y')
        amount = str(self.amount)
        if self.invalid_amount:
            amount = Fore.RED + amount + Style.RESET_ALL
        return f'{str(self.transaction_id):>18}  ' + f'{date:<9}  ' + f'{str(self.vendor):<30}' + f'{str(self.category):>20} - ' + f'{str(self.subcategory):<20}' + f'${amount:<15}' + f'#{str(self.tag):<20}' + f'NOTES: {str(self.notes):<10}'
    def copy(self):
        return BudgetLine(self.transaction_id, self.date, self.vendor, self.category, self.subcategory, self.amount, self.tag, self.notes)
    def refund(self, is_refund):
        is_refund.vendor = self.vendor
        is_refund.category = self.category
        is_refund.subcategory = self.subcategory
        is_refund.tag = 'REFUND'
        is_refund.notes = 'refund ' + self.transaction_id
    def get_amount(self):
        return self.amount
    def split(self):
        return BudgetLine(self.transaction_id, self.date, self.vendor, '', '', self.amount, '', '')

    def adjust_transaction_ids_for_splits(splits: []):
        for index, bl in enumerate(splits):
            bl.transaction_id = bl.transaction_id[0:-2] + '_' + str(index)

