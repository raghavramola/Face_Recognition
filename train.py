from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np

# Train class
class Train:

    def __init__(self,root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Trainig model")

        #Title
        title_label = Label(self.root,text="TRAIN DATA SET",font=("times new roman",35,"bold"),bg="white",fg="darkgreen")
        title_label.place(x=0,y=0,width=1530,height=45)

        #Top Image
        img_top = Image.open(r"images\face.jpg")
        img_top = img_top.resize((1530,325),Image.ANTIALIAS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_label = Label(self.root,image = self.photoimg_top)
        f_label.place(x=0,y=55,width=1530,height=325)
        
        #Button
        b1_1 = Button(self.root,text="TRAIN DATA",command=self.train_classifier,cursor="hand2",font=("times new roman",30,"bold"),bg="red",fg="white")
        b1_1.place(x=0,y=380,width=1530,height=60)
        
        #Bottom Image
        img_bottom = Image.open(r"images\background.jpg")
        img_bottom = img_bottom.resize((1530,315),Image.ANTIALIAS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)

        f_label = Label(self.root,image = self.photoimg_bottom)
        f_label.place(x=0,y=440,width=1530,height=325)
        
        
        
    #========LBPH(Local Binary Pattern Histogram) Algorithm======

    # Local Binary Pattern (LBP) is a simple yet very efficient texture operator
    #  which labels the pixels of an image by thresholding the neighborhood of each pixel and considers the result as a binary number.
    # when LBP is combined with histograms of oriented gradients (HOG) descriptor, it improves the detection performance considerably on some datasets.

    def train_classifier(self):
        data_dir = ("data")
        #List comprehensive
        path= [os.path.join(data_dir,file) for file in os.listdir(data_dir)]
        faces=[]
        ids=[]

        for image in path:
            img = Image.open(image).convert('L') #Conversion to Gray scale image
            #Now convert this gray scale image into grids for that we use numpy
            imageNp = np.array(img,'uint8')   # Convert img into numpy array and uint8 is a datatype
            
            #data\ user.1.1.jpg
            # 0                     1[0,1,2,3]
            id = int(os.path.split(image)[1].split('.')[1])

            faces.append(imageNp)
            ids.append(id)
            cv2.imshow("Training",imageNp)
            cv2.waitKey(1)==13

        #Convert ids into numpy
        ids = np.array(ids)

        #======Train the classifier and save=======
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces,ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Result","Training dataset complete successfully",parent=self.root)    
        
        
#Object of Train class
if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()        