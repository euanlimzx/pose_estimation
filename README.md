# pose_estimation

A computer vision project that uses pose estimation model to act as a pushup counter

Explaining how wave.py works
1. To be considered 1 rep, our model must go from the "UP" position, to the "DOWN" position
2. At any point of time, we are checking for either a proper "UP" or a proper "DOWN", using certain different criteria (angles of the elbow, elbow above hip etc.)
  - when in the UP position, we are actively checking for a DOWN, and vice versa

3. We define certain variables under initialization, these are variables that are "held" throughout the entire video (this is unlike the variables under run, which are reset during each frame)

4. Initialized values are
- number of pushups completed
- the most recent position of an individual (either UP or DOWN)
- upCondition, which refers to the number of conditions that have been met by the model, in order to be considered as a proper UP
- downCondition, which refers to the number of conditions that have been met by the model, in order to be considered a proper DOWN

5. During each run (under the .run method, this is ran every frame)
- we get the required inputs and match them to the required keypoints
- we define three functions that will be used to determine if different criteria are met (either for a proper DOWN, or a proper UP, or both)
- if the model was previously in DOWN form, we will actively check if the conditions of an UP are met
  - if they are, we change self.direction to DOWN, we reset self.downCondition, and we update the total pushup count
- vice versa for a model in the UP form

