#Azure Kinect Body Tracking SDK Model Engine
#by Jason Xanthakis

#Must: Set Up Engine, Set Up Camera API, Access Data, Draw Nodes & Edges, Ensure Works & Updates DATE:13/10/2023
#Update1 --> Must: Draw Edges, Improve Camera, Improve Data Recording, Provide Greater Variety of Data DATE: 27/10/2023
#Milestone1 --> Completed: Draw Edges, Set Up Engine, Draw Nodes & Edges, Ensure Works & Updates DATE: 02/11/2023
#Update2 --> Must: Improve Camera, Improve Data Recording, Provide Greater Variety of Data DATE: 02/11/2023

from ursina import *

#Holds, Controls and Provides API for the Ursina object
class Model(object):
    K4ABT_JOINT_NAMES = ["pelvis", "spine - navel", "spine - chest", "neck", "left clavicle", "left shoulder", "left elbow",
			"left wrist", "left hand", "left handtip", "left thumb", "right clavicle", "right shoulder", "right elbow",
			"right wrist", "right hand", "right handtip", "right thumb", "left hip", "left knee", "left ankle", "left foot",
			"right hip", "right knee", "right ankle", "right foot", "head", "nose", "left eye", "left ear","right eye", "right ear"]
    K4ABT_JOINT_LINKS = {
                        "pelvis":False,
                        "spine - navel":"pelvis",
                        "spine - chest":"spine - navel",
                        "neck":"spine - chest",
                        "left clavicle":"spine - chest",
                        "left shoulder":"left clavicle",
                        "left elbow":"left shoulder",
			"left wrist":"left elbow",
                        "left hand":"left wrist",
                        "left handtip":"left hand",
                        "left thumb":"left wrist",
                        "right clavicle":"spine - chest",
                        "right shoulder":"right clavicle",
                        "right elbow":"right shoulder",
			"right wrist":"right elbow",
                        "right hand":"right wrist",
                        "right handtip":"right hand",
                        "right thumb":"right wrist",
                        "left hip":"pelvis",
                        "left knee":"left hip",
                        "left ankle":"left knee",
                        "left foot":"left ankle",
			"right hip":"pelvis",
                        "right knee":"right hip",
                        "right ankle":"right knee",
                        "right foot":"right ankle",
                        "head":"neck",
                        "nose":"head",
                        "left eye":"head",
                        "left ear":"head",
                        "right eye":"head",
                        "right ear":"head"
                        }
    joint_number = len(K4ABT_JOINT_NAMES)
    edge_number = 31

    joints = []
    edges = []
    
    def __init__(self,app):
        self.app = app
        #Entity(model='quad',scale=60,texture='white_cube',texture_scale=(60,60),
        #       rotation_x=90,y=-5,color=color.light_gray)   #Plane
        Entity(model='sphere',texture='sky_default',scale=10000,double_sided=True)
        
        self.camera = EditorCamera(enabled=True)
        self.init_camera()
        
        self.create_nodes()
        
        self.clear_data()

        #Testing Phase Code
        #coords = (0,0,0)
        #for i in range(0,Model.joint_number):
        #    self.coords.append(coords)

    def init_camera(self):
        self.cam_x = 0
        self.cam_y = -100
        self.cam_z = -1500
        self.camr_x = 0
        self.camr_y = 0
        self.camr_z = 0

    def control_camera(self):
        if held_keys['space']:
            self.cam_y += 20
        elif held_keys['left shift']:
            self.cam_y -= 20
        if held_keys['up arrow']:
            self.cam_z += 20
        elif held_keys['down arrow']:
            self.cam_z -= 20
        if held_keys['left arrow']:
            self.cam_x -= 10
        elif held_keys['right arrow']:
            self.cam_x += 20
        
        if held_keys['w']:
            self.camr_x -= 1
        elif held_keys['s']:
            self.camr_x += 1
        if held_keys['a']:
            self.camr_y -= 1
        elif held_keys['d']:
            self.camr_y += 1

    def sync_camera(self):
        self.cam_x = self.camera.position[0]
        self.cam_y = self.camera.position[1]
        self.cam_z = self.camera.position[2]
        self.camr_x = self.camera.rotation[0]
        self.camr_y = self.camera.rotation[1]
        self.camr_z = self.camera.rotation[2]

    def find_node(name):
        i = 0
        joint = False
        for i in range(0,len(Model.joints)):
            if Model.joints[i].name == name:
                joint = Model.joints[i]
                return joint

    def clear_data(self):
        self.coords = []

    def load_data(self,joint,coords):
        self.coords.append(coords)

    def create_nodes(self):
        for i in range(0,self.joint_number):
            self.joints.append(Node(Model.K4ABT_JOINT_NAMES[i],i))

        for i in range(0,self.joint_number-1):
            self.edges[i].second_init()

        #print_all(self.joints)

    def draw_nodes(self):
        for i in range(0,self.joint_number):
            coords = self.coords[i]
            self.joints[i].pos = (coords[0],coords[1],coords[2])
            self.joints[i].draw_node()

    def update(self):
        self.draw_nodes()

        self.sync_camera()
        self.control_camera()
        self.camera.position = (self.cam_x,self.cam_y,self.cam_z)
        self.camera.rotation = (self.camr_x,self.camr_y,self.camr_z)

    def input(self,key):
        if key=="q":
            exit()
        if key=="r":
            self.init_camera()
            self.camera.position = (self.cam_x,self.cam_y,self.cam_z)
            self.camera.rotation = (self.camr_x,self.camr_y,self.camr_z)

#Draws Nodes/Joints
class Node(object):
    def __init__(self,name,num):
        self.name = name
        self.id = num
        
        self.parent = Model.K4ABT_JOINT_LINKS[self.name]
        if self.parent:
            self.edge = Edge(self.name,self.parent)
            Model.edges.append(self.edge)

        self.pos = (0,0,0)
        self.entity = Entity(model='sphere',scale=10,color=color.blue,position=self.pos)

    def draw_node(self):
        self.entity.position = self.pos
        if self.parent:
            self.edge.draw_edge()

#Draws Edges
class Edge(object):
    def __init__(self,name,parent):
        self.parent = parent
        self.child = name
        self.entity = Entity(model=Pipe(base_shape=Quad,origin=(0,0),path=((0,0,0),(0,0,0)),thicknesses=((1,1),),cap_ends=True),double_sided=False)

    def second_init(self):
        self.parent_obj = Model.find_node(self.parent)
        self.child_obj = Model.find_node(self.child)

    def draw_edge(self):
        path = (tuple(self.parent_obj.pos),tuple(self.child_obj.pos))
        self.entity.model.path = path
        self.entity.model.generate()

#Ursina Update Function
def update():
    model.update()

#Ursina Keyboard Input Function
def input(key):
    model.input(key)

#Print the Name of all Objects in an Iterable Object Into the Shell
def print_all(l):
    for obj in l:
        print(obj.name)

if __name__ == '__main__':
    print("Running demo model.")

    app = Ursina()
    model = Model(app)
    
    while True:
        model.app.step()
