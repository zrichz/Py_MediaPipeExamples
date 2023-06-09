'''ingests a video file and output **478** xyz face landmarks per frame to a csv-type file'''

'''
note: the Face Mesh data contains 468 (0-467) face landmarks as per the published canonical face model,
**BUT** also an *additional* 10 xyz coords - these are five per eye (iris), such that
index 468 is the centre of the character's right eye (468-472)
index 473 is the centre of the character's left eye (473-477)

so:
****************************************
***** 478 (0-477) points per frame  ****
****************************************
'''

import cv2
import csv
import numpy as np
import math
import mediapipe as mp

print("## begin prog #####")    
print("####################")

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

#create a NEW placeholder csv file which will later be used to APPEND face landmarks 
csvfilename="migraine" #used later to save csv data

with open(csvfilename+'.csv', mode='w', newline='\n') as landmark_file:
	landmark_writer = csv.writer(landmark_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')
	landmark_writer.writerow('#') #write one line of comment (note we can hopefully skip this header row on re-import)...

# For video file input:
frame=0
# example files are in the 'examples' subfolder: migraine.mp4 (full HD), newsreader.mp4 and men.mp4
cap = cv2.VideoCapture("examples/migraine.mp4")

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
      
      with open(csvfilename+'.csv', mode='a', newline='\n') as landmark_file:
        landmark_writer = csv.writer(landmark_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        point=0
        for lm in face_landmarks.landmark:
          # note I am rounding here, but you don't have to
          # try and write the frame and the landmark number, as well as the xyz co-ords...
          # ideally it should look like this:
          # 1: [(1.571, 1.571, 1), (1.571, 1.571, -1), (1.57, -1.57, 1), (1.57, -1.57, -1).......
          #can't use lm (it's not an iterator) - need to use manual iterator ('point')
          # using writerow generates many rows per frame - this may/may not be a problem
          if point==0: #first landmark in the list
                # use 'frame+1' below, as the first frame is 0, but we want to start at 1
                # the twelve leading spaces are needed to align the data correctly
                landmark_writer.writerow(["            "+str(frame+1)+": [("+str(round(lm.x,7))+", "+str(round(lm.y,7))+", "+str(round(lm.z,7))+")"])
          elif point==477: #last landmark in the list
                landmark_writer.writerow([", ("+str(round(lm.x,7))+", "+str(round(lm.y,7))+", "+str(round(lm.z,7))+")]\n"])
          else: #all intermediate landmarks
                landmark_writer.writerow([", ("+str(round(lm.x,7))+", "+str(round(lm.y,7))+", "+str(round(lm.z,7))+")"])
          point+=1
  
#     ==========still within the frame loop here=======================
    # for visualisation purposes only, Draw the face mesh on the video.
    # TRY ONLY EVERY n FRAMES FOR SPEED
    if (frame%10) == 0:
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
landmark_file.close()    # close the csv file
# the main frame loop ends here
# ================================
# =============================
# ==========================

print("last frame in the movie was (or is this off by one?): ",frame)

# at this point, we have written a .csv file of the raw-ish xyz co-ords
# We now need to create a .usda file, using boilerplate from a 'template.usda' file, and the new csv xyz data

#open "template.usda" and read it into a variable called "template"
#this contains the boilerplate
with open("template.usda", "r") as f_template:
    template = f_template.read()
print("### USDA template file opened successfully ###")

with open(csvfilename+".csv", "r") as f_csv:
    xyzcsv = f_csv.read()
print("### csv file opened successfully ###")

# #############################\
# ####                       ###\
# ####  USDA FILE CREATION    ###\
# ####                         ###\
# ################################/

#import data from the initial csv file in order to reformat it to the usda standard
# will need the actual last frame (remember frame in the data starts at 0)

# search template file for the end timecode string and alter it to show actual last frame,
# then write the new string to a new file called '<csvfilename>.usda'
with open(csvfilename+".usda", "w") as f_new_usda:               # create a new *USDA* file for writing
    for line in template.splitlines():                  # search the *TEMPLATE* file for the endTimeCode string
        if "endTimeCode =" in line:
            f_new_usda.write("    endTimeCode = " + str(frame)) # write the actual last frame into the *USDA* file (initial spaces are important)
        elif "1: [(1.571" in line: #effectively remove the three example 'timeSamples' lines, by locating the first few characters of each
            f_new_usda.write("#")
        elif "2: [(1.35" in line:
            f_new_usda.write("#")
        elif "3: [(0.19" in line:
            f_new_usda.write("#")
        elif "point3f[] points.timeSamples = {" in line:
            f_new_usda.write(line + "\n") #write the above-found line unchanged...
            # NOW WRITE ALL THE CSV DATA (initial spaces are important)
            for original_line in xyzcsv.splitlines(): #'csvfilename.csv'
                 #write the csv data here
                 f_new_usda.write(original_line + "")
                 #f_new_usda.write(original_line + "\n") # maybe don't use the \n here?
            
        else:
            f_new_usda.write(line + "\n") #write all other lines "as is"

# housekeeping:
f_new_usda.close()       # close the usda file
f_template.close()       # close the template file
f_csv.close()            # close the csv file
print("======= finished writing the filled in .usda file  ========")

print("about to remove all double-quotes from the .usda file")
# re-open .usda file and remove all double-quotes
with open(csvfilename+".usda", "w") as f_usda:               # open *USDA* file for writing
    for line in template.splitlines():                       # search for double-quotes
        if '""' in line:                                     # if double-quotes are found
            line.replace('""',"")                            # remove double-quotes
            f_usda.write(line + "\n")                        # write the revised line to the *USDA* file
        else:
            f_usda.write(line + "\n")                        # write all other lines "as is"    

f_usda.close() #close the usda file
print("======= finished removing all double-quotes from the .usda file  ========")

# END of main program
# ###################

#=================================================================================================================
#=================================================================================================================
#=================================================================================================================
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
        # *****note*****
        # below examples are truncated, but 'template.usda' has FULL lists for vertex counts and edges etc
        #
        # The Canonical vertex counts, vertex indices, and dummy points in next 3 lines
        # shouldn't need to alter these from the actual template values
        # (I think 'point3f[] points are superseded by the 'points.timeSamples' below)
        int[] faceVertexCounts = [3, 3, 3, 3,....... 3, 3, 3]
        int[] faceVertexIndices = [173, 155, 133, 246......324, 191, 95, 80]
        point3f[] points = [(0, -3.4064123, 5.977), (0, -1.12, 7.4), ...... (4.53, 2.91, 3.339685)]

        # the below timesamples will need to be replaced...
        # =================================================
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
