import tkinter as tk
import PersonalFinancePYData as data
from pfgui import SingleTransactionFrame as stlf
import pandas as pd
import Transaction as tx


class TransactionWizard(tk.Frame):
    # indices variable for ease of moving widgets without having to type every column value
    indices = ['index_Prev',
               'index_Split',
               'index_Next',
               'index_Delete',
               'index_Delete_Checkbutton',
               'index_StatementName',
               'index_Save']

    def __init__(self, master, transactions, statement_id):

        tk.Frame.__init__(self, master)

        self.new_transactions=transactions
        self.statement_id=statement_id
        self.current_index = 0

        self.statement_name = tk.StringVar()
        self.statement_entry = tk.Entry()

        self.t_frame_deck = []
        for t in self.new_transactions.iloc():
            new_tx = tx.Transaction(t['Transaction ID'], 'sid', t['Date'], t['Vendor'], t['Amount'])
            self.t_frame_deck.append(stlf.SingleTransactionLineFrame(self, new_tx, 'lightgray'))

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

        # TODO.txt // Set default text to filename
        self.statement_entry=tk.Entry(b_f, width=50, textvariable=self.statement_name).grid(row=0, column=TransactionWizard.indices.index('index_StatementName'))
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
        # # TODO.txt checkbox matching rotating through frames

    def save(self):

        bl_list = []

        for t_f in self.t_frame_deck:
            if t_f.delete_var.get() == 0:
                single_tx_bl = t_f.save()
                bl_list = bl_list + single_tx_bl

        df_bl = pd.DataFrame(columns=data.budget_col_names)
        l_transaction_id = []
        l_vendor = []
        l_category = []
        l_subcategory = []
        l_amount = []
        l_tag = []
        l_notes = []

        for bl in bl_list:
            l_transaction_id.append(self.statement_id + str(bl.transaction_id))
            l_vendor.append(bl.vendor)
            l_category.append(bl.category)
            l_subcategory.append(bl.subcategory)
            l_amount.append(bl.amount)
            l_tag.append(bl.tag)
            l_notes.append(bl.notes)

        df_bl['Transaction ID']=l_transaction_id
        df_bl['Vendor']=l_vendor
        df_bl['Category']=l_category
        df_bl['Subcategory']=l_subcategory
        df_bl['Amount']=l_amount
        df_bl['Tag']=l_tag
        df_bl['Notes']=l_notes
        print(df_bl)

