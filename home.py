from PIL import ImageTk
from tkinter import *
import os
def home():
    home_window.destroy()
    os.system('python Menu.py')
def login():
    home_window.destroy()
    os.system('python Admin_login.py')
def face_reco():
    home_window.destroy()
    os.system('python Face_recognition.py')

# Gui of Home Page
home_window = Tk()
home_window.title('Welcome Page')
home_window.geometry("1000x600+50+50")
home_window.resizable(True, True)
background = ImageTk.PhotoImage(file='bg122.png')
bgLabel = Label(home_window, image=background)
bgLabel.grid()

frame = Frame(home_window, bg='white')
frame.place(x=554, y=220, width=400, height=120)

heading = Label(frame, text='Welcome Mr/Ms Admin', font=('Microsoft Yahei UI Light', 18, 'bold'), bg='white',
                fg='black')
heading.grid(row=0, column=0, sticky='w', padx=60, pady=10)

menu_button = Button(frame, text='Home', width=12, font=('Open Sans', 12), bg='firebrick1', fg='Black', bd=0,
                     cursor='hand2', command=home)
menu_button.place(x=80, y=60)

FR_Button = Button(frame, text='Start Recognition', font=('Open Sans', 12), bg='firebrick1', fg='Black', bd=0,
                   cursor='hand2', command=face_reco)
FR_Button.place(x=200, y=60)

back = Button(frame, text='<<', font=('Open Sans', 8, 'bold'), bg='white', fg='Black', bd=0, cursor='hand2',
              command=login)
back.place(x=8, y=4)

home_window.mainloop()
