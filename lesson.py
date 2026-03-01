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
from datetime import datetime
from tkcalendar import Calendar, DateEntry
mydata=[]
class Lesson:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Hệ thống nhận diện khuôn mặt")
        today = strftime("%d-%m-%Y")

        # ================variable===================

        self.var_id = StringVar()
        self.var_timestart = StringVar()
        self.var_timeend = StringVar()
        self.var_teacherid = StringVar()
        self.var_subjectid = StringVar()



        img3 = PIL.Image.open(r"ImageFaceDetect\bgnt.png")
        img3 = img3.resize((1530, 790), PIL.Image.ANTIALIAS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=0, width=1530, height=790)

        #==================================heading====================================
        #====time====
        img_time = PIL.Image.open(r"ImageFaceDetect\timsearch50.png")
        img_time = img_time.resize((27, 27), PIL.Image.ANTIALIAS)
        self.photoimgtime = ImageTk.PhotoImage(img_time)
        time_img = Label(self.root, image=self.photoimgtime,bg="white")
        time_img.place(x=43, y=40, width=27, height=27)
        def time():
            string=strftime('%H:%M:%S %p')
            lbl.config(text=string)
            lbl.after(1000,time)
        lbl=Label(self.root,font=("yu gothic ui", 13, "bold"),bg="white", fg="black")
        lbl.place(x=80,y=35,width=100,height=20)
        time()
        lbl1 = Label(self.root,text=today, font=("yu gothic ui", 13, "bold"), bg="white", fg="black")
        lbl1.place(x=80, y=60, width=100, height=20)

        #====title=========
        self.txt = "Quản lý thông tin lịch học"
        self.count = 0
        self.text = ''
        self.color = ["#4f4e4d", "#f29844", "red2"]
        self.heading = Label(self.root, text=self.txt, font=("yu gothic ui", 28, "bold"), bg="white", fg="black",
                             bd=5, relief=FLAT)
        self.heading.place(x=400, y=22, width=650)
        self.slider()
        self.heading_color()

        main_frame = Frame(bg_img, bd=2, bg="white")
        main_frame.place(x=23, y=102, width=1482, height=671)

        # ===================left_label=====================
        self.getNextid()
        Left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                font=("times new roman", 12, "bold"))
        Left_frame.place(x=20, y=5, width=450, height=650)

        label_Update_att = Label(Left_frame, bg="#F0FFF0", fg="#483D8B", text="Thông tin giáo viên",
                                 font=("times new roman", 18, "bold"))
        label_Update_att.place(x=0, y=1, width=446, height=45)

        left_inside_frame = Frame(Left_frame, bd=1, bg="white")
        left_inside_frame.place(x=0, y=60, width=430, height=570)

        # lessonid
        auttendanceID_label = Label(left_inside_frame, text="ID Buổi học:", font=("times new roman", 12, "bold"),
                                    bg="white")
        auttendanceID_label.grid(row=0, column=0, padx=20, pady=10, sticky=W)

        auttendanceID_entry = ttk.Entry(left_inside_frame, textvariable=self.var_id, state="disabled",
                                        font=("times new roman", 12, "bold"), width=22)
        auttendanceID_entry.grid(row=0, column=1, padx=20, pady=10, sticky=W)

        # timestart
        roll_label = Label(left_inside_frame, text="Giờ bắt đầu:", font=("times new roman", 12, "bold"),
                           bg="white")
        roll_label.grid(row=1, column=0, padx=20, pady=10, sticky=W)

        self.timestart_entry = ttk.Entry(left_inside_frame, width=22, textvariable=self.var_timestart,
                               font=("times new roman", 12, "bold"))
        self.timestart_entry.grid(row=1, column=1, padx=20, pady=10, sticky=W)
        self.timestart_entry.insert(END, "")
        self.timestart_entry.bind('<KeyRelease>', self.timestart)

        # timeend
        nameLabel = Label(left_inside_frame, text="Giờ kết thúc:", font=("times new roman", 12, "bold"),
                          bg="white")
        nameLabel.grid(row=2, column=0, padx=20, pady=10, sticky=W)

        self.timeend_entry = ttk.Entry(left_inside_frame, width=22, textvariable=self.var_timeend,
                                    font=("times new roman", 12, "bold"))
        self.timeend_entry.grid(row=2, column=1, padx=20, pady=10, sticky=W)
        self.timeend_entry.insert(END, "")
        self.timeend_entry.bind('<KeyRelease>', self.timeend)

        #date

        dob_label = Label(left_inside_frame, text="Ngày:", font=("times new roman", 12, "bold"),
                          bg="white")
        dob_label.grid(row=3, column=0, padx=20, pady=10, sticky=W)

        self.dob_entry = DateEntry(left_inside_frame, width=20, bd=3, selectmode='day',
                                   year=int(strftime("%Y")), month=int(strftime("%m")), font=("times new roman", 12),
                                   day=int(strftime("%d")), date_pattern='dd/mm/yyyy')
        self.dob_entry.grid(row=3, column=1, padx=20, pady=10, sticky=W)

        # teacher
        self.var_teacherid.trace("w", lambda name, index, mode, var_teacherid=self.var_teacherid: self.callback())
        teacherLabel = Label(left_inside_frame, text="ID Giảng viên:", font=("times new roman", 12, "bold"),
                           bg="white")
        teacherLabel.grid(row=4, column=0, padx=20, pady=10, sticky=W)

        teacherLabel_entry = ttk.Entry(left_inside_frame, width=22, textvariable=self.var_teacherid,
                                     font=("times new roman", 12, "bold"))
        teacherLabel_entry.grid(row=4, column=1, padx=20, pady=10, sticky=W)


        #Name_teacher
        self.var_teachername=StringVar()
        teachernLabel = Label(left_inside_frame, text="Tên Giảng viên:", font=("times new roman", 12, "bold"),
                             bg="white")
        teachernLabel.grid(row=5, column=0, padx=20, pady=10, sticky=W)

        teachernLabel_entry = ttk.Entry(left_inside_frame, width=22, textvariable=self.var_teachername,
                                       font=("times new roman", 12, "bold"),state="disabled")
        teachernLabel_entry.grid(row=5, column=1, padx=20, pady=10, sticky=W)

        #subject
        self.var_subjectid.trace("w", lambda name, index, mode, var_subjectid=self.var_subjectid: self.callSubject())
        subjectLabel = Label(left_inside_frame, text="ID Môn học:", font=("times new roman", 12, "bold"),
                             bg="white")
        subjectLabel.grid(row=6, column=0, padx=20, pady=10, sticky=W)

        subjectLabel_entry = ttk.Entry(left_inside_frame, width=22, textvariable=self.var_subjectid,
                                       font=("times new roman", 12, "bold"))
        subjectLabel_entry.grid(row=6, column=1, padx=20, pady=10, sticky=W)

        #subject_name
        self.var_subjectname=StringVar()
        subjectnameLabel = Label(left_inside_frame, text="Tên Môn học:", font=("times new roman", 12, "bold"),
                             bg="white")
        subjectnameLabel.grid(row=7, column=0, padx=20, pady=10, sticky=W)

        subjectnameLabel_entry = ttk.Entry(left_inside_frame, width=22, textvariable=self.var_subjectname,
                                       font=("times new roman", 12, "bold"),state="disabled")
        subjectnameLabel_entry.grid(row=7, column=1, padx=20, pady=10, sticky=W)

        # =====btn_frame============

        btn_frame = Frame(left_inside_frame, bg="white")
        btn_frame.place(x=0, y=420, width=440, height=115)

        add_btn = Button(btn_frame, text="Thêm mới", command=self.add_data, font=("times new roman", 13, "bold"),
                         bg="#38a6f0", fg="white", width=17)
        add_btn.grid(row=9, column=0, pady=10, padx=20)

        delete_btn = Button(btn_frame, text="Xóa", command=self.delete_data,
                            font=("times new roman", 13, "bold"),
                            bg="#38a6f0", fg="white", width=17)
        delete_btn.grid(row=9, column=1, pady=10, padx=20)

        update_btn = Button(btn_frame, text="Cập nhật", command=self.update_data, font=("times new roman", 13, "bold"),
                            bg="#38a6f0", fg="white", width=17)
        update_btn.grid(row=10, column=0, pady=20, padx=20)

        reset_btn = Button(btn_frame, text="Làm mới", command=self.reset_data, font=("times new roman", 13, "bold"),
                           bg="#38a6f0", fg="white", width=17)
        reset_btn.grid(row=10, column=1, pady=0, padx=20)

        # ==================right_ label========================
        Right_frame = LabelFrame(main_frame, bd=2, bg="white",
                                 font=("times new roman", 12, "bold"))
        Right_frame.place(x=500, y=5, width=960, height=650)

        # search
        self.var_com_search = StringVar()
        search_label = Label(Right_frame, text="Tìm kiếm theo :", font=("times new roman", 13, "bold"),
                             bg="white")
        search_label.grid(row=0, column=0, padx=15, pady=5, sticky=W)

        search_combo = ttk.Combobox(Right_frame, font=("times new roman", 13, "bold"), textvariable=self.var_com_search,
                                    state="read only",
                                    width=13)
        search_combo["values"] = ("ID Buổi học", "ID GV", "ID Môn học","Ngày học")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=15, sticky=W)

        self.var_search = StringVar()
        search_entry = ttk.Entry(Right_frame, textvariable=self.var_search, width=15,
                                 font=("times new roman", 13, "bold"))
        search_entry.grid(row=0, column=2, padx=15, pady=5, sticky=W)

        search_btn = Button(Right_frame, command=self.search_data, text="Tìm kiếm",
                            font=("times new roman", 13, "bold"), bg="#38a6f0", fg="white",
                            width=12)
        search_btn.grid(row=0, column=3, padx=15)

        showAll_btn = Button(Right_frame, text="Xem tất cả", command=self.fetch_data,
                             font=("times new roman", 13, "bold"), bg="#38a6f0",
                             fg="white",
                             width=12)
        showAll_btn.grid(row=0, column=5, padx=15)

        # table_frame
        table_frame = Frame(Right_frame, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=5, y=55, width=940, height=580)

        # scroll bar
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.AttendanceReportTable = ttk.Treeview(table_frame, column=(
            "id", "timestart", "timeend", "date", "teacherid", "subjectid"),
                                                  xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)

        self.AttendanceReportTable.heading("id", text="ID Buổi học")
        self.AttendanceReportTable.heading("timestart", text="Giờ bắt đầu")
        self.AttendanceReportTable.heading("timeend", text="Giờ kết thúc")
        self.AttendanceReportTable.heading("date", text="Ngày")
        self.AttendanceReportTable.heading("teacherid", text="ID Giảng viên")
        self.AttendanceReportTable.heading("subjectid", text="ID Môn học")

        self.AttendanceReportTable["show"] = "headings"

        self.AttendanceReportTable.column("id", width=100)
        self.AttendanceReportTable.column("timestart", width=100)
        self.AttendanceReportTable.column("timeend", width=100)
        self.AttendanceReportTable.column("date", width=100)
        self.AttendanceReportTable.column("teacherid", width=100)
        self.AttendanceReportTable.column("subjectid", width=100)


        self.AttendanceReportTable.pack(fill=BOTH, expand=1)

        self.AttendanceReportTable.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()  # load du lieu len grid

    #================Function===================
    def timestart(self, event):
            if len(self.timestart_entry.get()) is 2:
                self.timestart_entry.insert(END, ":")
            elif len(self.timestart_entry.get()) is 5:
                self.timestart_entry.insert(END, ":")
            elif len(self.timestart_entry.get()) is 9:
                self.timestart_entry.delete(8, END)
    def timeend(self, event):
            if len(self.timeend_entry.get()) is 2:
                self.timeend_entry.insert(END, ":")
            elif len(self.timeend_entry.get()) is 5:
                self.timeend_entry.insert(END, ":")
            elif len(self.timeend_entry.get()) is 9:
                self.timeend_entry.delete(8, END)
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
    def callback(self):
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                       port='3306')
        my_cursor = conn.cursor()
        my_cursor.execute("select Teacher_id from `teacher` ")
        ckteacher = my_cursor.fetchall()
        arrayTeacher = []
        for cht in ckteacher:
            # print(cht[0])
            arrayTeacher.append(str(cht[0]))
        if(self.var_teacherid.get() not in arrayTeacher):

            self.var_teachername.set("")
        else:
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                           port='3306')
            my_cursor = conn.cursor()
            my_cursor.execute("select Name from `teacher` where Teacher_id=%s", (self.var_teacherid.get(),))
            ckteacher = my_cursor.fetchone()
            self.var_teachername.set(ckteacher[0])
        conn.commit()
        conn.close()
    def callSubject(self):
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                       port='3306')
        my_cursor = conn.cursor()
        my_cursor.execute("select Subject_id from `subject` ")
        ckteacher = my_cursor.fetchall()
        arrayTeacher = []
        for cht in ckteacher:
            # print(cht[0])
            arrayTeacher.append(str(cht[0]))
        if(self.var_subjectid.get() not in arrayTeacher):

            self.var_subjectname.set("")
        else:
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                           port='3306')
            my_cursor = conn.cursor()
            my_cursor.execute("select Subject_name from `subject` where Subject_id=%s", (self.var_subjectid.get(),))
            ckteacher = my_cursor.fetchone()
            self.var_subjectname.set(ckteacher[0])
        conn.commit()
        conn.close()
    def getNextid(self):
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                           port='3306')
            my_cursor = conn.cursor()
            my_cursor.execute(
                "SELECT  Lesson_id from lesson ORDER BY Lesson_id DESC limit 1")
            lastid = my_cursor.fetchone()
            if (lastid == None):
                self.var_id.set("1")
            else:
                nextid = int(lastid[0]) + 1
                self.var_id.set(str(nextid))

            conn.commit()
            conn.close()
    def get_cursor(self,event=""):
        cursor_row=self.AttendanceReportTable.focus()
        content=self.AttendanceReportTable.item(cursor_row)
        rows=content['values']
        self.var_id.set(rows[0])
        self.var_timestart.set(rows[1])
        self.var_timeend.set(rows[2])
        self.dob_entry.set_date(rows[3])
        self.var_teacherid.set(rows[4])
        self.var_subjectid.set(rows[5])


    def add_data(self):
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                       port='3306')
        my_cursor = conn.cursor()

        # =========check subject============
        my_cursor.execute("select Subject_id from teacher_has_subject where Teacher_id=%s",
                          (self.var_teacherid.get(),))
        ckSubject = my_cursor.fetchall()
        arraySub = []
        for chk in ckSubject:
            arraySub.append(str(chk[0]))

        #check_time
        time_start = datetime.strptime(self.var_timestart.get(), '%H:%M:%S').time()
        time_end = datetime.strptime(self.var_timeend.get(), '%H:%M:%S').time()

        if self.var_id.get()=="" or self.var_timestart.get()=="" or self.var_timeend.get()=="" \
                or self.dob_entry.get_date().strftime('%d/%m/%Y')=="" or self.var_teacherid.get()=="" or self.var_subjectid.get()=="":
            messagebox.showerror("Error","Vui lòng nhập đầy đủ thông tin",parent=self.root)
        elif(self.var_teachername.get() ==""):
            messagebox.showerror("Error","Không tồn tại ID Giảng viên này! Vui lòng kiểm tra lại!",parent=self.root)
        elif(self.var_subjectname.get() ==""):
            messagebox.showerror("Error","Không tồn tại ID Môn học này! Vui lòng kiểm tra lại",parent=self.root)
        elif(self.var_subjectid.get() not in arraySub):
            messagebox.showerror("Error","Giáo viên không giảng dạy môn học này! Vui lòng vào Môn Học và kiểm tra lại !! ",parent=self.root)
        elif(time_end<time_start):
            messagebox.showerror("Error","Thời gian kết thúc không thể nhỏ hơn thời gian bắt đầu !",parent=self.root)

        else:
            try:
                conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer', port='3306')

                my_cursor=conn.cursor()
                my_cursor.execute("insert into lesson values(%s,%s,%s,%s,%s,%s)",(
                    self.var_id.get(),
                    self.var_timestart.get(),
                    self.var_timeend.get(),
                    self.dob_entry.get_date().strftime('%d/%m/%Y'),
                    self.var_teacherid.get(),
                    self.var_subjectid.get(),
                ))

                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
                messagebox.showinfo("Thành công","Thêm thông tin giảng viên thành công",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)


    def reset_data(self):
        self.var_id.set("")
        self.var_timestart.set("")
        self.var_timeend.set("")
        self.var_teacherid.set("")
        self.var_subjectid.set("")
        self.dob_entry.set_date(strftime("%d/%m/%Y"))
        self.getNextid()
    def fetch_data(self):
            # global mydata
            # mydata.clear()
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                           port='3306')

            my_cursor = conn.cursor()
            my_cursor.execute("Select * from lesson")
            data = my_cursor.fetchall()

            if len(data) != 0:
                self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
                for i in data:
                    self.AttendanceReportTable.insert("", END, values=i)
                    mydata.append(i)
                conn.commit()
            conn.close()
    def update(self,rows):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
    def update_data(self):
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                       port='3306')
        my_cursor = conn.cursor()
        # =========check subject============
        my_cursor.execute("select Subject_id from teacher_has_subject where Teacher_id=%s",
                          (self.var_teacherid.get(),))
        ckSubject = my_cursor.fetchall()
        arraySub = []
        for chk in ckSubject:
            arraySub.append(str(chk[0]))

        # check_time
        time_start = datetime.strptime(self.var_timestart.get(), '%H:%M:%S').time()
        time_end = datetime.strptime(self.var_timeend.get(), '%H:%M:%S').time()

        if self.var_id.get()=="" or self.var_timestart.get()=="" or self.var_timeend.get()=="" \
                or self.dob_entry.get_date().strftime('%d/%m/%Y')=="" or self.var_teacherid.get()=="" or self.var_subjectid.get()=="":
            messagebox.showerror("Error","Vui lòng nhập đầy đủ thông tin",parent=self.root)
        elif (self.var_teachername.get() == ""):
            messagebox.showerror("Error", "Không tồn tại ID Giảng viên này! Vui lòng kiểm tra lại!", parent=self.root)
        elif (self.var_subjectname.get() == ""):
            messagebox.showerror("Error", "Không tồn tại ID Môn học này! Vui lòng kiểm tra lại", parent=self.root)
        elif (self.var_subjectid.get() not in arraySub):
            messagebox.showerror("Error",
                                 "Giáo viên không giảng dạy môn học này! Vui lòng vào Môn Học và kiểm tra lại !! ",parent=self.root)
        elif (time_end < time_start):
            messagebox.showerror("Error", "Thời gian kết thúc không thể nhỏ hơn thời gian bắt đầu !", parent=self.root)
        else:
            try:
                Update=messagebox.askyesno("Update","Bạn có muốn cập nhật bản ghi này không?",parent=self.root)
                if Update>0:
                    conn=mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer', port='3306')
                    my_cursor = conn.cursor()
                    my_cursor.execute("update lesson set Time_start=%s,Time_end=%s,Date=%s,Teacher_id=%s,Subject_id=%s"
                                      " where Teacher_id=%s",(
                                            self.var_timestart.get(),
                                            self.var_timeend.get(),
                                            self.dob_entry.get_date().strftime('%d/%m/%Y'),
                                            self.var_teacherid.get(),
                                            self.var_subjectid.get(),
                                            self.var_id.get(),
                                        ))
                else:
                    if not Update:
                        return
                messagebox.showinfo("Thành công","Cập nhật thông tin điểm danh thành công",parent=self.root)
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi",f"Due To:{str(es)}",parent=self.root)

    # Delete Function
    def delete_data(self):
            if self.var_id == "":
                messagebox.showerror("Lỗi", "Không được bỏ trống ID ", parent=self.root)
            else:
                try:
                    delete = messagebox.askyesno("Xoá bản ghi", "Bạn có muốn xóa bản ghi này ?", parent=self.root)
                    if delete > 0:
                        conn = mysql.connector.connect(host='localhost', user='root', password='',
                                                       database='face_recognizer', port='3306')
                        my_cursor = conn.cursor()
                        sql = "delete from lesson where Lesson_id=%s"
                        val = (self.var_id.get(),)
                        my_cursor.execute(sql, val)
                    else:
                        if not delete:
                            return
                    conn.commit()
                    # self.fetch_data()
                    conn.close()
                    messagebox.showinfo("Xóa", "Xóa bản ghi thành công", parent=self.root)
                    self.fetch_data()
                    self.reset_data()
                except Exception as es:
                    messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)

    def search_data(self):
        if self.var_com_search.get()=="" or self.var_search.get()=="":
            messagebox.showerror("Lỗi !","Vui lòng nhập thông tin đầy đủ")

        else:
            try:
                conn = mysql.connector.connect(host='localhost', user='root', password='',
                                               database='face_recognizer', port='3306')
                my_cursor = conn.cursor()#"ID Điểm Danh", "Ngày", "ID Sinh Viên"
                if(self.var_com_search.get()=="ID GV"):
                    self.var_com_search.set("Teacher_id")
                elif(self.var_com_search.get()=="ID Buổi học"):
                    self.var_com_search.set("Lesson_id")
                elif (self.var_com_search.get() == "ID Môn học"):
                    self.var_com_search.set("Subject_id")
                else:
                    if(self.var_com_search.get()=="Ngày học"):
                        self.var_com_search.set("Date")
                my_cursor.execute("select * from lesson where "+str(self.var_com_search.get())+" Like '%"+str(self.var_search.get())+"%'")
                data=my_cursor.fetchall()
                if(len(data)!=0):
                    self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
                    for i in data:
                        self.AttendanceReportTable.insert("",END,values=i)
                    messagebox.showinfo("Thông báo","Có "+str(len(data))+" bản ghi thỏa mãn điều kiện",parent=self.root)
                    conn.commit()
                else:
                    self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
                    messagebox.showinfo("Thông báo", " Không có bản ghi nào thỏa mãn điều kiện",parent=self.root)
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)
if __name__=="__main__":
    root=Tk() #khoi tao cua so va gan root vao
    obj=Lesson(root)
    root.mainloop()# cua so hien len