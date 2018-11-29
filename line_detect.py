import cv2
import numpy as np
import matplotlib
from matplotlib.pyplot import imshow
from matplotlib import pyplot as plt

# https://stackoverflow.com/questions/1585525/how-to-find-the-intersection-point-between-a-line-and-a-rectangle
# rectDims takes x1,y1,x2,y2
# lines is an array of array
# output: true if the rectangle dimensions intersect with a line
def isIntersect(line, minX, minY, maxX, maxY):
    for x1,y1,x2,y2 in line:
        if ((x1 <= minX and x2 <= minX) or \
            (y1 <= minY and y2 <= minY) or \
            (x1 >= maxX and x2 >= maxX) or \
            (y1 >= maxY and y2 >= maxY)):
            return False
        
        m = (y2 - y1) / (x2 - x1)
        
        y = m * (minX - x1) + y1
        if (y > minY and y < maxY): 
            return True
        y = m * (maxX - x1) + y1
        if (y > minY and y < maxY): 
            return True

        x = (minY - y1) / m + x1
        if (x > minX and x < maxX):
            return True

        x = (maxY - y1) / m + x1
        if (x > minX and x < maxX):
            return True
        
        return False

# This function finds the boundaries of a badminton court
def findBoundingBox(lines, width, height):
    minX = width
    minY = height
    maxX = 0
    maxY = 0
    for line in lines:
        for x1,y1,x2,y2 in line:
            if (x1 < minX):
                minX = x1
            if (x2 < minX):
                minX = x2
            if (y1 < minY):
                minY = y1
            if (y2 < minY):
                minY = y2

            if (x1 > maxX):
                maxX = x1
            if (x2 > maxX):
                maxX = x2
            if (y1 > maxY):
                maxY = y1
            if (y2 > maxY):
                maxY = y2

    return (minX, minY, maxX, maxY)

#white color mask
#img = cv2.imread('sample.png')
#img = cv2.imread('a.jpg')
#img = cv2.imread('b.jpg')
img = cv2.imread('rsz_b.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

kernel_size = 5
blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size), 0)

# the canny function is magical. see https://docs.opencv.org/3.1.0/da/d22/tutorial_py_canny.html
low_threshold = 50
high_threshold = 200
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 30  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 300  # minimum number of pixels making up a line
max_line_gap = 20  # maximum gap in pixels between connectable line segments
line_image = np.copy(img) * 0  # creating a blank to draw lines on

# Run Hough on edge detected image
# Output "lines" is an array containing endpoints of detected line segments
# array element is structed as x1,y1,x2,y2
lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)

for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)

# Draw a test rectangle down on the image
height, width, channels = line_image.shape
offset = 25
minX = width/2-offset
minY = height/2
maxX = width/2+offset
maxY = height/2+2*offset

# test rectangle to check for intersections
cv2.rectangle(line_image, (minX, minY), (maxX, maxY), (0,0,255), 10)

# Draw the court boundaries
height, width, channels = line_image.shape
(a,b,c,d) = findBoundingBox(lines, width, height)
print(a)
print(b)
print(c)
print(d)
cv2.rectangle(line_image, (a, b), (c, d), (0,255,0), 30)

# Draw the lines on the image
lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)

cv2.imwrite('sample_y.png', lines_edges)

for line in lines:
    if (isIntersect(line, minX, minY, maxX, maxY) == True):
        print("Intersection occurred")

