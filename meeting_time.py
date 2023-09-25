import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

did = day = time = None


def create_treeview():
    tree['columns'] = list(map(lambda x: '#' + str(x), range(1, 4)))
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("#1", width=70, stretch=tk.NO, anchor="center")
    tree.column("#2", width=150, stretch=tk.NO, anchor="center")
    tree.column("#3", width=150, stretch=tk.NO, anchor="center")
    tree.heading('#0', text="")
    tree.heading('#1', text="Did")
    tree.heading('#2', text="Day")
    tree.heading('#3', text="Tinming")
    tree['height'] = 12


def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    conn.execute("SELECT DID, DAY, TIME FROM M_T")
    cursor = conn.fetchall()
    # print(cursor)
    for row in cursor:
        tree.insert(
            "",
            0,
            values=(row[0], row[1], row[2])
        )
    tree.place(x=520, y=100)


def parse_data():
    did = str(did_entry.get())
    day = str(combo1.get()).upper()
    time = str(combo2.get())

    if did == "" or day == "" or time == "":
        messagebox.showwarning(
            "Bad Input", "Some fields are empty! Please fill them out!")
        return

    conn.execute(f"REPLACE INTO M_T (DID,day,TIME)\
        VALUES ('{did}','{day}','{time}')")
    cnx.commit()
    update_treeview()

    did_entry.delete(0, tk.END)
    combo1.current(0)
    combo2.current(0)


def update_data():
    did_entry.delete(0, tk.END)
    combo1.current(0)
    combo2.current(0)
    try:
        # print(len(tree.selection()))
        if len(tree.selection()) > 1:
            messagebox.showerror(
                "Bad Select", "Select one Meeting time at a time to update!")
            return

        q_did = tree.item(tree.selection()[0])['values'][0]
        conn.execute(f"SELECT * FROM M_T WHERE DID = '{q_did}'")
        cursor = conn.fetchall()
        cursor = list(cursor)
        # print(cursor)
        # print('HSJJSJDJDHJJSA')
        did_entry.insert(0, cursor[0][0])
        # day_entry.insert(0, cursor[0][1])
        combo1.current(subcode_li1.index(cursor[0][1]))
        combo2.current(subcode_li2.index(cursor[0][2]))
        conn.execute(F"DELETE FROM M_T WHERE DID = '{cursor[0][0]}'")
        cnx.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror(
            "Bad Select", "Please select a Meeting time from the list first!")
        return


def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror(
            "Bad Select", "Please select a Meeting time from the list first!")
        return
    for i in tree.selection():
        conn.execute(
            f"DELETE FROM M_T WHERE DID = '{tree.item(i)['values'][0]}'")
        cnx.commit()
        tree.delete(i)
        update_treeview()


cnx = mysql.connector.connect(
    user='root', password='', host='localhost', database='TKDB')
conn = cnx.cursor()

# creating Tabe in the database
conn.execute('CREATE TABLE IF NOT EXISTS M_T\
    (DID CHAR(10) NOT NULL PRIMARY KEY,\
    DAY CHAR(50) NOT NULL,\
    TIME CHAR(50) NOT NULL)')

# TKinter Window
subtk = tk.Tk()
subtk.geometry('1000x470')
subtk.title('Meeting Time')

# Label1
tk.Label(
    subtk,
    text='List of Meeting Time',
    font=('Consolas', 20, 'bold')
).place(x=620, y=50)

# Label2
tk.Label(
    subtk,
    text='Add/Update Meeting',
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
    text='M_T id:',
    font=('Consolas', 12)
).place(x=100, y=130)

# Entry1
did_entry = tk.Entry(
    subtk,
    font=('Consolas', 12),
    width=15
)
did_entry.place(x=260, y=130)


subcode_li1 = ["MONDAY",
               "TUESDAY",
               "WEDNESDAY",
               "THRUSDAY",
               "FRIDAY"
               ]
subcode_li2 = ["09:00 - 12:00",
               "14:00 - 17:00"
               ]
tk.Label(
    subtk,
    text='M_T day:',
    font=('Consolas', 12)
).place(x=100, y=170)

combo1 = ttk.Combobox(
    subtk,
    values=subcode_li1,
    width=20
)
combo1.place(x=260, y=170)
combo1.current(0)
tk.Label(
    subtk,
    text='TIME :',
    font=('Consolas', 12)
).place(x=100, y=210)

combo2 = ttk.Combobox(
    subtk,
    values=subcode_li2,
    width=20
)
combo2.place(x=260, y=210)
combo2.current(0)
# Button1
B1 = tk.Button(
    subtk,
    text='Add M_T',
    font=('Consolas', 12),
    command=parse_data
)
B1.place(x=150, y=400)

# Button2
B2 = tk.Button(
    subtk,
    text='Update M_T',
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
    text='Delete M_T',
    font=('Consolas', 12),
    command=remove_data
)
B3.place(x=650, y=400)

# looping Tkiniter window
subtk.mainloop()
conn.close()  # close database after all operations
