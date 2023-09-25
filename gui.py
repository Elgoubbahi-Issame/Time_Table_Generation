import os
import tkinter as tk


def run_teach(): os.system('py teacher.py')
def run_room(): os.system('py room.py')
def run_m_t(): os.system('py meeting_time.py')
def run_cour(): os.system('py cours.py')
def run_dep(): os.system('py departement.py')
def run_sc(): os.system('py section.py')
def run_tt(): os.system('py timeTable.py')


ad = tk.Tk()
ad.geometry('800x500')

ad.title('Administrator')

tk.Label(
    ad,
    text='A D M I N I S T R A T O R',
    font=('Consolas', 20, 'bold'),
    pady=10
).pack()

tk.Label(
    ad,
    text='You are the Administrator',
    font=('Consolas', 12, 'italic'),
).pack(pady=9, padx=9)

modify_frame = tk.LabelFrame(
    text='Dashboard-1', font=('Consolas'),  pady=20, padx=20)

modify_frame.place(x=50, y=100)
B1 = tk.Button(
    modify_frame,
    text='Teacher',
    font=('Consolas'),
    command=run_teach,
    width=10
)
B1.pack(pady=10)
B2 = tk.Button(
    modify_frame,
    text='Room',
    font=('Consolas'),
    command=run_room,
    width=10
)
B2.pack(pady=10)
B3 = tk.Button(
    modify_frame,
    text='MEETING',
    font=('Consolas'),
    command=run_m_t,
    width=10
)
B3.pack(pady=10)
B4 = tk.Button(
    modify_frame,
    text='COURS',
    font=('Consolas'),
    command=run_cour,
    width=10
)
B4.pack(pady=10)


tt_frame = tk.LabelFrame(
    text='Dashboard-2', font=('Consolas'), padx=20, height=100)
tt_frame.place(x=550, y=100)

B5 = tk.Button(
    tt_frame,
    text='DEPT',
    font=('Consolas'),
    command=run_dep,
    width=16
)
B5.pack(pady=20)
tk.Button(
    tt_frame,
    text='Section',
    font=('Consolas'),
    command=run_sc,
    width=16
).pack(pady=20)

tk.Button(
    tt_frame,
    text='Schedule Periods',
    font=('Consolas'),
    command=run_tt,
    width=16
).pack(pady=20)


tk.Button(
    ad,
    text='Quit',
    font=('Consolas'),
    command=ad.destroy,
    width=10
).place(x=360, y=420)

ad.mainloop()
