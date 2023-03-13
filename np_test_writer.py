'''a program that writes an array of numbers to a text file in a nice format'''

import numpy as np
#define an array of 6 floating point x,y,z coordinates
coords = np.array([[1.04, 2.02, 3.10], [16.0, 17.407125, 18.0], [19.0, 20.11, 21.0], [22.0, 23.08, 24.08], [25.05, 26.04, 27.03], [28.0, 29.0, 30.0]])
#write the array to a text file
np.savetxt('coords.txt', coords, fmt='%.6f', delimiter=' ', newline='\n')

#'{0}, {1}, {2}'.format('a', 'b', 'c')
#need it to look like this: 
#  1: [(1.571, 1.571, 1), (1.571, 1.571, -1), (1.57, -1.57, 1), (1.57......
#  2: [(1.0, 1.9, 2), (3.7, 1.1, -1.2), (1.4........

frame = 254 #test frame number

a= str(coords)
print("a=str(coords)=  ", a)
#replace square brackets with parentheses
a = a.replace('[', '(')
a = a.replace(']', ')')
#replace spaces with commas
a = a.replace(' ', ',')
a = a.replace(',,', ',')
a = a.replace(',,', ',')
a = a.replace(',,', ',')
a = a.replace(',,', ',')
a = a.replace(',)', ')')
a = a.replace('((', 'zzzz: [(')
a = a.replace('))', ')]')

print("a (after replacements)=  ",a)