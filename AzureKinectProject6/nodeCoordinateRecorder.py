#Module for Recording Node Coordinates of the Azure Kinect Body Tracking SDK
#by Jason Xanthakis

import os
import json
import pickle

#Joint Recorder Object
class JointRecorder:
    K4ABT_JOINT_NAMES = ["pelvis", "spine - navel", "spine - chest", "neck", "left clavicle", "left shoulder", "left elbow",
                         "left wrist", "left hand", "left handtip", "left thumb", "right clavicle", "right shoulder", "right elbow",
                         "right wrist", "right hand", "right handtip", "right thumb", "left hip", "left knee", "left ankle", "left foot",
			 "right hip", "right knee", "right ankle", "right foot", "head", "nose", "left eye", "left ear","right eye", "right ear"]
    frame = {"pelvis":[], "spine - navel":[], "spine - chest":[], "neck":[], "left clavicle":[], "left shoulder":[], "left elbow":[],
                         "left wrist":[], "left hand":[], "left handtip":[], "left thumb":[], "right clavicle":[], "right shoulder":[], "right elbow":[],
                         "right wrist":[], "right hand":[], "right handtip":[], "right thumb":[], "left hip":[], "left knee":[], "left ankle":[], "left foot":[],
			 "right hip":[], "right knee":[], "right ankle":[], "right foot":[], "head":[], "nose":[], "left eye":[], "left ear":[],"right eye":[], "right ear":[]}
    
    def initialise():
        pass
    
    #Record Node Coordinates in JSON format (CURRENTLY DOESN'T WORK!)
    def save_to_json(data,file):
        save = json.dumps(data)
        file_path = os.getcwd() + "\Recordings\\" + str(file) + ".txt"
        with open(file_path, "at") as file:
            file.write(data)

    #Record Node Coordinates in binary format
    def save_to_bin(data,file):
        file_path = os.getcwd() + "\Recordings\\" + str(file) + ".pkl"
        with open(file_path,"wb") as file:
            pickle.dump(data,file)

    #Pack Data
    def pack_data(node,data):
        JointRecorder.frame[node].append(data)

    #Unpack and Return JSON Data
    def extract_json_data(file_path):
        data = []
        with open(file_path, "rt") as file:
            while True:
                line = file.readline()
                if line == "":
                    break
                else:
                    line = json.loads(line)
                    data.append(line)
                
        return data

    #Unpack and Return Binary Data
    def extract_bin_data(file_path):
        with open(file_path,"rb") as file:
            data = pickle.load(file)
        return data

    #Reset the dictionary holding the data from each frame
    #def reset_frame():
    #    JointRecorder.frame = {JointRecorder.K4ABT_JOINT_NAMES[i]:""} for i in range(0,len(K4ABT_JOINT_NAMES))

    #Refresh the Recorder when recording a new frame
    def refresh():
        pass

if __name__ == "__main__":
    print("This is a module for recording joint coordinates from the Azure Kinect Body Tracking SDK over time")
