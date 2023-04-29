import pandas as pd
import PersonalFinancePYData as data
import PFPY_Console_Functions as func
import Transaction as tx

TRANSACTIONS_FILE = '/Users/johnmatthew/Documents/Personal Finance/0. PersonalFinancePY/TRANSACTIONS_PersonalFinancePY.csv'
BUDGET_LINES_FILE = '/Users/johnmatthew/Documents/Personal Finance/0. PersonalFinancePY/BUDGET_TRANSACTIONS_PersonalFinancePY.csv'

transactions = pd.read_csv(TRANSACTIONS_FILE)
transactions.set_index('Transaction ID')

budget_lines = pd.read_csv(BUDGET_LINES_FILE)
budget_lines.set_index('Transaction ID')

transactions_copy = transactions.copy(deep=True)
transactions_copy['Date'] = pd.to_datetime(transactions_copy['Date'])
transactions_copy.sort_values(by='Date', inplace=True)
transactions_copy = transactions_copy[transactions_copy['Transaction ID'].isin(budget_lines['Transaction ID']) == False]

last_tx = tx.Transaction
for t in transactions_copy.iloc():
    last_tx = func.input_transaction(t['Transaction ID'], str(t['Date']), t['Vendor'], t['Amount'])
    bl_budget_lines = { new_bl.transaction_id : new_bl }
    func.write_budget_line(new_bl)
