import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import test

days = 5
periods = 6
recess_break_aft = 3  # recess after 3rd Period
data = test.apply()
butt_grid = []
# print(section)


period_names = list(map(lambda x: 'Period ' + str(x), range(1, 6+1)))
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thrusday', 'Friday']


def process_button(d, p, sec):
    print('hello')


def student_tt_frame(tt, db):
    title_lab = tk.Label(
        tt,
        text='T  I  M  E  T  A  B  L  E',
        font=('Consolas', 20, 'bold'),
        pady=5
    )
    title_lab.pack()

    legend_f = tk.Frame(tt)
    legend_f.pack(pady=15)
    tk.Label(
        legend_f,
        text='Legend: ',
        font=('Consolas', 10, 'italic')
    ).pack(side=tk.LEFT)

    tk.Label(
        legend_f,
        text='Theory Classes',
        bg='green',
        fg='white',
        relief='raised',
        font=('Consolas', 10, 'italic'),
        height=2
    ).pack(side=tk.LEFT, padx=10)

    tk.Label(
        legend_f,
        text='Practical Classes',
        bg='blue',
        fg='white',
        relief='raised',
        font=('Consolas', 10, 'italic'),
        height=2
    ).pack(side=tk.LEFT, padx=10)

    global butt_grid
    global data
    sec_cls = db
    # print(sec_cls)
    table = tk.Frame(tt)
    table.pack(fill=tk.BOTH, expand=True)
    wrapper1 = LabelFrame(table)
    mycanvas = Canvas(wrapper1)
    mycanvas.pack(side=LEFT, fill="both", expand="yes")
    yscrollbar = ttk.Scrollbar(
        wrapper1, orient="vertical", command=mycanvas.yview)
    yscrollbar.pack(side=RIGHT, fill="y")

    mycanvas.configure(yscrollcommand=yscrollbar.set)

    mycanvas.bind('<Configure>', lambda e: mycanvas.configure(
        scrollregion=mycanvas.bbox('all')))
    myframe = Frame(mycanvas)
    mycanvas.create_window((0, 0), window=myframe, anchor="nw")
    wrapper1.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    classes = sec_cls['classes']
    section = sec_cls['section']
    # print(classes, section)
    for section in section:
        label = ttk.Label(myframe, text=section.get_id())
        label.pack(fill=tk.BOTH, expand=True)
        tree = ttk.Treeview(myframe)
        tree['columns'] = list(map(lambda x: '#' + str(x), range(1, 8)))
        tree.column("#0", width=0, stretch=tk.NO, anchor="center")
        tree.column("#1", width=50, stretch=tk.NO, anchor="center")
        tree.column("#2", width=50, stretch=tk.NO, anchor="center")
        tree.column("#3", width=130, stretch=tk.NO, anchor="center")
        tree.column("#4", width=150, stretch=tk.NO, anchor="center")
        tree.column("#5", width=100, stretch=tk.NO, anchor="center")
        tree.column("#6", width=180, stretch=tk.NO, anchor="center")
        tree.column("#7", width=200, stretch=tk.NO, anchor="center")
        tree.heading('#0', text="")
        tree.heading('#1', text="Class #")
        tree.heading('#2', text="section")
        tree.heading('#3', text="Dept")
        tree.heading('#4', text="Course(number, max of students)")
        tree.heading('#5', text="Room(Capacity)")
        tree.heading('#6', text="Instructor(Id)")
        tree.heading('#7', text="Meeting Time(Id)")
        tree.tag_configure("center")
        tree['height'] = section.get_num_class_in_week()
        for i in range(0, len(classes)):
            if str(classes[i].section).upper() == str(section.get_id()).upper():
                tree.insert("", 0, values=(str(i), classes[i].section, classes[i].get_dept().get_name(), classes[i].get_course().get_name() + "(" +
                                           classes[i].get_course().get_number() + ", " +
                                           str(classes[i].get_course(
                                           ).get_maxNumbOfStudents()) + ")",
                                           classes[i].get_room().get_number() + " (" +
                                           str(classes[i].get_room(
                                           ).get_seatingCapacity())+")",
                                           classes[i].get_instructor().get_name() +
                                           " (" +
                                           str(classes[i].get_instructor(
                                           ).get_id())+")",
                                           str(classes[i].get_meetingTime().get_day())+" ==> "+classes[i].get_meetingTime().get_time() + " (" + str(classes[i].get_meetingTime().get_id())+")"))
                tree.pack(fill=tk.BOTH, expand=True)


tt = tk.Tk()
tt.title('Student Timetable')
tt.geometry('910x500')
student_tt_frame(tt, data)

sec_select_f = tk.Frame(tt, pady=15)
sec_select_f.pack()

tt.mainloop()
