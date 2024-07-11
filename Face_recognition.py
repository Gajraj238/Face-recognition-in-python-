import mysql.connector
import io
import face_recognition
import cv2
import numpy
import numpy as np
import datetime
import pymysql
from tkinter import messagebox
import time
import threading
import os
known_face_encoding = []
empid_reco = []
emp_name = []
empdept_reco = []
cur_datetime = datetime.datetime.now()
cur_date = cur_datetime.date()
cur_time = cur_datetime.time()
name = ''
dept = ''
id = ''
#------------------------------------------------------------------------------------------------------
#Function to fetch Images from database
def database():
    while True:
        cur_time = datetime.datetime.now()
        try:
            con = pymysql.connect(host='localhost', user='root', password='gajraj123')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Database connectivity issue please try again')
            return
        query = 'use frs_db'
        mycursor.execute(query)
        query = 'insert into emp_record(emp_id,emp_name,emp_dept,date,time) values(%s,%s,%s,%s,%s)'
        global name
        mycursor.execute(query, (id, name, dept, cur_date, cur_time))
        con.commit()
        con.close()
        time.sleep(10)
        if cv2.waitKey(1) & 0xFF == ord('a'):
            break
#------------------------------------------------------------------------------------------------------
#Function to fetch Employee Information
def face_reco():
    print("connection is Establish for fetching Employee Information..")
    try:
        connection = mysql.connector.connect(host='localhost',database='frs_db',user='root',password='gajraj123')
        global known_face_encoding
        global empid_reco
        global emp_name
        global empdept_reco
        cursor = connection.cursor()
        sql_fetch_blob_query = """SELECT id from emp_info """
        cursor.execute(sql_fetch_blob_query)
        empid_reco = cursor.fetchall()
        sql_fetch_blob_query = """SELECT emp_name from emp_info """
        cursor.execute(sql_fetch_blob_query)
        emp_name = cursor.fetchall()
        sql_fetch_blob_query = """SELECT dept from emp_info """
        cursor.execute(sql_fetch_blob_query)
        empdept_reco = cursor.fetchall()
        sql_fetch_blob_query = """SELECT  emp_photo from emp_info """
        cursor.execute(sql_fetch_blob_query)
        img_record = cursor.fetchall()
        global a
        i = 0
        for a in img_record:
            file_l = io.BytesIO(a[0])
            image1 = face_recognition.load_image_file(file_l)
            face_encoding = face_recognition.face_encodings(image1)[0]
            known_face_encoding.append(face_encoding)
            i = i + 1
    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
#------------------------------------------------------------------------------------------------------
#Function to recognition face from Webcam
face_reco()
def face_reco2():

    print(known_face_encoding)
    video_capture = cv2.VideoCapture(0)
    face_locations = []
    face_encodings = []
    process_this_frame = True
    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = numpy.ascontiguousarray(small_frame[:, :, ::-1])
        print(rgb_small_frame)
        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            empdept = []
            emp_id = []
            global id
            for face_encoding1 in face_encodings:
                matches = face_recognition.compare_faces(known_face_encoding,face_encoding1, tolerance=0.6)
                global name
                global dept
                name = "Unknown"
                dept = " "
                id = " "
                face_distances = face_recognition.face_distance ( known_face_encoding, face_encoding1)
                best_match_index = np.argmin(face_distances,)
                if matches[best_match_index]:
                    name = emp_name[best_match_index]
                    dept = empdept_reco[best_match_index]
                    id = empid_reco[best_match_index]
                face_names.append(name)
                empdept.append(dept)
                emp_id.append(id)
        process_this_frame = not process_this_frame
        print ("Face detected :- ",emp_id, *face_names, *empdept )
        global name1
        global dept1
        for (top, right, bottom, left), name, id, dept in zip(face_locations, face_names, emp_id, empdept):
            top *= 4
            right *= 4
            bottom *= 5
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 65), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            name1 = str(name)
            dept1 =  str(dept)
            id1 = str(id)
            cv2.putText(frame, id1, (left + 4, bottom - 50), font, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, name1, (left + 4, bottom - 30), font, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, dept1, (left + 4, bottom - 4), font, 0.5, (255, 255, 255), 1)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
    os.system('python home.py')

thread3 = threading.Thread(target= face_reco2)
thread2 = threading.Thread(target= database)
thread2.start()
thread3.start()
thread3.join()
thread2.join()