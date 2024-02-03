#Check Pickle Object Contents

import nodeCoordinateRecorder as r

if __name__ == "__main__":
    data = r.JointRecorder.extract_bin_data("")
    print(data)
    print(type(data))

    print("\n\n")
    for i in range(0,len(r.JointRecorder.K4ABT_JOINT_NAMES)):
        line = data[r.JointRecorder.K4ABT_JOINT_NAMES[i]]
        joint_coords = line[0]
        print(data[r.JointRecorder.K4ABT_JOINT_NAMES[i]])
        print((joint_coords[0],joint_coords[1],joint_coords[2]))
        print("\n")
