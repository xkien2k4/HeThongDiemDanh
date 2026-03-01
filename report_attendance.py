import os
import random
from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
import PIL.Image
from time import strftime
from math import *
from tkinter import messagebox
import mysql.connector
import csv
from tkinter import filedialog
from tkcalendar import Calendar, DateEntry
mydata=[]
mydataNot=[]
mydataNotInAtt=[]
class Report:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Hệ thống nhận diện khuôn mặt")
        today = strftime("%d-%m-%Y")

        #===========variable============
        self.student = StringVar()
        self.att=StringVar()
        self.late=StringVar()
        self.noatt=StringVar()

        img3 = PIL.Image.open(r"ImageFaceDetect\bg1.png")
        img3 = img3.resize((1530, 790), PIL.Image.ANTIALIAS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=0, width=1530, height=790)

        # ==================================heading====================================
        # =========time=========

        # ========title=========
        self.txt = "Thống kê hệ thống"
        self.count = 0
        self.text = ''
        self.color = ["#4f4e4d", "#f29844", "red2"]
        self.heading = Label(self.root, text=self.txt, font=("yu gothic ui", 22, "bold"), bg="white", fg="black",
                             bd=0, relief=FLAT)
        self.heading.place(x=400, y=22, width=650,height=40)
        self.slider()
        self.heading_color()

        main_frame = Frame(bg_img, bd=2, bg="white")
        main_frame.place(x=20, y=69, width=1482, height=692)

        # ===================Top_label=====================
        Top_frame=LabelFrame(main_frame, bd=0, bg="white",
                                font=("times new roman", 12, "bold"))
        Top_frame.place(x=5,y=0,width=1470,height=120)
        #===================select_for_txt=================
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                       port='3306')
        my_cursor = conn.cursor()
        #========student==========
        my_cursor.execute("select count(*) from student")
        count_st = my_cursor.fetchone()
        self.student.set(count_st[0])
        #=======attendance========
        my_cursor.execute("select count(*) from attendance")
        count_att=my_cursor.fetchone()
        self.att.set(count_att[0])
        #=======late=============
        my_cursor.execute("select  count(Student_id) from attendance where AttendanceStatus like '%Đi muộn%'")
        count_late = my_cursor.fetchone()
        self.late.set(count_late[0])
        #========no-attendance=======
        #not_in_attendance_table
        my_cursor.execute("select count(student.Student_id) from student,lesson,student_has_subject,`subject` where student.Student_id=student_has_subject.Student_id "
                          "and student_has_subject.Subject_id=`subject`.Subject_id and `subject`.Subject_id=lesson.Subject_id "
                          "and CONCAT(student.Student_id,Lesson_id) not in (select CONCAT(Student_id,Lesson_id) from attendance) ")
        count_noatt = my_cursor.fetchone()
        #in_attendance_table
        my_cursor.execute("select  count(Student_id) from attendance where AttendanceStatus like '%Vắng%'")
        count_noatt1 = my_cursor.fetchone()


        a=int(count_noatt[0])+int(count_noatt1[0])
        self.noatt.set(a)
        conn.commit()
        conn.close()

        #student_frame
        student_frame=LabelFrame(Top_frame,bd=1,bg='#27a9e3')
        student_frame.place(x=5,y=0,width=355,height=120)

        img_student = PIL.Image.open(r"ImageFaceDetect\sv.png")
        # img_student = img_student.resize((50, 50), PIL.Image.ANTIALIAS)
        self.photoimgsv = ImageTk.PhotoImage(img_student)
        student_img = Label(student_frame, image=self.photoimgsv, bg="#27a9e3")
        student_img.place(x=20, y=40, width=50, height=50)
        student_text=Label(student_frame,text="Số sinh viên",font=("times new roman", 20, "bold"),fg="white",bg="#27a9e3")
        student_text.place(x=100,y=30)
        student_text = Label(student_frame,textvariable=self.student, font=("times new roman", 16, "bold"),fg="white",bg="#27a9e3")
        student_text.place(x=100, y=70)

        #attendance_success
        att_frame = LabelFrame(Top_frame, bd=1, bg='#28b779')
        att_frame.place(x=375, y=0, width=355, height=120)

        img_att = PIL.Image.open(r"ImageFaceDetect\sodd.png")
        img_att = img_att.resize((50, 50), PIL.Image.ANTIALIAS)
        self.photoimgatt = ImageTk.PhotoImage(img_att)
        att_img = Label(att_frame, image=self.photoimgatt, bg="#28b779")
        att_img.place(x=20, y=40, width=50, height=50)
        att_text = Label(att_frame, text="Số bản điểm danh", font=("times new roman", 20, "bold"), fg="white",
                             bg="#28b779")
        att_text.place(x=100, y=30)
        att_text = Label(att_frame, textvariable=self.att, font=("times new roman", 16, "bold"), fg="white",
                             bg="#28b779")
        att_text.place(x=100, y=70)

        #late_attendance
        late_frame = LabelFrame(Top_frame, bd=1, bg='#852b99')
        late_frame.place(x=745, y=0, width=355, height=120)

        img_late = PIL.Image.open(r"ImageFaceDetect\late.png")
        # img_student = img_student.resize((50, 50), PIL.Image.ANTIALIAS)
        self.photoimglate = ImageTk.PhotoImage(img_late)
        late_img = Label(late_frame, image=self.photoimglate, bg="#852b99")
        late_img.place(x=20, y=40, width=50, height=50)
        late_text = Label(late_frame, text="Số lần đi muộn", font=("times new roman", 20, "bold"), fg="white",
                         bg="#852b99")
        late_text.place(x=100, y=30)
        late_text = Label(late_frame, textvariable=self.late, font=("times new roman", 16, "bold"), fg="white",
                         bg="#852b99")
        late_text.place(x=100, y=70)

        #no_attendance
        late_frame = LabelFrame(Top_frame, bd=1, bg='#DC143C')
        late_frame.place(x=1115, y=0, width=355, height=120)

        img_noatt = PIL.Image.open(r"ImageFaceDetect\vang.png")
        # img_student = img_student.resize((50, 50), PIL.Image.ANTIALIAS)
        self.photoimgnoatt = ImageTk.PhotoImage(img_noatt)
        noatt_img = Label(late_frame, image=self.photoimgnoatt, bg="#DC143C")
        noatt_img.place(x=20, y=40, width=50, height=50)
        noatt_text = Label(late_frame, text="Số lần vắng", font=("times new roman", 20, "bold"), fg="white",
                          bg="#DC143C")
        noatt_text.place(x=100, y=30)
        noatt_text = Label(late_frame, textvariable=self.noatt, font=("times new roman", 16, "bold"), fg="white",
                          bg="#DC143C")
        noatt_text.place(x=100, y=70)

        #====================Left_label====================
        Left_frame = LabelFrame(main_frame, bd=2, bg="white",
                               font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=125, width=725, height=560)
        #topleft
        late_group=LabelFrame(Left_frame,bd=1,bg="white",text="Sinh viên đi muộn",font=("times new roman", 11, "bold"),fg="black",relief=RIDGE)
        late_group.place(x=0,y=0,width=720,height=270)

        self.var_com_searchlate = StringVar()
        search_combo = ttk.Combobox(late_group, font=("times new roman", 12, "bold"),
                                    textvariable=self.var_com_searchlate,
                                    state="read only",
                                    width=12)
        search_combo["values"] = ("ID Sinh viên", "Ngày","Tên môn học","ID Buổi học")
        search_combo.current(0)
        search_combo.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.var_searchlate = StringVar()
        searchtc_entry = ttk.Entry(late_group, textvariable=self.var_searchlate, width=13,
                                   font=("times new roman", 11, "bold"))
        searchtc_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)

        searchtc_btn = Button(late_group, text="Tìm kiếm",
                              font=("times new roman", 11, "bold"), bg="#38a6f0", fg="white",command=self.search_Latedata,
                              width=10)
        searchtc_btn.grid(row=0, column=2, padx=5)

        showAlltc_btn = Button(late_group, text="Xem tất cả",
                               font=("times new roman", 11, "bold"), bg="#38a6f0",command=self.fetch_Latedata,
                               fg="white",
                               width=10)
        showAlltc_btn.grid(row=0, column=3, padx=5)

        exportLate_btn = Button(late_group, text="Xuất CSV",
                               font=("times new roman", 11, "bold"), bg="#38a6f0", command=self.exportCsv,
                               fg="white",
                               width=10)
        exportLate_btn.grid(row=0, column=4, padx=10)

        # table_frame
        tabletc_frame = Frame(late_group, bd=2, relief=RIDGE, bg="white")
        tabletc_frame.place(x=10, y=38, width=695, height=205)

        # scroll bar
        scroll_x = ttk.Scrollbar(tabletc_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(tabletc_frame, orient=VERTICAL)

        self.LateTable = ttk.Treeview(tabletc_frame, column=(
            "studentid", "name","date", "subname","lessonid", "status"),
                                         xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.LateTable.xview)
        scroll_y.config(command=self.LateTable.yview)

        self.LateTable.heading("studentid", text="ID SV")
        self.LateTable.heading("name", text="Tên sinh viên")
        self.LateTable.heading("date", text="Ngày")
        self.LateTable.heading("subname", text="Môn học")
        self.LateTable.heading("lessonid", text="ID Buổi học")
        self.LateTable.heading("status", text="Trạng thái")

        self.LateTable["show"] = "headings"
        self.LateTable.column("studentid", width=100)
        self.LateTable.column("name", width=100)
        self.LateTable.column("date", width=100)
        self.LateTable.column("subname", width=100)
        self.LateTable.column("lessonid", width=100)
        self.LateTable.column("status", width=100)

        self.LateTable.pack(fill=BOTH, expand=1)

        self.fetch_Latedata()

        #===========under-left===============
        noatt_group = LabelFrame(Left_frame, bd=1, bg="white", text="Sinh viên vắng",
                                font=("times new roman", 11, "bold"), fg="black", relief=RIDGE)
        noatt_group.place(x=0, y=275, width=720, height=270)

        self.var_com_searchnoatt = StringVar()
        search_combo = ttk.Combobox(noatt_group, font=("times new roman", 12, "bold"),
                                    textvariable=self.var_com_searchnoatt,
                                    state="read only",
                                    width=12)
        search_combo["values"] = ("ID Sinh viên", "Ngày","Tên môn học","ID Buổi học")
        search_combo.current(0)
        search_combo.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.var_searchnoatt = StringVar()
        searchnoatt_entry = ttk.Entry(noatt_group, textvariable=self.var_searchnoatt, width=13,
                                   font=("times new roman", 11, "bold"))
        searchnoatt_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)

        searchnoatt_btn = Button(noatt_group, text="Tìm kiếm",
                              font=("times new roman", 11, "bold"), bg="#38a6f0", fg="white",command=self.search_Notdata,
                              width=10)
        searchnoatt_btn.grid(row=0, column=2, padx=5)

        showAllnoatt_btn = Button(noatt_group, text="Xem tất cả",
                               font=("times new roman", 11, "bold"), bg="#38a6f0",command=self.fetch_Notdata,
                               fg="white",
                               width=10)
        showAllnoatt_btn.grid(row=0, column=3, padx=5)

        exportNoatt_btn = Button(noatt_group, text="Xuất CSV",
                                font=("times new roman", 11, "bold"), bg="#38a6f0", command=self.exportUnpresetCsv,
                                fg="white",
                                width=10)
        exportNoatt_btn.grid(row=0, column=4, padx=10)

        # table_frame
        tableatt_frame = Frame(noatt_group, bd=2, relief=RIDGE, bg="white")
        tableatt_frame.place(x=10, y=38, width=695, height=205)

        # scroll bar
        scroll_x = ttk.Scrollbar(tableatt_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(tableatt_frame, orient=VERTICAL)

        self.NoAttTable = ttk.Treeview(tableatt_frame, column=(
            "studentid", "name", "date", "subname", "lessonid", "status"),
                                      xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.NoAttTable.xview)
        scroll_y.config(command=self.NoAttTable.yview)

        self.NoAttTable.heading("studentid", text="ID SV")
        self.NoAttTable.heading("name", text="Tên sinh viên")
        self.NoAttTable.heading("date", text="Ngày")
        self.NoAttTable.heading("subname", text="Môn học")
        self.NoAttTable.heading("lessonid", text="ID Buổi học")
        self.NoAttTable.heading("status", text="Trạng thái")

        self.NoAttTable["show"] = "headings"
        self.NoAttTable.column("studentid", width=100)
        self.NoAttTable.column("name", width=100)
        self.NoAttTable.column("date", width=100)
        self.NoAttTable.column("subname", width=100)
        self.NoAttTable.column("lessonid", width=100)
        self.NoAttTable.column("status", width=100)

        self.NoAttTable.pack(fill=BOTH, expand=1)
        self.fetch_Notdata()
        # self.LateTable.bind("<ButtonRelease>", self.get_cursorLate)

        #===================right_label====================
        Right_frame = LabelFrame(main_frame, bd=2, bg="white",
                                font=("times new roman", 12, "bold"))
        Right_frame.place(x=750, y=125, width=725, height=560)

        noatt_lbl = Label(Right_frame, bd=0, bg="white", text="Sinh viên không điểm danh", font=("yu gothic ui", 14, "bold"),
                         fg="red2", )
        noatt_lbl.place(x=0, y=0, width=720, height=30)

        notinGroup=LabelFrame(Right_frame,bd=0,bg="white")
        notinGroup.place(x=0,y=35,width=720,height=525)
        self.var_com_searchNotin = StringVar()
        search_combo = ttk.Combobox(notinGroup, font=("times new roman", 12, "bold"),
                                    textvariable=self.var_com_searchNotin,
                                    state="read only",
                                    width=12)
        search_combo["values"] = ("ID Sinh viên", "Ngày", "Tên môn học", "ID Buổi học")
        search_combo.current(0)
        search_combo.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.var_searchNotin = StringVar()
        searchtc_entry = ttk.Entry(notinGroup, textvariable=self.var_searchNotin, width=13,
                                   font=("times new roman", 11, "bold"))
        searchtc_entry.grid(row=0, column=1, padx=5, pady=0, sticky=W)

        searchtc_btn = Button(notinGroup, text="Tìm kiếm",
                              font=("times new roman", 11, "bold"), bg="#38a6f0", fg="white",
                              command=self.search_Notindata,
                              width=10)
        searchtc_btn.grid(row=0, column=2, padx=5)

        showAlltc_btn = Button(notinGroup, text="Xem tất cả",
                               font=("times new roman", 11, "bold"), bg="#38a6f0", command=self.fetch_Notindata,
                               fg="white",
                               width=10)
        showAlltc_btn.grid(row=0, column=3, padx=5)

        exportLate_btn = Button(notinGroup, text="Xuất CSV",
                                font=("times new roman", 11, "bold"), bg="#38a6f0", command=self.exportNotinCsv,
                                fg="white",
                                width=10)
        exportLate_btn.grid(row=0, column=4, padx=10)

        # table_frame
        tablenotin_frame = Frame(notinGroup, bd=2, relief=RIDGE, bg="white")
        tablenotin_frame.place(x=10, y=38, width=700, height=485)

        # scroll bar
        scroll_x = ttk.Scrollbar(tablenotin_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(tablenotin_frame, orient=VERTICAL)

        self.NotInTable = ttk.Treeview(tablenotin_frame, column=(
            "studentid", "name", "date", "subname", "lessonid"),
                                      xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.NotInTable.xview)
        scroll_y.config(command=self.NotInTable.yview)

        self.NotInTable.heading("studentid", text="ID SV")
        self.NotInTable.heading("name", text="Tên sinh viên")
        self.NotInTable.heading("date", text="Ngày")
        self.NotInTable.heading("subname", text="Môn học")
        self.NotInTable.heading("lessonid", text="ID Buổi học")


        self.NotInTable["show"] = "headings"
        self.NotInTable.column("studentid", width=100)
        self.NotInTable.column("name", width=100)
        self.NotInTable.column("date", width=100)
        self.NotInTable.column("subname", width=100)
        self.NotInTable.column("lessonid", width=100)


        self.NotInTable.pack(fill=BOTH, expand=1)
        self.fetch_Notindata()


    def slider(self):
        if self.count>=len(self.txt):
            self.count = -1
            self.text = ''
            self.heading.config(text=self.text)

        else:
            self.text = self.text+self.txt[self.count]
            self.heading.config(text=self.text)

        self.count+=1
        self.heading.after(100,self.slider)

    def heading_color(self):
        fg = random.choice(self.color)
        self.heading.config(fg=fg)
        self.heading.after(50, self.heading_color)

    def fetch_Latedata(self):
            # global mydata
            mydata.clear()
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                           port='3306')
            my_cursor = conn.cursor()
            my_cursor.execute("select DISTINCT Student_id,`Name`,attendance.Date,Subject_name,lesson.Lesson_id,AttendanceStatus from attendance,`subject`,lesson where   AttendanceStatus like '%Đi muộn%' "
                              "and lesson.Subject_id=subject.Subject_id and attendance.Lesson_id=lesson.Lesson_id")
            data = my_cursor.fetchall()
            if len(data) != 0:
                self.LateTable.delete(*self.LateTable.get_children())
                for i in data:
                    self.LateTable.insert("", END, values=i)
                    mydata.append(i)
                conn.commit()
            conn.close()
    def search_Latedata(self):
        if self.var_com_searchlate.get()=="" or self.var_searchlate.get()=="":
            messagebox.showerror("Lỗi !","Vui lòng nhập thông tin đầy đủ",parent=self.root)

        else:
            try:
                conn = mysql.connector.connect(host='localhost', user='root', password='',
                                               database='face_recognizer', port='3306')
                my_cursor = conn.cursor()#"ID Điểm Danh", "Ngày", "ID Sinh Viên"
                if(self.var_com_searchlate.get()=="ID Sinh viên"):
                    self.var_com_searchlate.set("Student_id")
                elif(self.var_com_searchlate.get()=="Ngày"):
                    self.var_com_searchlate.set("attendance.Date")
                elif (self.var_com_searchlate.get() == "Tên môn học"):
                    self.var_com_searchlate.set("Subject_name")
                else:
                    if(self.var_com_searchlate.get()=="ID Buổi học"):
                        self.var_com_searchlate.set("lesson.Lesson_id")

                mydata.clear()
                my_cursor.execute("select DISTINCT Student_id,`Name`,attendance.Date,Subject_name,lesson.Lesson_id,AttendanceStatus from attendance,`subject`,lesson where"
                                  "  AttendanceStatus like '%Đi muộn%' and lesson.Subject_id=subject.Subject_id and attendance.Lesson_id=lesson.Lesson_id and  "
                                  +str(self.var_com_searchlate.get())+" Like '%"+str(self.var_searchlate.get())+"%'")
                data=my_cursor.fetchall()
                if(len(data)!=0):
                    self.LateTable.delete(*self.LateTable.get_children())
                    for i in data:
                        self.LateTable.insert("",END,values=i)
                        mydata.append(i)
                    messagebox.showinfo("Thông báo","Có "+str(len(data))+" bản ghi thỏa mãn điều kiện",parent=self.root)
                    conn.commit()
                else:
                    self.LateTable.delete(*self.LateTable.get_children())
                    messagebox.showinfo("Thông báo", " Không có bản ghi nào thỏa mãn điều kiện",parent=self.root)
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)
    def exportCsv(self):
        try:
            if len(mydata)<1:
                messagebox.showerror("Không có dữ liệu","Không có dữ liệu để xuất file",parent=self.root)
                return  False

            with open('Attendance_CSV/diemdanhmuon.csv',mode="w",newline="",encoding="utf-8") as myfile:
                exp_write=csv.writer(myfile,delimiter=",")
                exp_write.writerow(('ID Sinh viên', 'Tên sinh viên', 'Ngày', 'Môn học', 'ID Buổi học', 'Trạng thái'))
                for i in mydata:
                    exp_write.writerow(i)
                messagebox.showinfo("Xuất Dữ Liệu","Dữ liệu của bạn đã được xuất đến "+os.path.basename('Attendance_CSV/diemdanhmuon.csv')+" thành công",parent=self.root)
        except Exception as es:
            messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)

    #===================No ATT=========================
    def fetch_Notdata(self):
            # global mydata
            mydataNot.clear()
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                           port='3306')
            my_cursor = conn.cursor()
            my_cursor.execute("select DISTINCT Student_id,`Name`,attendance.Date,Subject_name,lesson.Lesson_id,AttendanceStatus from attendance,`subject`,lesson where   AttendanceStatus like '%Vắng%' "
                              "and lesson.Subject_id=subject.Subject_id and attendance.Lesson_id=lesson.Lesson_id")
            data = my_cursor.fetchall()
            if len(data) != 0:
                self.NoAttTable.delete(*self.NoAttTable.get_children())
                for i in data:
                    self.NoAttTable.insert("", END, values=i)
                    mydataNot.append(i)
                conn.commit()
            conn.close()
    def search_Notdata(self):
        if self.var_com_searchnoatt.get()=="" or self.var_searchnoatt.get()=="":
            messagebox.showerror("Lỗi !","Vui lòng nhập thông tin đầy đủ",parent=self.root)

        else:
            try:
                conn = mysql.connector.connect(host='localhost', user='root', password='',
                                               database='face_recognizer', port='3306')
                my_cursor = conn.cursor()#"ID Điểm Danh", "Ngày", "ID Sinh Viên"
                if(self.var_com_searchnoatt.get()=="ID Sinh viên"):
                    self.var_com_searchnoatt.set("Student_id")
                elif(self.var_com_searchnoatt.get()=="Ngày"):
                    self.var_com_searchnoatt.set("attendance.Date")
                elif (self.var_com_searchnoatt.get() == "Tên môn học"):
                    self.var_com_searchnoatt.set("Subject_name")
                else:
                    if(self.var_com_searchnoatt.get()=="ID Buổi học"):
                        self.var_com_searchnoatt.set("lesson.Lesson_id")

                mydataNot.clear()
                my_cursor.execute("select DISTINCT Student_id,`Name`,attendance.Date,Subject_name,lesson.Lesson_id,AttendanceStatus from attendance,`subject`,lesson where"
                                  "  AttendanceStatus like '%Vắng%' and lesson.Subject_id=subject.Subject_id and attendance.Lesson_id=lesson.Lesson_id and  "
                                  +str(self.var_com_searchnoatt.get())+" Like '%"+str(self.var_searchnoatt.get())+"%'")
                data=my_cursor.fetchall()
                if(len(data)!=0):
                    self.NoAttTable.delete(*self.NoAttTable.get_children())
                    for i in data:
                        self.NoAttTable.insert("",END,values=i)
                        mydataNot.append(i)
                    messagebox.showinfo("Thông báo","Có "+str(len(data))+" bản ghi thỏa mãn điều kiện",parent=self.root)
                    conn.commit()
                else:
                    self.NoAttTable.delete(*self.NoAttTable.get_children())
                    messagebox.showinfo("Thông báo", " Không có bản ghi nào thỏa mãn điều kiện",parent=self.root)
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)
    def exportUnpresetCsv(self):
        try:
            if len(mydataNot)<1:
                messagebox.showerror("Không có dữ liệu","Không có dữ liệu để xuất file",parent=self.root)
                return  False

            with open('Attendance_CSV/diemdanhvang.csv',mode="w",newline="",encoding="utf-8") as myfile:
                exp_write=csv.writer(myfile,delimiter=",")
                exp_write.writerow(('ID Sinh viên', 'Tên sinh viên', 'Ngày', 'Môn học', 'ID Buổi học','Trạng thái'))
                for i in mydataNot:
                    exp_write.writerow(i)
                messagebox.showinfo("Xuất Dữ Liệu","Dữ liệu của bạn đã được xuất đến "+os.path.basename('Attendance_CSV/diemdanhvang.csv')+" thành công",parent=self.root)
        except Exception as es:
            messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)

    #===========================NOT IN ATT============================
    def fetch_Notindata(self):
            # global mydata
            mydataNotInAtt.clear()
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                           port='3306')
            my_cursor = conn.cursor()
            my_cursor.execute("select student.Student_id,Name,Date,Subject_name,Lesson_id from student,lesson,student_has_subject,`subject` "
                              "where student.Student_id=student_has_subject.Student_id and student_has_subject.Subject_id=`subject`.Subject_id "
                              "and `subject`.Subject_id=lesson.Subject_id and CONCAT(student.Student_id,Lesson_id) not in (select CONCAT(Student_id,Lesson_id) from attendance) ")
            data = my_cursor.fetchall()
            if len(data) != 0:
                self.NotInTable.delete(*self.NotInTable.get_children())
                for i in data:
                    self.NotInTable.insert("", END, values=i)
                    mydataNotInAtt.append(i)
                conn.commit()
            conn.close()
    def search_Notindata(self):
        if self.var_com_searchNotin.get()=="" or self.var_searchNotin.get()=="":
            messagebox.showerror("Lỗi !","Vui lòng nhập thông tin đầy đủ",parent=self.root)

        else:
            try:
                conn = mysql.connector.connect(host='localhost', user='root', password='',
                                               database='face_recognizer', port='3306')
                my_cursor = conn.cursor()#"ID Điểm Danh", "Ngày", "ID Sinh Viên"
                if(self.var_com_searchNotin.get()=="ID Sinh viên"):
                    self.var_com_searchNotin.set("student.Student_id")
                elif(self.var_com_searchNotin.get()=="Ngày"):
                    self.var_com_searchNotin.set("Date")
                elif (self.var_com_searchNotin.get() == "Tên môn học"):
                    self.var_com_searchNotin.set("Subject_name")
                else:
                    if(self.var_com_searchNotin.get()=="ID Buổi học"):
                        self.var_com_searchNotin.set("Lesson_id")

                mydataNotInAtt.clear()
                my_cursor.execute("select student.Student_id,Name,Date,Subject_name,Lesson_id from student,lesson,student_has_subject,`subject` where "
                                  "student.Student_id=student_has_subject.Student_id and student_has_subject.Subject_id=`subject`.Subject_id and `subject`.Subject_id=lesson.Subject_id"
                                  " and CONCAT(student.Student_id,Lesson_id) not in (select CONCAT(Student_id,Lesson_id) from attendance)  and "
                                  +str(self.var_com_searchNotin.get())+" Like '%"+str(self.var_searchNotin.get())+"%'")
                data=my_cursor.fetchall()
                if(len(data)!=0):
                    self.NotInTable.delete(*self.NotInTable.get_children())
                    for i in data:
                        self.NotInTable.insert("",END,values=i)
                        mydataNotInAtt.append(i)
                    messagebox.showinfo("Thông báo","Có "+str(len(data))+" bản ghi thỏa mãn điều kiện",parent=self.root)
                    conn.commit()
                else:
                    self.NotInTable.delete(*self.NotInTable.get_children())
                    messagebox.showinfo("Thông báo", " Không có bản ghi nào thỏa mãn điều kiện",parent=self.root)
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)
    def exportNotinCsv(self):
        try:
            if len(mydataNotInAtt)<1:
                messagebox.showerror("Không có dữ liệu","Không có dữ liệu để xuất file",parent=self.root)
                return  False

            with open('Attendance_CSV/khongdiemdanh.csv',mode="w",newline="",encoding="utf-8") as myfile:

                exp_write=csv.writer(myfile,delimiter=",")
                exp_write.writerow(('ID Sinh viên', 'Tên sinh viên', 'Ngày', 'Môn học', 'ID Buổi học'))
                for i in mydataNotInAtt:
                    exp_write.writerow(i)
                messagebox.showinfo("Xuất Dữ Liệu","Dữ liệu của bạn đã được xuất đến "+os.path.basename('Attendance_CSV/khongdiemdanh.csv')+" thành công")
        except Exception as es:
            messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)
if __name__=="__main__":
    root=Tk() #khoi tao cua so va gan root vao
    obj=Report(root)
    root.mainloop()# cua so hien len