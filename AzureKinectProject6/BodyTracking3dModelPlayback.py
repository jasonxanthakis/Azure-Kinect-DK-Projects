#Model Pre-Recorded Joint Data from Azure Kinect Body Tracking SDK in 3D using Ursina Engine
#by Jason Xanthakis

from ursina import *
from model3dEngine import Model
import nodeCoordinateRecorder as r
import os
import time

#Loads all joints in a recorded frame
def load_frame(data, frame_count):
    model.clear_data()

    #Loop through each joint
    for joint_id in range(0,len(r.JointRecorder.K4ABT_JOINT_NAMES)):
        
        #Load Data Into Model
        line = data[r.JointRecorder.K4ABT_JOINT_NAMES[joint_id]]
        joint_coords = line[frame_count]
        y_value = -joint_coords[1]
        joint_coords = [joint_coords[0],y_value,joint_coords[2]]
        
        model.load_data(r.JointRecorder.K4ABT_JOINT_NAMES[joint_id],joint_coords)

#Ursina Update Function
def update():
    model.update()

#Ursina Keyboard Input Function
def input(key):
    model.input(key)

if __name__ == "__main__":
    #Initialise Ursina Object & Extension
    app = Ursina()
    model = Model(app)

    #Set a frame counter
    frame_count = 0

    #Select file and extract data
    file_path = ""      #Insert file path HERE

    data = r.JointRecorder.extract_bin_data(file_path)
    limit = len(data[r.JointRecorder.K4ABT_JOINT_NAMES[0]])
    print(limit)

    #Main Event Loop
    while True:
        #Set the frame rate of the model compared to the engine
        model_frame_count = frame_count // 5
        #model_frame_count = frame_count // 20
        #model_frame_count = frame_count // 50
        #model_frame_count = frame_count // 100
        
        #Restart when the data runs out
        if model_frame_count >= limit - 1:
            frame_count = 0
            model_frame_count = 0
        
        #Load frame from extracted data
        load_frame(data, model_frame_count)

        #Move to Next Frame (Update Engine)
        model.app.step()
        frame_count += 1

        #if frame_count >= len(data):
        #   break
