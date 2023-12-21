
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

with sqlite3.connect("SkiEnter_database.db") as db:
    cursor = db.cursor()

user_id = 7

root = Tk()
root.geometry("600x450")

# Header Frame
frame_header = ttk.Frame(root)
frame_header.pack(pady=10)

logo = PhotoImage(file='skienter.gif').subsample(2, 2)
logolabel = ttk.Label(frame_header, text='logo', image=logo)
logolabel.grid(row=0, column=0, rowspan=2)

headerlabel = ttk.Label(frame_header, text='RENT SKIS LIST', foreground='red', font=('Arial', 24))
headerlabel.grid(row=0, column=1, padx=20)

# Content Frame
frame_content = ttk.Frame(root)
frame_content.pack()
listbox = Listbox(root, width=50, height=10)
listbox.pack(side=LEFT, fill=BOTH)
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=BOTH)



# Fetch skis from the Skis table in the database
cursor.execute(f"SELECT user_id, ski_number, name, manufacturer, proficiency, stiffness, Length, Width FROM Skis JOIN Rentals ON Skis.ski_number = Rentals.item_id WHERE Rentals.user_id = {user_id}")
skis_from_database = cursor.fetchall()

# Sample list of available skis
available_skis = [{"ski_number": ski[0], "name": ski[1], "manufacturer": ski[2],
                   "proficiency": ski[3], "stiffness": ski[4], "Length": ski[5],
                   "Width": ski[6]} for ski in skis_from_database]

# var = Variable(value = skis_from_database)
# listbox = Listbox(root, listvariable = var, height = 6, selectmode=SINGLE)

for ski in available_skis:
    listbox.insert(END, f"{ski['name']} - {ski['manufacturer']} - {ski['proficiency']} - {ski['stiffness']} - {ski['Length']} - {ski['Width']} - {ski['ski_number']}")

# Variables for selected attributes
selected_name_var = StringVar()
selected_manufacturer_var = StringVar()
selected_proficiency_var = StringVar()
selected_stiffness_var = StringVar()
selected_length_var = StringVar()
selected_width_var = StringVar()

# # Labels for each attribute
# attributes_labels = ["Select a Name:", "Select a Manufacturer:", "Select Proficiency:",
#                      "Select Stiffness:", "Select Length:", "Select Width:"]
# for i, label_text in enumerate(attributes_labels):
#     ttk.Label(frame_content, text=label_text).grid(row=i, column=2, padx=10, pady=10)

# Comboboxes for each attribute
# ski_combobox = ttk.Combobox(frame_content, textvariable=selected_name_var, values=[ski["name"] for ski in available_skis])
# ski_combobox.grid(row=0, column=3, padx=10, pady=10)

# manufacturer_combobox = ttk.Combobox(frame_content, textvariable=selected_manufacturer_var, values=list(set(ski["manufacturer"] for ski in available_skis)))
# manufacturer_combobox.grid(row=1, column=3, padx=10, pady=10)

# proficiency_combobox = ttk.Combobox(frame_content, textvariable=selected_proficiency_var, values=list(set(ski["proficiency"] for ski in available_skis)))
# proficiency_combobox.grid(row=2, column=3, padx=10, pady=10)

# stiffness_combobox = ttk.Combobox(frame_content, textvariable=selected_stiffness_var, values=list(set(ski["stiffness"] for ski in available_skis)))
# stiffness_combobox.grid(row=3, column=3, padx=10, pady=10)

# length_combobox = ttk.Combobox(frame_content, textvariable=selected_length_var, values=list(set(ski["Length"] for ski in available_skis)))
# length_combobox.grid(row=4, column=3, padx=10, pady=10)

# width_combobox = ttk.Combobox(frame_content, textvariable=selected_width_var, values=list(set(ski["Width"] for ski in available_skis)))
# width_combobox.grid(row=5, column=3, padx=10, pady=10)

def save_to_favorites():
    selected_ski_name = selected_name_var.get()
    selected_ski_manufacturer = selected_manufacturer_var.get()
    selected_ski_proficiency = selected_proficiency_var.get()
    selected_ski_stiffness = selected_stiffness_var.get()
    selected_ski_length = selected_length_var.get()
    selected_ski_width = selected_width_var.get()

    if selected_ski_name:
        # Get the selected ski from the available skis list
        # selected_ski = next((ski for ski in available_skis if ski["name"] == selected_ski_name
        #                      and ski["manufacturer"] == selected_ski_manufacturer
        #                      and ski["proficiency"] == selected_ski_proficiency
        #                      and ski["stiffness"] == selected_ski_stiffness
        #                      and ski["Length"] == selected_ski_length
        #                      and ski["Width"] == selected_ski_width), None)
        selected_ski = next((ski for ski in available_skis if ski[1] == selected_ski_name
                             and ski[2] == selected_ski_manufacturer
                             and ski[3] == selected_ski_proficiency
                             and ski[4] == selected_ski_stiffness
                             and ski[5] == selected_ski_length
                             and ski[6] == selected_ski_width), None)


        if selected_ski:
            selected_ski_id = selected_ski["ski_number"]

            # Insert the selected ski into the preference_on table
            cursor.execute("INSERT INTO preference_on(profile_id, ski_id) VALUES(?, ?)", (user_id, selected_ski_id))
            db.commit()
            messagebox.showinfo(title='Save to Favorites', message='Ski saved to favorites')
        else:
            messagebox.showinfo(title='Error', message='Selected ski not found in the available skis list')

def open_favorites():
    cursor.execute(
        f"""
        select *
        from skis
        join preference_on on preference_on.ski_id = skis.ski_number
        where profile_id = {user_id};
        """)
    favorite_skis = cursor.fetchall()

    if not favorite_skis:
        messagebox.showinfo(title='Favorites', message='No favorite skis yet')
    else:
        favorite_skis_names = [ski[1] for ski in favorite_skis]
        favorite_skis_manuf = [ski[2] for ski in favorite_skis]
        favorite_skis_prof = [ski[3] for ski in favorite_skis]
        favorite_skis_stiff = [ski[4] for ski in favorite_skis]
        favorite_skis_length = [ski[5] for ski in favorite_skis]
        favorite_skis_width = [ski[6] for ski in favorite_skis]

        favorites_message = ''
        for ski, manuf, prof in zip(favorite_skis_names, favorite_skis_manuf, favorite_skis_prof):
        #for ski, manuf, prof, stiff, length, width in zip(favorite_skis_names, favorite_skis_manuf, favorite_skis_prof, str(favorite_skis_stiff),str(favorite_skis_length),str(favorite_skis_width)):
            favorites_message += ski + ' , ' + manuf + ' , ' + prof + '\n'
        messagebox.showinfo(title='FAVOURITE LIST', message=favorites_message)

# Buttons for saving to favorites and opening favorites
# save_button = ttk.Button(frame_content, text='Save to Favorites', command=save_to_favorites)
# save_button.grid(row=6, column=2, pady=10)

open_button = ttk.Button(frame_content, text='OPEN FAVOURITE LIST', command=open_favorites)
open_button.grid(row=6, column=3, pady=10)

root.mainloop()
