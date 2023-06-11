import tkinter as tk

from pfgui import SingleBudgetLineFrame


class SingleTransactionLineFrame(tk.Frame):

	def __init__(self, master, tx_transaction, background_color):

		tk.Frame.__init__(self, master)

		self.delete_var = tk.IntVar()

		self.background_color = background_color
		self.tx_transaction = tx_transaction

		self.import_label = str(self.tx_transaction.transaction_id) + ": " + str(self.tx_transaction.vendor)
		self.vendor_import = tk.Label(self, text=self.import_label, font=('Arial', 10), pady=2).grid(row=0, column=0, sticky='w')

		self.b_frame_deck = []
		self.b_frame_deck.append(SingleBudgetLineFrame.SingleBudgetLineFrame(self, self.tx_transaction))

		self.current_index = 1
		self.paint_budget_lines()

	def add_budget_line_frame(self):
		new_frame = SingleBudgetLineFrame.SingleBudgetLineFrame(self, self.tx_transaction)
		self.b_frame_deck.append(new_frame)
		self.paint_budget_lines()

	def remove_budget_line_frame(self, b_f):
		if len(self.b_frame_deck) != 1:
			b_f.grid_remove()
			self.b_frame_deck.remove(b_f)
			self.current_index -= 1
			self.paint_budget_lines()

	def paint_budget_lines(self):
		self.current_index = len(self.b_frame_deck)
		for b_f in self.b_frame_deck:
			b_f.grid(row=self.current_index, column=0)
			self.current_index += 1

	def match_checkbutton(self):

		for b_f in self.b_frame_deck:
			if self.delete_var.get() == 1:
				b_f.enable_disable('disabled')
			else:
				b_f.enable_disable('normal')

	def save(self) -> []:

		bl_list = []

		for b_f in self.b_frame_deck:
			bl_list.append(b_f.save())

		return bl_list



