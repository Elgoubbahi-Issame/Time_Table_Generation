import mysql.connector
import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import messagebox

dept_id = name = teachers = None


def create_treeview():
    tree['columns'] = list(map(lambda x: '#' + str(x), range(1, 4)))
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("#1", width=50, stretch=tk.NO)
    tree.column("#2", width=250, stretch=tk.NO)
    tree.column("#2", width=200, stretch=tk.NO)
    tree.heading('#0', text="")
    tree.heading('#1', text="DEPT_ID")
    tree.heading('#2', text="Departement Name")
    tree.heading('#3', text="COURS")
    tree['height'] = 12


def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    conn.execute("SELECT DEPT_ID ,NAME , cours FROM DEPARTEMENT")
    cursor = conn.fetchall()
    # print(cursor)
    for row in cursor:
        tree.insert(
            "",
            0,
            values=(row[0], row[1], row[2])
        )
    tree.place(x=530, y=100)


def parse_data():
    name = str(name_entry.get()).upper()
    curselection = lstbox.curselection()
    print(lstbox.curselection())

    if name == "" or curselection == ():
        messagebox.showwarning(
            "Bad Input", "Some fields are empty! Please fill them out!")
        return
    for index in curselection:
        conn.execute(f"REPLACE INTO DEPARTEMENT (NAME ,COURS)\
            VALUES ('{name}','{lstbox.get(index)}')")
        cnx.commit()
    update_treeview()

    name_entry.delete(0, tk.END)
    lstbox.selection_clear(0, tk.END)


def update_data():
    name_entry.delete(0, tk.END)
    lstbox.selection_clear(0, tk.END)
    try:
        #         # print(len(tree.selection()))
        if len(tree.selection()) > 1:
            messagebox.showerror(
                "Bad Select", "Select one DEPT at a time to update!")
            return

        q_dept_id = tree.item(tree.selection()[0])['values'][0]
        conn.execute(
            f"SELECT * FROM DEPARTEMENT WHERE dept_id = '{q_dept_id}'")
        cursor = conn.fetchall()
        cursor = list(cursor)
        # print(cursor)/
        name_entry.insert(0, cursor[0][1])
        # lstbox.selection_set(0, cursor[0][3])
        conn.execute(
            f"DELETE FROM DEPARTEMENT WHERE dept_id = '{cursor[0][0]}'")
        cnx.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror(
            "Bad Select", "Please select a DEPT from the list first!")
        return


def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror(
            "Bad Select", "Please select a DEPT from the list first!")
        return
    for i in tree.selection():
        conn.execute(
            f"DELETE FROM DEPARTEMENT WHERE dept_id = '{tree.item(i)['values'][0]}'")
        cnx.commit()
        tree.delete(i)
        update_treeview()


cnx = mysql.connector.connect(
    user='root', password='', host='localhost', database='TKDB')
conn = cnx.cursor()

# creating Tabe in the database
conn.execute('CREATE TABLE IF NOT EXISTS DEPARTEMENT\
    (dept_id INT(5) AUTO_INCREMENT NOT NULL PRIMARY KEY,\
    NAME CHAR(50) NOT NULL,\
    COURS CHAR(20) NOT NULL,\
    CONSTRAINT cours_unique UNIQUE (NAME,COURS))')

# TKinter Window
subtk = tk.Tk()
subtk.geometry('1000x470')
subtk.title('Departments')

# Label1
tk.Label(
    subtk,
    text='List of Departments',
    font=('Consolas', 20, 'bold')
).place(x=620, y=50)

# Label2
tk.Label(
    subtk,
    text='Add/Update Department',
    font=('Consolas', 20, 'bold')
).place(x=110, y=50)

# Label3
tk.Label(
    subtk,
    text='Add information in the following prompt!',
    font=('Consolas', 10, 'italic')
).place(x=110, y=85)

# Label7
tk.Label(
    subtk,
    text='Department Name:',
    font=('Consolas', 12)
).place(x=100, y=170)

# Entry4
name_entry = tk.Entry(
    subtk,
    font=('Consolas', 12),
    width=20,
)
name_entry.place(x=260, y=170)

tk.Label(
    subtk,
    text='Courses :',
    font=('Consolas', 12)
).place(x=100, y=210)


conn.execute(f"SELECT distinct name FROM COURS ")
cursor = conn.fetchall()
cursor = list(cursor)
lstbox = tk.Listbox(subtk, selectmode='multiple', width=22, height=8)
lstbox.place(x=260, y=210)
for item in cursor:
    lstbox.insert(cursor.index(item), item[0])
cnx.commit()
# Button1
B1 = tk.Button(
    subtk,
    text='Add DEPT',
    font=('Consolas', 12),
    command=parse_data
)
B1.place(x=150, y=400)

# Button2
B2 = tk.Button(
    subtk,
    text='Update DEPT',
    font=('Consolas', 12),
    command=update_data
)
B2.place(x=440, y=400)

# Treeview1
tree = ttk.Treeview(subtk)
create_treeview()
update_treeview()

# Button3
B3 = tk.Button(
    subtk,
    text='Delete DEPT',
    font=('Consolas', 12),
    command=remove_data
)
B3.place(x=750, y=400)

# looping Tkiniter window
subtk.mainloop()
conn.close()  # close database after all operations
