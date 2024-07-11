from tkinter import messagebox
from PIL import ImageTk
from tkinter import *
import pymysql
import os
global con

def menu():
    delete_window.destroy()
    os.system('python Menu.py')
def clear () :
    id_Entry.delete(0, END)
    name_Entry.delete(0, END)

#______________________________________________________________________________________________________
#Function to connect database
def delete_emp():
    if id_Entry.get() == '' or name_Entry.get() == '':
        messagebox.showerror('Warning..', 'All fields are Required')
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='gajraj123')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Connection is not established try again')
            return
        print("Connection Establish For Deleteion Employee details")
        query = 'use frs_db'
        mycursor.execute(query)
        query = 'delete from emp_info where id=%s and emp_name=%s'
        result = mycursor.execute(query, (id_Entry.get(), name_Entry.get()))
        if result != 1:
            messagebox.showerror('Warning..', 'Invalid ID and Employee Name')
        else:
            messagebox.showinfo('Message..', "Employee Details has been removed.")
            con.commit()
            clear()
            print("Connection is closed")
            con.close()
            delete_window.destroy()
            os.system('python Menu.py')

#______________________________________________________________________________________________________
#GUI of Delete Emp Record
delete_window = Tk()
delete_window.title('Modify Employee Details')
delete_window.geometry("1000x600+50+50")
delete_window.resizable(False, False)
background = ImageTk.PhotoImage(file='bg122.png')
bgLabel = Label(delete_window, image=background)
bgLabel.grid()

frame = Frame(delete_window, bg='white')
frame.place(x=554, y=150, width=350, height=250)

heading = Label(frame, text='Delete-Employee-Details', font=('Microsoft Yahei UI Light', 18, 'bold'),
                bg='white', fg='black')
heading.grid(row=0, column=0, sticky='w', padx=30, pady=10)

emp_id = Label(frame, text='Employee Id', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='white', fg='black')
emp_id.grid(row=1, column=0, sticky='w', padx=35,pady=0)
id_Entry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 12), bg='white', fg='black')
id_Entry.grid(row=2, column=0, sticky='w', padx=35,pady=0)


emp_name = Label(frame, text='Employee Name', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='white', fg='black')
emp_name.grid(row=3, column=0, sticky='w', padx=35,pady=(20,0))
name_Entry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 12), bg='white', fg='black')
name_Entry.grid(row=4, column=0, sticky='w', padx=35,pady=0)

del_Button = Button(frame, text='Delete', font=('Open Sans', 12),
                    bd=0, bg='red', fg='white', width=14,command=delete_emp)
del_Button.grid(row=5, column=0, sticky='w', padx=105,pady=(30, 0))

back = Button(frame, text='<<', font=('Open Sans',8,'bold'), bd=0, bg='white', fg='black', cursor='hand2',width=2,command=menu)
back.place(x=6,y=3)

delete_window.mainloop()
