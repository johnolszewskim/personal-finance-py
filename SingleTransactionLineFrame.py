import tkinter as tk
from tkinter import ttk

import pandas as pd

import PersonalFinancePYData as data
import SingleBudgetLineFrame

class SingleTransactionLineFrame(tk.Frame):

	def __init__(self, master, trans, background_color):

		tk.Frame.__init__(self, master)

		self.delete_var = tk.IntVar()
		self.delete_var.set(0)

		self.background_color = background_color
		self.trans = trans

		self.vendor_import = tk.Label(self, text=trans['Vendor'], font=('Arial', 10), pady=2).grid(row=0, column=0, sticky='w')

		self.b_frame_deck = []
		self.b_frame_deck.append(SingleBudgetLineFrame.SingleBudgetLineFrame(self, trans))

		self.index = 1
		self.paint_budget_lines()

	def add_budget_line_frame(self):
		new_frame = SingleBudgetLineFrame.SingleBudgetLineFrame(self, self.trans)
		self.b_frame_deck.append(new_frame)
		self.paint_budget_lines()

	def remove_budget_line_frame(self, b_f):
		if len(self.b_frame_deck) != 1:
			b_f.grid_remove()
			self.b_frame_deck.remove(b_f)
			self.index -= 1
			self.paint_budget_lines()

	def paint_budget_lines(self):
		self.index = len(self.b_frame_deck)
		for b_f in self.b_frame_deck:
			b_f.grid(row=self.index, column=0)
			self.index += 1

	def match_checkbutton(self):
		delete = self.delete_var.get()

		for b_f in self.b_frame_deck:
			if delete == 1:
				b_f.enable_disable('disabled')
			else:
				b_f.enable_disable('normal')

	def save(self):

		df_transaction = pd.DataFrame(columns=data.budget_col_names)

		for b_f in self.b_frame_deck:
			b_f.save(df_transaction)

		print(df_transaction)

