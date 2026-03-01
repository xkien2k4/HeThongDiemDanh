import os

from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
import PIL.Image
from student import Student
from train import Train
from face_recognition import Face_Recognition
from attendance import Attendance
from face_recognition import new_tcid

value_from_p1 = None

def new_print(value):
    global value_from_p1
    value_from_p1 = value
    print(value)



class Face_Recognition_System:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self,root.title("Face Recognition System")


        # new_tcid(value_from_p1)
        # thư mục chứa ảnh cho giao diện
        img=PIL.Image.open(r"ImageFaceDetect\epu1.jpg")
        img=img.resize((500,130),PIL.Image.ANTIALIAS)
        self.photoimg=ImageTk.PhotoImage(img)

        f_lbl=Label(self.root,image=self.photoimg)
        f_lbl.place(x=0,y=0,width=500,height=130)

        #anh 2
        img1 = PIL.Image.open(r"ImageFaceDetect\student2.jpg")
        img1 = img1.resize((500, 130), PIL.Image.ANTIALIAS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl = Label(self.root, image=self.photoimg1)
        f_lbl.place(x=500, y=0, width=500, height=130)

        #anh3
        img2 = PIL.Image.open(r"ImageFaceDetect\facedt.png")
        img2 = img2.resize((550, 130), PIL.Image.ANTIALIAS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl = Label(self.root, image=self.photoimg2)
        f_lbl.place(x=1000, y=0, width=550, height=130)

        #bg
        img3 = PIL.Image.open(r"ImageFaceDetect\fd1.jpg")
        img3 = img3.resize((1530, 710), PIL.Image.ANTIALIAS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=130, width=1530, height=710)

        title_lbl=Label(bg_img,text="Phần mềm điểm danh bằng nhận diện khuôn mặt",font=("times new roman",25,"bold"),bg="white",fg="blue")
        title_lbl.place(x=0,y=0,width=1530,height=45)


        #student button
        img4 = PIL.Image.open(r"ImageFaceDetect\sv2.jpg")
        img4 = img4.resize((220, 220), PIL.Image.ANTIALIAS)
        self.photoimg4 = ImageTk.PhotoImage(img4)

        b1=Button(bg_img,image=self.photoimg4,command=self.student_details,cursor="hand2")
        b1.place(x=200,y=100,width=220,height=220)

        b1_1 = Button(bg_img, text="Thông tin sinh viên", cursor="hand2",command=self.student_details,font=("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=200, y=300, width=220, height=40)


        #detect_button
        img5 = PIL.Image.open(r"ImageFaceDetect\images.jpg")
        img5 = img5.resize((220, 220), PIL.Image.ANTIALIAS)
        self.photoimg5 = ImageTk.PhotoImage(img5)

        b1 = Button(bg_img, image=self.photoimg5, cursor="hand2",command=self.face_recognition)
        b1.place(x=500, y=100, width=220, height=220)

        b1_1 = Button(bg_img, text="Nhận diện", cursor="hand2",command=self.face_recognition, font=("times new roman", 15, "bold"),
                      bg="darkblue", fg="white")
        b1_1.place(x=500, y=300, width=220, height=40)


        #diem danh
        img6 = PIL.Image.open(r"ImageFaceDetect\reg1.jpg")
        img6 = img6.resize((220, 220), PIL.Image.ANTIALIAS)
        self.photoimg6 = ImageTk.PhotoImage(img6)

        b1 = Button(bg_img, image=self.photoimg6,command=self.attendance_data, cursor="hand2")
        b1.place(x=800, y=100, width=220, height=220)

        b1_1 = Button(bg_img, text="Điểm danh",command=self.attendance_data, cursor="hand2", font=("times new roman", 15, "bold"),
                      bg="darkblue", fg="white")
        b1_1.place(x=800, y=300, width=220, height=40)


        #help
        img7 = PIL.Image.open(r"ImageFaceDetect\help.jpg")
        img7 = img7.resize((220, 220), PIL.Image.ANTIALIAS)
        self.photoimg7 = ImageTk.PhotoImage(img7)

        b1 = Button(bg_img, image=self.photoimg7, cursor="hand2")
        b1.place(x=1100, y=100, width=220, height=220)

        b1_1 = Button(bg_img, text="Trợ giúp", cursor="hand2", font=("times new roman", 15, "bold"),
                      bg="darkblue", fg="white")
        b1_1.place(x=1100, y=300, width=220, height=40)


        #Train
        img8 = PIL.Image.open(r"ImageFaceDetect\train.jpg")
        img8 = img8.resize((220, 220), PIL.Image.ANTIALIAS)
        self.photoimg8 = ImageTk.PhotoImage(img8)

        b1 = Button(bg_img, image=self.photoimg8, cursor="hand2",command=self.train_data)
        b1.place(x=200, y=380, width=220, height=220)

        b1_1 = Button(bg_img, text="Train Data", cursor="hand2",command=self.train_data, font=("times new roman", 15, "bold"),
                      bg="darkblue", fg="white")
        b1_1.place(x=200, y=580, width=220, height=40)


        #QL anh
        img9 = PIL.Image.open(r"ImageFaceDetect\anh.png")
        img9 = img9.resize((220, 220), PIL.Image.ANTIALIAS)
        self.photoimg9 = ImageTk.PhotoImage(img9)

        b1 = Button(bg_img, image=self.photoimg9, cursor="hand2",command=self.open_img)
        b1.place(x=500, y=380, width=220, height=220)

        b1_1 = Button(bg_img, text="Xem Ảnh", cursor="hand2", command=self.open_img,font=("times new roman", 15, "bold"),
                      bg="darkblue", fg="white")
        b1_1.place(x=500, y=580, width=220, height=40)


        #Thong tin laptrinh
        img10 = PIL.Image.open(r"ImageFaceDetect\manage.jpg")
        img10 = img10.resize((220, 220), PIL.Image.ANTIALIAS)
        self.photoimg10 = ImageTk.PhotoImage(img10)

        b1 = Button(bg_img, image=self.photoimg10, cursor="hand2")
        b1.place(x=800, y=380, width=220, height=220)

        b1_1 = Button(bg_img, text="Nhà phát triển", cursor="hand2", font=("times new roman", 15, "bold"),
                      bg="darkblue", fg="white")
        b1_1.place(x=800, y=580, width=220, height=40)



        #exit
        img11 = PIL.Image.open(r"ImageFaceDetect\exit.png")
        img11 = img11.resize((220, 220), PIL.Image.ANTIALIAS)
        self.photoimg11 = ImageTk.PhotoImage(img11)

        b1 = Button(bg_img, image=self.photoimg11, cursor="hand2")
        b1.place(x=1100, y=380, width=220, height=220)

        b1_1 = Button(bg_img, text="Thoát", cursor="hand2", font=("times new roman", 15, "bold"),
                      bg="darkblue", fg="white")
        b1_1.place(x=1100, y=580, width=220, height=40)


        #=============Functions Btn=================
    def student_details(self):
        self.new_window=Toplevel(self.root)
        self.app=Student(self.new_window)

    def train_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Train(self.new_window)

    def face_recognition(self):
        self.new_window=Toplevel(self.root)
        self.app=Face_Recognition(self.new_window)

    def attendance_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Attendance(self.new_window)


    def open_img(self):
        os.startfile("data")

if __name__=="__main__":
    root=Tk() #khoi tao cua so va gan root vao
    obj=Face_Recognition_System(root)
    root.mainloop()# cua so hien len


