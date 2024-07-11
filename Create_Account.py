from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import pymysql
import cv2
import re
import os
global con
global counter
counter = 0

# ********************************************************************************************************************
# FUNCTION TO CAPTURE IMAGE
def Image_capture():
    global counter
    cam = cv2.VideoCapture(0)
    result, image = cam.read()
    if result:
        cv2.imshow("Admin-IMG", image)
        cv2.imwrite("Admin-IMG.png", image)
    else:
        messagebox.showerror('Error', "No image detected. Please! try again")
    cv2.waitKey(0)
    cam.release()
    cv2.destroyWindow("Admin-IMG")
    counter = 1


# ******************************************************************************************************************
# FUNCTION TO CONVERT IMAGE INTO BINARY
def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# FUNCTION TO SHOW AND HIDE PASSWORD
def hide():
    openeye.config(file='closeeye1.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)


def show():
    openeye.config(file='openeye1.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)


def hide1():
    openeye1.config(file='closeeye1.png')
    confirmEntry.config(show='*')
    eyeButton1.config(command=show1)


def show1():
    openeye1.config(file='openeye1.png')
    confirmEntry.config(show='')
    eyeButton1.config(command=hide1)


# ***********************************************************************************************************************
# DATABASE Connectivity
def clear():
    emailEntry.delete(0, END)
    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)
    confirmEntry.delete(0, END)


# Password Validation
def validate_password(password):
    if 6 <= len(password) <= 8:
        return False
        if not re.search("[a-z]", password):
            return False
        if not re.search("[A-Z]", password):
            return False
        if not re.search("[0-9]", password):
            return False
    return True

def validate_username(password):
    if 3 <= len(password) <= 20:
        return False
        if not re.search("[a-z]", password):
            return False
        if not re.search("[A-Z]", password):
            return False
        if not re.search("[0-9]", password):
            return False
    return True


def connect_database():
    global counter
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    email = emailEntry.get()
    password = passwordEntry.get()
    username = usernameEntry.get()
    valid = re.fullmatch(regex, email)
    valid_pass = validate_password(password)
    valid_user = validate_username(username)
    if emailEntry.get() == '' or usernameEntry.get() == '' or passwordEntry.get() == '' or confirmEntry.get() == '':
        messagebox.showerror('Warning..', 'All fields are required')
    elif passwordEntry.get() != confirmEntry.get():
        messagebox.showerror('Warning..', 'Password mismatch')
    elif valid is None:
        messagebox.showerror("Error", "Enter a valid Email")
    elif valid_user:
        messagebox.showerror("Error", "Invalid username\n ->username lenght Should be 3 to 20 character\n ->username can be "
                                      "Numeric,Alphabetic or Alphanumeric ")
    elif valid_pass:
        messagebox.showerror("Error", "Invalid Password\n ->Password lenght Should be 6 to 8\n ->Pasword can be "
                                      "Numeric,Alphabetic or Alphanumeric ")
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='gajraj123')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Database connectivity issue please try again')
            return
        try:
            print("Connection is Establish for storing Registeration info")
            query = 'create database FRS_DB'
            mycursor.execute(query)
            query = 'use FRS_DB'
            mycursor.execute(query)
            query = ('create table login_info(id int auto_increment primary key not null, email varchar(50), username '
                     'varchar(100), password varchar(20), photo longBLOB)')
            mycursor.execute(query)
        except:
            mycursor.execute('use FRS_DB')
        query = 'select * from login_info where username=%s'
        row = mycursor.execute(query, (usernameEntry.get()))
        if row == 1:
            messagebox.showerror('Error', 'Username already exists')
        else:
            query = 'insert into login_info(email,username,password,photo) values(%s,%s,%s,%s)'
            emp_img = convertToBinaryData("Admin-IMG.png")
            result = mycursor.execute(query, (emailEntry.get(), usernameEntry.get(), passwordEntry.get(), emp_img))
            if result != counter:
                messagebox.showerror('Error', "Admin Face Expression is Required ")
                counter = 0
            else:
                messagebox.showinfo('Success', 'Congrats Your Account Successfully Created ')
                con.commit()
                con.close()
                clear()
                print("connection is close")
                signup_window.destroy()
                os.system('python Admin_login.py')


def login_page():
    signup_window.destroy()
    os.system('python Admin_login.py')


# GUI OF Registration
signup_window = Tk()
signup_window.title('Signup Page')
signup_window.geometry("1000x600+50+50")
signup_window.resizable(True, True)
background = ImageTk.PhotoImage(file='bg122.png')

bgLabel = Label(signup_window, image=background)
bgLabel.grid()
frame = Frame(signup_window, bg='white')
frame.place(x=554, y=100, width=360, height=395)

heading = Label(frame, text='Admin Registration', font=('Microsoft Yahei UI Light', 18, 'bold'), bg='white', fg='black')
heading.grid(row=0, column=0, sticky='w', padx=80, pady=10)

emailLabel = Label(frame, text='Email', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='white', fg='black')
emailLabel.grid(row=1, column=0, sticky='w', padx=25, pady=(10, 0))

emailEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 12), bg='white', fg='black')
emailEntry.grid(row=2, column=0, sticky='w', padx=25)

usernameLabel = Label(frame, text='Username', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='white', fg='black')
usernameLabel.grid(row=3, column=0, sticky='w', padx=25, pady=(10, 0))

usernameEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 12), bg='white', fg='black')
usernameEntry.grid(row=4, column=0, sticky='w', padx=25)

passwordLabel = Label(frame, text='Password', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='white', fg='black')
passwordLabel.grid(row=5, column=0, sticky='w', padx=25)

passwordEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 12), bg='white', fg='black', show="*")
passwordEntry.grid(row=6, column=0, sticky='w', padx=25)
openeye = PhotoImage(file='closeeye1.png')
eyeButton = Button(frame, image=openeye, width=30, height=12, bd=0, bg='white', activebackground='white',
                   cursor='hand2', command=show)
eyeButton.grid(row=6, column=0, sticky='w', padx=260)

confirmLabel = Label(frame, text='Confirm Password', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='white',
                     fg='black')
confirmLabel.grid(row=7, column=0, sticky='w', padx=25)

confirmEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 12), bg='white', fg='black', show="*")
confirmEntry.grid(row=8, column=0, sticky='w', padx=25)
openeye1 = PhotoImage(file='closeeye1.png')
eyeButton1 = Button(frame, image=openeye1, width=30, height=12, bd=0, bg='white', activebackground='white',
                    cursor='hand2', command=show1)
eyeButton1.grid(row=8, column=0, sticky='w', padx=260)

signupButton = Button(frame, text='Signup', font=('Open Sans', 12, 'bold'), bd=0, bg='red', fg='white', width=12,
                      command=connect_database)
signupButton.place(x=23, y=300)
Take_PicButton = Button(frame, text='Add Facial Image', font=('Open Sans', 12, 'bold'), bd=0, bg='sky blue', fg='black',
                        width=14, command=Image_capture)
Take_PicButton.place(x=150, y=300)

(Label(frame, text='Dont have an account?', font=('Open Sans', 9, 'bold'), fg='black', bg='white').grid(row=11,
                                                                                                        column=0,
                                                                                                        sticky='w',
                                                                                                        padx=25,
                                                                                                        pady=55))

loginButton = Button(frame, text='Login', font=('Open Sans', 9, 'bold underline'), bg='white', fg='blue', bd=0,
                     cursor='hand2', command=login_page)

loginButton.place(x=170, y=330)
signup_window.mainloop()
