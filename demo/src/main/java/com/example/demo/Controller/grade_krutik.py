# -*- coding: utf-8 -*-
# from signal import signal
# from curses import window
#from itertools import accumulate
from PIL import Image
from PIL import ImageFilter
import sys
#import random
import numpy as np
from scipy import ndimage #, signal, fftpack
from scipy.signal import fftconvolve
#from numpy import fft


#im = Image.open(sys.argv[1]).convert('L')

im = Image.open("D:\\IUB course\\temp\\spring-python\\demo\\images\\image.jpg").convert('L')

# convert to numpy array
im_arr = np.array(im)
# get rows and column length
column_len = len(im_arr)
row_len = len(im_arr[0])






# # gaussian filter
def gaussian(img):
      blured_image = ndimage.gaussian_filter(im_arr,2)
      return blured_image





# # sobel filter
def sobel(blured_image):
      sobel_filter_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])/8
      sobel_filter_y = np.array([[1, 2, 1],[0, 0, 0],[-1, -2, -1]])/8


      x = fftconvolve(blured_image,sobel_filter_x)
      y = fftconvolve(blured_image,sobel_filter_y)
      


      sobel = np.sqrt(np.square(x) + np.square(y))


      return sobel,x,y



# non-max suppression.
def non_max(sobel,x,y):
      # Referance: https://towardsdatascience.com/canny-edge-detection-step-by-step-in-python-computer-vision-b49c3a2d8123
      # https://www.youtube.com/watch?v=9cpTmJCsI0M
      
      gradient_direction = np.rad2deg(np.arctan2(y, x))
      gradient_direction[gradient_direction < 0] += 180 # make every direction positive

      gradient_magnitude = sobel

      non_max = np.zeros(gradient_magnitude.shape)


      for i in range(1,len(gradient_magnitude)-1,1):
            for j in range(1,len(gradient_magnitude[1])-1,1):
                  q = 255
                  r = 255
                  
                  #angle 0
                  if (0 <= gradient_direction[i,j] < 22.5) or (157.5 <= gradient_direction[i,j] <= 180):
                        q = gradient_magnitude[i, j+1]
                        r = gradient_magnitude[i, j-1]
                  #angle 45
                  elif (22.5 <= gradient_direction[i,j] < 67.5):
                        q = gradient_magnitude[i-1, j-1]
                        r = gradient_magnitude[i+1, j+1]
                  #angle 90
                  elif (67.5 <= gradient_direction[i,j] < 112.5):
                        q = gradient_magnitude[i+1, j]
                        r = gradient_magnitude[i-1, j]
                  #angle 135
                  elif (112.5 <= gradient_direction[i,j] < 157.5):
                        q = gradient_magnitude[i+1, j-1]
                        r = gradient_magnitude[i-1, j+1]

                  if (gradient_magnitude[i,j] >= q) and (gradient_magnitude[i,j] >= r):
                        non_max[i,j] = gradient_magnitude[i,j]
                  else:
                        non_max[i,j] = 0



      


      non_max[non_max > 20] = 255
      canny = np.zeros(non_max.shape)

      # hysteresis
      for i in range(1,len(non_max)-1,1):
            for j in range(1,len(non_max[0])-1,1):
                  if non_max[i][j] == 255:
                        canny[i][j] = 255
                        continue
                  elif non_max[i][j] == 0:
                        continue
                  else:
                        if non_max[i-1][j] == 255 or non_max[i-1][j-1] == 255 or non_max[i-1][j+1] == 255 or non_max[i+1][j] == 255 or non_max[i+1][j+1] == 255 or non_max[i+1][j-1] == 255 or non_max[i][j+1] == 255 or non_max[i][j-1] == 255:
                              canny[i][j] = 255
            
      return canny

def canny():
      
      canny_im = im.filter(ImageFilter.Kernel((3, 3), (-1, -1, -1, -1, 8, -1, -1, -1, -1), 1, 0)).convert('L') #Laplacian kernel
      
      
      canny = np.array(canny_im)
      return canny








