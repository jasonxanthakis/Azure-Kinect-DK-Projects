#Extract & Output Joint Data
#by Jason Xanthakis

import pykinect_azure as pykinect

#Goes through all joints present in a body tracker present in a frame every time it's called
def print_all_joints(body_id):
    K4ABT_JOINT_NAMES = ["pelvis", "spine - navel", "spine - chest", "neck", "left clavicle", "left shoulder", "left elbow",
                         "left wrist", "left hand", "left handtip", "left thumb", "right clavicle", "right shoulder", "right elbow",
                         "right wrist", "right hand", "right handtip", "right thumb", "left hip", "left knee", "left ankle", "left foot",
			 "right hip", "right knee", "right ankle", "right foot", "head", "nose", "left eye", "left ear","right eye", "right ear"]
    
    #Loop through each joint
    body_3d = body_frame.get_body(body_id)
    for joint_id in range(pykinect.K4ABT_JOINT_COUNT):
        joint = body_3d.joints[joint_id].numpy()
        print(f'{K4ABT_JOINT_NAMES[joint_id].capitalize()}:\n{joint}\n')
		
        joint_coords = joint[0:3]
        #print(joint_coords)

if __name__ == "__main__":
    #Initialize the library, if the library is not found, add the library path as argument
    pykinect.initialize_libraries(track_body=True)

    #Modify camera configuration
    device_config = pykinect.default_configuration
    device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_OFF
    device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED

    #Start device
    device = pykinect.start_device(config=device_config)
	
    #Start body tracker
    bodyTracker = pykinect.start_body_tracker()

    #Main Event Loop
    while True:
        # Get capture
        capture = device.update()

        #Get body tracker frame
        body_frame = bodyTracker.update()

        #Get the color depth image from the capture
        ret_depth, depth_color_image = capture.get_colored_depth_image()

        #Get the colored body segmentation
        ret_color, body_image_color = body_frame.get_segmentation_image()

        if not ret_depth or not ret_color:
            continue

        #Loop through each body frame
        for body_id in range(body_frame.get_num_bodies()):
            print_all_joints(body_id)
