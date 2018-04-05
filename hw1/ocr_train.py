import sys
import cv2, numpy as np

import image_resize 

img = cv2.imread('images/IwQY6.png')
img = image_resize.resize(img, width=600)

img1 = img.copy()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(3,3),0)
thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)

imx, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

samples =  np.empty((0,100))
responses = []
keys = [i for i in range(48,58)]

for cnt in contours:
  if cv2.contourArea(cnt)>50:
    [x,y,w,h] = cv2.boundingRect(cnt)
    if  h>28:
      cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
      roi = thresh[y:y+h,x:x+w]
      roistd = cv2.resize(roi,(10,10))

      cv2.imshow('norm',img)
      key = cv2.waitKey(0)

      if key == 27:  # (escape to quit)
        sys.exit()
      elif key in keys:
        responses.append(int(chr(key)))
        sample = roistd.reshape((1,100))
        samples = np.append(samples,sample,0)

responses = np.array(responses,np.float32)
responses = responses.reshape((responses.size,1))
print("training complete")

np.savetxt('samples.data',samples)
np.savetxt('responses.data',responses)



