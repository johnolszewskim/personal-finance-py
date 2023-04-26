import tkinter as tk
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
from tkinter import ttk

import pandas as pd

import PersonalFinancePYData as data
import SingleTransactionLineFrame
import TransactionWizard as tw

class PersonalFinancePYGUI(tk.Frame):
	def __init__(self, master, df_all_transactions, df_all_budget_transactions):

		tk.Frame.__init__(self, master)

		self.df_all_transactions = df_all_transactions
		self.df_all_budget_transactions = df_all_budget_transactions

		self.resources_label = self.make_resources_label()
		self.transactions_label = self.make_transactions_label()
		self.budget_transactions_label = self.make_budget_transactions_label()
		self.bank = self.make_load_transactions_row()


	def make_resources_label(self) -> tk.Label:
		tk.Label(self, text="Resources file:", font=('Helvetica', '16', 'bold')).grid(row=0, column=0, columnspan=2)
		file_label = tk.Label(self, text="resources file").grid(row=1, column=0)
		tk.Button(self, text="Change").grid(row=1, column=1)

		return file_label

	def make_transactions_label(self) -> tk.Label:
		tk.Label(self, text="Transactions file:", font=('Helvetica', '16', 'bold')).grid(row=2, column=0, columnspan=2)
		file_label = tk.Label(self, text="transactions file").grid(row=3, column=0)
		tk.Button(self, text="Change").grid(row=3, column=1)

		return file_label

	def make_budget_transactions_label(self) -> tk.Label:
		tk.Label(self, text="Budget Transactions file:", font=('Helvetica', '16', 'bold')).grid(row=4, column=0, columnspan=2)
		file_label = tk.Label(self, text="transactions file").grid(row=5, column=0)
		tk.Button(self, text="Change").grid(row=5, column=1)

		return file_label

	def make_load_transactions_row(self) -> tk.StringVar:
		banks = ['Chase', 'American Express', 'Bank of America', 'Citi']
		bank_selection = tk.StringVar()
		bank_combobox = ttk.Combobox(self, values=banks, textvariable=bank_selection)
		bank_combobox.grid(row=6, column=0)
		bank_combobox.current(0)

		tk.Button(self, text='Load transactions', command=self.startTransactionWizard).grid(row=6, column=1)

		return bank_selection

	def startTransactionWizard(self):

		new_transactions_file = fd.askopenfilename()
		import_trans = pd.read_csv(new_transactions_file)

		# print(data.transaction_column_map['Date'][self.bank.get()])
		imported_transactions = pd.DataFrame(columns=data.transaction_column_map.keys())
		imported_transactions['Date'] = import_trans[data.transaction_column_map['Date'][self.bank.get()]]
		imported_transactions['Vendor'] = import_trans[data.transaction_column_map['Vendor'][self.bank.get()]]
		imported_transactions['Amount'] = import_trans[data.transaction_column_map['Amount'][self.bank.get()]]

		t = tk.Tk()
		t.title("Transaction Wizard")

		transaction_wizard = tw.TransactionWizard(t, imported_transactions, new_transactions_file).grid(row=0, column=0)

		# t.mainloop()
