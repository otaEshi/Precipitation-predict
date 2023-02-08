import tkinter as tk
from tkinter import *
from tkinter import CENTER, ttk
import numpy as np
import tensorflow as tf

class GUI:
    def __init__(self):
        self.mean = [5.30704225e+00, 4.30036836e+00, 1.14944529e+02, 1.01540904e+05]
        self.variation = [4.09575756e+00, 1.58111613e+01, 7.81008620e+03, 1.15623340e+06]
        self.model = tf.keras.models.load_model("./rain_model/rain.savedmodel")

        self.root = tk.Tk()
        self.root.resizable(0,0)

        self.root.geometry("800x300")
        self.root.title("Precipitation Prediction")
        
        self.frame = tk.Frame(self.root)
        self.cloudCoverLabel = tk.Label(self.frame, text="Cloud cover ")
        self.cloudCoverLabel.grid(row=0, column=0)

        self.cloudCoverEntry = tk.Entry(self.frame)
        self.cloudCoverEntry.grid(row=0, column=1)

        self.sunShineEntry = tk.Entry(self.frame)
        self.sunShineEntry.grid(row=1, column=1)

        self.sunShineLabel = tk.Label(self.frame, text="Sunshine ")
        self.sunShineLabel.grid(row=1, column=0)

        self.globalRadiationLabel = tk.Label(self.frame, text="Global radiation ")
        self.globalRadiationLabel.grid(row=2, column=0)

        self.globalRadiationEntry = tk.Entry(self.frame)
        self.globalRadiationEntry.grid(row=2, column=1)

        self.pressureLabel = tk.Label(self.frame, text="Pressure ")
        self.pressureLabel.grid(row=3, column=0)

        self.pressureEntry = tk.Entry(self.frame)
        self.pressureEntry.grid(row=3, column=1)

        self.exercuteBtn = tk.Button(self.frame, text="Predict", command=self.show_result)
        self.exercuteBtn.place(x=80,y=95,height=30,width=90)

        self.resultLabel = tk.Label(self.root, text = "", font=("Arial",15))
        self.resultLabel.place(x=0,y=160,height=20, width= 330)

        self.historyFrame = tk.Frame(self.root)
        self.historyFrame.pack(side=RIGHT,expand=True,fill=BOTH)

        self.scroll = Scrollbar(self.historyFrame)
        self.scroll.pack(pady=20,side=RIGHT,fill=Y)

        self.myHistory = ttk.Treeview(self.historyFrame,yscrollcommand=self.scroll.set)
        self.myHistory.pack()
        
        self.scroll.config(command=self.myHistory.yview)

        self.myHistory['columns']=('Cloud cover','Sunshine','Global radiation','Pressure','Precipitation')

        self.myHistory.column("#0", width=0,  stretch=NO)
        self.myHistory.column("Cloud cover",anchor=CENTER, width=80)
        self.myHistory.column("Sunshine",anchor=CENTER,width=80)
        self.myHistory.column("Global radiation",anchor=CENTER,width=80)
        self.myHistory.column("Pressure",anchor=CENTER,width=80)
        self.myHistory.column("Precipitation",anchor=CENTER,width=80)

        self.myHistory.heading("#0",text="",anchor=CENTER)
        self.myHistory.heading("Cloud cover",text="Cloud cover",anchor=CENTER)
        self.myHistory.heading("Sunshine",text="Sunshine",anchor=CENTER)
        self.myHistory.heading("Global radiation",text="Global radiation",anchor=CENTER)
        self.myHistory.heading("Pressure",text="Pressure",anchor=CENTER)
        self.myHistory.heading("Precipitation",text="Precipitation",anchor=CENTER)

        self.myHistory.pack()

        self.frame.pack(padx=30,pady=20,side=LEFT,expand=True,fill=BOTH)
        self.root.mainloop()


    def show_result(self):
        cloudCover= float(self.cloudCoverEntry.get())
        sunShine= float(self.sunShineEntry.get())
        globalRadiation= float(self.globalRadiationEntry.get())
        pressure= float(self.pressureEntry.get())
        arr = np.array([[cloudCover,sunShine,globalRadiation,pressure]])
        arr=(arr-self.mean)/self.variation
        y= self.model.predict(arr)
        result = "Precipitation is:  " + str(y[0][0])
        self.myHistory.insert(parent='',index='end',text='',
        values=(cloudCover,sunShine,globalRadiation,pressure, str(y[0][0])))
        print(result)
        self.resultLabel.config(text=result)

GUI()

