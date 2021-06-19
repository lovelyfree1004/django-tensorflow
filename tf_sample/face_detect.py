import cv2

class FaceDetect(object):
    cascade = './data/haarcascade_frontalface_alt.xml'
    girl = './data/girl.jpg'

    def read_file(self):
        cascade = cv2.CascadeClassifier(self.cascade)
        img = cv2.imread(self.girl)
        face = cascade.detectMultiScale(img, minSize=(150, 150))
        if len(face) == 0:
            print('얼굴인식 실패')
            quit()

        for(x,y,w,h) in face:
            print(f'얼굴의 좌표 = {x}, {y}, {w}, {h}')
            red = (0,0,255)
            cv2.rectangle(img, (x, y), (x+w, y+h), red, thickness=20)
        cv2.imwrite('./saved-data/girl-face.png', img)
        cv2.imshow('./saved-data/girl-face', img)
        cv2.waitKey(0)
        cv2.destroyAllWindow()

if __name__ == '__main__':
    f = FaceDetect()
    f.read_file()

