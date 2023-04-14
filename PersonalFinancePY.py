import pandas as pd
import tkinter as tk

import PersonalFinancePYData as data
import os
import PersonalFinancePYGUI as GUI

app_directory = '/Users/johnmatthew/Documents/Personal Finance/0. PersonalFinancePY/'
resources_filename = 'RESOURCES_PersonalFinancePY.csv'
print("Loading from: " + app_directory)
resources = pd.read_csv(app_directory + resources_filename, index_col=0)
data.import_resources(resources)

root = tk.Tk()
root.title("Personal Finance PY")
gui = GUI.PersonalFinancePYGUI(root, data.transactions_SAVED, data.budget_transactions_SAVED)
gui.grid(row=0, column=0)
root.mainloop()

# GUI.startGUI()

imported = pd.read_csv('transactions.csv')
statement_id = '3387_20230108'

#start_index = data.import_transactions(imported, data.master_transaction_lines, data.chase_col_map, statement_id)
#data.transactions_to_budget(data.master_transaction_lines[start_index:])

#print(data.master_budget_lines)




