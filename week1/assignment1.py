import cv2
import numpy as np

image1 = cv2.imread("image1.jpeg")
image2 = cv2.imread("image2.jpeg")
image3 = cv2.imread("image3.jpeg")
image4 = cv2.imread("image4.jpeg")

collage_width = image1.shape[1] + image2.shape[1] + image3.shape[1] + image4.shape[1]
collage_image = np.zeros((200, collage_width , 3), dtype=np.uint8)

image1_resized = cv2.resize(image1, (image1.shape[1], 200))
image2_resized = cv2.resize(image2, (image2.shape[1], 200))
image3_resized = cv2.resize(image3, (image3.shape[1], 200))
image4_resized = cv2.resize(image4, (image4.shape[1], 200))

collage_image[:, :image1_resized.shape[1], :] = image1_resized
collage_image[:, image1_resized.shape[1]:image1_resized.shape[1]+image2_resized.shape[1], :] = image2_resized
collage_image[:, image1_resized.shape[1]+image2_resized.shape[1]:image1_resized.shape[1]+image2_resized.shape[1]+image3_resized.shape[1], :] = image3_resized
collage_image[:, image1_resized.shape[1]+image2_resized.shape[1]+image3_resized.shape[1]:, :] = image4_resized

cv2.imshow("Collage Image", collage_image)
cv2.waitKey(0)
