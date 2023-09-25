import mysql.connector
import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import messagebox

Sec_id = dept = nb_cls_in_week = None


def create_treeview():
    tree['columns'] = list(map(lambda x: '#' + str(x), range(1, 4)))
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("#1", width=80, stretch=tk.NO, anchor="center")
    tree.column("#2", width=250, stretch=tk.NO, anchor="center")
    tree.column("#3", width=120, stretch=tk.NO, anchor="center")
    tree.heading('#0', text="")
    tree.heading('#1', text="SEC_ID")
    tree.heading('#2', text="Departement")
    tree.heading('#3', text="Nb_classes_in_week")
    tree['height'] = 12


def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    conn.execute(
        "SELECT sec_id ,departement , nb_classes_in_week FROM SECTION")
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
    Sec_id = str(name_entry.get()).upper()
    dept = str(combo1.get()).upper()
    nb_cls_in_week = nb_cls_in_week_entry.get()

    if Sec_id == "" or dept == "" or nb_cls_in_week == None:
        messagebox.showwarning(
            "Bad Input", "Some fields are empty! Please fill them out!")
        return
    conn.execute(f"REPLACE INTO SECTION (sec_id ,departement ,nb_classes_in_week )\
            VALUES ('{Sec_id}','{dept}','{nb_cls_in_week}')")
    cnx.commit()
    update_treeview()

    name_entry.delete(0, tk.END)
    nb_cls_in_week_entry.delete(0, tk.END)
    combo1.current(0)


def update_data():
    name_entry.delete(0, tk.END)
    nb_cls_in_week_entry.delete(0, tk.END)
    combo1.current(0)
    try:
        #         # print(len(tree.selection()))
        if len(tree.selection()) > 1:
            messagebox.showerror(
                "Bad Select", "Select one SECTION at a time to update!")
            return

        q_Sec_id = tree.item(tree.selection()[0])['values'][0]
        conn.execute(
            f"SELECT * FROM SECTION WHERE Sec_id = '{q_Sec_id}'")
        cursor = conn.fetchall()
        cursor = list(cursor)
        # print(cursor)/
        name_entry.insert(0, cursor[0][0])
        combo1.current(cursor1.index(cursor[0][1]))
        nb_cls_in_week_entry.insert(0, cursor[0][2])
        # lstbox.selection_set(0, cursor[0][3])
        conn.execute(
            f"DELETE FROM SECTION WHERE Sec_id = '{cursor[0][0]}'")
        cnx.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror(
            "Bad Select", "Please select a SECTION from the list first!")
        return


def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror(
            "Bad Select", "Please select a SECTION from the list first!")
        return
    for i in tree.selection():
        # print(tree.item(i)['values'][0])
        conn.execute(
            f"DELETE FROM SECTION WHERE Sec_id = '{tree.item(i)['values'][0]}'")
        cnx.commit()
        tree.delete(i)
        update_treeview()


cnx = mysql.connector.connect(
    user='root', password='', host='localhost', database='TKDB')
conn = cnx.cursor()

# creating Tabe in the database
conn.execute('CREATE TABLE IF NOT EXISTS SECTION\
    (Sec_id CHAR(10) NOT NULL PRIMARY KEY,\
    Departement CHAR(50) NOT NULL,\
    Nb_classes_in_week int(5) NOT NULL,\
    CONSTRAINT section_unique UNIQUE (Sec_id,Departement))')

# TKinter Window
subtk = tk.Tk()
subtk.geometry('1000x470')
subtk.title('Sections')

# Label1
tk.Label(
    subtk,
    text='List of Sections',
    font=('Consolas', 20, 'bold')
).place(x=620, y=50)

# Label2
tk.Label(
    subtk,
    text='Add/Update Sections',
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
    text='Section Name:',
    font=('Consolas', 12)
).place(x=40, y=170)

# Entry4
name_entry = tk.Entry(
    subtk,
    font=('Consolas', 12),
    width=20,
)
name_entry.place(x=325, y=170)

tk.Label(
    subtk,
    text='Departments :',
    font=('Consolas', 12)
).place(x=40, y=210)


conn.execute(f"SELECT distinct name FROM DEPARTEMENT ")
cursor1 = conn.fetchall()
cursor1 = [itm[0] for itm in cursor1]
print(cursor1)
combo1 = ttk.Combobox(
    subtk,
    values=cursor1,
)
combo1.place(x=325, y=210)
combo1.current(0)
cnx.commit()
tk.Label(
    subtk,
    text='Numbre of classes in the week :',
    font=('Consolas', 12)
).place(x=40, y=250)

# Entry4
nb_cls_in_week_entry = tk.Entry(
    subtk,
    font=('Consolas', 12),
    width=20,
)
nb_cls_in_week_entry.place(x=325, y=250)
# Button1
B1 = tk.Button(
    subtk,
    text='Add Section',
    font=('Consolas', 12),
    command=parse_data
)
B1.place(x=150, y=400)

# Button2
B2 = tk.Button(
    subtk,
    text='Update Section',
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
    text='Delete Section',
    font=('Consolas', 12),
    command=remove_data
)
B3.place(x=690, y=400)

# looping Tkiniter window
subtk.mainloop()
conn.close()
# close database after all operations
