import os
import random
from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
import PIL.Image
from time import strftime
from math import *
from tkinter import messagebox
from student_upd import Student
from train import Train
from face_recognition import Face_Recognition
from attendance import Attendance
from face_recognition import new_tcid
from subject import Subject
from teacher import Teacher
from lesson import Lesson
from report_attendance import Report
import mysql.connector

value_from_p1 = None

def new_print(value):
    global value_from_p1
    value_from_p1 = value
    print(value_from_p1)


class Face_Recognition_System:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Hệ thống nhận diện khuôn mặt")
        today = strftime("%d-%m-%Y")

        new_tcid(value_from_p1)
        #background
        print(value_from_p1)
        img3 = PIL.Image.open(r"ImageFaceDetect\bgbtn.png")
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
        self.txt = "Hệ thống nhận diện khuôn mặt"
        self.count = 0
        self.text = ''
        self.color = ["#4f4e4d", "#f29844", "red2"]
        self.heading = Label(self.root, text=self.txt, font=("yu gothic ui", 26, "bold"), bg="white", fg="black",
                             bd=5, relief=FLAT)
        self.heading.place(x=360, y=22, width=500)
        self.slider()
        self.heading_color()

        #=========account===========
        #===get email from db=============
        self.account=""
        if(value_from_p1=="0"):
            self.account = "Admin"
        elif(value_from_p1==None):
            self.account="AdminSafe"
        else:

            conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                           port='3306')
            my_cursor = conn.cursor()
            my_cursor.execute("select Email from teacher where Teacher_id=%s", (
                value_from_p1,
            ))
            row = my_cursor.fetchone()
            self.account = row[0]
        img_peop = PIL.Image.open(r"ImageFaceDetect\peop.png")
        img_peop = img_peop.resize((27, 27), PIL.Image.ANTIALIAS)
        self.photoimgpeop = ImageTk.PhotoImage(img_peop)
        time_img = Label(self.root, image=self.photoimgpeop, bg="white")
        time_img.place(x=970, y=45, width=27, height=27)
        self.lblemail = Label(self.root,text=self.account, font=("yu gothic ui", 12, "bold"), bg="white", fg="green")
        self.lblemail.place(x=1000, y=48, width=150, height=22)

        #=======logout==========
        img_logout = PIL.Image.open(r"ImageFaceDetect\logout.png")
        img_logout = img_logout.resize((27, 27), PIL.Image.ANTIALIAS)
        self.photoimglogout = ImageTk.PhotoImage(img_logout)

        b1 = Button(self.root, image=self.photoimglogout, cursor="hand2", command=self.exit,borderwidth=0,bg="white")
        b1.place(x=1350, y=45, width=27, height=27)

        b1_1 = Button(self.root, text="Đăng xuất", cursor="hand2", command=self.exit,
                      font=("times new roman", 13, "bold"),
                      bg="white", fg="black",borderwidth=0)
        b1_1.place(x=1380, y=48, width=100, height=27)


        #=============Button================
        img_btn1 = PIL.Image.open(r"ImageFaceDetect\report.png")
        img_btn1 = img_btn1.resize((80, 113), PIL.Image.ANTIALIAS)
        self.photobtn1 = ImageTk.PhotoImage(img_btn1)

        b2 = Button(self.root, text="Thống kê",font=("yu gothic ui", 16, "bold"),command=self.report_data,image=self.photobtn1,cursor="hand2",
                    activebackground="white",bg="white",borderwidth=0,compound="top")
        b2.place(x=180, y=490, width=180, height=180)

        #============student================
        img_btn2 = PIL.Image.open(r"ImageFaceDetect\student.png")
        img_btn2 = img_btn2.resize((80, 113), PIL.Image.ANTIALIAS)
        self.photobtn2 = ImageTk.PhotoImage(img_btn2)

        btn2 = Button(self.root, text="Sinh viên", font=("yu gothic ui", 16, "bold"),command=self.student_details, image=self.photobtn2,
                    cursor="hand2",
                    activebackground="white", bg="white", borderwidth=0, compound="top")
        btn2.place(x=180, y=200, width=180, height=180)

        #============nhan dien============
        img_btn3 = PIL.Image.open(r"ImageFaceDetect\nhandien.png")
        img_btn3 = img_btn3.resize((80, 113), PIL.Image.ANTIALIAS)
        self.photobtn3 = ImageTk.PhotoImage(img_btn3)

        b3 = Button(self.root, text="Nhận diện", font=("yu gothic ui", 16, "bold"),command=self.face_recognition ,image=self.photobtn3,
                    cursor="hand2",
                    activebackground="white", bg="white", borderwidth=0, compound="top")
        b3.place(x=520, y=200, width=180, height=180)

        #===========diem-danh===============
        img_btn4 = PIL.Image.open(r"ImageFaceDetect\ghichu.png")
        img_btn4 = img_btn4.resize((80, 113), PIL.Image.ANTIALIAS)
        self.photobtn4 = ImageTk.PhotoImage(img_btn4)

        b4 = Button(self.root, text="Điểm danh", font=("yu gothic ui", 16, "bold"),command=self.attendance_data ,image=self.photobtn4,
                    cursor="hand2",
                    activebackground="white", bg="white", borderwidth=0, compound="top")
        b4.place(x=860, y=200, width=180, height=180)

        #==========monhoc=================
        img_btn5 = PIL.Image.open(r"ImageFaceDetect\book.png")
        img_btn5 = img_btn5.resize((80, 113), PIL.Image.ANTIALIAS)
        self.photobtn5 = ImageTk.PhotoImage(img_btn5)

        b5 = Button(self.root, text="Môn học", font=("yu gothic ui", 16, "bold"),command=self.subject_data, image=self.photobtn5,
                    cursor="hand2",
                    activebackground="white", bg="white", borderwidth=0, compound="top")
        b5.place(x=1175, y=200, width=180, height=180)

        #==========thaygiao=============
        img_btn6 = PIL.Image.open(r"ImageFaceDetect\teacher.png")
        img_btn6 = img_btn6.resize((80, 113), PIL.Image.ANTIALIAS)
        self.photobtn6 = ImageTk.PhotoImage(img_btn6)

        b6 = Button(self.root, text="Giáo viên", font=("yu gothic ui", 16, "bold"),command=self.teacher_data, image=self.photobtn6,
                    cursor="hand2",
                    activebackground="white", bg="white", borderwidth=0, compound="top")
        b6.place(x=520, y=490, width=180, height=180)


        #==========chuyen nganh================
        img_btn7 = PIL.Image.open(r"ImageFaceDetect\lesson.png")
        img_btn7 = img_btn7.resize((80, 113), PIL.Image.ANTIALIAS)
        self.photobtn7 = ImageTk.PhotoImage(img_btn7)

        b7 = Button(self.root, text="Buổi học", font=("yu gothic ui", 16, "bold"),command=self.lesson_data, image=self.photobtn7,
                    cursor="hand2",
                    activebackground="white", bg="white", borderwidth=0, compound="top")
        b7.place(x=860, y=490, width=180, height=180)

        #==========XemAnh===============
        img_btn8 = PIL.Image.open(r"ImageFaceDetect\picture.png")
        img_btn8 = img_btn8.resize((80, 113), PIL.Image.ANTIALIAS)
        self.photobtn8 = ImageTk.PhotoImage(img_btn8)

        b8 = Button(self.root, text="Xem ảnh", font=("yu gothic ui", 16, "bold"),command=self.open_img, image=self.photobtn8,
                    cursor="hand2",
                    activebackground="white", bg="white", borderwidth=0, compound="top")
        b8.place(x=1175, y=490, width=180, height=180)
        if(value_from_p1=="0" or value_from_p1==None):
            b4['state']="normal"
            b5['state'] = "normal"
            b6['state']="normal"
            b7['state']="normal"
            b8['state']="normal"
        else:
            change_pass = Button(self.root, text="Đổi mật khẩu", cursor="hand2", command=self.change_pass,
                          font=("times new roman", 13, "bold"),
                          bg="white", fg="black", borderwidth=0)
            change_pass.place(x=1220, y=48, width=100, height=27)
            b4['state'] = "disabled"
            b5['state'] = "disabled"
            b6['state'] = "disabled"
            b7['state'] = "disabled"
            b8['state'] = "disabled"

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
    def exit(self):
        Exit = messagebox.askyesno("Đăng xuất", "Bạn có chắc chắn muốn đăng xuất không?", parent=self.root)
        if(Exit>0):
            self.root.destroy()
        else:
            if not Exit:
                return
    def student_details(self):
        self.new_window=Toplevel(self.root)
        self.app=Student(self.new_window)

    def train_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Train(self.new_window)

    def report_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Report(self.new_window)

    def face_recognition(self):
        self.new_window=Toplevel(self.root)
        self.app=Face_Recognition(self.new_window)

    def attendance_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Attendance(self.new_window)

    def subject_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Subject(self.new_window)
    def teacher_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Teacher(self.new_window)
    def lesson_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Lesson(self.new_window)

    def open_img(self):
        os.startfile("data")
    def reset_pass(self):
        if self.changePass_entry.get=="Select":
            messagebox.showerror("Error","Hãy chọn câu hỏi bảo mật",parent=self.root2)
        elif self.answerLabel_entry.get()=="":
            messagebox.showerror("Error","Hãy nhập câu trả lời",parent=self.root2)
        elif self.passLabel_entry.get()=="":
            messagebox.showerror("Error", "Hãy nhập mật khẩu mới",parent=self.root2)
        else:
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='face_recognizer',
                                           port='3306')
            my_cursor = conn.cursor()
            my_cursor.execute(
                "SELECT  * from teacher where Teacher_id=%s and SecurityQ=%s and SecurityA=%s",
                (str(value_from_p1),self.changePass_entry.get(),self.answerLabel_entry.get(),))
            row = my_cursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Sai câu hỏi bảo mật hoặc đáp án ",parent=self.root2)
            else:
                my_cursor.execute("update teacher set Password=%s where Teacher_id=%s",(self.passLabel_entry.get(),str(value_from_p1),))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thông báo","Đổi mật khẩu thành công",parent=self.root2)

                self.root2.destroy()
    def change_pass(self):
        self.root2=Toplevel()
        self.root2.title("Đổi mật khẩu")
        self.root2.geometry("340x450+910+70")
        l=Label(self.root2,text="Đổi mật khẩu",font=("times new roman",20,"bold"),fg="black",bg="white")
        l.place(x=0,y=10,relwidth=1)
        changePass = Label(self.root2, text="Câu hỏi bảo mật:", font=("times new roman", 12, "bold"),
                          bg="white")
        changePass.place(x=50,y=80)

        self.changePass_entry = ttk.Combobox(self.root2, width=20,
                                       font=("times new roman", 12, "bold"), state='readonly')
        self.changePass_entry["values"] = ("Select", "Bạn thích ăn gì", "Sở thích của bạn", "Chữ số bạn thích")
        self.changePass_entry.place( x=50,y=110,width=250)
        self.changePass_entry.current(0)

        # answer
        answerLabel = Label(self.root2, text="Câu trả lời:", font=("times new roman", 12, "bold"),
                          bg="white")
        answerLabel.place(x=50,y=150)

        self.answerLabel_entry = ttk.Entry(self.root2, width=22,
                                    font=("times new roman", 12, "bold"))
        self.answerLabel_entry.place(x=50,y=180,width=250)

        # pass
        passLabel = Label(self.root2, text="Mật khẩu mới:", font=("times new roman", 12, "bold"),
                          bg="white")
        passLabel.place(x=50,y=220)

        self.passLabel_entry = ttk.Entry(self.root2, width=22,
                                    font=("times new roman", 12, "bold"),show="*")
        self.passLabel_entry.place(x=50,y=250,width=250)

        btn=Button(self.root2,text="Đổi mật khẩu",font=("times new roman", 12, "bold"),fg="white",bg="darkblue",command=self.reset_pass)
        btn.place(x=120,y=300)
if __name__=="__main__":
    root=Tk() #khoi tao cua so va gan root vao
    obj=Face_Recognition_System(root)
    root.mainloop()# cua so hien len