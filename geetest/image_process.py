import cv2 as cv

# one pic about 250 * 150
img = cv.imread('pic.png')
info = img.shape
height = info[0]
width = info[1]
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

count = 0
gap = 0
stop = 0
line = 0


def is_yellow(a, b):
    if (hsv[a,b]>= [26,43,46]).all() and (hsv[a,b] <= [34,255,255]).all():
        return True
    else:
        return False



for i in range(height):
    count = 0
    for j in range(width):
        if is_yellow(i,j):
            count += 1
        else:
            count = 0

        if count == 36:
            if is_yellow(i+38,j) or is_yellow(i-35,j):
                line = i
                print('line ' + str(line))
                print('column ' + str(j-count))
                stop = 1
                break

    if stop == 1:
        break

count = 0
stop = 0

for e in range(width):
    if hsv[line,e][2] <= 150:
        count += 1
    else:
        count = 0

    if count == 36:
        print('e ' + str(e) + ' count '+ str(count) + ' gap ' + str(gap))
        print('match found: ' + str(e-count))
        stop = 1
        break

    i += 1
    if stop == 1:
        break
