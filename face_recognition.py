import os
import numpy as np
from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
import PIL.Image
import PIL.ImageTk
import PIL.ImageOps
from tkinter import messagebox
import mysql.connector
import cv2
from datetime import datetime
from time import strftime

import sys

value_from_home = None
def new_tcid(value):
    global value_from_home
    value_from_home = value



class Face_Recognition:
    panel=None
    camara=cv2.VideoCapture(0)
    btnOpen=None
    btnClose = None

    check=1
    camara.set(3, 800) ##chiều dài
    camara.set(4, 580)  ##chiều rộng
    camara.set(10, 150)
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("NHẬN DIỆN KHUÔN MẶT")
        self.isClicked=False
        self.teacherid = None

        img3 = PIL.Image.open(r"ImageFaceDetect\bg1.png")
        img3 = img3.resize((1530, 790), PIL.Image.ANTIALIAS)
        self.photoimg3 = ImageTk.PhotoImage(img3)




        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=0, width=1530, height=790)

        heading = Label(bg_img, text="Hệ thống điểm danh khuôn mặt", font=("yu gothic ui", 20, "bold"), bg="white",
                        fg="red2",
                        bd=0, relief=FLAT)
        heading.place(x=400, y=20, width=650, height=40)

        self.current_image = None


        #teacher _ ID
        print(value_from_home)
        self.teacher_id=value_from_home #Chọn teacher id = id người ms đăng nhập
        #lesson_id
        self.lessonid=None


        today = strftime("%d/%m/%Y")#time_today
        subject_array = [] #array for append id_lesson,subject
        #call lesson_id from db
        if(value_from_home=="0" or value_from_home==None):
            conn = mysql.connector.connect(host='localhost', user='root', password='',
                                           database='face_recognizer', port='3306')
            my_cursor = conn.cursor()
            self.teacher_id=0
            my_cursor.execute(
                "SELECT DISTINCT Subject_name,Lesson_Id  from lesson,`subject` where lesson.Subject_id=`subject`.Subject_id and Date=%s",
                (today,))
            subject_ls = my_cursor.fetchall()
            for i in subject_ls:
                t = str(i).replace("'", "", 4).replace("(", "").replace(")", "").replace(" ",
                                                                                         "")  ##Subject_lsid to attendance
                # print(t)
                subject_array.append(t)
        else:
            conn = mysql.connector.connect(host='localhost', user='root', password='',
                                           database='face_recognizer', port='3306')
            my_cursor = conn.cursor()
            my_cursor.execute(
                "SELECT DISTINCT Subject_name,Lesson_Id  from lesson,`subject` where lesson.Subject_id=`subject`.Subject_id and Date=%s and Teacher_id=%s",
                (today, self.teacher_id))
            subject_ls = my_cursor.fetchall()
            for i in subject_ls:
                t = str(i).replace("'", "", 4).replace("(", "").replace(")", "").replace(" ", "")##Subject_lsid to attendance
                # print(t)
                subject_array.append(t)

        #=======================================LEFT FRAME=========================================
        Left_frame = LabelFrame(self.root, bd=2, bg="white", relief=RIDGE, text="Màn hình nhận diện",
                                font=("times new roman", 12, "bold"))
        Left_frame.place(x=80, y=70, width=820, height=640)

        self.panel = ttk.Label(Left_frame,borderwidth=2, relief="groove")

        self.panel.place(x=8, y=60, width=800, height=480)

        #choose lesson to attendance
        self.choose_frame = LabelFrame(Left_frame, bd=1, bg="white", relief=RIDGE,
                                  font=("times new roman", 11, "bold"))
        self.choose_frame.place(x=8, y=0, width=800, height=50)

        search_label = Label(self.choose_frame, text="Chọn Môn/ID buổi học: ", font=("times new roman", 12, "bold"),
                             bg="white")
        search_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.selectsub=StringVar()
        self.lesson_combo = ttk.Combobox(self.choose_frame,textvariable=self.selectsub ,font=("times new roman", 12, "italic"), state="readonly",
                                    width=18)
        self.lesson_combo["values"] = subject_array
        self.lesson_combo.current()
        self.lesson_combo.bind("<<ComboboxSelected>>", self.callbackFunc)
        self.lesson_combo.grid(row=0, column=1, padx=5, pady=10, sticky=W)

        #choose attendance_value
        choose_type_att=Label(self.choose_frame, text="Chọn loại Điểm Danh: ", font=("times new roman", 12, "bold"),
                             bg="white")
        choose_type_att.grid(row=0, column=2, padx=35, pady=10, sticky=W)

        self.type_attendance=StringVar()
        self.type_combo=ttk.Combobox(self.choose_frame,textvariable=self.type_attendance ,font=("times new roman", 11, "bold"), state="readonly",
                                    width=18)
        self.type_combo["values"] = ("Vào","Ra")
        self.type_combo.current(0)
        self.type_combo.grid(row=0, column=3, padx=0, pady=10, sticky=W)


        #notify-attendance
        self.notify_frame = LabelFrame(Left_frame, bd=1, bg="white", relief=RIDGE,
                                       font=("times new roman", 11, "bold"))
        self.notify_frame.place(x=8, y=550, width=800, height=60)
        self.notify_label = Label(self.notify_frame, text="Thông báo: Vui lòng chọn Môn/ID Buổi học để mở Camera điểm danh !!!", font=("times new roman", 13, "bold"),
                             bg="white",fg="red")
        self.notify_label.grid(row=0, column=0, padx=10, pady=15, sticky=W)

        #btn Cam
        img_btn1 = PIL.Image.open(r"ImageFaceDetect\btnOpen.png")
        img_btn1 = img_btn1.resize((350, 45), PIL.Image.ANTIALIAS)
        self.photobtn1 = ImageTk.PhotoImage(img_btn1)
        self.btnOpen= Button(self.root ,bg="white", cursor="hand2",
                      borderwidth=0,image=self.photobtn1,command=self.face_recog,fg="white",disabledforeground="black")
        self.btnOpen.place(x=80, y=720, width=350, height=45)
        if self.selectsub.get()=="":
            self.btnOpen['state'] = "disabled"

        img_btn2 = PIL.Image.open(r"ImageFaceDetect\btnClose.png")
        img_btn2 = img_btn2.resize((350, 45), PIL.Image.ANTIALIAS)
        self.photobtn2 = ImageTk.PhotoImage(img_btn2)
        self.btnClose = Button(self.root, cursor="hand2",
                      borderwidth=0,image=self.photobtn2, bg="white",command=self.is_clicked, fg="white")
        self.btnClose.place(x=550, y=720, width=350, height=45)


        #Right_frame
        self.Right_frame = LabelFrame(self.root, bd=2, bg="white", relief=RIDGE, text="Điểm danh thành công",
                                font=("times new roman", 12, "bold"))
        self.Right_frame.place(x=1000, y=70, width=420, height=450)

        self.img_right = PIL.Image.open(r"ImageFaceDetect\unknow.jpg")
        self.img_right = self.img_right.resize((190, 190), PIL.Image.ANTIALIAS)
        self.photoimg_left = ImageTk.PhotoImage(self.img_right)

        self.f_lbl = Label(self.Right_frame, image=self.photoimg_left,bg="white",borderwidth=2, relief="groove",highlightcolor="darkblue")
        self.f_lbl.place(x=110, y=10, width=190, height=190)

        self.studentID_atten_info=Label(self.Right_frame, bg="white",
                                font=("times new roman", 12, "bold"))
        self.studentID_atten_info.place(x=5,y=220,width=410,height=130)

        #IDSV
        self.studentID_label = Label(self.studentID_atten_info, text="ID Sinh Viên:", font=("times new roman", 13, "bold"), bg="white")
        self.studentID_label.grid(row=0, column=0, padx=10,pady=10, sticky=W)

        self.studentID_atten_label = Label(self.studentID_atten_info, text="", font=("times new roman", 13, "bold"),
                                bg="white")
        self.studentID_atten_label.grid(row=0, column=1, padx=10, pady=10, sticky=W)


        #TenSV
        self.studentname_label = Label(self.studentID_atten_info, text="Tên Sinh Viên:", font=("times new roman", 13, "bold"),
                                     bg="white")
        self.studentname_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        self.studentname_atten_label = Label(self.studentID_atten_info, text="", font=("times new roman", 13, "bold"),
                                           bg="white")
        self.studentname_atten_label.grid(row=1, column=1, padx=10, pady=10, sticky=W)


        #Time
        self.studentclass_label = Label(self.studentID_atten_info, text="Thời gian:",
                                       font=("times new roman", 13, "bold"),
                                       bg="white")
        self.studentclass_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)

        self.studentclass_atten_label = Label(self.studentID_atten_info, text="",
                                             font=("times new roman", 13, "bold"),
                                             bg="white")
        self.studentclass_atten_label.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        #======================Class-info==============================
        self.RightU_frame = LabelFrame(self.root, bd=2, bg="white", relief=RIDGE, text="Thông tin buổi học",
                                      font=("times new roman", 12, "bold"))
        self.RightU_frame.place(x=1000, y=540, width=420, height=220)

        #Class
        self.className_label = Label(self.RightU_frame, text="Lớp tín chỉ:",
                                     font=("times new roman", 12, "bold"), bg="white")
        self.className_label.grid(row=0, column=0, padx=10, pady=20, sticky=W)

        self.className_atten_label = Label(self.RightU_frame, text="", font=("times new roman", 12, "bold"),
                                           bg="white",fg="red2")
        self.className_atten_label.grid(row=0, column=1, padx=10, pady=20, sticky=W)

        # subject/lesson
        self.subject_lesson_label = Label(self.RightU_frame, text="Tên môn học/ID Buổi học:",
                                       font=("times new roman", 12, "bold"),
                                       bg="white")
        self.subject_lesson_label.grid(row=1, column=0, padx=10, pady=20, sticky=W)

        self.subject_lesson_atten_label = Label(self.RightU_frame, text="", font=("times new roman", 12, "bold"),
                                             bg="white",fg="red2")
        self.subject_lesson_atten_label.grid(row=1, column=1, padx=10, pady=20, sticky=W)

        # Time
        self.classtime_label = Label(self.RightU_frame, text="Thời gian:",
                                        font=("times new roman", 12, "bold"),
                                        bg="white")
        self.classtime_label.grid(row=2, column=0, padx=10, pady=20, sticky=W)

        self.classtime_atten_label = Label(self.RightU_frame, text="",
                                              font=("times new roman", 12, "bold"),
                                              bg="white",fg="red2")
        self.classtime_atten_label.grid(row=2, column=1, padx=10, pady=20, sticky=W)



        #=============Kiem tra xem hom nay co mon hoc can diem danh khuong=====
        if not subject_array:
            self.lesson_combo['state'] = "disabled"
            self.notify_label[
                'text'] = "Bạn không có môn học nào cần điểm danh hôm nay"
            self.btnOpen['state']= "disabled"

    def is_clicked(self):
        self.isClicked=True
        self.lesson_combo['state'] = "readonly"
        self.type_combo['state']="readonly"
        self.notify_label[
            'text'] = "Vui lòng chọn ID Buổi học/Tên môn học để điểm danh"
        self.notify_label['fg']="red"

        print("Camera is Closed")

    def on_closing(self):
        self.isClicked = True
        self.root.destroy()

    def callbackFunc(self,event):
        mls = event.widget.get()
        # print(mls)

        if self.selectsub.get()=="":
            self.btnOpen['state'] = "disabled"
        else:
            c = str(mls).split(",")
            self.lessonid=str(c[1])
            self.subject_name=str(c[0])
            print(self.subject_name)
            self.btnOpen['state']="normal"
            conn = mysql.connector.connect(host='localhost', user='root', password='',
                                           database='face_recognizer', port='3306')
            my_cursor = conn.cursor()
            my_cursor.execute("select Time_start,Time_end,Class from lesson,subject where `subject`.Subject_id=lesson.Subject_id and Lesson_id=%s ",
                              (self.lessonid,))
            getInfo=my_cursor.fetchone()
            timeclass=str(getInfo[0])+" - "+str(getInfo[1])
            class_name=getInfo[2]
            subles=self.subject_name+" / "+self.lessonid
            self.className_atten_label['text']=class_name
            self.subject_lesson_atten_label['text']=subles
            self.classtime_atten_label['text']=timeclass
        # print(self.lessonid)


    #===========attendance===================
    def mark_attendance(self,i,r,n,d,face_cropped):
        img_id=0
        self.lesson_combo['state']="disabled"
        self.type_combo['state']="disabled"
        while True:# khi camera mở lên không có lỗi
            #Them data len csdl
            now = datetime.now()
            d1 = strftime("%d/%m/%Y")
            dtString = now.strftime("%H:%M:%S")
            ma="SV"+str(i)+d1+self.lessonid
            masp=ma.replace("/","")
            # print(masp)
            img_id+=1

            # kiểm tra xem sinh viên có trong ds lớp hay không
            conn = mysql.connector.connect(host='localhost', user='root', password='',
                                           database='face_recognizer', port='3306')
            my_cursor = conn.cursor()
            my_cursor.execute(
                "SELECT Student_id from student_has_subject,lesson,`subject` WHERE `subject`.Subject_id=lesson.Subject_id and"
                " `subject`.Subject_id=student_has_subject.Subject_id and lesson.Lesson_id=" + self.lessonid)
            chkStudent = my_cursor.fetchall()
            chkarray = []
            for cks in chkStudent:

                chkarray.append(cks[0])

            if(i not in chkarray):
                self.notify_label['text']="Thông báo: Sinh viên "+n+" Không có trong danh sách lớp"
                print("Sinh viên:" + n + " không có trong danh sách lớp học ")
            else:
                try:
                        conn = mysql.connector.connect(host='localhost', user='root', password='',
                                                       database='face_recognizer', port='3306')

                        my_cursor = conn.cursor()
                        my_cursor.execute("select Date,Lesson_id from attendance where Student_id=" + str(i))

                        idn = my_cursor.fetchall()
                        a = [] #mảng ngày
                        b=[]    #mảng lesson_id

                        for i1 in idn:
                            str2 = ''.join(i1[0])
                            # str1=''.join(i1[1])
                            a.append(str2)
                            b.append(str(i1[1]))
                        #nếu chọn loại điểm danh là ra hoặc vào
                        if(self.type_attendance.get()=="Vào"):
                            if((d1 not in a)) or ((self.lessonid not in b)):

                                my_cursor = conn.cursor()
                                my_cursor.execute("insert into attendance values(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                                    masp,
                                    str(i),
                                    n,
                                    d,
                                    dtString,
                                    None,
                                    d1,
                                    self.lessonid,
                                    "",
                                ))
                                cv2.imwrite("DiemDanhImage\ " + masp + ".jpg",
                                           face_cropped)
                                #=============================Check_attendance===============================

                                self.img_right = PIL.Image.open(r"DiemDanhImage\ " + masp + ".jpg")
                                self.img_right = self.img_right.resize((190, 190), PIL.Image.ANTIALIAS)
                                self.photoimg_left = ImageTk.PhotoImage(self.img_right)

                                self.f_lbl = Label(self.Right_frame, image=self.photoimg_left, bg="white", borderwidth=1,
                                                   relief="groove")
                                self.f_lbl.place(x=110, y=10, width=190, height=190)

                                # stdID
                                self.studentID_label = Label(self.studentID_atten_info, text="ID Sinh Viên:",
                                                             font=("times new roman", 13, "bold"), bg="white")
                                self.studentID_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
                                self.studentID_atten_label = Label(self.studentID_atten_info, text=i,
                                                                   font=("times new roman", 13, "bold"),
                                                                   bg="white", relief="sunken", width=20, justify="left")
                                self.studentID_atten_label.grid(row=0, column=1, padx=15, pady=10, sticky=W)

                                # name
                                self.studentname_label = Label(self.studentID_atten_info, text="Tên Sinh Viên:",
                                                               font=("times new roman", 13, "bold"),
                                                               bg="white")
                                self.studentname_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

                                self.studentname_atten_label = Label(self.studentID_atten_info, text=n,
                                                                     font=("times new roman", 13, "bold"), relief="sunken",
                                                                     width=18,
                                                                     bg="white", justify="left")
                                self.studentname_atten_label.grid(row=1, column=1, padx=15, pady=10, ipadx=10)

                                # class
                                self.studentclass_label = Label(self.studentID_atten_info, text="Thời gian:",
                                                                font=("times new roman", 13, "bold"),
                                                                bg="white")
                                self.studentclass_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
                                self.studentclass_atten_label = Label(self.studentID_atten_info, text=dtString,
                                                                      font=("times new roman", 13, "bold"),
                                                                      bg="white", relief="sunken", width=20, justify="left")
                                self.studentclass_atten_label.grid(row=2, column=1, padx=15, pady=10, sticky=W)
                            else:
                                # print("Sinh vien:" + n+ " Đã điểm danh ngày "+d1+ ". Vui lòng ra khỏi Camera !!")
                                self.notify_label['text'] = "Thông báo: Sinh viên: " + n + " đã điểm danh vào lớp thành công môn học "+self.subject_name
                                self.notify_label['fg']="green"

                                #=====================Change_AttendanceStatus===================================
                                my_cursor = conn.cursor()
                                my_cursor.execute("Select Time_in from attendance where Student_id=%s and Lesson_id=%s ",(str(i),(self.lessonid),))
                                ckTime_in = my_cursor.fetchone()
                                time_in = ckTime_in[0]
                                # print(time_in)

                                # -======Timestart========

                                my_cursor.execute("Select Time_start from lesson where Lesson_id=%s ",(self.lessonid,))
                                ckStart_in = my_cursor.fetchone()
                                time_start = ckStart_in[0]
                                # print(time_start)
                                if(time_in<time_start):
                                    my_cursor.execute(
                                        "update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                        ("Có mặt", str(i), (self.lessonid),))
                                else:
                                    a = datetime.strptime(str(time_in - time_start), '%H:%M:%S').time()
                                    b = datetime.strptime('0:00:00', '%H:%M:%S').time()#thoi gian dc phep diem danh co mat 15 phut
                                    c = datetime.strptime('0:50:00', '%H:%M:%S').time()# thoi gian dc phep diem danh muon
                                    d = datetime.strptime('1:00:00', '%H:%M:%S').time()#thoi gian cho phep sv vang 1 tiet

                                    if (b < a < c):

                                        stt="Đi muộn " + str(a.minute)+" phút"
                                        # print(stt)
                                        my_cursor.execute("update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                                          (stt,str(i),(self.lessonid),))
                                    elif (c < a < d):
                                        my_cursor.execute("update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                                          ("Vắng 1 tiết",str(i),(self.lessonid),))
                                    else:
                                        my_cursor.execute("update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                                          ("Vắng",str(i),(self.lessonid),))
                                    # print("Vắng")
                            conn.commit()
                            # self.fetch_data()
                            conn.close()
                            # messagebox.showinfo("Thành công", "Thêm thông tin sinh viên thành công", parent=self.root)
                        elif(self.type_attendance.get()=="Ra"):
                            conn = mysql.connector.connect(host='localhost', user='root', password='',
                                                           database='face_recognizer', port='3306')

                            my_cursor = conn.cursor()
                            my_cursor.execute("select IdAuttendance from attendance")
                            idatt = my_cursor.fetchall()
                            att=[]
                            for ida in idatt:
                                att.append(str(ida[0]))
                            if(masp not in att):
                                if ((d1 not in a)) or ((self.lessonid not in b)):

                                    my_cursor = conn.cursor()
                                    my_cursor.execute("insert into attendance values(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                                        masp,
                                        str(i),
                                        n,
                                        d,
                                        None,
                                        dtString,
                                        d1,
                                        self.lessonid,
                                        "Có mặt",
                                    ))
                                    cv2.imwrite("DiemDanhImage\ " + masp +"Ra"+ ".jpg",
                                                face_cropped)
                                    # =============================Check_attendance===============================

                                    self.img_right = PIL.Image.open(r"DiemDanhImage\ " + masp +"Ra" +".jpg")
                                    self.img_right = self.img_right.resize((190, 190), PIL.Image.ANTIALIAS)
                                    self.photoimg_left = ImageTk.PhotoImage(self.img_right)

                                    self.f_lbl = Label(self.Right_frame, image=self.photoimg_left, bg="white",
                                                       borderwidth=1,
                                                       relief="groove")
                                    self.f_lbl.place(x=110, y=10, width=190, height=190)

                                    # stdID
                                    self.studentID_label = Label(self.studentID_atten_info, text="ID Sinh Viên:",
                                                                 font=("times new roman", 13, "bold"), bg="white")
                                    self.studentID_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
                                    self.studentID_atten_label = Label(self.studentID_atten_info, text=i,
                                                                       font=("times new roman", 13, "bold"),
                                                                       bg="white", relief="sunken", width=20,
                                                                       justify="left")
                                    self.studentID_atten_label.grid(row=0, column=1, padx=15, pady=10, sticky=W)

                                    # name
                                    self.studentname_label = Label(self.studentID_atten_info, text="Tên Sinh Viên:",
                                                                   font=("times new roman", 13, "bold"),
                                                                   bg="white")
                                    self.studentname_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

                                    self.studentname_atten_label = Label(self.studentID_atten_info, text=n,
                                                                         font=("times new roman", 13, "bold"),
                                                                         relief="sunken",
                                                                         width=18,
                                                                         bg="white", justify="left")
                                    self.studentname_atten_label.grid(row=1, column=1, padx=15, pady=10, ipadx=10)

                                    # class
                                    self.studentclass_label = Label(self.studentID_atten_info, text="Thời gian:",
                                                                    font=("times new roman", 13, "bold"),
                                                                    bg="white")
                                    self.studentclass_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
                                    self.studentclass_atten_label = Label(self.studentID_atten_info, text=dtString,
                                                                          font=("times new roman", 13, "bold"),
                                                                          bg="white", relief="sunken", width=20,
                                                                          justify="left")
                                    self.studentclass_atten_label.grid(row=2, column=1, padx=15, pady=10, sticky=W)
                                else:
                                    # print(
                                    #     "Sinh vien:" + n + " Đã điểm danh ngày " + d1 + ". Vui lòng ra khỏi Camera !!")
                                    self.notify_label[
                                        'text'] = "Thông báo: Sinh viên: " + n + " đã điểm danh ra thành công môn học " + self.subject_name
                                    self.notify_label['fg'] = "green"

                                    # =====================Change_AttendanceStatus===================================
                                    my_cursor = conn.cursor()
                                    my_cursor.execute(
                                        "Select Time_out from attendance where Student_id=%s and Lesson_id=%s ",
                                        (str(i), (self.lessonid),))
                                    ckTime_out = my_cursor.fetchone()
                                    time_out = ckTime_out[0]
                                    # print(time_out)

                                    # -======Timeend========

                                    my_cursor.execute("Select Time_end from lesson where Lesson_id=%s ",
                                                      (self.lessonid,))
                                    ckend_in = my_cursor.fetchone()
                                    time_end = ckend_in[0]
                                    # print(time_start)
                                    if(time_end<time_out):
                                        my_cursor.execute(
                                            "update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                            ("Có mặt", str(i), (self.lessonid),))
                                    else:
                                        a = datetime.strptime(str(time_end - time_out), '%H:%M:%S').time()
                                        b = datetime.strptime('0:15:00',
                                                              '%H:%M:%S').time()  # thoi gian dc phep diem danh co mat trc 15p
                                        c = datetime.strptime('0:50:00',
                                                              '%H:%M:%S').time()  # thoi gian dc phep diem danh muon

                                        if (a < b):
                                            my_cursor.execute(
                                                "update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                                ("Có mặt", str(i), (self.lessonid),))
                                        elif (b < a < c):
                                            my_cursor.execute(
                                                "update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                                ("Vắng 1 tiết", str(i), (self.lessonid),))
                                        else:
                                            my_cursor.execute(
                                                "update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                                ("Vắng", str(i), (self.lessonid),))

                            else:
                                my_cursor = conn.cursor()
                                my_cursor.execute("select Time_out from attendance where IdAuttendance=%s",(masp,))
                                timeout_check=my_cursor.fetchone()
                                if(timeout_check[0]==None):
                                    my_cursor = conn.cursor()
                                    my_cursor.execute(
                                        "update  attendance set Time_out=%s where Student_id=%s and Lesson_id=%s",
                                        (dtString, str(i), (self.lessonid),))
                                    cv2.imwrite("DiemDanhImage\ " + masp + "Ra" + ".jpg",
                                                face_cropped)
                                    # =============================Check_attendance===============================

                                    self.img_right = PIL.Image.open(r"DiemDanhImage\ " + masp + "Ra" + ".jpg")
                                    self.img_right = self.img_right.resize((190, 190), PIL.Image.ANTIALIAS)
                                    self.photoimg_left = ImageTk.PhotoImage(self.img_right)

                                    self.f_lbl = Label(self.Right_frame, image=self.photoimg_left, bg="white",
                                                       borderwidth=1,
                                                       relief="groove")
                                    self.f_lbl.place(x=110, y=10, width=190, height=190)

                                    # stdID
                                    self.studentID_label = Label(self.studentID_atten_info, text="ID Sinh Viên:",
                                                                 font=("times new roman", 13, "bold"), bg="white")
                                    self.studentID_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
                                    self.studentID_atten_label = Label(self.studentID_atten_info, text=i,
                                                                       font=("times new roman", 13, "bold"),
                                                                       bg="white", relief="sunken", width=20,
                                                                       justify="left")
                                    self.studentID_atten_label.grid(row=0, column=1, padx=15, pady=10, sticky=W)

                                    # name
                                    self.studentname_label = Label(self.studentID_atten_info, text="Tên Sinh Viên:",
                                                                   font=("times new roman", 13, "bold"),
                                                                   bg="white")
                                    self.studentname_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

                                    self.studentname_atten_label = Label(self.studentID_atten_info, text=n,
                                                                         font=("times new roman", 13, "bold"),
                                                                         relief="sunken",
                                                                         width=18,
                                                                         bg="white", justify="left")
                                    self.studentname_atten_label.grid(row=1, column=1, padx=15, pady=10, ipadx=10)

                                    # class
                                    self.studentclass_label = Label(self.studentID_atten_info, text="Thời gian:",
                                                                    font=("times new roman", 13, "bold"),
                                                                    bg="white")
                                    self.studentclass_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
                                    self.studentclass_atten_label = Label(self.studentID_atten_info, text=dtString,
                                                                          font=("times new roman", 13, "bold"),
                                                                          bg="white", relief="sunken", width=20,
                                                                          justify="left")
                                    self.studentclass_atten_label.grid(row=2, column=1, padx=15, pady=10, sticky=W)
                                else:
                                    # print(
                                    #     "Sinh vien:" + n + " Đã điểm danh ngày " + d1 + ". Vui lòng ra khỏi Camera !!")
                                    self.notify_label[
                                        'text'] = "Thông báo: Sinh viên: " + n + " đã điểm danh ra thành công môn học " + self.subject_name
                                    self.notify_label['fg'] = "green"
                                    # =====================Change_AttendanceStatus===================================
                                    my_cursor = conn.cursor()
                                    my_cursor.execute(
                                        "Select Time_out from attendance where Student_id=%s and Lesson_id=%s ",
                                        (str(i), (self.lessonid),))
                                    ckTime_out = my_cursor.fetchone()
                                    time_out = ckTime_out[0]
                                    # print(time_out)

                                    # -======Timestart========

                                    my_cursor.execute("Select Time_end from lesson where Lesson_id=%s ",
                                                      (self.lessonid,))
                                    ckend_in = my_cursor.fetchone()
                                    time_end = ckend_in[0]
                                    # print(time_start)
                                    if (time_end < time_out):
                                        my_cursor.execute(
                                            "update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                            ("Có mặt", str(i), (self.lessonid),))
                                    else:
                                        a = datetime.strptime(str(time_end - time_out), '%H:%M:%S').time()
                                        b = datetime.strptime('0:15:00',
                                                              '%H:%M:%S').time()  # thoi gian dc phep diem danh co mat trc 15p
                                        c = datetime.strptime('0:50:00',
                                                              '%H:%M:%S').time()  # thoi gian dc phep diem danh muon

                                        if (a < b):
                                            my_cursor.execute(
                                                "update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                                ("Có mặt", str(i), (self.lessonid),))
                                        elif (b < a < c):
                                            my_cursor.execute(
                                                "update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                                ("Vắng 1 tiết", str(i), (self.lessonid),))
                                        else:
                                            my_cursor.execute(
                                                "update  attendance set AttendanceStatus=%s where Student_id=%s and Lesson_id=%s",
                                                ("Vắng", str(i), (self.lessonid),))


                            conn.commit()
                            conn.close()


                except Exception as es:
                        messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)
            if img_id==1:
                break


    def face_recog(self):
            self.isClicked=False
            def draw_boundray(img,classifier,scaleFactor,minNeighbors,color,text,clf):
                gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                features=classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)

                coord=[]
                for(x,y,w,h) in features:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(225,0,0),3)
                    id,predict=clf.predict(gray_image[y:y+h,x:x+w])
                    confidence=int((100*(1-predict/300)))

                    #Cat anh
                    face_cropped = gray_image[y:y + h+35, x:x + w+35]
                    face_cropped=cv2.cvtColor(face_cropped,cv2.COLOR_GRAY2BGR)
                    face_cropped=cv2.resize(face_cropped,(190,190))

                    conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer', port='3306')
                    my_cursor = conn.cursor()

                    my_cursor.execute("select Name from student where Student_id="+str(id))
                    n=my_cursor.fetchone()

                    n="+".join(n)

                    my_cursor.execute("select Roll from student where Student_id=" + str(id))
                    r = my_cursor.fetchone()
                    r = "+".join(r)

                    my_cursor.execute("select Class from student where Student_id=" + str(id))
                    d = my_cursor.fetchone()
                    d = "+".join(d)

                    my_cursor.execute("select Student_id from student where Student_id=" + str(id))
                    i = my_cursor.fetchone()
                    i = i[0]

                    if confidence>77:
                        cv2.putText(img,f"ID:{i}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),2)
                        cv2.putText(img, f"Name:{n}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)


                        # cv2.imwrite("DiemDanhImage\ " + i + "." + n + '.' + d + ".jpg",
                        #            array[0])

                        self.mark_attendance(i,r,n,d,face_cropped)
                    else:
                        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                        cv2.putText(img,"Unknow Face",(x,y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    coord=[x,y,w,h]
                return coord

            def recognize(img,clf,faceCascade):
                coord=draw_boundray(img,faceCascade,1.1,10,(255,25,255),"Face",clf)
                return img
            faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            clf=cv2.face.LBPHFaceRecognizer_create()
            clf.read("classifier.xml")

            self.camara=cv2.VideoCapture(0)
            self.camara.set(3, 800) ##chiều dài
            self.camara.set(4, 580)  ##chiều rộng
            self.camara.set(10, 150)  #độ sáng
            while True:

                ret,img=self.camara.read()
                img=recognize(img,clf,faceCascade)
                # cv2.imshow("Welcome to face REg",img)
                img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = PIL.Image.fromarray(img, mode='RGB')
                img = PIL.ImageTk.PhotoImage(img)  # convert image for tkinter
                self.panel['image']=img
                # self.panel.update()
                self.panel.update()


                if (self.isClicked==True): ##Bam Q de thoat cam
                    break
            self.camara.release()
            cv2.destroyAllWindows()



if __name__=="__main__":
    root=Tk() #khoi tao cua so va gan root vao
    obj=Face_Recognition(root)
    root.mainloop()# cua so hien len