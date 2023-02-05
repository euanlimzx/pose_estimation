# pose_estimation
A computer vision project that uses the pose estimation model provided by PeekingDuck to act as a pushup counter.

Watch the demonstration video:
https://www.youtube.com/watch?v=UDV_IQ2eH20 

<h3>How the program works</h3>
1. We decided on a few different criteria that had to be met for a proper "UP" pushup position - when arms are fully extended - and a proper "DOWN" pushup position - body is closest to the ground.<br>
2. To be considered 1 rep, our model must go from the "UP" position, to the "DOWN" position.<br>
3. At any point of time, we are checking for either a proper "UP" or a proper "DOWN", using certain criteria specified. 
4. If the individual has just registered a proper "UP", the code will begin looking checking the conditions for a proper "DOWN", and vice versa.<br>

<h3>Explaining the code in pushup.py</h3>
1. tkinter module initialises a basic UI with a web-cam for the user to get into position first<br>
2.<strong>map_keypoint_to_image_coords</strong> converts relative keypoint coordinates to absolute image coordinates.<br>
3.<strong>draw_text</strong> is a function we use later on to write text on our screen<br>
4. we define a Node class, where <strong>_init_</strong> initializes variables that we want to keep track of throughout our video (pushup count, number of conditions met etc.)<br>
5. under <strong>run</strong> (in which the code runs every frame), we first get the required input from the pipeline, and actively try to detect and assign values to our required keypoints, as long the confidence score is higher than our predefined threshold. We also label these keypoints using our <strong>draw_text</strong> function<br>
6. Function <strong>getAngle(A,B,C)</strong> as a function to be used later. The function takes in three coordinates A,B,C as arguments, and returns angle ABC.<br>
7. Function <strong>noFlare</strong> as a function to be used later. The function returns False if the individual is flaring elbows during the push up, and returns True if the individual is doing proper form.<br>
8. Regarding the rest of the code, here is the basic structure.<br>
- 1. Checks if individual is going up or down<br>
- 2. For each condition function, we first check for the existence of the required keypoints, before checking if the condition is met.<br>
- 3. If the condition is met, the values will be updated accordingly<br>
- 4. All conditions met will reset to zero, if the individual's back is not straight.<br>
- 5. Check if all required conditions for a proper "UP"/"DOWN" is met, and update values accordingly - Push Up Count, Direction est. <br>

<h3>Usage Guidelines</h3>
1. Make sure nobody else is in frame<br>
2. Don't have your body parts leave the frame too quick<br>
3. If you would like to not use webcam and use a demonstration video instead, change source:0 to source:pushupwhite.mp4 in the pipeline_config.yml file
