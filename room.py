import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

number = seatingCapacity = None


def create_treeview():
    tree['columns'] = list(map(lambda x: '#' + str(x), range(1, 3)))
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("#1", width=70, stretch=tk.NO)
    tree.column("#2", width=200, stretch=tk.NO)
    tree.heading('#0', text="")
    tree.heading('#1', text="number")
    tree.heading('#2', text="Seating Capacity")
    tree['height'] = 12


def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    conn.execute("SELECT NUMBER, seatingCapacity FROM ROOM")
    cursor = conn.fetchall()
    for row in cursor:
        tree.insert(
            "",
            0,
            values=(row[0], row[1])
        )
    tree.place(x=580, y=100)


def parse_data():
    number = str(number_entry.get())
    seatingCapacity = str(seatingCapacity_entry.get()).upper()

    if number == "" or seatingCapacity == "":
        messagebox.showwarning(
            "Bad Input", "Some fields are empty! Please fill them out!")
        return

    conn.execute(f"REPLACE INTO ROOM (NUMBER ,seatingCapacity)\
        VALUES ('{number}','{seatingCapacity}')")
    cnx.commit()
    update_treeview()

    number_entry.delete(0, tk.END)
    seatingCapacity_entry.delete(0, tk.END)


def update_data():
    number_entry.delete(0, tk.END)
    seatingCapacity_entry.delete(0, tk.END)
    try:
        if len(tree.selection()) > 1:
            messagebox.showerror(
                "Bad Select", "Select one ROOM at a time to update!")
            return

        q_number = tree.item(tree.selection()[0])['values'][0]
        conn.execute(f"SELECT * FROM ROOM WHERE NUMBER = '{q_number}'")
        cursor = conn.fetchall()
        cursor = list(cursor)
        number_entry.insert(0, cursor[0][0])
        seatingCapacity_entry.insert(0, cursor[0][1])

        conn.execute(f"DELETE FROM ROOM WHERE NUMBER = '{cursor[0][0]}'")
        cnx.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror(
            "Bad Select", "Please select a ROOM from the list first!")
        return


def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror(
            "Bad Select", "Please select a ROOM from the list first!")
        return
    for i in tree.selection():
        conn.execute(
            f"DELETE FROM ROOM WHERE NUMBER = '{tree.item(i)['values'][0]}'")
        cnx.commit()
        tree.delete(i)
        update_treeview()


cnx = mysql.connector.connect(
    user='root', password='', host='localhost', database='TKDB')
conn = cnx.cursor()

# creating Tabe in the database
conn.execute('CREATE TABLE IF NOT EXISTS ROOM\
    (NUMBER CHAR(10) NOT NULL PRIMARY KEY,\
    seatingCapacity INT(5) NOT NULL)')

# TKinter Window
subtk = tk.Tk()
subtk.geometry('1000x470')
subtk.title('Room')

# Label1
tk.Label(
    subtk,
    text='List of ROOM',
    font=('Consolas', 20, 'bold')
).place(x=620, y=50)

# Label2
tk.Label(
    subtk,
    text='Add/Update ROOM',
    font=('Consolas', 20, 'bold')
).place(x=110, y=50)

# Label3
tk.Label(
    subtk,
    text='Add information in the following prompt!',
    font=('Consolas', 10, 'italic')
).place(x=110, y=85)

# Label4
tk.Label(
    subtk,
    text='Room number:',
    font=('Consolas', 12)
).place(x=100, y=130)

# Entry1
number_entry = tk.Entry(
    subtk,
    font=('Consolas', 12),
    width=15
)
number_entry.place(x=310, y=130)

# Label7
tk.Label(
    subtk,
    text='Room seating Capacity:',
    font=('Consolas', 12)
).place(x=100, y=250)

# Entry4
seatingCapacity_entry = tk.Entry(
    subtk,
    font=('Consolas', 12),
    width=15,
)
seatingCapacity_entry.place(x=310, y=250)

# Button1
B1 = tk.Button(
    subtk,
    text='Add ROOM',
    font=('Consolas', 12),
    command=parse_data
)
B1.place(x=150, y=400)

# Button2
B2 = tk.Button(
    subtk,
    text='Update ROOM',
    font=('Consolas', 12),
    command=update_data
)
B2.place(x=410, y=400)

# Treeview1
tree = ttk.Treeview(subtk)
create_treeview()
update_treeview()

# Button3
B3 = tk.Button(
    subtk,
    text='Delete ROOM',
    font=('Consolas', 12),
    command=remove_data
)
B3.place(x=670, y=400)

# looping Tkiniter window
subtk.mainloop()
conn.close()  # close database after all operations
