import pymysql
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk
from tkinter import *
import os

def back():
    search_emp_window.destroy()
    os.system('python Menu.py')
def back2():
    search_emp_window.destroy()
    os.system('python Menu.py')

def clear():
    id_Entry.delete(0, END)
#_______________________________________________________________________________________________________
#Function to View Record by ID and Date
def search_emp_detail():
    if id_Entry.get() == '':
        messagebox.showerror("Error", "All fields are required..")

    else:

        id = id_Entry.get()
        my_connect = pymysql.connect(host="localhost", user="root", password="gajraj123", database="frs_db")
        my_conn = my_connect.cursor()
        query = 'SELECT id,emp_name,email,dept FROM emp_info where id = %s'
        result = my_conn.execute(query, (id,))
        print (result)
        if result == 0 :
            messagebox.showerror("Error", "No Record Found")
            clear()
        else:
            my_w = tk.Tk()
            my_w.geometry("620x350")
            i = 1
            e = Label(my_w, width=17, text='Emp_ID', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
            e.grid(row=0, column=0, padx=(0, 0))
            e = Label(my_w, width=17, text='Emp_Name', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
            e.grid(row=0, column=1)
            e = Label(my_w, width=17, text='Email', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
            e.grid(row=0, column=2)
            e = Label(my_w, width=17, text='Department', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
            e.grid(row=0, column=3)
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
def search_emp_detail2():
        my_connect = pymysql.connect(host="localhost", user="root", password="gajraj123", database="frs_db")
        my_conn = my_connect.cursor()
        query = 'SELECT id, emp_name, email, dept FROM emp_info'
        result = my_conn.execute(query)
        print (result)
        if result == 0 :
            messagebox.showerror("Error", "No Record Found")
            clear()
        else:
            my_w = tk.Tk()
            my_w.geometry("620x350")
            i = 1
            e = Label(my_w, width=20, text='Emp_ID', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
            e.grid(row=0, column=0, padx=(0, 0))
            e = Label(my_w, width=20, text='Emp_Name', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
            e.grid(row=0, column=1)
            e = Label(my_w, width=20, text='Email', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
            e.grid(row=0, column=2)
            e = Label(my_w, width=20, text='Department', borderwidth=2, relief='ridge', anchor='w', bg='yellow')
            e.grid(row=0, column=3)
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
search_emp_window = Tk()
search_emp_window.title('View Emp Details')
search_emp_window.geometry("1000x600+50+50")
search_emp_window.resizable(True, True)
background = ImageTk.PhotoImage(file='bg122.png')
bgLabel = Label(search_emp_window, image=background)
bgLabel.grid()

frame = Frame(search_emp_window, bg='sky blue')
frame.place(x=600, y=100, width=350, height=160)

heading = Label(frame, text='View Employee Detail', font=('Microsoft Yahei UI Light', 14, 'bold'), bg='sky blue', fg='black')
heading.grid(row=0, column=0, sticky='w', padx=70, pady=4)

emp_id = Label(frame, text='Employee ID', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='sky blue', fg='black')
emp_id.grid(row=1, column=0, sticky='w', padx=110, pady=(10, 0))
id_Entry = Entry(frame, width=12, font=('Microsoft Yahei UI Light', 12), bg='sky blue', fg='black')
id_Entry.grid(row=2, column=0, sticky='w', padx=110)


View = Button(frame, text='View', font=('Microsoft Yahei UI Light', 10, 'bold'), bd=0, bg='red', fg='black', width=14,
              command=search_emp_detail)
View.grid(row=3, column=0, sticky='w', padx=100, pady=(10, 0))

back = Button(frame, text='<<', font=('Open Sans', 10, 'bold'), bd=0, bg='sky blue', fg='black', cursor='hand2',
              width=2, command=back)
back.place(x=5, y=2)

frame1 = Frame(search_emp_window, bg='sky blue')
frame1.place(x=600, y=280, width=350, height=160)

heading = Label(frame1, text='View Employee Details', font=('Microsoft Yahei UI Light', 14, 'bold'), bg='sky blue', fg='black')
heading.grid(row=0, column=0, sticky='w', padx=70, pady=4)

View = Button(frame1, text='View All', font=('Microsoft Yahei UI Light', 10, 'bold'), bd=0, bg='red', fg='black', width=14,
              command=search_emp_detail2)
View.grid(row=3, column=0, sticky='w', padx=110, pady=(25, 0))

back = Button(frame1, text='<<', font=('Open Sans', 10, 'bold'), bd=0, bg='sky blue', fg='black', cursor='hand2',
              width=2, command=back2)
back.place(x=5, y=2)

search_emp_window.mainloop()
