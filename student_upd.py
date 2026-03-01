from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
import PIL.Image
import numpy as np
import random
from tkinter import messagebox
import mysql.connector
from tkcalendar import Calendar, DateEntry
from time import strftime
import cv2
import os
mydata=[]
class Student:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("QLSV")
        today = strftime("%d-%m-%Y")
        #======================variables================
        self.var_dep=StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div = StringVar()
        self.var_roll = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()

        #==================classvariables================
        self.var_class=StringVar()
        self.var_nameclass=StringVar()


        img3 = PIL.Image.open(r"ImageFaceDetect\bgnt.png")
        img3 = img3.resize((1530, 790), PIL.Image.ANTIALIAS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=0, width=1530, height=790)

        # ==================================heading====================================
        # ====time====
        img_time = PIL.Image.open(r"ImageFaceDetect\timsearch50.png")
        img_time = img_time.resize((27, 27), PIL.Image.ANTIALIAS)
        self.photoimgtime = ImageTk.PhotoImage(img_time)
        time_img = Label(self.root, image=self.photoimgtime, bg="white")
        time_img.place(x=43, y=40, width=27, height=27)

        def time():
            string = strftime('%H:%M:%S %p')
            lbl.config(text=string)
            lbl.after(1000, time)

        lbl = Label(self.root, font=("yu gothic ui", 13, "bold"), bg="white", fg="black")
        lbl.place(x=80, y=35, width=100, height=20)
        time()
        lbl1 = Label(self.root, text=today, font=("yu gothic ui", 13, "bold"), bg="white", fg="black")
        lbl1.place(x=80, y=60, width=100, height=20)

        # ====title=========
        self.txt = "Quản lý thông tin sinh viên"
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

        #left_label
        self.getNextid()
        Left_frame=LabelFrame(main_frame,bd=2,bg="white",font=("times new roman",12,"bold"))
        Left_frame.place(x=10,y=10,width=730,height=646)

        label_Update_att = Label(Left_frame, bg="white", fg="red2", text="Thông tin sinh viên",
                                 font=("yu gothic ui", 16, "bold"))
        label_Update_att.place(x=0, y=1, width=700, height=42)


        #course
        current_course_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE, text="Thông tin khoá học",
                                font=("times new roman", 12, "bold"))
        current_course_frame.place(x=5, y=55, width=720, height=130)

        #department
        dep_label=Label(current_course_frame,text="Chuyên ngành",font=("times new roman",13,"bold"),bg="white")
        dep_label.grid(row=0,column=0,padx=10,sticky=W)

        dep_combo=ttk.Combobox(current_course_frame,textvariable=self.var_dep,font=("times new roman",13,"bold"),state="readonly",width=20)
        dep_combo["values"]=("Chọn chuyên ngành","Điện tử viễn thông","IT","Cơ khí","Điện","Kế toán","Tự động hóa")
        dep_combo.current(0)
        dep_combo.grid(row=0,column=1,padx=2,pady=10,sticky=W)


        #course
        course_label = Label(current_course_frame, text="Hệ đào tạo", font=("times new roman", 13, "bold"), bg="white")
        course_label.grid(row=0, column=2, padx=10, sticky=W)

        course_combo = ttk.Combobox(current_course_frame,textvariable=self.var_course, font=("times new roman", 13, "bold"), state="readonly",width=20)
        course_combo["values"] = ("Chọn hệ", "Chính quy", "Liên Thông", "CLC")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=2, pady=10, sticky=W)

        #year
        year_label = Label(current_course_frame, text="Năm học", font=("times new roman", 13, "bold"), bg="white")
        year_label.grid(row=1, column=0, padx=10, sticky=W)

        year_combo = ttk.Combobox(current_course_frame,textvariable=self.var_year, font=("times new roman", 13, "bold"), state="readonly",
                                    width=20)
        year_combo["values"] = ("Chọn năm học", "2020-21", "2021-22", "2022-23", "2023-24")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)


        #semester
        semester_label = Label(current_course_frame, text="Học kì", font=("times new roman", 13, "bold"), bg="white")
        semester_label.grid(row=1, column=2, padx=10, sticky=W)

        semester_combo = ttk.Combobox(current_course_frame,textvariable=self.var_semester ,font=("times new roman", 13, "bold"), state="readonly",
                                  width=20)
        semester_combo["values"] = ("Chọn học kì", "Học kì I", "Học kì II")
        semester_combo.current(0)
        semester_combo.grid(row=1, column=3, padx=2, pady=10, sticky=W)

        #Class_student
        class_student_frame = LabelFrame(Left_frame, bd=2, bg="white", relief=RIDGE, text="Thông tin lớp học",
                                          font=("times new roman", 13, "bold"))
        class_student_frame.place(x=5, y=195, width=720, height=420)

        #student_id
        studentID_label = Label(class_student_frame, text="ID Sinh Viên:", font=("times new roman", 13, "bold"), bg="white")
        studentID_label.grid(row=0, column=0, padx=10,pady=10, sticky=W)

        studentID_entry=ttk.Entry(class_student_frame,width=20,textvariable=self.var_std_id,font=("times new roman", 13, "bold"),state="disabled")
        studentID_entry.grid(row=0,column=1,padx=10,pady=10,sticky=W)

        #studentName
        studentName_label = Label(class_student_frame, text="Tên Sinh Viên:", font=("times new roman", 13, "bold"),
                                bg="white")
        studentName_label.grid(row=0, column=2, padx=10,pady=10, sticky=W)

        studentName_entry = ttk.Entry(class_student_frame, width=20,textvariable=self.var_std_name, font=("times new roman", 13, "bold"))
        studentName_entry.grid(row=0, column=3, padx=10,pady=10, sticky=W)

        #class
        class_div_label = Label(class_student_frame, text="Lớp học:", font=("times new roman", 13, "bold"),
                                  bg="white")
        class_div_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        class_div_entry = ttk.Entry(class_student_frame, width=20,textvariable=self.var_div, font=("times new roman", 13, "bold"))
        class_div_entry.grid(row=1, column=1, padx=10, pady=10, sticky=W)


        #roll
        roll_no_label = Label(class_student_frame, text="CMND", font=("times new roman", 13, "bold"),
                                  bg="white")
        roll_no_label.grid(row=1, column=2, padx=10, pady=10, sticky=W)

        roll_no_entry = ttk.Entry(class_student_frame, width=20,textvariable=self.var_roll ,font=("times new roman", 13, "bold"))
        roll_no_entry.grid(row=1, column=3, padx=10, pady=10, sticky=W)

        #gender
        gender_label = Label(class_student_frame, text="Giới tính:", font=("times new roman", 13, "bold"),
                                bg="white")
        gender_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)

        # gender_entry = ttk.Entry(class_student_frame, width=20,textvariable=self.var_gender ,font=("times new roman", 13, "bold"))
        # gender_entry.grid(row=2, column=1, padx=10, pady=5, sticky=W)
        gender_combo = ttk.Combobox(class_student_frame, textvariable=self.var_gender,
                                  font=("times new roman", 13, "bold"), state="readonly",
                                  width=18)
        gender_combo["values"] = ("Nam", "Nữ", "Khác")
        gender_combo.current(0)
        gender_combo.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        #DOB
        dob_label = Label(class_student_frame, text="Ngày sinh:", font=("times new roman", 13, "bold"),
                              bg="white")
        dob_label.grid(row=2, column=2, padx=10, pady=10, sticky=W)

        self.dob_entry = DateEntry(class_student_frame, width=18, bd=3,selectmode='day',
                       year=2021, month=5,font=("times new roman", 13),
                       day=22,date_pattern='dd/mm/yyyy')
        self.dob_entry.grid(row=2, column=3, padx=10, pady=10, sticky=W)

        #email
        email_label = Label(class_student_frame, text="Email:", font=("times new roman", 13, "bold"),
                             bg="white")
        email_label.grid(row=3, column=0, padx=10, pady=10, sticky=W)

        email_entry = ttk.Entry(class_student_frame, width=20,textvariable=self.var_email, font=("times new roman", 13, "bold"))
        email_entry.grid(row=3, column=1, padx=10, pady=10, sticky=W)


        #Phone
        phone_label = Label(class_student_frame, text="SĐT:", font=("times new roman", 13, "bold"),
                          bg="white")
        phone_label.grid(row=3, column=2, padx=10, pady=10, sticky=W)

        phone_entry = ttk.Entry(class_student_frame, width=20,textvariable=self.var_phone, font=("times new roman", 13, "bold"))
        phone_entry.grid(row=3, column=3, padx=10, pady=10, sticky=W)


        #Address
        address_label = Label(class_student_frame, text="Địa chỉ:", font=("times new roman", 13, "bold"),
                            bg="white")
        address_label.grid(row=4, column=0, padx=10, pady=10, sticky=W)

        address_entry = ttk.Entry(class_student_frame, width=20,textvariable=self.var_address ,font=("times new roman", 13, "bold"))
        address_entry.grid(row=4, column=1, padx=10, pady=10, sticky=W)


        #radioBtn
        self.var_radio1=StringVar()
        radionbtn1=ttk.Radiobutton(class_student_frame,variable=self.var_radio1,text="Có ảnh",value="Yes")
        radionbtn1.grid(row=6,column=0)


        radionbtn2 = ttk.Radiobutton(class_student_frame,variable=self.var_radio1, text="Không ảnh", value="No")
        radionbtn2.grid(row=6, column=1)

        #btn_frame
        btn_frame=Frame(class_student_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame.place(x=0,y=280,width=715,height=35)

        save_btn=Button(btn_frame,text="Lưu",command=self.add_data,font=("times new roman",13,"bold"),bg="#38a6f0", fg="white",width=17)
        save_btn.grid(row=0,column=0)

        update_btn = Button(btn_frame, text="Sửa",command=self.update_data, font=("times new roman", 13, "bold"), bg="#38a6f0", fg="white", width=17)
        update_btn.grid(row=0, column=1)

        delete_btn = Button(btn_frame, text="Xóa",command=self.delete_data, font=("times new roman", 13, "bold"), bg="#38a6f0", fg="white", width=17)
        delete_btn.grid(row=0, column=2)

        reset_btn = Button(btn_frame, text="Làm mới",command=self.reset_data, font=("times new roman", 13, "bold"), bg="#38a6f0", fg="white", width=17)
        reset_btn.grid(row=0, column=3)

        btn_frame1 = Frame(class_student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame1.place(x=0, y=335, width=715, height=35)

        take_photo_btn = Button(btn_frame1, text="Lấy ảnh sinh viên",command=self.generate_dataset, font=("times new roman", 13, "bold"), bg="#38a6f0", fg="white",
                           width=35)
        take_photo_btn.grid(row=1, column=0)

        update_photo_btn = Button(btn_frame1, text="Training Data",command=self.train_classifier, font=("times new roman", 13, "bold"), bg="#38a6f0", fg="white",
                                width=35)
        update_photo_btn.grid(row=1, column=1)



        # --------------------------right_label-------------------------
        Right_frame = LabelFrame(main_frame, bd=2, bg="white",
                                font=("times new roman", 12, "bold"))
        Right_frame.place(x=750, y=10, width=720, height=330)


        #Search_frame
        search_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE, text="Hệ Thống Tìm kiếm",
                                         font=("yu gothic ui", 13, "bold"))
        search_frame.place(x=5, y=5, width=710, height=70)

        self.var_com_search= StringVar()
        search_label = Label(search_frame, text="Tìm kiếm theo :", font=("times new roman", 13, "bold"),
                            bg="white",fg="red2")
        search_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        search_combo = ttk.Combobox(search_frame, font=("times new roman", 13, "bold"), state="readonly",
                                      width=13,textvariable=self.var_com_search)
        search_combo["values"] = ("ID Sinh viên", "Tên sinh viên", "Lớp biên chế")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        self.var_search = StringVar()
        search_entry = ttk.Entry(search_frame, width=15, font=("times new roman", 13, "bold"),textvariable=self.var_search)
        search_entry.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        search_btn = Button(search_frame, text="Tìm kiếm", font=("times new roman", 12, "bold"),bg="#38a6f0", fg="white", width=12,command=self.search_data)
        search_btn.grid(row=0, column=3,padx=4)

        showAll_btn = Button(search_frame, text="Xem tất cả", font=("times new roman", 12, "bold"), bg="#38a6f0", fg="white",
                            width=12,command=self.fetch_data)
        showAll_btn.grid(row=0, column=4,padx=4)


        #table-------frame
        table_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=85, width=710, height=230)

        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.student_table=ttk.Treeview(table_frame,column=("id","dep","course","year","sem","name","div","roll","gender","dob","email","phone","address","photo"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("id", text="ID Sinh viên")
        self.student_table.heading("dep",text="Chuyên ngành")
        self.student_table.heading("course", text="Chương trình học")
        self.student_table.heading("year", text="Năm học")
        self.student_table.heading("sem", text="Học kì")
        self.student_table.heading("name", text="Họ tên")
        self.student_table.heading("div", text="Lớp biên chế")
        self.student_table.heading("roll", text="CMND")
        self.student_table.heading("gender", text="Giới tính")
        self.student_table.heading("dob", text="Ngày sinh")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="Số điện thoại")
        self.student_table.heading("address",text="Địa chỉ")

        self.student_table.heading("photo", text="Trạng thái ảnh")
        self.student_table["show"]="headings"

        self.student_table.column("id", width=100)
        self.student_table.column("dep", width=100)
        self.student_table.column("course", width=100)
        self.student_table.column("year", width=100)
        self.student_table.column("sem", width=100)
        self.student_table.column("name", width=100)
        self.student_table.column("div", width=100)
        self.student_table.column("roll", width=100)
        self.student_table.column("gender", width=100)
        self.student_table.column("dob", width=100)
        self.student_table.column("email", width=100)
        self.student_table.column("phone", width=100)
        self.student_table.column("address", width=100)
        self.student_table.column("photo", width=150)

        self.student_table.pack(fill=BOTH,expand=1)
        self.student_table.bind("<ButtonRelease>",self.get_cursor)#click datagrid
        self.fetch_data()#load du lieu len grid
        self.getNextid()
        #===============================bottomright-Class==============================

        Underright_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                      font=("yu gothic ui", 12, "bold"))
        Underright_frame.place(x=750, y=345, width=720, height=310)

        label_studentsb = Label(Underright_frame, bg="white", fg="red2", text="Quản lý lớp học",
                                font=("yu gothic ui", 14, "bold"))
        label_studentsb.place(x=0, y=1, width=700, height=35)

        # search
        self.var_com_searchclass = StringVar()
        search_combo = ttk.Combobox(Underright_frame, font=("times new roman", 12, "bold"),
                                    textvariable=self.var_com_searchclass,
                                    state="readonly",
                                    width=12)
        search_combo["values"] = ("Lớp", "Tên lớp")
        search_combo.current(0)
        search_combo.grid(row=0, column=0, padx=10, pady=40, sticky=W)

        self.var_searchclass = StringVar()
        searchstd_entry = ttk.Entry(Underright_frame, textvariable=self.var_searchclass, width=13,
                                    font=("times new roman", 11, "bold"))
        searchstd_entry.grid(row=0, column=1, padx=5, pady=35, sticky=W)

        searchstd_btn = Button(Underright_frame, command=self.search_Classdata, text="Tìm kiếm",
                               font=("times new roman", 11, "bold"), bg="#38a6f0", fg="white",
                               width=10)
        searchstd_btn.grid(row=0, column=2, padx=5)

        showAllstd_btn = Button(Underright_frame, text="Xem tất cả", command=self.fetch_Classdata,
                                font=("times new roman", 11, "bold"), bg="#38a6f0",
                                fg="white",
                                width=10)
        showAllstd_btn.grid(row=0, column=3, padx=5)

        # student
        studentid_label = Label(Underright_frame, text="Lớp học:", font=("times new roman", 12, "bold"),
                                bg="white", width=12)
        studentid_label.place(x=20, y=120, width=100)

        studentid_entry = ttk.Entry(Underright_frame, textvariable=self.var_class,
                                    font=("times new roman", 12, "bold"), width=20)
        studentid_entry.place(x=135, y=120, width=200)

        # subject
        subsub_label = Label(Underright_frame, text="Tên lớp học:", font=("times new roman", 12, "bold"),
                             bg="white")
        subsub_label.place(x=20, y=165, width=80)

        subsub_entry = ttk.Entry(Underright_frame, width=22, textvariable=self.var_nameclass,
                                 font=("times new roman", 12, "bold"))
        subsub_entry.place(x=135, y=165, width=200)

        # btn_frameteacher
        btn_framestd = Frame(Underright_frame, bg="white", bd=2, relief=RIDGE)
        btn_framestd.place(x=20, y=245, width=455, height=55)

        addTc_btn = Button(btn_framestd, text="Thêm mới", command=self.add_Classdata,
                           font=("times new roman", 12, "bold"),
                           bg="#fbd568", fg="#996319", width=10)
        addTc_btn.grid(row=9, column=0, pady=10, padx=5)

        deleteTc_btn = Button(btn_framestd, text="Xóa", command=self.delete_Classdata,
                              font=("times new roman", 12, "bold"),
                              bg="#fbd568", fg="#996319", width=10)
        deleteTc_btn.grid(row=9, column=1, pady=10, padx=5)

        updateTc_btn = Button(btn_framestd, text="Cập nhật", command=self.update_Classdata,
                              font=("times new roman", 12, "bold"),
                              bg="#fbd568", fg="#996319", width=10)
        updateTc_btn.grid(row=9, column=2, pady=10, padx=5)

        resetTc_btn = Button(btn_framestd, text="Làm mới", command=self.reset_Classdata,
                             font=("times new roman", 12, "bold"),
                             bg="#fbd568", fg="#996319", width=10)
        resetTc_btn.grid(row=9, column=3, pady=10, padx=5)

        # table_frame
        tablestd_frame = Frame(Underright_frame, bd=2, relief=RIDGE, bg="white")
        tablestd_frame.place(x=490, y=40, width=200, height=260)

        # scroll bar
        scroll_x = ttk.Scrollbar(tablestd_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(tablestd_frame, orient=VERTICAL)

        self.StudentTable = ttk.Treeview(tablestd_frame, column=(
            "class", "name"),
                                         xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.StudentTable.xview)
        scroll_y.config(command=self.StudentTable.yview)

        self.StudentTable.heading("class", text="Lớp học")
        self.StudentTable.heading("name", text="Tên")

        self.StudentTable["show"] = "headings"
        self.StudentTable.column("class", width=80)
        self.StudentTable.column("name", width=80)

        self.StudentTable.pack(fill=BOTH, expand=1)
        self.StudentTable.bind("<ButtonRelease>", self.get_cursorClass)
        self.fetch_Classdata()

    #============function decration===============
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

    def getNextid(self):
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                       port='3306')
        my_cursor = conn.cursor()
        my_cursor.execute(
            "SELECT  Student_id from student ORDER BY Student_id DESC limit 1")
        lastid = my_cursor.fetchone()
        if (lastid == None):
            self.var_std_id.set("1")
        else:
            nextid = int(lastid[0]) + 1
            self.var_std_id.set(str(nextid))

        conn.commit()
        conn.close()
        # return  self.var_id
    def add_data(self):
        # ========check class================
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                       port='3306')

        my_cursor = conn.cursor()
        my_cursor.execute("select Class from `class` ")
        ckclass = my_cursor.fetchall()
        arrayClass = []
        for chc in ckclass:
            # print(chc[0])
            arrayClass.append(str(chc[0]))
        if self.var_dep.get()=="Chọn chuyên ngành" or self.var_std_name.get()=="" or self.var_std_id.get()=="" or self.var_div.get()=="":
            messagebox.showerror("Error","Vui lòng nhập đầy đủ thông tin",parent=self.root)
        elif (self.var_div.get() not in arrayClass):
            messagebox.showerror("Error", "Tên lớp học không tồn tại ! Vui lòng kiểm tra lại", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer', port='3306')

                my_cursor=conn.cursor()
                my_cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                    self.var_std_id.get(),
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_std_name.get(),
                    self.var_div.get(),
                    self.var_roll.get(),
                    self.var_gender.get(),
                    # self.var_dob.get(),
                    self.dob_entry.get_date().strftime('%d/%m/%Y'),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_radio1.get()
                ))
                print(conn)
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
                messagebox.showinfo("Thành công","Thêm thông tin sinh viên thành công",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)


    #=======================fetch-data========================
    def fetch_data(self):
        conn=mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer', port='3306')

        my_cursor = conn.cursor()
        my_cursor.execute("Select * from student")
        data=my_cursor.fetchall()

        if len(data)!=0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("",END,values=i)
            conn.commit()
        conn.close()

    #======================get-cursor==============================
    def get_cursor(self,event=""):
        cursor_focus=self.student_table.focus()
        content=self.student_table.item(cursor_focus)
        data=content["values"]
        self.var_std_id.set(data[0]),
        self.var_dep.set(data[1]),
        self.var_course.set(data[2]),
        self.var_year.set(data[3]),
        self.var_semester.set(data[4]),
        self.var_std_name.set(data[5]),
        self.var_div.set(data[6]),
        self.var_roll.set(data[7]),
        self.var_gender.set(data[8]),
        self.dob_entry.set_date(data[9]),
        self.var_email.set(data[10]),
        self.var_phone.set(data[11]),
        self.var_address.set(data[12]),
        self.var_radio1.set(data[13]),

    def update_data(self):
        if self.var_dep.get()=="Chọn chuyên ngành" or self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","Vui lòng nhập đầy đủ thông tin",parent=self.root)
        else:
            try:
                Update=messagebox.askyesno("Update","Bạn có muốn cập nhật thông tin sinh viên này không?",parent=self.root)
                if Update>0:
                    conn=mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer', port='3306')
                    my_cursor = conn.cursor()
                    my_cursor.execute("update student set Dep=%s,course=%s,Year=%s,Semester=%s,Name=%s,Class=%s,"
                                      "Roll=%s,Gender=%s,Dob=%s,Email=%s,Phone=%s,Address=%s,PhotoSample=%s where Student_id=%s",(
                                            self.var_dep.get(),
                                            self.var_course.get(),
                                            self.var_year.get(),
                                            self.var_semester.get(),
                                            self.var_std_name.get(),
                                            self.var_div.get(),
                                            self.var_roll.get(),
                                            self.var_gender.get(),
                                            self.dob_entry.get_date().strftime('%d/%m/%Y'),
                                            self.var_email.get(),
                                            self.var_phone.get(),
                                            self.var_address.get(),
                                            self.var_radio1.get(),
                                            self.var_std_id.get()
                                        ))
                else:
                    if not Update:
                        return
                messagebox.showinfo("Thành công","Cập nhật thông tin sinh viên thành công",parent=self.root)
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Lỗi",f"Due To:{str(es)}",parent=self.root)

    #Delete Function
    def delete_data(self):
        if self.var_std_id.get()=="":
            messagebox.showerror("Lỗi","Không được bỏ trống ID sinh viên",parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Xoá sinh viên","Bạn có muốn xóa sinh viên này?",parent=self.root)
                if delete>0:
                        conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer', port='3306')
                        my_cursor = conn.cursor()
                        sql="delete from student where Student_id=%s"
                        val=(self.var_std_id.get(),)
                        my_cursor.execute(sql,val)
                else:
                    if not delete:
                        return
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
                messagebox.showinfo("Xóa","Xóa sinh viên thành công",parent=self.root)
            except Exception as es:
                messagebox.showerror("Lỗi",f"Due To:{str(es)}",parent=self.root)


    #===================Reset function====================
    def reset_data(self):
        self.var_dep.set("Chọn chuyên ngành"),
        self.var_course.set("Chọn hệ"),
        self.var_year.set("Chọn năm học"),
        self.var_semester.set("Chọn học kì"),
        self.var_std_id.set(""),
        self.var_std_name.set(""),
        self.var_div.set(""),
        self.var_roll.set(""),
        self.var_gender.set("Nam"),
        self.dob_entry.set_date(strftime("%d/%m/%Y")),
        self.var_email.set(""),
        self.var_phone.set(""),
        self.var_address.set(""),

        self.var_radio1.set(""),
        self.getNextid()
    def search_data(self):
            if self.var_com_search.get() == "" or self.var_search.get() == "":
                messagebox.showerror("Lỗi !", "Vui lòng nhập thông tin đầy đủ",parent=self.root)

            else:
                try:
                    conn = mysql.connector.connect(host='localhost', user='root', password='',
                                                   database='face_recognizer', port='3306')
                    my_cursor = conn.cursor()  # "ID Điểm Danh", "Ngày", "ID Sinh Viên"
                    if (self.var_com_search.get() == "ID Sinh viên"):
                        self.var_com_search.set("Student_id")
                    elif (self.var_com_search.get() == "Tên sinh viên"):
                        self.var_com_search.set("Name")
                    elif (self.var_com_search.get() == "Lớp biên chế"):
                        self.var_com_search.set("Class")

                    my_cursor.execute("select * from student where " + str(
                        self.var_com_search.get()) + " Like '%" + str(self.var_search.get()) + "%'")
                    data = my_cursor.fetchall()
                    if (len(data) != 0):
                        self.student_table.delete(*self.student_table.get_children())
                        for i in data:
                            self.student_table.insert("", END, values=i)
                        messagebox.showinfo("Thông báo", "Có " + str(len(data)) + " bản ghi thỏa mãn điều kiện",parent=self.root)
                        conn.commit()
                    else:
                        self.student_table.delete(*self.student_table.get_children())
                        messagebox.showinfo("Thông báo", " Không có bản ghi nào thỏa mãn điều kiện",parent=self.root)
                    conn.close()
                except Exception as es:
                    messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)
    #=============generate dataset and take photo=================
    def generate_dataset(self):
        if self.var_dep.get()=="Chọn chuyên ngành" or self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","Vui lòng nhập đầy đủ thông tin",parent=self.root)
        else:
            try:
                conn=mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer', port='3306')

                my_cursor = conn.cursor()
                # my_cursor.execute("select * from student")
                # myresult=my_cursor.fetchall()
                id=self.var_std_id.get()
                # for x in myresult:
                #     id+=1
                my_cursor.execute("update student set Dep=%s,course=%s,Year=%s,Semester=%s,Name=%s,Class=%s,"
                              "Roll=%s,Gender=%s,Dob=%s,Email=%s,Phone=%s,Address=%s,PhotoSample=%s where Student_id=%s",
                              (
                                  self.var_dep.get(),
                                  self.var_course.get(),
                                  self.var_year.get(),
                                  self.var_semester.get(),
                                  self.var_std_name.get(),
                                  self.var_div.get(),
                                  self.var_roll.get(),
                                  self.var_gender.get(),
                                  self.dob_entry.get_date().strftime('%d/%m/%Y'),
                                  self.var_email.get(),
                                  self.var_phone.get(),
                                  self.var_address.get(),
                                  self.var_radio1.get(),
                                  self.var_std_id.get()
                              ))
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
                #=========load haar===================
                face_classifier=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                def face_cropped(img):
                    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    faces=face_classifier.detectMultiScale(gray,1.3,5)
                    #scaling factor 1.3
                    ##minimum neighbor 5
                    for(x,y,w,h) in faces:
                        face_cropped=img[y:y+h,x:x+w]

                        return  face_cropped
                cap=cv2.VideoCapture(0)
                img_id=0
                while True:
                    net,my_frame=cap.read()
                    if face_cropped(my_frame) is not None:
                        img_id+=1
                        # face=cv2.resize(face_cropped(my_frame),(190,190))
                        face=cv2.cvtColor(face_cropped(my_frame),cv2.COLOR_BGR2GRAY)
                        fill_name_path="data/user."+str(id)+"."+str(img_id)+".jpg"

                        cv2.imwrite(fill_name_path,face)
                        cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),2)
                        cv2.imshow("Cropped Face",face)

                    if cv2.waitKey(1)==13 or int(img_id)==120:#duyet du 120 anh
                        break
                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Kết quả","Tạo dữ liệu khuôn mặt thành công",parent=self.root)
            except Exception as es:
                messagebox.showerror("Lỗi",f"Due To:{str(es)}",parent=self.root)

    #==========================TrainDataSet=======================
    def train_classifier(self):
        data_dir=("data")
        path=[os.path.join(data_dir,file) for file in os.listdir(data_dir)]

        faces=[]
        ids=[]
        for image in path:
            img=PIL.Image.open(image).convert('L')
            imageNp=np.array(img,'uint8')
            id=int(os.path.split(image)[1].split('.')[1])
            faces.append(imageNp)
            ids.append(id)
            cv2.imshow("Training",imageNp)
            cv2.waitKey(1)==13
        ids=np.array(ids)

        #=================Train data classifier and save============
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces,ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Kết quả","Training dataset Completed",parent=self.root)

    # ========================================Function Student======================================

    def get_cursorClass(self, event=""):
            cursor_row = self.StudentTable.focus()
            content = self.StudentTable.item(cursor_row)
            rows = content['values']
            self.var_class.set(rows[0])
            self.var_nameclass.set(rows[1])


    def add_Classdata(self):
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                           port='3306')
            my_cursor = conn.cursor()


            # =========check class=================
            my_cursor.execute("select Class from `class` ")
            ckClass = my_cursor.fetchall()
            arrayClass = []
            for chs in ckClass:
                # print(chs[0])
                arrayClass.append(str(chs[0]))
            conn.commit()
            conn.close()
            if self.var_class.get() == "" or self.var_nameclass.get() == "":
                messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin", parent=self.root)

            elif (self.var_class.get()  in arrayClass):
                messagebox.showerror("Error", "Class đã tồn tại! Vui lòng kiểm tra lại", parent=self.root)
            else:
                try:
                    conn = mysql.connector.connect(host='localhost', user='root', password='',
                                                   database='face_recognizer', port='3306')
                    my_cursor = conn.cursor()
                    my_cursor.execute("insert into class values(%s,%s)", (
                        self.var_class.get(),
                        self.var_nameclass.get(),
                    ))
                    conn.commit()
                    self.fetch_Classdata()
                    self.reset_Classdata()
                    conn.close()
                    messagebox.showinfo("Thành công", "Thêm thông tin lớp học thành công",
                                        parent=self.root)
                except Exception as es:
                    messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def reset_Classdata(self):
            self.var_class.set("")
            self.var_nameclass.set("")

    def fetch_Classdata(self):
            # global mydata
            # mydata.clear()
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                           port='3306')
            my_cursor = conn.cursor()
            my_cursor.execute("Select * from class")
            data = my_cursor.fetchall()
            if len(data) != 0:
                self.StudentTable.delete(*self.StudentTable.get_children())
                for i in data:
                    self.StudentTable.insert("", END, values=i)
                    mydata.append(i)
                conn.commit()
            conn.close()

    def update_Classdata(self):
            if self.var_class == "" or self.var_nameclass.get() == "":
                messagebox.showerror("Error", "Vui lòng nhập đầy đủ thông tin", parent=self.root)

            else:
                try:
                    Update = messagebox.askyesno("Update", "Bạn có muốn cập nhật bản ghi này không?", parent=self.root)
                    if Update > 0:
                        conn = mysql.connector.connect(host='localhost', user='root', password='',
                                                       database='face_recognizer', port='3306')
                        my_cursor = conn.cursor()
                        my_cursor.execute("UPDATE `class` SET Name = %s  WHERE "
                                          "`Class` = %s",
                                          (
                                              self.var_nameclass.get(),
                                              self.var_class.get(),
                                          ))
                    else:
                        if not Update:
                            return
                    messagebox.showinfo("Thành công", "Cập nhật thông tin lớp học thành công",
                                        parent=self.root)
                    conn.commit()
                    self.reset_Classdata()
                    self.fetch_Classdata()
                    conn.close()
                except Exception as es:
                    messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)

            # Delete Function

    def delete_Classdata(self):
            if self.var_class== "" or self.var_nameclass.get() == "":
                messagebox.showerror("Lỗi", "Không được bỏ trống thông tin! ", parent=self.root)
            else:
                try:
                    delete = messagebox.askyesno("Xoá bản ghi", "Bạn có muốn xóa bản ghi này ?", parent=self.root)
                    if delete > 0:
                        conn = mysql.connector.connect(host='localhost', user='root', password='',
                                                       database='face_recognizer', port='3306')
                        my_cursor = conn.cursor()
                        sql = "delete from class where Class=%s "
                        val = (self.var_class.get(),)
                        my_cursor.execute(sql, val)
                    else:
                        if not delete:
                            return
                    conn.commit()
                    # self.fetch_data()p
                    conn.close()
                    messagebox.showinfo("Xóa", "Xóa bản ghi thành công", parent=self.root)
                    self.reset_Classdata()
                    self.fetch_Classdata()
                except Exception as es:
                    messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)

    def search_Classdata(self):
            if self.var_com_searchclass.get() == "" or self.var_searchclass.get() == "":
                messagebox.showerror("Lỗi !", "Vui lòng nhập thông tin đầy đủ",parent=self.root)

            else:
                try:
                    conn = mysql.connector.connect(host='localhost', user='root', password='',
                                                   database='face_recognizer', port='3306')
                    my_cursor = conn.cursor()  # "ID Điểm Danh", "Ngày", "ID Sinh Viên"
                    if (self.var_com_searchclass.get() == "Lớp"):
                        self.var_com_searchclass.set("Class")
                    elif (self.var_com_searchclass.get() == "Tên lớp"):
                        self.var_com_searchclass.set("Name")

                    my_cursor.execute("select * from class where " + str(
                        self.var_com_searchclass.get()) + " Like '%" + str(self.var_searchclass.get()) + "%'")
                    data = my_cursor.fetchall()
                    if (len(data) != 0):
                        self.StudentTable.delete(*self.StudentTable.get_children())
                        for i in data:
                            self.StudentTable.insert("", END, values=i)
                        messagebox.showinfo("Thông báo", "Có " + str(len(data)) + " bản ghi thỏa mãn điều kiện",parent=self.root)
                        conn.commit()
                    else:
                        self.StudentTable.delete(*self.StudentTable.get_children())
                        messagebox.showinfo("Thông báo", " Không có bản ghi nào thỏa mãn điều kiện",parent=self.root)
                    conn.close()
                except Exception as es:
                    messagebox.showerror("Lỗi", f"Due To:{str(es)}", parent=self.root)
if __name__=="__main__":
    root=Tk() #khoi tao cua so va gan root vao
    obj=Student(root)
    root.mainloop()# cua so hien len
