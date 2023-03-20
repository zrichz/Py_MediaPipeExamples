'''a program that writes an array of numbers to a text file in a nice format'''

import numpy as np
#define a random 300x479x3 array of numbers
#coords = np.array([[1.04, 2.02, 3.10], [-16.0, 17.407125, -18.0], [1, -2.005, -1.001], [22, 23, 24], [5,6,7], [28.0, 29.0, 30.0]])
coords = np.random.rand(300,479,3)
print (coords.shape)

#======================================
#write the array to a text file. must be a 1D or 2D array, NOT 3D, so need to reshape the array to 2D
coords = coords.reshape(300,479*3)
print("reshaped array= ",coords.shape)

np.savetxt('coords.txt', coords, fmt='%+0.6f', delimiter=',', newline='\n')
print("SAVED coords.txt")

#open coords.txt using numpy
loadedArray = np.loadtxt('coords.txt', dtype=str, delimiter=',', skiprows=0) 
print("LOADED coords.txt")

#read the file into a string
#loadedArray = np.read()
#iterate through each row of the array

for i in range(0, 300): 
    rowString=str(loadedArray[i])
    print("i= ",i,"     rowString= ",rowString)
    print("rowString length= ",len(rowString))
    rowString = rowString.replace("'", "") #strip all single quotes from the string
    rowString = rowString.replace(" ", ', ') #replace spaces with commas
    rowString = rowString.replace('[', '(')  #replace square brackets with parentheses
    rowString = rowString.replace(']', ')')
    rowString = str(i+1)+": ["+rowString
    print("rowString (after manipulation)= ",rowString)
    print(" ")


#need it to look like this for .usda file: 
#  1: [(1.571, 1.571, 1), (5, 5, 1), (7, 7, 4), (1.57......
#  2: [(1.0, 1.9, 2), (3.7, 1.1, -1.2), (1.4........
