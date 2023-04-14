import tkinter as tk
from tkinter import ttk
import PersonalFinancePYData as data
import SingleBudgetLineFrame

class SingleTransactionLineFrame(tk.Frame):

	def __init__(self, master, trans, background_color):

		tk.Frame.__init__(self, master)

		self.delete = False

		self.background_color = background_color
		self.trans = trans

		self.vendor_import = tk.Label(self, text=trans['Vendor'], font=('Arial', 10), pady=2).grid(row=0, column=0, sticky='w')

		self.budget_frames = []
		self.budget_frames.append(SingleBudgetLineFrame.SingleBudgetLineFrame(self, trans))

		self.index = 1
		self.paint_budget_lines()

	def add_budget_line_frame(self):
		new_frame = SingleBudgetLineFrame.SingleBudgetLineFrame(self, self.trans)
		self.budget_frames.append(new_frame)
		self.paint_budget_lines()

	def remove_budget_line_frame(self, b_f):
		if len(self.budget_frames) != 1:
			b_f.grid_remove()
			self.budget_frames.remove(b_f)
			self.index -= 1
			self.paint_budget_lines()

	def paint_budget_lines(self):
		self.index = len(self.budget_frames)
		for b_f in self.budget_frames:
			b_f.grid(row=self.index, column=0)
			self.index += 1

	def match_checkbutton(self, checkbutton_status):
		self.delete = checkbutton_status

		for b_f in self.budget_frames:
			if self.delete == 1:
				b_f.enable_disable('disabled')
			else:
				b_f.enable_disable('normal')

	def save(self):
		for b_f in self.budget_frames:
			b_f.save()