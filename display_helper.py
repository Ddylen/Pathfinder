import numpy as np
import time
from tkinter import Tk, Label


def pretty_matrix(mat: np.array) -> str:
    """convert a numpy array into a neatly formatted string"""
    output_string = ""
    max_entry_len = 1
    column_spacer = "  "
    row_spacer = "\n"

    for i, row in enumerate(mat):
        for j, entry in enumerate(row):

            if j != 0:
                output_string += column_spacer

            entry_str = str(round(entry, max_entry_len))
            entry_char_len = len(entry_str)
            if entry_char_len > max_entry_len:
                fixed_len_entry_str = entry_str[0:max_entry_len]
            elif entry_char_len < max_entry_len:
                fixed_len_entry_str = entry_str + (max_entry_len-entry_char_len)*" "
            else:
                fixed_len_entry_str = entry_str

            output_string += fixed_len_entry_str

        output_string += row_spacer

    return output_string



def example_window():
    """Generate an example window"""
    win = Tk()
    win.geometry("750x270")

    Label(win, text=pretty_matrix(np.zeros((5,5))), font=('Helvetica 14 bold')).pack(pady=20)
    win.update()
    time.sleep(3)

    print("DESTORY")
    win.destroy()