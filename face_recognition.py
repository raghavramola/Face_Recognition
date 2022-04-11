from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np
from time import strftime
from datetime import datetime

# Face_recognition class
class Face_recognition:
   
    def __init__(self,root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition")
        
        #Title
        title_label = Label(self.root,text="Face Recognition",font=("times new roman",35,"bold"),bg="white",fg="darkgreen")
        title_label.place(x=0,y=0,width=1530,height=60)
        
        #Top Image
        img_top = Image.open(r"images\detect.jpg")
        img_top = img_top.resize((650,700),Image.ANTIALIAS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_label = Label(self.root,image = self.photoimg_top)
        f_label.place(x=20,y=55,width=650,height=700)

        #Bottom Image
        img_bottom = Image.open(r"images\detect2.jpg")
        img_bottom = img_bottom.resize((650,700),Image.ANTIALIAS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)

        f_label = Label(self.root,image = self.photoimg_bottom)
        f_label.place(x=650,y=55,width=950,height=700)
        
        #Button
        b1_1 = Button(f_label,text="Face Recognition",cursor="hand2",command=self.face_recog,font=("times new roman",18,"bold"),bg="darkgreen",fg="white")
        b1_1.place(x=350,y=600,width=200,height=60)
        
    #============Attendance====================
    def mark_attendance(self,i,r,n,d):
        with open("attendance.csv","r+",newline="\n") as f:
            myDataList = f.readlines()
            name_list=[]
            for line in myDataList:
                entry=line.split((","))
                name_list.append(entry[0])
            if((i not in name_list) and (r not in name_list) and (n not in name_list) and (d not in name_list)):
                now=datetime.now()
                d1=now.strftime("%d/%m/%Y")
                dtString=now.strftime("%H:%M:%S")
                f.writelines(f"\n{i},{r},{n},{d},{dtString},{d1},Present")  
        
        
    #========Face Recognition========
    def face_recog(self):
        def draw_boundray(img,classifier,scaleFactor,minNeighbors,color,text,clf):
            gray_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Grey scale
            ##The detectMultiScale() method returns a list of rectangles of all the detected objects (faces in our first case).
            features = classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)

            coord = [] # make empty coord for making rectangle

            
            for(x,y,w,h) in features:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                user_id,predict = clf.predict(gray_image[y:y+h,x:x+w])
                # e can use the Euclidean distance
                confidence =int((100*(1-predict/300)))

                conn = mysql.connector.connect(host="localhost",user="root",password="Abcd@1234",database="face_recognizer")
                my_cursor = conn.cursor()

                my_cursor.execute("select Name from student where stud_id="+str(user_id))
                n = my_cursor.fetchone()
                n ='+'.join(n)

                my_cursor.execute("select Roll from student where stud_id="+str(user_id))
                r = my_cursor.fetchone()
                r ='+'.join(r)

                my_cursor.execute("select Dep from student where stud_id="+str(user_id))
                d = my_cursor.fetchone()
                d ='+'.join(d)
                
                my_cursor.execute("select student_id from student where stud_id="+str(user_id))
                i = my_cursor.fetchone()
                i ='+'.join(i)


                #So the algorithm output is the ID from the image with the closest histogram.
                #  The algorithm should also return the calculated distance, which can be used as a ‘confidence’ measurement.
                # Note: don’t be fooled about the ‘confidence’ name, as lower confidences are better because it means the distance between the two histograms is closer. 


                if confidence>78:
                    cv2.putText(img,f"stud_id:{i}",(x,y-75),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Roll:{r}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Name:{n}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Dep:{d}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    self.mark_attendance(i,r,n,d)

                else:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                    cv2.putText(img,"Unknown face",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)

                coord = [x,y,w,h]
            
            return coord

        #For recognition
        def recognize(img,clf,faceCascade):
            coord = draw_boundray(img,faceCascade,1.1,10,(255,25,255),"Face",clf)
            return img

        #===== Store harcascade in file====
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        # For reading LBPHF we store this train data 
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        #===Open web cam=====
        video_cap = cv2.VideoCapture(0)

        while True:
            ret,img = video_cap.read()
            img = recognize(img,clf,faceCascade)
            cv2.imshow("Welcome to face recognition",img)

            #Waitkey  1 means when u press  enter web cam will close
            if cv2.waitKey(1)==13:
                break
        video_cap.release()
        cv2.destroyAllWindows()    
        
        
#Object of Face_recognition class
if __name__ == "__main__":
    root = Tk()
    obj = Face_recognition(root)
    root.mainloop()        