import pandas as pd
import PersonalFinancePYData as data
import PFPY_Console_Functions as func
import Transaction as tx
import BudgetLine as bl
from tkinter import filedialog as fd
import datetime
YEAR = '2023'
TRANSACTIONS_FILE = '/Users/johnmatthew/Documents/Personal Finance/0. PersonalFinancePY/TRANSACTIONS_PersonalFinancePY.csv'
BUDGET_LINES_FILE = '/Users/johnmatthew/Documents/Personal Finance/0. PersonalFinancePY/BUDGET_LINES_PersonalFinancePY.csv'
IMPORT_TRANSACTIONS_FILE = '/Users/johnmatthew/Documents/Personal Finance/3. Credit Card Statements/CHASE Freedom Unlimited 3387/1. Chase3387_Activity20221209_20230108_20230225.CSV'

BANK = 'Chase'
ACCOUNT = '3387'

saved_transactions = pd.read_csv(TRANSACTIONS_FILE)
saved_transactions.set_index('Transaction ID')

saved_budget_lines = pd.read_csv(BUDGET_LINES_FILE)
saved_budget_lines.set_index('Transaction ID')

# ask for bank type
# ask for account
# ask for statement date
# STATEMENT_ID = account_date
STATEMENT_ID = '_3387_20230108'

# IMPORT_TRANSACTIONS_FILE = fd.askopenfilename()
imported_transactions = pd.read_csv(IMPORT_TRANSACTIONS_FILE)
new_transactions = func.map_import_transactions(imported_transactions, BANK, STATEMENT_ID)
new_transactions = new_transactions.loc[new_transactions['Date'].dt.strftime('%Y') == YEAR]
print(new_transactions)

for i, t in new_transactions.iterrows():

        if new_transactions.loc[i,'Transaction ID'] not in saved_transactions['Transaction ID'].values:
                func.import_single_transaction(
                        bl.BudgetLine(t['Transaction ID'], t['Date'], t['Vendor'], '', '', t['Amount'], '', ''),
                        BUDGET_LINES_FILE)

                saved_transactions.loc[len(saved_transactions.index)] = t
                saved_transactions.to_csv(TRANSACTIONS_FILE, index=False)
