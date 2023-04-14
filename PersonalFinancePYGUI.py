import tkinter as tk
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
from tkinter import ttk

import pandas as pd

import PersonalFinancePYData as data
import SingleTransactionLineFrame
import TransactionWizard as tw

class PersonalFinancePYGUI(tk.Frame):
	def __init__(self, master, df_transactions, df_budget_transactions):

		tk.Frame.__init__(self, master)

		self.df_transactions = df_transactions
		self.df_budget_transactions = df_budget_transactions

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
		ttk.Combobox(self, values=banks, textvariable=bank_selection).grid(row=6, column=0)

		tk.Button(self, text='load transactions', command=self.startTransactionWizard).grid(row=6, column=1)

		return bank_selection

	def startTransactionWizard(self):

		new_transactions_file = fd.askopenfilename()
		import_trans = pd.read_csv(new_transactions_file)

		# print(data.transaction_column_map['Date'][self.bank.get()])
		trans = pd.DataFrame(columns=data.transaction_column_map.keys())
		trans['Date'] = import_trans[data.transaction_column_map['Date'][self.bank.get()]]
		trans['Vendor'] = import_trans[data.transaction_column_map['Vendor'][self.bank.get()]]
		trans['Amount'] = import_trans[data.transaction_column_map['Amount'][self.bank.get()]]

		root = tk.Tk()
		root.title("Transaction Wizard")

		transaction_wizard = tw.TransactionWizard(root, trans).grid(row=0, column=0)

		root.mainloop()


def startTransactionWizard(transactions) -> pd.DataFrame:

	root = tk.Tk()
	root.title("Transaction Wizard")

	transaction_wizard = tw.TransactionWizard(root, transactions).grid(row=0, column=0)

	root.mainloop()