def hough(im_arr):
      
            
      # Hough transform
      # Reference: https://alyssaq.github.io/2014/understanding-hough-transform/#Extras
      thetas = np.deg2rad(np.arange(-90, 90))
      im_height, im_width = im_arr.shape

      # create max distance (diagonal)
      max_dist = np.ceil(np.sqrt(im_width * im_width + im_height * im_height))   
      max_dist_int = int(max_dist) # 2781

      # steps creation from max distance
      rhos = np.linspace(-max_dist_int, max_dist_int, max_dist_int * 2) #shape (5562,)
      

      # hough equation: ρ = x cos θ + y sin θ
      cos_thetas = np.cos(thetas)
      sin_thetas = np.sin(thetas)

      # hough accumulater, value of rho and the thetas (angles to search)
      accumulator = np.zeros((2*max_dist_int, len(thetas)))  # shape (5562,179)


      y_index, x_index = np.nonzero(im_arr)  # len is 3602745

      # xcos 0
      xcost = np.round(np.dot(x_index.reshape((-1,1)),cos_thetas.reshape((1,-1))))
      # ysin 0
      ycost = np.round(np.dot(y_index.reshape((-1,1)),sin_thetas.reshape((1,-1))))
      


      # ρ = x cos θ + y sin θ
      rhos_matrix = xcost + ycost + max_dist_int # adding max_dist ensure positive values
      rhos_matrix  = rhos_matrix.astype(int) # shape (3602745, 40)

      for i in range(len(thetas)):
            rho,counts = np.unique(rhos_matrix[:,i], return_counts=True)
            accumulator[rho,i] = counts # shape (5562, 40)
      
  
      return accumulator, rhos, thetas
            


# Find peaks:
def hough_peak(accumulator, neighbor):
      acc_copy = accumulator.copy()
      indicies = []
      
      for i in range(len(accumulator)):       # number of peak values
            
            ## next two line of code were taken from saumya metha:
            idx = np.argmax(acc_copy) # find argmax in flattened array
            H1_idx = np.unravel_index(idx, acc_copy.shape) # (y,x)
            ## saumya's code end.
            
            
            
            
            indicies.append(H1_idx)
            
            
            x_max = H1_idx[1] + neighbor
            y_max = H1_idx[0] + neighbor
            
            x_min = H1_idx[1] - neighbor
            y_min = H1_idx[0] - neighbor
            
            
            # edge cases
            if x_max > len(acc_copy[1]):
                  x_max = len(acc_copy[1])-1
            if x_min < 0:
                  x_min = 0
            if y_min < 0:
                  y_min = 0
            if y_max > len(acc_copy):
                  y_max = len(acc_copy)-1
                  
            # change the block around the max value to zero.
            for x in range(x_min, x_max,1):
                  for y in range(y_min, y_max,1):
                        
                        acc_copy[y][x] = 0      
            acc_copy[H1_idx[0]][H1_idx[1]] = 0
            
      return indicies



def plot_hough_lines(indicies, rhos, thetas):   # indicies (r,0)
      # referance: https://stackoverflow.com/questions/51009135/how-do-i-transform-the-values-of-an-accumulator-hough-transformation-back-to-a
      img_copy = im_arr.copy()
      
      
      x_points = []
      y_points = []
      for i in range(len(indicies)):
                  
            rho = rhos[indicies[i][0]]
            theta = thetas[indicies[i][1]]
            a = np.cos(theta)
            b = np.sin(theta)
            
            
            # get the point on the line.  c == (rho* cos 0, rho* sin 0) == (x,y),  where c is the point where line intersects perpendicular from the origin with angle 0.
            x = a*rho  
            y = b*rho 
            
            
            p1 = (int(x + (-b)), int(y + (a)))
            
            
            # multiply by large value to get distant points so that we can plot a line across the image.
            point11 = (int(x + 3000*(-b)), int(y + 3000*(a)))
            point21 = (int(x - 3000*(-b)), int(y - 3000*(a)))
           
            # convert radian to degree. As we were using theta in radian.
            theta_degree = np.abs(np.round(np.rad2deg(theta)))
            
            
            # we only want horizontal and vertical lines.
            if ((theta_degree == 0) or (theta_degree == 90)):
                  
                  # store the points of each line in x-axis and y-axis.
                  if theta_degree == 0:
                        x_points.append(p1[0])
                  if theta_degree == 90:
                        y_points.append(p1[1])
                  
      
      
      # add the edge points.
      if len(im_arr[1]) not in x_points:
            x_points.append(len(im_arr[1]))
            
      if 0 not in x_points:
            x_points.append(0)
      
      if len(im_arr) not in y_points:
            y_points.append(len(im_arr))
      if 0 not in y_points:
            y_points.append(0)
      
      
      # lines are plotted randomly, sorting it in reverse or.
      x_points = np.sort(x_points)
      y_points = np.sort(y_points)
      x_points = x_points[::-1]
      y_points = y_points[::-1]
      
      
      
      # return x and y axis of the lines found
      return x_points, y_points
            
      



