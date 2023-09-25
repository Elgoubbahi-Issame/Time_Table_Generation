import mysql.connector
import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import messagebox

cid = name = mx_nbs = teachers = None


def create_treeview():
    tree['columns'] = list(map(lambda x: '#' + str(x), range(1, 5)))
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("#1", width=50, stretch=tk.NO, anchor="center")
    tree.column("#2", width=150, stretch=tk.NO, anchor="center")
    tree.column("#3", width=50, stretch=tk.NO, anchor="center")
    tree.column("#4", width=150, stretch=tk.NO, anchor="center")
    tree.heading('#0', text="")
    tree.heading('#1', text="Cid")
    tree.heading('#2', text="Name")
    tree.heading('#3', text="Max_NS")
    tree.heading('#4', text="Teacher")
    tree['height'] = 12


def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    conn.execute("SELECT CID, NAME , MAX_NB_STD , TEACHER FROM COURS")
    cursor = conn.fetchall()
    # print(cursor)
    for row in cursor:
        tree.insert(
            "",
            0,
            values=(row[0], row[1], row[2], row[3])
        )
    tree.place(x=530, y=100)


def parse_data():
    cid = str(cid_entry.get())
    name = str(name_entry.get()).upper()
    mx_nbs = str(mx_nbs_entry.get())
    curselection = lstbox.curselection()
    # for index in curselection:
    print(lstbox.curselection())

    if cid == "" or name == "" or mx_nbs == "" or curselection == ():
        messagebox.showwarning(
            "Bad Input", "Some fields are empty! Please fill them out!")
        return
    for index in curselection:
        conn.execute(f"REPLACE INTO COURS (CID ,NAME ,MAX_NB_STD ,TEACHER)\
            VALUES ('{cid+'-'+str(index)}','{name}','{mx_nbs}','{lstbox.get(index)}')")
        cnx.commit()
    update_treeview()

    cid_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    mx_nbs_entry.delete(0, tk.END)
    lstbox.selection_clear(0, tk.END)


def update_data():
    cid_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    mx_nbs_entry.delete(0, tk.END)
    lstbox.selection_clear(0, tk.END)
    try:
        #         # print(len(tree.selection()))
        if len(tree.selection()) > 1:
            messagebox.showerror(
                "Bad Select", "Select one Cours at a time to update!")
            return

        q_cid = tree.item(tree.selection()[0])['values'][0]
        conn.execute(f"SELECT * FROM COURS WHERE CID = '{q_cid}'")
        cursor = conn.fetchall()
        cursor = list(cursor)
        # print(cursor)/
        cid_entry.insert(0, cursor[0][0])
        name_entry.insert(0, cursor[0][1])
        mx_nbs_entry.insert(0, cursor[0][2])
        # lstbox.selection_set(0, cursor[0][3])
        conn.execute(f"DELETE FROM COURS WHERE CID = '{cursor[0][0]}'")
        cnx.commit()
        update_treeview()

    except IndexError:
        messagebox.showerror(
            "Bad Select", "Please select a Teacher from the list first!")
        return


def remove_data():
    if len(tree.selection()) < 1:
        messagebox.showerror(
            "Bad Select", "Please select a Cours from the list first!")
        return
    for i in tree.selection():
        # print(tree.item(i)['values'][0])
        conn.execute(
            f"DELETE FROM COURS WHERE CID = '{tree.item(i)['values'][0]}'")
        cnx.commit()
        tree.delete(i)
        update_treeview()


cnx = mysql.connector.connect(
    user='root', password='', host='localhost', database='TKDB')
conn = cnx.cursor()

# creating Tabe in the database
conn.execute('CREATE TABLE IF NOT EXISTS COURS\
    (CID CHAR(10) NOT NULL PRIMARY KEY,\
    NAME CHAR(50) NOT NULL,\
    MAX_NB_STD INT(5) NOT NULL,\
    TEACHER CHAR(20) NOT NULL,\
    CONSTRAINT teacher_unique UNIQUE(TEACHER,NAME))')

# TKinter Window
subtk = tk.Tk()
subtk.geometry('1000x470')
subtk.title('Courses')

# Label1
tk.Label(
    subtk,
    text='List of Courses',
    font=('Consolas', 20, 'bold')
).place(x=620, y=50)

# Label2
tk.Label(
    subtk,
    text='Add/Update Cours',
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
    text='Cours id:',
    font=('Consolas', 12)
).place(x=100, y=130)

# Entry1
cid_entry = tk.Entry(
    subtk,
    font=('Consolas', 12),
    width=20
)
cid_entry.place(x=260, y=130)

# Label7
tk.Label(
    subtk,
    text='Cours Name:',
    font=('Consolas', 12)
).place(x=100, y=170)

# Entry4
name_entry = tk.Entry(
    subtk,
    font=('Consolas', 12),
    width=20,
)
name_entry.place(x=260, y=170)

# Label7
tk.Label(
    subtk,
    text='NB of Students :',
    font=('Consolas', 12)
).place(x=100, y=210)

# Entry4
mx_nbs_entry = tk.Entry(
    subtk,
    font=('Consolas', 12),
    width=20,
)
mx_nbs_entry.place(x=260, y=210)

tk.Label(
    subtk,
    text='Teachers :',
    font=('Consolas', 12)
).place(x=100, y=240)


conn.execute(f"SELECT distinct name FROM TEACHER ")
cursor = conn.fetchall()
cursor = list(cursor)
lstbox = tk.Listbox(subtk, selectmode='multiple', width=22, height=8)
lstbox.place(x=260, y=240)
for item in cursor:
    lstbox.insert(cursor.index(item), item[0])
cnx.commit()
# Button1
B1 = tk.Button(
    subtk,
    text='Add Cours',
    font=('Consolas', 12),
    command=parse_data
)
B1.place(x=150, y=400)

# Button2
B2 = tk.Button(
    subtk,
    text='Update Cours',
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
    text='Delete Cours',
    font=('Consolas', 12),
    command=remove_data
)
B3.place(x=650, y=400)

# looping Tkiniter window
subtk.mainloop()
conn.close()  # close database after all operations
