from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

with sqlite3.connect("SkiEnter_database.db") as db:
    cursor = db.cursor()

root = Tk()
root.geometry("600x450")

# Header Frame
frame_header = ttk.Frame(root)
frame_header.pack(pady=10)

logo = PhotoImage(file='skienter.gif').subsample(2, 2)
logolabel = ttk.Label(frame_header, text='logo', image=logo)
logolabel.grid(row=0, column=0, rowspan=2)

headerlabel = ttk.Label(frame_header, text='FAVOURITE LIST', foreground='red', font=('Arial', 24))
headerlabel.grid(row=0, column=1, padx=20)

# Content Frame
frame_content = ttk.Frame(root)
frame_content.pack()

# Fetch skis from the Skis table in the database
cursor.execute("SELECT ski_number, name, manufacturer, proficiency, stiffness, Length, Width FROM Skis")
skis_from_database = cursor.fetchall()
cursor.execute("SELECT profile_id FROM preference_on")
profile_id = cursor.fetchone()[0]


# Sample list of available skis
available_skis = [{"ski_number": ski[0], "name": ski[1], "manufacturer": ski[2],
                   "proficiency": ski[3], "stiffness": ski[4], "Length": ski[5],
                   "Width": ski[6]} for ski in skis_from_database]

# Variables for selected attributes
selected_name_var = StringVar()
selected_manufacturer_var = StringVar()
selected_proficiency_var = StringVar()
selected_stiffness_var = StringVar()
selected_length_var = StringVar()
selected_width_var = StringVar()

# Labels for each attribute
attributes_labels = ["Select a Name:", "Select a Manufacturer:", "Select Proficiency:",
                     "Select Stiffness:", "Select Length:", "Select Width:"]
for i, label_text in enumerate(attributes_labels):
    ttk.Label(frame_content, text=label_text).grid(row=i, column=0, padx=10, pady=10)

# Comboboxes for each attribute
ski_combobox = ttk.Combobox(frame_content, textvariable=selected_name_var, values=[ski["name"] for ski in available_skis])
ski_combobox.grid(row=0, column=1, padx=10, pady=10)

manufacturer_combobox = ttk.Combobox(frame_content, textvariable=selected_manufacturer_var, values=list(set(ski["manufacturer"] for ski in available_skis)))
manufacturer_combobox.grid(row=1, column=1, padx=10, pady=10)

proficiency_combobox = ttk.Combobox(frame_content, textvariable=selected_proficiency_var, values=list(set(ski["proficiency"] for ski in available_skis)))
proficiency_combobox.grid(row=2, column=1, padx=10, pady=10)

stiffness_combobox = ttk.Combobox(frame_content, textvariable=selected_stiffness_var, values=list(set(ski["stiffness"] for ski in available_skis)))
stiffness_combobox.grid(row=3, column=1, padx=10, pady=10)

length_combobox = ttk.Combobox(frame_content, textvariable=selected_length_var, values=list(set(ski["Length"] for ski in available_skis)))
length_combobox.grid(row=4, column=1, padx=10, pady=10)

width_combobox = ttk.Combobox(frame_content, textvariable=selected_width_var, values=list(set(ski["Width"] for ski in available_skis)))
width_combobox.grid(row=5, column=1, padx=10, pady=10)

def save_to_favorites():
    selected_ski_name = selected_name_var.get()
    selected_ski_manufacturer = selected_manufacturer_var.get()
    selected_ski_proficiency = selected_proficiency_var.get()
    selected_ski_stiffness = selected_stiffness_var.get()
    selected_ski_length = selected_length_var.get()
    selected_ski_width = selected_width_var.get()

    if selected_ski_name:
        # Get the selected ski from the available skis list
        selected_ski = next((ski for ski in available_skis if ski["name"] == selected_ski_name
                             and ski["manufacturer"] == selected_ski_manufacturer
                             and ski["proficiency"] == selected_ski_proficiency
                             and ski["stiffness"] == selected_ski_stiffness
                             and ski["Length"] == selected_ski_length
                             and ski["Width"] == selected_ski_width), None)

        if selected_ski:
            selected_ski_id = selected_ski["ski_number"]

            # Insert the selected ski into the preference_on table
            cursor.execute("INSERT INTO preference_on(profile_id, ski_id) VALUES(?, ?)", (profile_id, selected_ski_id))
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
        where profile_id = {profile_id};
        """)
    favorite_skis = cursor.fetchall()

    if not favorite_skis:
        messagebox.showinfo(title='Favorites', message='No favorite skis yet')
    else:
        favorite_skis_names = [ski[1] for ski in favorite_skis]
        favorite_skis_manuf = [ski[2] for ski in favorite_skis]
        # favorites_message = 'Favorite skis: ' + ' , ' + (favorite_skis_names) + ' , ' +(favorite_skis_manuf)
        favorites_message = ''
        for ski, manuf in zip(favorite_skis_names, favorite_skis_manuf):
            favorites_message += ski + ' , ' + manuf + '\n'
        messagebox.showinfo(title='Favorites', message=favorites_message)



# Buttons for saving to favorites and opening favorites
save_button = ttk.Button(frame_content, text='Save to Favorites', command=save_to_favorites)
save_button.grid(row=6, column=0, pady=10)

open_button = ttk.Button(frame_content, text='Open Favorites', command=open_favorites)
open_button.grid(row=6, column=1, pady=10)

root.mainloop()
