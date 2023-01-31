# pose_estimation
A computer vision project that uses the pose estimation model provided by PeekingDuck to act as a pushup counter.

<h3>How the program works</h3>
1. We decided on a few different criteria that had to be met for a proper "up" pushup position (when arms are fully extended) and a proper "down" pushup position (body is closest to the ground)
2. To be considered 1 rep, our model must go from the "UP" position, to the "DOWN" position
3. At any point of time, we are checking for either a proper "UP" or a proper "DOWN", using certain criteria specified. If the individual has just registered a proper "UP", the code will begin looking checking the conditions for a proper "DOWN", and vice versa.

<h3>Explaining the code in pushup.py</h3>
1. Setting up of global constants
2. **map_keypoint_to_image_coords** converts relative keypoint coordinates to absolute image coordinates.
3. **draw_text** is a function we use later on to write text on our screen
4. we define a Node class, where **_init_** initializes variables that we want to keep track of throughout our video (pushup count, number of conditions met etc.)
5. under **run** (in which the code runs every frame), we first get the required input from the pipeline, and actively try to detect and assign values to our required keypoints, as long the confidence score is higher than our predefined threshold. We also label these keypoints using our **draw_text** function
6. We define the function **getAngle(A,B,C)** as a function to be used later. The function takes in three coordinates A,B,C as arguments, and returns angle ABC.
7. We define the function **noFlare** as a function to be used later. The function returns False if the individual is flaring, and returns True if the individual is doing proper form.
8. Regarding the rest of the code, here is the basic structure.
- first, if the individual has just achieved a proper "up" position, our code will only check the conditions for a proper "down" position, and vice versa
- for each individual condition, we first check if the keypoints required are present, before checking if the condition is met. if the condition is met, we will update the required values accordingly. 
- at any point in time, if the back of the individual curves, we will reset all conditions met to zero.
- Lastly, we will first check if the required number of conditions to be considered proper form has been met. if they are, we will change the pushup count accordingly.
