import mysql.connector
import tkinter as tk
from tkinter import messagebox
import datetime
from PIL import ImageTk
from tkinter import *
import os


def back():
    search_window.destroy()
    os.system('python Menu.py')

def back2():
    search_window.destroy()
    os.system('python Menu.py')

def clear():
    id_Entry.delete(0, END)
    date_Entry.delete(0, END)
    date_Entry1.delete(0, END)


def validate_date(date_string):
    date_format = '%Y-%m-%d'
    try:
        datetime.datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False
#_______________________________________________________________________________________________________
#Function to View Record by ID and Date
def search_emp():
    date1 = date_Entry1.get()
    validate = validate_date(date1)
    if date_Entry1.get() == '' or id_Entry.get() == '':
        messagebox.showerror("Error", "All fields are required..")
    elif validate != True:
        messagebox.showerror("Error", "Invalid Date Format")
    else:
        date = date_Entry1.get()
        id = id_Entry.get()
        my_connect = mysql.connector.connect(host="localhost", user="root", password="gajraj123", database="frs_db")
        my_conn = my_connect.cursor()
        query = 'SELECT emp_id, emp_name, emp_dept, date, time FROM emp_record where emp_id = %s AND date = %s'
        my_conn.execute(query, (id, date,))
        result = my_conn.fetchone()
        print(result)
        if result is None:
            messagebox.showerror("Error", "No Record Found")
            clear()
        else:
            my_w = tk.Tk()
            my_w.geometry("620x350")
            i = 1
            e = Label(my_w, width=15, text='Emp_ID', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
            e.grid(row=0, column=0, padx=(0, 0))
            e = Label(my_w, width=15, text='Name', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
            e.grid(row=0, column=1)
            e = Label(my_w, width=15, text='Department', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
            e.grid(row=0, column=2)
            e = Label(my_w, width=15, text='Date', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
            e.grid(row=0, column=3)
            e = Label(my_w, width=15, text='Date', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
            e.grid(row=0, column=4)
            for emp_record in my_conn:
                for j in range(len(emp_record)):
                    e = Entry(my_w, width=20, fg='Black')
                    e.grid(row=i, column=j, padx=(0, 0))
                    e.insert(END, emp_record[j])
                i = i + 1
            my_connect.commit()
            my_connect.close()
            clear()
            my_w.mainloop()
#_______________________________________________________________________________________________________
#Function to View Record by Date
def search_emp2():
    date1 = date_Entry.get()
    validate = validate_date(date1)
    if date_Entry.get() == '':
        messagebox.showerror("Error", "All fields are required..")
    elif validate != True:
        messagebox.showerror("Error", "Invalid Date Format")
    else:
        date = date_Entry.get()
        my_connect = mysql.connector.connect(host="localhost", user="root", password="gajraj123", database="frs_db")

        my_conn = my_connect.cursor()
        query = 'SELECT emp_id, emp_name, emp_dept, date, time FROM emp_record where date = %s'
        my_conn.execute(query, (date,))
        result = my_conn.fetchone()
        if result == None:
            messagebox.showerror("Error", "No Record Found")
            clear()
        else:
            my_w = tk.Tk()
            my_w.geometry("620x350")
            i = 1
            e = Label(my_w, width=15, text='Emp_ID', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
            e.grid(row=0, column=0, padx=(0, 0))
            e = Label(my_w, width=15, text='Name', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
            e.grid(row=0, column=1)
            e = Label(my_w, width=15, text='Department', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
            e.grid(row=0, column=2)
            e = Label(my_w, width=15, text='Date', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
            e.grid(row=0, column=3)
            e = Label(my_w, width=15, text='Date', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
            e.grid(row=0, column=4)
            for emp_record in my_conn:
                for j in range(len(emp_record)):
                    e = Entry(my_w, width=20, fg='Black')
                    e.grid(row=i, column=j, padx=(0, 0))
                    e.insert(END, emp_record[j])
                i = i + 1
            my_connect.commit()
            my_connect.close()
            clear()
            my_w.mainloop()
#----------------------------------------------------------------------------------------------------------
#GUI of View Emp record
search_window = Tk()
search_window.title('View Emp Records')
search_window.geometry("1000x600+50+50")
search_window.resizable(True, True)
background = ImageTk.PhotoImage(file='bg122.png')
bgLabel = Label(search_window, image=background)
bgLabel.grid()

frame = Frame(search_window, bg='sky blue')
frame.place(x=600, y=100, width=350, height=160)

heading = Label(frame, text='View Record', font=('Microsoft Yahei UI Light', 14, 'bold'), bg='sky blue', fg='black')
heading.grid(row=0, column=0, sticky='w', padx=110, pady=4)

emp_id = Label(frame, text='Employee ID', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='sky blue', fg='black')
emp_id.grid(row=1, column=0, sticky='w', padx=45, pady=(10, 0))
id_Entry = Entry(frame, width=12, font=('Microsoft Yahei UI Light', 12), bg='sky blue', fg='black')
id_Entry.grid(row=2, column=0, sticky='w', padx=45)

date = Label(frame, text='YYYY-MM-DD', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='sky blue', fg='black')
date.grid(row=1, column=0, sticky='w', padx=185, pady=(10, 0))
date_Entry1 = Entry(frame, width=12, font=('Microsoft Yahei UI Light', 12), bg='sky blue', fg='black')
date_Entry1.grid(row=2, column=0, sticky='w', padx=185)

View = Button(frame, text='View', font=('Microsoft Yahei UI Light', 10, 'bold'), bd=0, bg='red', fg='black', width=14,
              command=search_emp)
View.grid(row=3, column=0, sticky='w', padx=100, pady=(10, 0))

back = Button(frame, text='<<<', font=('Open Sans', 10, 'bold'), bd=0, bg='sky blue', fg='black', cursor='hand2',
              width=2, command=back)
back.place(x=5, y=2)

frame1 = Frame(search_window, bg='sky blue')
frame1.place(x=600, y=280, width=350, height=160)

heading = Label(frame1, text='View Records', font=('Microsoft Yahei UI Light', 14, 'bold'), bg='sky blue', fg='black')
heading.grid(row=0, column=0, sticky='w', padx=110, pady=4)

date = Label(frame1, text='YYYY-MM-DD', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='sky blue', fg='black')
date.grid(row=1, column=0, sticky='w', padx=30, pady=(10, 0))
date_Entry = Entry(frame1, width=30, font=('Microsoft Yahei UI Light', 12), bg='sky blue', fg='black')
date_Entry.grid(row=2, column=0, sticky='w', padx=30)

View = Button(frame1, text='View', font=('Microsoft Yahei UI Light', 10, 'bold'), bd=0, bg='red', fg='black', width=14,
              command=search_emp2)
View.grid(row=3, column=0, sticky='w', padx=110, pady=(10, 0))

back = Button(frame1, text='<<<', font=('Open Sans', 10, 'bold'), bd=0, bg='sky blue', fg='black', cursor='hand2',
              width=2, command=back2)
back.place(x=5, y=2)

search_window.mainloop()
