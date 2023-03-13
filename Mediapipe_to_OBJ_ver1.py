'''ingests a video file and output 480 xyz face landmarks per frame to a csv-type file'''

'''
note: the Face Mesh data contains 468 (0-467) face landmarks as per the published canonical face model,
but also an *additional* 10 xyz coords - these are five per eye (iris), such that
index 468 is the centre of the character's right eye (468-472)
index 473 is the centre of the character's left eye (473-477)
'''
import cv2
import csv
import numpy as np
import math
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

#create a NEW placeholder csv file which will later be used to APPEND face landmarks 
csvfilename="businesswoman" #used later to save csv data

with open(csvfilename+'.csv', mode='w', newline='') as landmark_file:
						landmark_writer = csv.writer(landmark_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
						landmark_writer.writerow('#test comment') #write one line of comment...

# For video file input:
frame=0
#cap = cv2.VideoCapture("examples/newsreader.mp4")
cap = cv2.VideoCapture("examples/businesswoman.mp4")

with mp_face_mesh.FaceMesh(
    max_num_faces=2,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("end of video!")
      break

    # To improve performance, optionally mark the image as not writeable to pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)
    
    # results.multi_face_landmarks contains the x,y,z co-ords for the mesh
    # save this per frame as below
    # Write XYZ landmark values into a csv file
    # (note mode 'a' means we are APPENDING this data to the existing placeholder file)
    for face_landmarks in results.multi_face_landmarks:
      
      with open(csvfilename+'.csv', mode='a', newline='') as landmark_file:
        landmark_writer = csv.writer(landmark_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        point=0
        for lm in face_landmarks.landmark:
          # note I am rounding here, but you don't have to
          # try and write the frame and the landmark number, as well as the xyz co-ords...
          landmark_writer.writerow([frame,point, round(lm.x,7), round(lm.y,7), round(lm.z,7)])
          point+=1
  

#=================================================================================================================
    # for visualisation purposes only, Draw the face mesh on the video.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())
    
    cv2.imshow('MediaPipe Face Mesh', image)
    
    frame+=1 #increase frame index. NOTE: careful with correct indentation!

    if cv2.waitKey(5) & 0xFF == 27: #ESC key will stop programme
      break

cap.release()

print("last frame in the movie was (or is this off by one?): ",frame)

# so, once we've written out the raw-ish xyz co-ords, we now need
# to import a base .usda file, and amend it / append
# the actual xyz points in the correct format! simples!

#open a template file called "template.usda" and read it into a variable called "template"
with open("template.usda", "r") as f:
    template = f.read()

#import data from a csv file to a numpy array
data=np.genfromtxt(csvfilename+'.csv', delimiter=',', skip_header=1)

print("original csv file data shape : ", data.shape)
# so, data.shape is (number of frames, number of landmarks, 3)
# get and print the value of frame in the last row of data
frame = int(data[-1][0])
print ("last frame=",frame)

np.delete(data, [0,1], axis=1) #delete the first two columns of data (frame and landmark number)

# reshape the data into <frame> rows by 480 columns of x,y,z co-ords
data=data.reshape(int(frame),480*3)
print("reshaped data: ", data.shape)
print ("example first few rows of data:")

for a in range(0,5):
      print("frame ",a,": ", data[a])


'''
# search template for a string and replace it
# then write the new string to a new file called '<csvfilename>.usda'
with open(csvfilename+".usda", "w") as f:
    for line in template.splitlines():
        if "endTimeCode = 5" in line:
            f.write("endTimeCode = " + frame + "")
        else:
            f.write(line + "")
'''

#=================================================================================================================
'''here is the format of 'template.usda':
#usda 1.0
(
    doc = "Blender v3.4.1"
    endTimeCode = 5              <--- this will need to be changed to the number of frames in the video
    metersPerUnit = 1            <--- this may need to be scaled
    startTimeCode = 1
    timeCodesPerSecond = 24      <--- this may need to be changed to the fps of the video
    upAxis = "Z"
)

def Xform "FaceMesh"
{
    def Mesh "FaceMesh"
    {
        uniform bool doubleSided = 1
        # canonical vertex counts, vertex indices, and dummy points in next 3 lines
        # shouldn't need to alter these from the template values
        # (I think 'point3f[] points are superseded by the 'points.timeSamples' below)
        int[] faceVertexCounts = [3, 3, 3, 3,....... 3, 3, 3, 3, 3, 3]
        int[] faceVertexIndices = [173, 155, 133, 246, 33, 7, 382, 398, 362, 263......324, 191, 95, 80]
        point3f[] points = [(0, -3.406404, 5.979507), (0, -1.126865, 7.475604), ...... (4.53, 2.91, 3.339685)]

        # the below timesamples will need to be replaced...
        point3f[] points.timeSamples = {
            1: [(1.571, 1.571, 1), (1.571, 1.571, -1), (1.57, -1.57, 1), (1.57, -1.57, -1), (-1.57, 1.57, 1), (-1.5, 1.57, -1), (-1.5, -1.57, 1), (-1.57, -1.57, -1)],
            2: [(1.35, 1.35, 1), (1.35, 1.35, -1), (1.35, -1.35, 1), (1.35, -1.35, -1), (-1.35, 1.35, 1), (-1.35, 1.35, -1), (-1.35, -1.35, 1), (-1.35, -1.35, -1)],
            3: [(x,y,z), (x,y,z), (.......)],
        }
        #the below UV mappings should not require alteration
        texCoord2f[] primvars:UVMap = [(0.40, 0.62), (0.41, 0.60), .......(0.41, 0.30), (0.43, 0.30)] (
            interpolation = "faceVarying"
        )
        uniform token subdivisionScheme = "none"
    }
}

'''
