import tkinter as tk
from tkinter import ttk
import PersonalFinancePYData as data
import SingleBudgetLineFrame as sblf
import SingleTransactionLineFrame as stlf

class TransactionWizard(tk.Frame):
    # indices variable for ease of moving widgets without having to type every column value
    indices = ['index_Prev',
               'index_Split',
               'index_Next',
               'index_Delete',
               'index_Delete_Checkbutton',
               'index_StatementName',
               'index_Save']

    def __init__(self, master, transactions, filename):

        tk.Frame.__init__(self, master)

        self.imported_transactions=transactions

        self.current_index = 0

        self.statement_name = tk.StringVar()

        self.t_frame_deck = []
        for t in self.imported_transactions.iloc():
            self.t_frame_deck.append(stlf.SingleTransactionLineFrame(self, t, 'lightgray'))

        self.current_t_frame = self.t_frame_deck[self.current_index]
        self.current_t_frame.grid(row=0, column=0)

        self.delete_cb = tk.Checkbutton
        self.button_frame = self.create_button_frame().grid(row=1, column=0, stick='w')

    def create_button_frame(self) -> tk.Frame:
        b_f = tk.Frame(self.master)

        tk.Button(b_f, text='Prev', command=self.prev_clicked).grid(row=0, column=TransactionWizard.indices.index('index_Prev'))
        tk.Button(b_f, text='Split', command=self.split_clicked).grid(row=0, column=TransactionWizard.indices.index('index_Split'))
        tk.Button(b_f, text='Next', command=self.next_clicked).grid(row=0, column=TransactionWizard.indices.index('index_Next'))
        tk.Label(b_f, text='Delete').grid(row=0, column=TransactionWizard.indices.index('index_Delete'))

        self.delete_cb = tk.Checkbutton(b_f, command=self.delete_checkbutton_clicked, variable=self.current_t_frame.delete_var.get(), onvalue=1, offvalue=0)
        self.delete_cb.grid(row=0, column=TransactionWizard.indices.index('index_Delete_Checkbutton'))
        print(self.current_t_frame.delete_var.get())

        # TODO // Set default text to filename
        tk.Entry(b_f, width=50, textvariable=self.statement_name).grid(row=0, column=TransactionWizard.indices.index('index_StatementName'))
        tk.Button(b_f, text='Save', command=self.save).grid(row=0, column=TransactionWizard.indices.index('index_Save'), sticky='e')
        return b_f

    def next_clicked(self):
        if self.current_index < len(self.t_frame_deck)-1:
            self.current_t_frame.grid_remove()
            self.current_index += 1
            self.current_t_frame = self.t_frame_deck[self.current_index]
            self.current_t_frame.grid(row=0, column=0)
            if self.current_t_frame.delete_var.get() == 1:
                self.delete_cb.select()
            else:
                self.delete_cb.deselect()
            print(self.current_t_frame.delete_var.get())

    def split_clicked(self):
        if self.current_t_frame.delete_var.get() == 0:
            self.current_t_frame.add_budget_line_frame()

    def prev_clicked(self):
        if self.current_index > 0:
            self.current_t_frame.grid_remove()
            self.current_index -= 1
            self.current_t_frame = self.t_frame_deck[self.current_index]
            self.current_t_frame.grid(row=0, column=0)
            if self.current_t_frame.delete_var.get() == 1:
                self.delete_cb.select()
            else:
                self.delete_cb.deselect()

    def delete_checkbutton_clicked(self):
        if self.current_t_frame.delete_var.get() == 0:
            self.current_t_frame.delete_var.set(1)
        else:
            self.current_t_frame.delete_var.set(0)

        self.current_t_frame.match_checkbutton()
        # # TODO checkbox matching rotating through frames

    def save(self):
        for t_f in self.t_frame_deck:
            if t_f.delete == 0:
                t_f.save()