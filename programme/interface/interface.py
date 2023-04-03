import tkinter as tk
from tkinter import ttk
root = tk.Tk()
root_2 = tk.Tk()

frm = tk.ttk.Frame(root, padding=5)

frm_2 =  tk.ttk.Frame(root_2,padding=5)
frm.grid()

frm_2.grid()
ttk.Label(frm, text="Hello World!").grid(column=5, row=0)
ttk.Button(frm, text="ding", command=root.destroy).grid(column=1, row=0)

ttk.Label(frm_2, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm_2, text="ding", command=root_2.destroy).grid(column=1, row=0)
root.mainloop()
root_2.mainloop()