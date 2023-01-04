## Other Approach: Robust Hough Lines

### Getting canny edge detection working
The first step was to get the canny edge detection working. We implemented gaussian blur, but ended up using the scipy library to get the gaussian blur. Then we applied sobel filter to the image. The naive implementation was giving perfect result, but was taking long time to exicute. So we explored other inbuilt function for convolution where we found out that convolution function of, for example, ndimage.convolve is different then the fftconvolve from scipy. The fftconvolve function was giving better results.

Next step was to get the non-max suppression and apply hysteresis. We found some referance on the internet and followed that to get the result. The final result of the canny edge detection was not that good. Also tried to use some other approach but we failed to get acceptable results so we decided to not using all that work and ended up using simple laplacian filter to get the edges and move on to the next problem.

### Hough lines and peaks.

We managed to get the hough lines working and the lines were acceptable. We only selected the lines which were vertical or horizontal (0 or 90) as we assumed that the oriantation of the image will remain almost the same. 

Getting the peaks was a little tough to get correct. The problem in the naive approach was, getting the 'n' number of peaks from the hough space, most of the selected peak were just around the first peak selected. That approach was giving unacceptable lines. So, we found one other approach. When the peak value is found, we removed some pixels around that peak value, so the next peak would not be just next to the first peak. And, that approach worked really well. Was using naive way to get the index from accumulator, got shorter way to get the index from saumya metha. And after that we converted the values to the coordinates to the points for our actual image.So the peak lines we were getting using this approach were acceptable. And at the end of this, we had the 'x' and 'y' coordinates of the hough lines.


### Get the segments.

After getting the hough lines, we needed the coordinates of every options. Here we made an assumption that the hough lines that we are getting are consistent, which was true across the given test images. Then we applied thresholds around the images to exactly get the points around the options. Once we were getting proper border points, we divided the area by ratio.The idea was, hough lines were very dense near the options. We used that and found the approximate coordinates of all the options. There were some challenges we faced as there were some noisey and unwanted lines which we took care of applying some threshold between the lines. 

## Getting the answers.
Once the segment part was done, most of the hard work was done. We had the coordinates of every options on the sheet. Firstly, we converted the image to binary form(0-1) as we used the intensity values to find out the correct answer. To get the intensity, we just sum the values within that block. And used some threshold, out of the 5 blocks(5 options), if the intensity of the options are more than the threshold, those options are the answer. We tuned the threshold until we got acceptable answers and saved it on the output.txt file.

## Improvements.

On some image, specifically images like 'a-48.jpg' it has a box above our options, which created some dense hough lines just above, where the options starts. And thus our code counted that as our working area. And then dividing the area using the ratio did not provide good boxes, as some part of the boxes were overlaping with the question above, as the working area shifted up a bit because of that.

If we could have got the canny edge detection working perfectly, we would have definately got better results and also the gaussian do remove some noisey lines, from what we tried. But considering the time constrain and the trial and error we did, using only laplaican filter gave acceptable answers.
