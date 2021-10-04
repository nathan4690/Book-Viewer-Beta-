# import tkinter as tk
# from os.path import abspath,dirname

# PICPATH = abspath(dirname(__file__)) + "\\users\\"

# def add_image():
#     text.image_create(tk.END, image = img) # Example 1
#     # text.window_create(tk.END, window = tk.Label(text, image = img)) # Example 2

# root = tk.Tk()

# text = tk.Text(root)
# text.pack(padx = 20, pady = 20)

# tk.Button(root, text = "Insert", command = add_image).pack()

# img = tk.PhotoImage(file = PICPATH + "checked.png")

# root.mainloop()

import os

print(os.path.split(r"E:\Tin hoc\Lap trinh\Project\Python practices\pygame games\Tkinter\users\introduction.npb"))