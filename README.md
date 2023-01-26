## Run The Application

#### Below is the empty sheet for which this application is built on.
![blank_form](https://user-images.githubusercontent.com/61111725/212433186-48418aee-c904-407e-9acf-c29187f1e633.jpg)


#### In this application sheet which is marked can be uploaded and the answers will be automatically detected and returned as a .txt file. Let's look at the process. Below is the main page and there is an option to upload a image.
![Merge1](https://user-images.githubusercontent.com/61111725/212433050-9f80fff0-45c1-46c7-ad15-3fd875c763df.png)

#### Once the image is uploaded, we can see the uploaded image with all the details about the image. User can select another image to change or replace the currently selected image. Then user can submit the image.
![Merge2](https://user-images.githubusercontent.com/61111725/212433052-7566a0b7-07bf-43db-bd58-6d8a86cad37c.png)
#### As the image is submitted, backend will start extracting the answers from the provided image.
![Merge3](https://user-images.githubusercontent.com/61111725/212433053-e2808354-4ea5-4250-a5d3-2c387fcb99f7.png)

#### Once the processing is done, image will be ready to be downloaded.
![Merge4](https://user-images.githubusercontent.com/61111725/212433056-0bac9cc3-be70-42bb-8b3c-59b78707cc34.png)

#### Extracted answers will be in text file and are in format given below.
![Merge5](https://user-images.githubusercontent.com/61111725/212433094-0c6d8ad8-efe7-45b1-877e-1f3ef828c771.png)




## Approach: Robust Hough Lines

### Getting canny edge detection working
The first step was to get the canny edge detection working. We implemented gaussian blur, but ended up using the scipy library to get the gaussian blur. Then we applied sobel filter to the image. The naive implementation was giving perfect result, but was taking long time to exicute. So we explored other inbuilt function for convolution where we found out that convolution function of, for example, ndimage.convolve is different then the fftconvolve from scipy. The fftconvolve function was giving better results.

Next step was to get the non-max suppression and apply hysteresis. We found some referance on the internet and followed that to get the result. The final result of the canny edge detection was not that good. Also tried to use some other approach but we failed to get acceptable results so we decided to not using all that work and ended up using simple laplacian filter to get the edges and move on to the next problem.

### Hough lines and peaks.

We managed to get the hough lines working and the lines were acceptable. We only selected the lines which were vertical or horizontal (0 or 90) as we assumed that the oriantation of the image will remain almost the same. 
![Screenshot 2022-02-16 163836](https://user-images.githubusercontent.com/61111725/212432750-52cc11c3-5ed7-4ca0-83f9-567d1b3aa01c.png)

Getting the peaks was a little tough to get correct. The problem in the naive approach was, getting the 'n' number of peaks from the hough space, most of the selected peak were just around the first peak selected. That approach was giving unacceptable lines. So, we found one other approach. When the peak value is found, we removed some pixels around that peak value, so the next peak would not be just next to the first peak. And, that approach worked really well. Was using naive way to get the index from accumulator, got shorter way to get the index from saumya metha. And after that we converted the values to the coordinates to the points for our actual image.So the peak lines we were getting using this approach were acceptable. And at the end of this, we had the 'x' and 'y' coordinates of the hough lines![PXL_20220218_233725315](https://user-images.githubusercontent.com/61111725/212432822-8eed0b2c-4f1f-4d32-b2f7-8e03fbd07ae0.jpg)
.


### Get the segments.

After getting the hough lines, we needed the coordinates of every options. Here we made an assumption that the hough lines that we are getting are consistent, which was true across the given test images. Then we applied thresholds around the images to exactly get the points around the options. Once we were getting proper border points, we divided the area by ratio.The idea was, hough lines were very dense near the options. We used that and found the approximate coordinates of all the options. There were some challenges we faced as there were some noisey and unwanted lines which we took care of applying some threshold between the lines.
![PXL_20220220_065630567](https://user-images.githubusercontent.com/61111725/212432841-df3c92a2-cc10-4239-a552-73d409fb4de4.jpg)


## Getting the answers.
Once the segment part was done, most of the hard work was done. We had the coordinates of every options on the sheet. Firstly, we converted the image to binary form(0-1) as we used the intensity values to find out the correct answer. To get the intensity, we just sum the values within that block. And used some threshold, out of the 5 blocks(5 options), if the intensity of the options are more than the threshold, those options are the answer. We tuned the threshold until we got acceptable answers and saved it on the output.txt file.

## Improvements.

On some image, specifically images like 'a-48.jpg' it has a box above our options, which created some dense hough lines just above, where the options starts. And thus our code counted that as our working area. And then dividing the area using the ratio did not provide good boxes, as some part of the boxes were overlaping with the question above, as the working area shifted up a bit because of that.

If we could have got the canny edge detection working perfectly, we would have definately got better results and also the gaussian do remove some noisey lines, from what we tried. But considering the time constrain and the trial and error we did, using only laplaican filter gave acceptable answers.