def get_every_segment(x_points, y_points):
      # get the edge points in x direction
      
      columns = []
      rows = []
      
      count = 0
      temp = []      
      x_threshold = 34
      y_threshold = 60
      
      
      
      
      
      # for x_axis.
      for i in range(1,len(x_points),1):
            if abs(x_points[i]-x_points[i-1]) < x_threshold:
                  temp.append(x_points[i-1])
                  count += 1
            else:
                  temp.append(x_points[i-1])
                  
                  if count >15:
                        
                        # fix for wrong hough lines
                        t = len(temp)-1

                        count = 0
                        for x in range(len(temp)-1,-1,-1):
                              
                              if abs(temp[x]-temp[x-1]) > 17:
                                    t = x-1
                                    if count >= 3:
                                          t = len(temp)-1
                                          break
                                    else:
                                          
                                          break
                              else:
                                   count +=1
                                   
                                   if count >=3:
                                         t = len(temp)-1
                                         break
                        # code for fix ends
                              
                        columns.append([temp[t], temp[0]])
                  count = 0
                  temp = []
      
      count = 0
      temp = []
      
      
      
      # for y_axis
      for i in range(1,len(y_points),1):
            if abs(y_points[i]-y_points[i-1]) < y_threshold:
                  temp.append(y_points[i-1])
                  count += 1
            else:
                  temp.append(y_points[i-1])
                  
                  if count >60:      
                        rows.append([temp[-1], temp[0]])
                  count = 0
                  temp = []


      

      
      # plot lines dividing 3 columns:
      c1 = np.linspace(columns[0][0],columns[0][1],6)
      c2 = np.linspace(columns[1][0],columns[1][1],6)
      c3 = np.linspace(columns[2][0],columns[2][1],6)
      
      c = [c1]+ [c2] + [c3]
         
      all_row_points = np.linspace(rows[0][0], rows[0][1], 30)
      
      
      

      return c,all_row_points


def ans_by_intensity(columns, rows, im_arr):
      
      # file1 = open("D:\\IUB course\\temp\\spring-python\\demo\\src\\main\\java\\com\\example\\demo\\Controller\\ans.txt", "w")

      file1 = open("D:\\IUB course\\temp\\spring-python\\proj1\\src\\ans.txt", "w")


      
      
      # mask
      binary_img = 1.0*(im_arr<=200)
      
      
      
      final_ans = []
      count = 0
      for i in range(len((columns))-1,-1,-1):
            for y in range(0,len(rows)-1,1):
                  count += 1
                  temp = []
                  for x in range(0,len(columns[i])-1,1):

                        y1 = int(rows[y])
                        y2 = int(rows[y+1])
                        x1 = int(columns[i][x])
                        x2 = int(columns[i][x+1])
                        
                        temp.append(np.sum(binary_img[y1:y2+1,x1:x2+1]))
                        
                        


                  f_temp = []
                  for k in range(len(temp)):
                        f_temp.append(temp[k])
                              
                  final_ans.append([count]+f_temp)
                  

      final = []
      for i in range(len(final_ans)):
            max = -9999999999
            final.append([])
            final[i].append(str(final_ans[i][0]))
            
            t = ""
            for j in range(1,len(final_ans[i]),1):
                  if final_ans[i][j] > 600:
                        if j == 1:
                              t += 'A'
                        if j == 2:
                              t += 'B'
                        if j == 3:
                              t += 'C'
                        if j == 4:
                              t += 'D'
                        if j == 5:
                              t += 'E'
            final[i] += t 
                  
      

      a = ""
      for i in range(len(final)-2):
            for j in range(len(final[i])):
                  if j == 0:
                        a += final[i][0]
                        a+= " "
                  else: 
                        a += final[i][j]
            
            
            file1.write(a+'\n')
            a = ""
      
      


im_canny = canny()
acc, rhos, thetas = hough(im_canny)

# plot_hough(acc)
indicies = hough_peak(acc, 7)  # neighbor==7 works best for all test images.

x_points, y_points = plot_hough_lines(indicies,rhos, thetas)


columns, rows = get_every_segment(x_points, y_points) # columns = [[],[],[]]    rows = [[3,4,5]]

ans_by_intensity(columns, rows, im_arr)