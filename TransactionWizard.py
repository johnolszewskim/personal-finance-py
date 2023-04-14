import tkinter as tk
from tkinter import ttk
import PersonalFinancePYData as data
import SingleBudgetLineFrame as sblf
import SingleTransactionLineFrame as stlf

class TransactionWizard(tk.Frame):

    def __init__(self, master, trans):

        tk.Frame.__init__(self, master)

        self.trans = trans
        self.delete_checkbutton_var = tk.IntVar()
        self.t_index = 0

        self.t_frame_deck = []
        for t in trans.iloc():
            self.t_frame_deck.append(stlf.SingleTransactionLineFrame(self, t, 'lightgray'))

        self.t_frame = self.t_frame_deck[self.t_index]
        self.t_frame.grid(row=0, column=0)

        self.b_frame = self.buttons().grid(row=1, column=0, stick='w')
        self.buttons()

    def buttons(self) -> tk.Frame:
        b_f = tk.Frame(self.master)
        tk.Button(b_f, text='Prev', command=self.prev_clicked).grid(row=0, column=0)
        tk.Button(b_f, text='Split', command=self.split_clicked).grid(row=0, column=1)
        tk.Button(b_f, text='Next', command=self.next_clicked).grid(row=0, column=2)
        tk.Label(b_f, text='Delete').grid(row=0, column=3)
        tk.Checkbutton(b_f, command=self.delete_checkbutton_clicked, variable=self.delete_checkbutton_var, onvalue=1, offvalue=0).grid(row=0, column=4)
        tk.Button(b_f, text='Save', command=self.save).grid(row=0, column=5, sticky='e')
        return b_f

    def next_clicked(self):
        self.t_frame.grid_remove()
        self.t_index += 1
        self.t_frame = self.t_frame_deck[self.t_index]
        self.t_frame.grid(row=0, column=0)
        self.delete_checkbutton_var.set(self.t_frame.delete)

    def split_clicked(self):
        if self.delete_checkbutton_var.get() == 0:
            self.t_frame.add_budget_line_frame()

    def prev_clicked(self):
        if self.t_index > 0:
            self.t_frame.grid_remove()
            self.t_index -= 1
            self.t_frame = self.t_frame_deck[self.t_index]
            self.t_frame.grid(row=0, column=0)
            self.delete_checkbutton_var.set(self.t_frame.delete)

    def delete_checkbutton_clicked(self):
        self.t_frame.match_checkbutton(self.delete_checkbutton_var.get())

    def save(self):
        for t_f in self.t_frame_deck:
            if t_f.delete == 0:
                t_f.save()