from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import sqlite3
with sqlite3.connect("SkiEnter_database.db") as db:
    cursor=db.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS feedback(user_id integer
 PRIMARY KEY AUTOINCREMENT,name text NOT NULL,email text NOT NULL,comment text NOT NULL); """)

root = Tk()
root.geometry("450x360")
frame_header = ttk.Frame(root)
frame_header.pack()
logo = PhotoImage(file='skienter.gif').subsample(2, 2)
logolabel = ttk.Label(frame_header, text='logo', image=logo)
logolabel.grid(row=0, column=0, rowspan=2)
headerlabel = ttk.Label(frame_header, text='USER FEEDBACK', foreground='red',
                        font=('Arial', 24))
headerlabel.grid(row=0, column=1)
messagelabel = ttk.Label(frame_header,
                         text='LEAVE FEEDBACK ABOUT SKIS',
                         foreground='black', font=('Arial', 14))
messagelabel.grid(row=1, column=1)

frame_content = ttk.Frame(root)
frame_content.pack()
myvar = StringVar()
var = StringVar()
namelabel = ttk.Label(frame_content, text='Enter Name')
namelabel.grid(row=0, column=0, padx=5, sticky='sw')
entry_name = ttk.Entry(frame_content, width=18, font=('Arial', 14), textvariable=myvar)
entry_name.grid(row=1, column=0)

emaillabel = ttk.Label(frame_content, text='Enter Email')
emaillabel.grid(row=0, column=1, sticky='sw')
entry_email = ttk.Entry(frame_content, width=18, font=('Arial', 14), textvariable=var)
entry_email.grid(row=1, column=1)

commentlabel = ttk.Label(frame_content, text='Comment', font=('Arial', 10))
commentlabel.grid(row=2, column=0, sticky='sw')
textcomment = Text(frame_content, width=55, height=10)
textcomment.grid(row=3, column=0, columnspan=2)


textcomment.config(wrap ='word')

def clear():
    global entry_name
    global entry_email
    global textcomment
    messagebox.showinfo(title='clear', message='Do you want to clear?')
    entry_name.delete(0, END)
    entry_email.delete(0, END)
    textcomment.delete(1.0, END)


def submit():
    global entry_name
    global entry_email
    global textcomment
    newComment = textcomment.get(1.0, END)
    newUsername = entry_name.get()
    newEmail = entry_email.get()

    cursor.execute("select count(*) from feedback WHERE comment = '" + newComment + "' " )
    result = cursor.fetchall()

    if (result[0][0] > 0):
        messagebox.showinfo(title='Submit', message='You have already submitted this comment')
        return
    else:
        cursor.execute("INSERT INTO feedback(comment,name,email) VALUES(?,?,?)", (newComment,newUsername,newEmail))
        db.commit()
        messagebox.showinfo(title='Submit', message='Thank you for your Feedback, Your Comments Submited')
        entry_name.delete(0, END)
        entry_email.delete(0, END)
        textcomment.delete(1.0, END)

submitbutton = ttk.Button(frame_content, text='Submit', command=submit).grid(row=4, column=0, sticky='e')
clearbutton = ttk.Button(frame_content, text='Clear', command=clear).grid(row=4, column=1, sticky='w')

root.mainloop()
