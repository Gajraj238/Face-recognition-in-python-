from tkinter import *
from PIL import ImageTk, Image
from tkinter import Label
from tkinter import messagebox
import face_recognition
import pymysql
import cv2
import mysql.connector
import os
global photo
global username
global counter
counter = 0
# _________________________________________________________________________________________________________________
# Function To Capture Image
def Image_capture():
    global username
    cam = cv2.VideoCapture(0)
    result, image = cam.read()
    if result:
        cv2.imshow("Admin-IMG", image)
        cv2.imwrite("Admin-IMG.png", image)
    else:
        messagebox.showerror("Error","No image detected. Please! try again")
    cv2.waitKey(0)
    cam.release()
    cv2.destroyWindow("Admin-IMG")
    fatch_image("username", "Admin-IMG2.png")
    compare_img()
# _________________________________________________________________________________________________________________

# Convert binary data to proper format and write it on Hard Disk
def write_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

# _________________________________________________________________________________________________________________
# Function to fatch image from database
def fatch_image(username, photo):
    try:
        connection=mysql.connector.connect(host='localhost', database='frs_db', user='root', password='gajraj123')
        print("Connection Establish for Fetching Image from DataBase...")
        cursor = connection.cursor()
        sql_fetch_blob_query = 'SELECT photo from login_info where username = %s'
        cursor.execute(sql_fetch_blob_query, (usernameEntry.get(),))
        record = cursor.fetchall()
        global row
        for row in record:
            image = row[0]
            write_file(image, photo)
    except mysql.connector.Error as error:
        print("Failed to fetch image from MySQL table {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

#-----------------------------------------------------------------------------------------------------------------------
#Function to Compare to image
def compare_img():
    global counter
    img = cv2.imread("Admin-IMG.png")
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_loc = face_recognition.face_locations(rgb_img)[0]
    cv2.rectangle(img, (img_loc[3], img_loc[0]), (img_loc[1], img_loc[2]), (0, 255, 0), 2)
    img_encoding = face_recognition.face_encodings(rgb_img)[0]

    img1 = cv2.imread("Admin-IMG2.png")
    rgb_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img_loc1 = face_recognition.face_locations(rgb_img1)[0]
    cv2.rectangle(img1, (img_loc1[3], img_loc1[0]), (img_loc1[1], img_loc1[2]), (0, 255, 0), 2)
    img_encoding1 = face_recognition.face_encodings(rgb_img1)[0]

    result = face_recognition.compare_faces([img_encoding], img_encoding1)
    print("result:", result)
    if result == [True]:
        counter = 1
        messagebox.showinfo('Success', "Match found")
    else:
        messagebox.showerror('Error', "Match not Found")
        counter = 0
    return True
# _______________________________________________________________________________________________________________
# FORGET PASSWORD FUNCTION
def forget_pass():
    reset_window = Toplevel()
    reset_window.title('Reset page')
    reset_window.geometry("400x300+50+50")
    reset_window.resizable(False, False)

    def forget_page():
        forget_db()
        reset_window.destroy()

    def forget_db():
        if usernameEntry1.get() == '' or passwordEntry1.get() == '' or confirmEntry1.get() == '':
            messagebox.showerror('Warning..', 'All fields are Required')
        else:
            password = passwordEntry1.get()
            cpassword = confirmEntry1.get()
            username0 = usernameEntry1.get()
            if password != cpassword:
                messagebox.showinfo('Warning..', "Both Password and Confirm Password should be same ")
            else:
                try:
                    con = pymysql.connect(host='localhost', user='root', password='gajraj123')
                    mycursor = con.cursor()
                except:
                    messagebox.showerror('Error', 'Connection is not established try again')
                    return
                print("Connection is Establish for Reset Password")
                query = 'use frs_db'
                mycursor.execute(query)
                query = 'select * from login_info where username = %s '
                row = mycursor.execute(query, (usernameEntry1.get(),))
                if row != 1:
                    messagebox.showerror('Warning..', 'Invalid username ')
                else:
                    query = 'update login_info  set password = %s where username = %s '
                    mycursor.execute(query, (passwordEntry1.get(), usernameEntry1.get()))
                    messagebox.showinfo("Congrats", "Password has been succesfully Changed")
                    con.commit()
                    print("Connection is Closed")
                    con.close()

    def user_enter1(event):
        if usernameEntry1.get() == 'Username':
            usernameEntry1.delete(0, END)

    def password_enter1(event):
        if passwordEntry1.get() == 'Password':
            passwordEntry1.delete(0, END)

    def password_enter2(event):
        if confirmEntry1.get() == 'New Password':
            confirmEntry1.delete(0, END)

    def hide():
        openeye.config(file='closeeye1.png')
        passwordEntry1.config(show='*')
        eyeButton.config(command=show)

    def show():
        openeye.config(file='openeye1.png')
        passwordEntry1.config(show='')
        eyeButton.config(command=hide)

    def hide1():
        openeye1.config(file='closeeye1.png')
        confirmEntry1.config(show='*')
        eyeButton1.config(command=show1)

    def show1():
        openeye1.config(file='openeye1.png')
        confirmEntry1.config(show='')
        eyeButton1.config(command=hide1)

    frame = Frame(reset_window, bg='sky blue')
    frame.place(x=0, y=0, width=400, height=300)
    heading = Label(frame, text='RESET PASSWORD', font=('Microsoft Yahei UI Light', 14, 'bold'), bg='sky blue',
                    fg='black')
    heading.grid(row=0, column=0, sticky='w', padx=100, pady=10)

    usernameLabel = Label(frame, text='Username', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='sky blue',
                          fg='black')
    usernameLabel.grid(row=1, column=0, sticky='w', padx=35)
    usernameEntry1 = Entry(frame, width=35, font=('Microsoft Yahei UI Light', 10, 'bold'), bg='sky blue', fg='black')
    usernameEntry1.grid(row=2, column=0, sticky='w', padx=35)
    usernameEntry1.bind('<FocusIn>', user_enter1)

    passwordLabel = Label(frame, text='Password', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='sky blue',
                          fg='black')
    passwordLabel.grid(row=3, column=0, sticky='w', padx=35)
    passwordEntry1 = Entry(frame, width=35, font=('Microsoft Yahei UI Light', 10, 'bold'), bg='sky blue', fg='black',
                           show="*")
    passwordEntry1.grid(row=4, column=0, sticky='w', padx=35)
    passwordEntry1.bind('<FocusIn>', password_enter1)

    openeye = PhotoImage(file='closeeye1.png')
    eyeButton = Button(frame, image=openeye, width=30, height=12, bd=0, bg='sky blue', activebackground='sky blue',
                       cursor='hand2', command=show)
    eyeButton.grid(row=4, column=0, sticky='w', padx=280)

    confirmLabel = Label(frame, text='Confirm Password', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='sky blue',
                         fg='black')
    confirmLabel.grid(row=5, column=0, sticky='w', padx=35)
    confirmEntry1 = Entry(frame, width=35, font=('Microsoft Yahei UI Light', 10, 'bold'), bg='sky blue', fg='black',
                          show="*")
    confirmEntry1.grid(row=6, column=0, sticky='w', padx=35)
    confirmEntry1.bind('<FocusIn>', password_enter2)

    openeye1 = PhotoImage(file='closeeye1.png')
    eyeButton1 = Button(frame, image=openeye1, width=30, height=12, bd=0, bg='sky blue', activebackground='sky blue',
                        cursor='hand2', command=show1)
    eyeButton1.grid(row=6, column=0, sticky='w', padx=280)

    submitButton = Button(frame, text='Submit', font=('Open Sans', 14), bd=0, bg='firebrick1', fg='white', width=17,
                          command=forget_page)
    submitButton.grid(row=7, column=0, sticky='w', padx=70, pady=25)
    reset_window.mainloop()


#_______________________________________________________________________________________________________________________
# LOGIN  VALIDATION + DATABASE CONNECTION
def login_user():
    global counter, username, con
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Warning..', 'All fields are Required')
    else:
        try:
            username = usernameEntry.get()
            con = pymysql.connect(host='localhost', user='root', password='gajraj123')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Connection is not established try again')
            return
        print("Connection Establish For fetching Username and Password")
        query = 'use frs_db'
        mycursor.execute(query)
        query = 'select * from login_info where username=%s and password=%s'
        row = mycursor.execute(query, (usernameEntry.get(), passwordEntry.get()))
        if row != 1:
            messagebox.showerror('Warning..', 'Invalid username and password')
        else:
            if counter == 1:
                messagebox.showinfo('Message..', "Welcome Mr/Ms " + username)
                login_window.destroy()
                os.system('python home.py')
            else:
                counter = 0
                messagebox.showerror('Warning', "Face Authentication is required")
                con.commit()
                print("Connection is closed")
                con.close()
#GUI of Login Page
# _______________________________________________________________________________________________________________________
def signup_page():
    login_window.destroy()
    os.system('python Create_Account.py')


# ___________________________________________________________________________________________________________________
# SHOW PASSWORD & HIDE
def hide():
    openeye.config(file='closeeye1.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)


def show():
    openeye.config(file='openeye1.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)


def user_enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)


def password_enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)


# _____________________________________________________________________________________________________________________________
# LOGIN GUI
login_window = Tk()
login_window.geometry("1000x600")
login_window.resizable(False,False)
login_window.title('Login Page')
background = ImageTk.PhotoImage(file='Login1.jpg')
bgLabel = Label(login_window, image=background)
bgLabel.place(x=0, y=0)
frame = Frame(login_window, bd=0,bg='sky blue')
frame.place(x=60, y=100,width=380, height=350)
heading = Label(frame, text='LOGIN ', font=('Microsoft Yahei UI Light', 18, 'bold'), bg='sky blue', fg='black')
heading.grid(row=0, column=0, sticky='w', padx=150, pady=10)
usernameLabel = Label(frame, text='Username', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='sky blue', fg='black')
usernameLabel.grid(row=1, column=0, sticky='w', padx=25, pady=(10, 0))
usernameEntry = Entry(frame, width=35, font=('Microsoft Yahei UI Light', 11), bg='sky blue',bd=1, fg='black')
usernameEntry.grid(row=2, column=0, sticky='w', padx=25)
usernameEntry.bind('<FocusIn>', user_enter)

passwordLabel = Label(frame, text='Password', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='sky blue', fg='black')
passwordLabel.grid(row=3, column=0, sticky='w', padx=25, pady=(10, 0))
passwordEntry = Entry(frame, width=35, font=('Microsoft Yahei UI Light', 11), bd=1, bg='sky blue', fg='black', show="*")
passwordEntry.grid(row=4, column=0, sticky='w', padx=25)
passwordEntry.bind('<FocusIn>', password_enter)

openeye = PhotoImage(file='closeeye1.png')
eyeButton = Button(frame, image=openeye, width=30, height=12, bd=0, bg='sky blue', activebackground='sky blue',
                   cursor='hand2', command=show)
eyeButton.grid(row=4, column=0, sticky='w', padx=270, pady=(9, 0))

forgetButton = Button(frame, width=15, pady=4, text='Forgot Password?', bd=0, bg='sky blue',
                      activebackground='sky blue', cursor='hand2', font=('Microsoft Yahei UI Light', 9, 'bold'), fg='blue',
                      activeforeground='firebrick1', command=forget_pass)
forgetButton.grid(row=5, column=0, sticky='w', padx=25, pady=(10, 0))

loginButton = Button(frame, text='Login', pady=7, fg='white', font=('Open Sans', 9, 'bold'), bg='firebrick1',activeforeground='sky blue', activebackground='firebrick1',cursor='hand2', bd=0, width=20, command=login_user)
loginButton.grid(row=6, column=0, sticky='w', padx=25, pady=(10, 0))
face_match = Button(frame, text='Face Authentication', pady=7, fg='Black', bg='white', font=('Open Sans', 9, 'bold'),activeforeground='white', activebackground='white',cursor='hand2', bd=0, width=17, command=Image_capture)
face_match.grid(row=6, column=0, sticky='w', padx=180, pady=(10, 0))
signupLabel = Label(frame, text='Dont have an account?', font=('Open Sans', 9, 'bold'), fg='black', bg='sky blue')
signupLabel.place(x=35, y=264)

newaccountButton = Button(frame, text='Create New', font=('Microsoft Yahei UI Light', 9, 'bold'),fg='blue', bg='sky blue', activeforeground='sky blue', activebackground='sky blue',cursor='hand2', bd=0, command=signup_page)
newaccountButton.grid(row=7, column=0, sticky='w', padx=210)

login_window.mainloop()
