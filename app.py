import tkinter as tk 
import customtkinter as ck 

import pandas as pd 
import numpy as np 
import pickle 

import mediapipe as mp
import cv2
from PIL import Image, ImageTk 

#from landmarks import landmarks
window = tk.Tk()
window.geometry("800x900")
window.title("window") 
ck.set_appearance_mode("dark")



classLabel = ck.CTkLabel(window, height=40, width=120,  text_color="black") 
counterLabel = ck.CTkLabel(window, height=40, width=120,  text_color="black")
probLabel = ck.CTkLabel(window, height=40, width=120,  text_color="black") 
classBox = ck.CTkLabel(window, height=40, width=120,  text_color="black", fg_color="grey")
counterBox = ck.CTkLabel(window, height=40, width=120,  text_color="black", fg_color="grey")
probBox = ck.CTkLabel(window, height=40, width=120,  text_color="black", fg_color="grey")
classLabel.place(x=10, y = 1)
counterLabel.place(x=160, y = 1)
probLabel.place(x=300, y = 1)
classBox.place(x=10, y = 41)
counterBox.place(x=160, y = 41)
probBox.place(x=300, y = 41)
classLabel.configure(text = 'STAGE')
counterLabel.configure(text = 'REPS')
probLabel.configure(text = 'PROB')
classBox.configure(text = '0')
counterBox.configure(text = '0')
probBox.configure(text = '0')

window.mainloop()