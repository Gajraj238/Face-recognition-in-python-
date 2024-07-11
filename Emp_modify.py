from tkinter import messagebox
from PIL import ImageTk
from tkinter import *
import pymysql
import cv2
import re
global con
global counter
import os
counter = 0
def menu():
    modify_window.destroy()
    os.system('python Menu.py')

#__________________________________________________________________________________________________________
#function to capture Image
def Image_capture():
    global counter
    cam = cv2.VideoCapture(0)
    result, image = cam.read()
    if result:
        cv2.imshow("Up-Emp-IMG", image)
        cv2.imwrite("Up-Emp-IMG.png", image)
    else:
        messagebox.showerror('Error', "No image detected. Please! try again")
    cv2.waitKey(0)
    cam.release()
    cv2.destroyWindow("Up-Emp-IMG")
    counter = 1

# ******************************************************************************************************************
# FUNCTION TO CONVERT IMAGE INTO BINARY
def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def clear():
    name_Entry.delete(0, END)
    emailEntry.delete(0, END)
    Dept_Entry.delete(0, END)
#_____________________________________________________________________________________________________________
#function to Validate Emp Name
def validate_name(name):
    if len(name) >= 3 and len(name) <= 30:
        if re.search("[a-z]", name):
            return False
        if re.search("[A-Z]", name):
            return False
    return True
#_________________________________________________________________________________________________________
#function to Valiadte Department Name
def validate_dept(dept):
    if len(dept) >= 2 and len(dept) <= 30:
        if re.search("[a-z]", dept):
            return False
        if re.search("[A-Z]", dept):
            return False
    return True

#_________________________________________________________________________________________________________
#Function to Cnnect Database
def connect_database():
    global counter
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    email = emailEntry.get()
    name = name_Entry.get()
    dept = Dept_Entry.get()
    result = validate_name(name)
    result1 = validate_dept(dept)
    valid = re.fullmatch(regex, email)
    if id_Entry.get() == '' or emailEntry.get() == '' or name_Entry.get() == '' or Dept_Entry.get() == '':
       messagebox.showerror('Warning..', 'All fields are required')
    elif valid == None:
        messagebox.showerror("Error","Enter a valid Email")
    elif result != False:
        messagebox.showerror("Error","Invalid Employee Name \n -> Name lenght Should be 3 to 30\n ->Name should be only Alphabetic")
    elif result1 != False:
        messagebox.showerror("Error","Invalid Department  Name \n -> Dept name lenght Should be 3 to 30\n ->Dept name should be only Alphabetic")
    else:
        try:
            emp_id = id_Entry.get()
            con =pymysql.connect(host='localhost', user='root', password='gajraj123')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Database connectivity issue please try again')
            return
        print("Connection is establish for modifying Employee Details")
        mycursor.execute('use FRS_DB')
        query = 'select * from emp_info where id=%s '
        mycursor.execute(query , (id_Entry.get(),))
        row = mycursor.fetchone()
        if row == None:
            messagebox.showerror('Error', 'Employee Id not Found')
        else:
            query = 'update emp_info set emp_name= %s, email= %s, dept=%s, emp_photo=%s  where id = %s '
            up_emp_img = convertToBinaryData("Up-Emp-IMG.png")
            result = mycursor.execute(query, (name_Entry.get(), emailEntry.get(), Dept_Entry.get(),up_emp_img,emp_id))
            if result != counter:
                messagebox.showerror('Error', "Updated  Face Field is Required ")
                counter = 0
            else:
                messagebox.showinfo('Success', 'Employee Details has been Updated  successfully')
                con.commit()
                con.close()
                print("Connection is Closed..")
                clear()
                modify_window.destroy()
                os.system('python Menu.py')
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#__GUI OF Modify emp
modify_window = Tk()
modify_window.title('Modify Employee Details')
modify_window.geometry("1000x600+50+50")
modify_window.resizable(False, False)
background = ImageTk.PhotoImage(file='bg122.png')
bgLabel = Label(modify_window, image=background)
bgLabel.grid()

frame = Frame(modify_window, bg='white')
frame.place(x=554, y=100, width=370, height=400)

heading = Label(frame, text='Modify-Employee-Details', font=('Microsoft Yahei UI Light', 18, 'bold'), bg='white', fg='black')
heading.grid(row=0, column=0, sticky='w', padx=30, pady=10)

emp_id = Label(frame, text='Employee Id', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='white', fg='black')
emp_id.grid(row=1, column=0, sticky='w', padx=35, pady=(10, 0))
id_Entry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 12), bg='white', fg='black')
id_Entry.grid(row=2, column=0, sticky='w', padx=35)


emp_name = Label(frame, text='Updated Employee Name', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='white', fg='black')
emp_name.grid(row=3, column=0, sticky='w', padx=35, pady=(10, 0))
name_Entry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 12), bg='white', fg='black')
name_Entry.grid(row=4, column=0, sticky='w', padx=35)

emailLabel = Label(frame, text='Updated Email', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='white', fg='black')
emailLabel.grid(row=5, column=0, sticky='w', padx=35, pady=(10, 0))
emailEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 12), bg='white', fg='black')
emailEntry.grid(row=6, column=0, sticky='w', padx=35)

Dept_Label = Label(frame, text='Updated Department', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='white', fg='black')
Dept_Label.grid(row=7, column=0, sticky='w', padx=35,pady=(10, 0))
Dept_Entry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 12), bg='white', fg='black')
Dept_Entry.grid(row=8, column=0, sticky='w', padx=35)

Addface_Button = Button(frame, text='updated Face', font=('Open Sans', 12), bd=0, bg='sky blue', fg='black', width=14,command= Image_capture)
Addface_Button.grid(row=9, column=0, sticky='w', padx=35,pady=(18, 0))

Save_Button = Button(frame, text='Save', font=('Open Sans', 12), bd=0, bg='red', fg='white', width=14,command=connect_database)
Save_Button.grid(row=9, column=0, sticky='w', padx=180,pady=(18, 0))

back = Button(frame, text='<<', font=('Open Sans',8,'bold'), bd=0, bg='white', fg='black', cursor='hand2',width=2,command=menu)
back.place(x=3,y=3)
modify_window.mainloop()
