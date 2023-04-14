import cv2

fileName = 'testImg.png'
markLineWeight = 2
markLineColor = (255,0,0)

def main():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + \
                                         'haarcascade_frontalface_default.xml')
    img = cv2.imread(fileName)
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(imgGray,\
                                          scaleFactor =1.3,\
                                          minNeighbors = 5  )
    for (x,y,w,h) in faces:
        img = cv2.rectangle(img,(x,y),(x + w,y + h),markLineColor,markLineWeight)
    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()