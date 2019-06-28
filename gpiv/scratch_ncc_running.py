from piv_option import get_image_arrays
import numpy as np
import matplotlib.pyplot as plt
import json
import time

tptSize = 32
rowStart = 400
colStart = 400

# image and template
fromHeight, fromError, toHeight, toError, transform = get_image_arrays()
tpt = fromHeight[rowStart+1:rowStart+1+tptSize,colStart+1:colStart+1+tptSize]
img = toHeight[rowStart:rowStart+tptSize+2,colStart:colStart+tptSize+2]
# tpt = fromHeight[int(rowStart+tptSize*0.5):int(rowStart+tptSize*1.5),int(colStart+tptSize*0.5):int(colStart+tptSize*1.5)]
# img = toHeight[rowStart:rowStart+tptSize*2,colStart:colStart+tptSize*2]

#################
# running sums and squares NCC
#################

# running sum and square
t0 = time.time()
for i in range(1000):
    s = np.zeros((img.shape[0]+1, img.shape[1]+1))
    s2 = s.copy()
    for u in range(1,img.shape[1]+1): # columns
        for v in range(1,img.shape[0]+1): # rows
            s[u,v] = img[u-1,v-1] + s[u-1,v] + s[u,v-1] - s[u-1,v-1]
            s2[u,v] = img[u-1,v-1]**2 + s2[u-1,v] + s2[u,v-1] - s2[u-1,v-1]

    tptZeroMean = tpt  - np.mean(tpt)
    tptZeroMeanSquareSum = np.sum(tptZeroMean**2)
    N = tpt.shape[0]
    M = img.shape[0]

    ncc = np.zeros((M-N+1,M-N+1))
    for u in range(M-N+1):
        for v in range (M-N+1):
            imgSum = s[u+N,v+N] - s[u,v+N] - s[u+N,v] + s[u,v]
            fBarUv = imgSum / (N*N)
            numerator = np.sum((img[u:u+N,v:v+N]-fBarUv) * tptZeroMean)
            denominator = np.sqrt(((s2[u+N,v+N] - s2[u,v+N] - s2[u+N,v] + s2[u,v]) - imgSum**2 / (N*N)) * tptZeroMeanSquareSum)
            ncc[u,v] = numerator / denominator
        
t1 = time.time()
print(t1-t0)

# f, axs = plt.subplots(1, 3, gridspec_kw={'width_ratios':[1,1,2]})
# axs[0].imshow(ncc, cmap='gray')
# axs[0].set_title('NCC Running Sum')
# axs[1].imshow(tpt, cmap='gray')
# axs[1].set_title('Template')
# axs[2].imshow(img, cmap='gray')
# axs[2].set_title('Image')
# plt.show()

# # image energy and sum under the template
# imgE = np.zeros((img.shape[0], img.shape[1]))
# imgS = imgE.copy()
# N = tptSize
# for u in range(1,img.shape[1]-tptSize+1):
#     for v in range(1,img.shape[0]-tptSize+1):
#         imgE[u-1,v-1] = s2[u+N-1,v+N-1] - s2[u-1,v+N-1] - s2[u+N-1,v-1] + s2[u-1,v-1]
#         imgS[u-1,v-1] = s[u+N-1,v+N-1] - s[u-1,v+N-1] - s[u+N-1,v-1] + s[u-1,v-1]

# # ncc
# tptMR = tpt - np.mean(tpt)
# tptD = np.sum(tptMR*tptMR)
# nccFast = np.zeros((img.shape[1]-tptSize+1,img.shape[1]-tptSize+1))
# for u in range(img.shape[1]-tptSize+1):
#     for v in range(img.shape[0]-tptSize+1):
#         imgSub = img[v:v+tptSize,u:u+tptSize]
#         numerator = np.sum(imgSub*tptMR)
#         fbar = imgS[u,v]/(N*N)
#         denominator = np.sqrt((imgE[u,v] - 2*fbar*imgS[u,v] + fbar**2)*tptD)
#         nccFast[u,v] = numerator / denominator

