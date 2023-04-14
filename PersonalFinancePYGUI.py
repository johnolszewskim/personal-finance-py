import tkinter as tk
from tkinter import ttk

import pandas as pd

import PersonalFinancePYData as data
import SingleTransactionLineFrame
import TransactionWizard as tw

def startGUI():
	home = tk.Tk()
	home.title("PersonalFinancePY")

	make_resources_label()

	home.mainloop()


def startTransactionWizard(transactions) -> pd.DataFrame:

	root = tk.Tk()
	root.title("Transaction Wizard")

	transaction_wizard = tw.TransactionWizard(root, transactions).grid(row=0, column=0)

	root.mainloop()

	def labels(self):
		tk.Label(self, text='Vendor', width=55, anchor='w', font=('Arial', 12), fg='gray').grid(row=0, column=0, sticky='w')
		tk.Label(self, text='Category', anchor='w', font=('Arial', 12), fg='gray').grid(row=0, column=1, sticky='w')
		tk.Label(self, text='Subcategory', anchor='w', font=('Arial', 12), fg='gray').grid(row=0, column=2,stick='w')
		tk.Label(self, text='Amount', anchor='w', font=('Arial', 12), fg='gray').grid(row=0, column=3, stick='w')

def make_resources_label() -> tk.Label:
	tk.Label(text="Resources file:").grid(row=0, column=0, columnspan=2)
	resources = data.df_resources
	print(resources)
	file_label = tk.Label(text="text").grid(row=1, column=0)
	tk.Button(text="Change").grid(row=1, column=1)

	return file_label