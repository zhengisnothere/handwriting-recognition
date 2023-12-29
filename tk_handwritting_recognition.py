# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 10:31:58 2023

@author: userid
"""
import tkinter as tk
import numpy as np

class PixelCanvas:
    def __init__(self, pixel_size=10, length=20, width=20):
        self.pixel_size = pixel_size
        self.matrix_length = length
        self.matrix_width = width
        self.split_size=10
        self.canvas_length = length * pixel_size
        self.canvas_width = width * pixel_size
        self.window = tk.Tk()
        self.window.title("handwriting recognition")
        self.window.geometry(f"{self.canvas_length}x{self.canvas_width+55}")
        self.canvas_matrix=[[0 for _ in range(self.matrix_length)] for _ in range(self.matrix_width)]
        self.canvas = tk.Canvas(self.window, width=self.canvas_length, height=self.canvas_width, bg="white")
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.pack()
        self.clear_botton=tk.Button(text='clear',command=self.clear_canvas)
        self.clear_botton.pack()
        self.clear_botton.place(x=10,y=self.canvas_width+5)
        self.train_button=tk.Button(text='train',command=self.train)
        self.train_button.pack()
        self.train_button.place(x=80,y=self.canvas_width+5)
        self.test_button=tk.Button(text='test',command=self.test)
        self.test_button.pack()
        self.test_button.place(x=180,y=self.canvas_width+5)
        self.user_input=tk.Entry(width=10)
        self.user_input.pack()
        self.user_input.insert(0, 'label')
        self.user_input.place(x=80,y=self.canvas_width+35)
        self.output=tk.Label(text='result: None')
        self.output.pack()
        self.output.place(x=180,y=self.canvas_width+35)
        self.train_data={}

    def on_mouse_drag(self, event):
        mouse_x, mouse_y = event.x, event.y
        matrix_x=min(self.matrix_length-1,max(0,int(mouse_x/self.pixel_size)))
        matrix_y=min(self.matrix_width-1,max(0,int(mouse_y/self.pixel_size)))
        if self.canvas_length>mouse_x>0 and self.canvas_width>mouse_y>0:
            self.size_fill(matrix_x,matrix_y)
    
    def size_fill(self, mx, my):
        for ay in range(-1, 2):
            for ax in range(-1, 2):
                if self.matrix_length > mx - ax >= 0 and self.matrix_width > my - ay >= 0:
                    x1 = (mx - ax) * self.pixel_size
                    y1 = (my - ay) * self.pixel_size
                    x2 = x1 + self.pixel_size
                    y2 = y1 + self.pixel_size
                    self.canvas_matrix[my - ay][mx - ax] = 1
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="black")
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.canvas_matrix=[[0 for _ in range(self.matrix_length)] for _ in range(self.matrix_width)]
        
    def train(self):
        image_data=self.get_image_data()
        image_label=self.user_input.get()
        try:
            self.train_data[image_label].append(image_data)
        except KeyError:
            self.train_data[image_label]=[]
            self.train_data[image_label].append(image_data)
        print(self.train_data.keys())
    
    def get_image_data(self):
        result=[0 for _ in range(int((self.matrix_length/self.split_size)*(self.matrix_width/self.split_size)))]
        for my in range(self.matrix_width):
            for mx in range(self.matrix_length):
                if self.canvas_matrix[my][mx]==1:
                    sx=int(mx/self.split_size)
                    sy=int(my/self.split_size)
                    index=sy*int(self.matrix_length/self.split_size)+sx
                    result[index]=result[index]+1
        return result
                
    def test(self):
        image_data=self.get_image_data()
        label_distance={}
        for label in self.train_data:
            this_label_distance=[]
            for data in self.train_data[label]:
                distance=self.euclidean_distance(image_data,data)
                this_label_distance.append(distance)
            label_distance[label]=min(this_label_distance)
        print(label_distance)
        if len(label_distance)>0:
            min_distance_key=min(label_distance, key=label_distance.get)
        else:
            min_distance_key='None'
        self.output['text']='result: '+min_distance_key
        self.user_input.delete(0, tk.END)
        self.user_input.insert(0, min_distance_key)
                
    
    def euclidean_distance(self,l1,l2):
        arr1 = np.array(l1)
        arr2 = np.array(l2)
        distance = np.sqrt(np.sum((arr1 - arr2) ** 2))
        return distance
    
    def run(self):
        self.window.mainloop()

pixel_canvas = PixelCanvas(2,150,150)
pixel_canvas.run()