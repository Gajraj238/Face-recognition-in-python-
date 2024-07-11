from PIL import ImageTk
from tkinter import *
import os

def home():
    menu_window.destroy()
    os.system('python home.py')


def add_emp():
    menu_window.destroy()
    os.system('python Add_emp.py')


def modify():
    menu_window.destroy()
    os.system('python Emp_modify.py')


def delete_emp():
    menu_window.destroy()
    os.system('python emp_Delete.py')


def emp_search():
    menu_window.destroy()
    os.system('python emp_Search.py')

def search_emp():
    menu_window.destroy()
    os.system('python search_emp.py')
#-----------------------------------------------------------------------------------------------------------------
#GUI OF MENU
menu_window = Tk()
menu_window.title('Home Page')
menu_window.geometry("1000x600+50+50")
menu_window.resizable(True, True)
background = ImageTk.PhotoImage(file='bg122.png')
bgLabel = Label(menu_window, image=background)
bgLabel.grid()

frame=Frame(menu_window, bg='skyblue')
frame.place(x=650, y=140, width=260, height=320)

heading=Label(frame, text='Home', font=('Microsoft Yahei UI Light', 18, 'bold'), bg='Sky blue', fg='black')
heading.grid(row=0,column=0,sticky='w',padx=100,pady=10)

add_button=Button(frame,text='Add Emp Details', width=14,font=('Open Sans',12),bg='sky blue',fg='blue',bd=1,cursor='hand2',command=add_emp)
add_button.place(x=70,y=70)

modify_Button=Button(frame,text='Modify Emp Details', width=14,font=('Open Sans',12),bg='sky blue',fg='blue',bd=1,cursor='hand2',command=modify)
modify_Button.place(x=70,y=120)

search_button1=Button(frame,text='Search Employee', width=14,font=('Open Sans',12),bg='sky blue',fg='blue',bd=1,cursor='hand2',command=search_emp )
search_button1.place(x=70,y=170)

search_button=Button(frame,text='Search Records', width=14,font=('Open Sans',12),bg='sky blue',fg='Blue',bd=1,cursor='hand2',command=emp_search )
search_button.place(x=70,y=220)

delete_Button=Button(frame,text='Delete Employee',width=14, font=('Open Sans',12),bg='sky blue', fg='blue', bd=1, cursor= 'hand2', command=delete_emp)
delete_Button.place(x=70,y=270)

back=Button(frame,text='<<',width=2, font=('Open Sans',10,'bold'),bg='sky blue',fg='Black',bd=0,cursor='hand2',command=home)
back.place(x=4,y=3)


menu_window.mainloop()