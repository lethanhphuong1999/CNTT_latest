import numpy as np
import cv2
import glob

cap = cv2.VideoCapture(0)

images = glob.glob('*.PNG') #all the jpg images in the folder could be displayed
currentImage=0  #the first image is selected

replaceImg=cv2.imread(images[currentImage])
rows,cols,ch = replaceImg.shape
pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])    #this points are necesary for the transformation

zoomLevel = 0   #when zoomLevel is positive it zooms in, when its negative it zooms out
processing = True   #boolean variable using for disabling the image processing
maskThreshold=10

while(True):
    # Capture frame-by-frame
    ret, img = cap.read()
    # Our operations on the frame come here
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #This function is used to detect the corners of the chessboard, 9x6 is the number of corners to find
    ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

    # If found, do the processing
    if ret == True and processing:
        #pts2 is used for defining the perspective transform
        pts2 = np.float32([corners[0,0],corners[8,0],corners[len(corners)-1,0],corners[len(corners)-9,0]])
        #compute the transform matrix
        M = cv2.getPerspectiveTransform(pts1,pts2)
        rows,cols,ch = img.shape
        #make the perspective change in a image of the size of the camera input
        dst = cv2.warpPerspective(replaceImg,M,(cols,rows))
        #A mask is created for adding the two images
        #maskThreshold is a variable because that allows to substract the black background from different images
        ret, mask = cv2.threshold(cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY),maskThreshold, 1, cv2.THRESH_BINARY_INV)     
        #Erode and dilate are used to delete the noise
        mask = cv2.erode(mask,(3,3))
        mask = cv2.dilate(mask,(3,3))         
        #The two images are added using the mask
        for c in range(0,3):
            img[:, :, c] = dst[:,:,c]*(1-mask[:,:]) + img[:,:,c]*mask[:,:]
#        cv2.imshow('mask',mask*255)
     #finally the result is presented
    cv2.imshow('img',img)
       
    #Wait for the key 
    key = cv2.waitKey(1)
#    print key
    #decide the action based on the key value (quit, zoom, change image)
    if key == ord('q'): # quit
        print ('Thoát')
        break
    if key == ord('p'): # processing
        processing = not processing
        if processing: 
            print ('Kích hoạt xử lý ảnh')
        else: 
            print ('Hủy xử lý ảnh')
    if key == 43: # + zoom in
        zoomLevel=zoomLevel+0.05
        rows,cols,ch = replaceImg.shape
        pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])
        pts1 = pts1 + np.float32([[zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,-zoomLevel*rows],[zoomLevel*cols,-zoomLevel*rows]])
        print ('Phóng to')
    if key == 45: # - zoom out
        zoomLevel=zoomLevel-0.05
        rows,cols,ch = replaceImg.shape
        pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])
        pts1 = pts1 + np.float32([[zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,-zoomLevel*rows],[zoomLevel*cols,-zoomLevel*rows]])
        print ('Thu nhỏ')
    if key ==  ord('a'):# -> next image
        if currentImage<len(images)-1:
            currentImage=currentImage+1
            replaceImg=cv2.imread(images[currentImage])
            rows,cols,ch = replaceImg.shape
            pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])
            pts1 = pts1 + np.float32([[zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,-zoomLevel*rows],[zoomLevel*cols,-zoomLevel*rows]])
            print ('ảnh tiếp theo')
        else:
            print ('Không có thêm hình ảnh bên phải')
    if key == ord('s'): # <- previous image
        if currentImage>0:
            currentImage=currentImage-1
            replaceImg=cv2.imread(images[currentImage])
            rows,cols,ch = replaceImg.shape
            pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])
            pts1 = pts1 + np.float32([[zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,zoomLevel*rows],[-zoomLevel*cols,-zoomLevel*rows],[zoomLevel*cols,-zoomLevel*rows]])

            print ('ảnh trước đó')
        else:
            print ('Không có thêm hình ảnh bên trái')
            
    if key == ord('d'): # increase threshold
        if maskThreshold<255:
            maskThreshold=maskThreshold+1
            print ('Tăng ngưỡng')
        else:
            print ('Ngưỡng ở giá trị maximun')
    if key == ord('f'): # decrease threshold
        if maskThreshold>0:
            maskThreshold=maskThreshold-1
            print ('Giảm ngưỡng')
        else:
            print ('Ngưỡng ở giá trị minimun')
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
