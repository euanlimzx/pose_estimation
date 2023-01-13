from typing import Any, Dict, List, Tuple
import cv2
import math
from peekingduck.pipeline.nodes.abstract_node import AbstractNode

# setup global constants
FONT = cv2.FONT_HERSHEY_SIMPLEX
WHITE = (255, 255, 255)       
BLACK = (0, 0,0)
THRESHOLD = 0.3               # ignore keypoints below this threshold
KP_RIGHT_EAR = 4              # PoseNet's skeletal keypoints
KP_RIGHT_SHOULDER = 6         
KP_RIGHT_WRIST = 10
KP_RIGHT_ELBOW = 8
KP_RIGHT_HIP = 12
KP_RIGHT_KNEE = 14
KP_RIGHT_ANKLE = 16
keypointList = [4,6,10,8,12,14,16]

def map_keypoint_to_image_coords(
   keypoint: List[float], image_size: Tuple[int, int]
) -> List[int]:
   """Second helper function to convert relative keypoint coordinates to
   absolute image coordinates.
   Keypoint coords ranges from 0 to 1
   where (0, 0) = image top-left, (1, 1) = image bottom-right.

   Args:
      bbox (List[float]): List of 2 floats x, y (relative)
      image_size (Tuple[int, int]): Width, Height of image

   Returns:
      List[int]: x, y in integer image coords
   """
   width, height = image_size[0], image_size[1]
   x, y = keypoint
   x *= width
   y *= height
   return int(x), int(y)

def draw_text(img, x, y, text_str: str, color_code):
   """Helper function to call opencv's drawing function,
   to improve code readability in node's run() method.
   """
   cv2.putText(
      img=img,
      text=text_str,
      org=(x, y),
      fontFace=cv2.FONT_HERSHEY_SIMPLEX,
      fontScale=0.4,
      color=color_code,
      thickness=2,
   )
class Node(AbstractNode):
   def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
      super().__init__(config, node_path=__name__, **kwargs)
      self.upCondition = 0   #check if all conditions have been fufilled to consider a successful up
      self.downCondition = 0 #check if all conditions have been fufilled to consider a successful down
      self.direction = "up"      #initialize as up, so later on we are looking our for a successful "down" 
      self.num_pushups = 0

   def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
      # get required inputs from pipeline
      img = inputs["img"]
      keypoints = inputs["keypoints"]
      keypoint_scores = inputs["keypoint_scores"]
      img_size = (img.shape[1], img.shape[0])  # image width, height
      
      #the section below is on keypoint detection
      the_keypoints = keypoints[0]                 # image only has one person
      the_keypoint_scores = keypoint_scores[0]     # only one set of scores
      right_ear = None    
      right_shoulder = None
      right_wrist = None
      right_elbow = None
      right_hip = None
      right_knee = None
      right_ankle = None


      for i, keypoints in enumerate(the_keypoints):
         keypoint_score = the_keypoint_scores[i]

         if keypoint_score >= THRESHOLD:
            if i in keypointList:
               # drawing the coordinates of each keypoint
               x, y = map_keypoint_to_image_coords(keypoints.tolist(), img_size)
               x_y_str = f"({x}, {y})"
               draw_text(img, x, y, x_y_str, WHITE)

            # matching keypoints to body parts
            if i == KP_RIGHT_EAR:
               right_ear = keypoints
            if i == KP_RIGHT_SHOULDER:
               right_shoulder = keypoints
            if i == KP_RIGHT_WRIST:
               right_wrist = keypoints
            if i == KP_RIGHT_ELBOW:
               right_elbow = keypoints
            if i == KP_RIGHT_HIP:
               right_hip = keypoints
            if i == KP_RIGHT_KNEE:
               right_knee = keypoints
            if i == KP_RIGHT_ANKLE:
               right_ankle = keypoints

      def getAngle(A, B, C):
         AB = math.sqrt((B[0]-A[0])**2 + (B[1]-A[1])**2)
         BC = math.sqrt((B[0]-C[0])**2 + (B[1]-C[1])**2)
         AC = math.sqrt((C[0]-A[0])**2 + (C[1]-A[1])**2)
         return math.degrees(math.acos((BC**2 + AB**2 - AC**2)/(2*AB*BC)))      

      def earBelowElbow(ear,elbow): #take note graph axes go diagonally downwards to the right
         if ear[1] > elbow[1]:
            return True
         else:
            return False
      
      def elbowAboveShoulderAndHip(elbow,shoulder,hip):
         if elbow[1] < shoulder [1] and elbow [1] < hip [1]:
            return True
         else:
            return False

      if self.direction == "up": #to check for a proper down
         draw_text(img, 160, 200, "going down", BLACK)

         #to check if there is a proper down position. if there is, we acknowledge the down, count the rep, and begin to lookout for an up
         if self.downCondition == 4:
            self.downCondition = 0
            self.direction = "down"
            self.num_pushups +=1
         
         #conditions that need to be met to be considered a successful "down position"
         if right_shoulder is not None and right_elbow is not None and right_wrist is not None:
            angle = getAngle(right_shoulder,right_elbow,right_wrist)
            draw_text(img, 60, 60, str(angle), BLACK)
            if angle <= 100:
               self.downCondition += 1
         if right_ear is not None and right_elbow is not None:
            if earBelowElbow(right_ear,right_elbow) is True:
               self.downCondition +=1
         if right_elbow is not None and right_shoulder is not None and right_hip is not None:
            if elbowAboveShoulderAndHip(right_elbow,right_shoulder,right_hip) is True:
               self.downCondition +=1
         if right_wrist is not None and right_shoulder is not None and right_ankle is not None:
            angle = getAngle(right_shoulder,right_ankle,right_wrist)
            if angle <= 10:
               self.downCondition +=1

      if self.direction == "down": #to check for a proper up
         draw_text(img, 160, 200, "going up", BLACK)
         #draw_text(img, 200, 200, str(self.upCondition), BLACK)
         if self.upCondition == 2:
            self.upCondition = 0
            self.direction = "up"
         if right_shoulder is not None and right_elbow is not None and right_wrist is not None:
            angle = getAngle(right_shoulder,right_elbow,right_wrist)
            draw_text(img, 60, 60, str(angle), BLACK)
            if angle >= 170:
               self.upCondition += 1
         if right_wrist is not None and right_shoulder is not None and right_ankle is not None:
            angle = getAngle(right_shoulder,right_ankle,right_wrist)
            if angle >= 40:
               self.upCondition +=1
               
      pushup_str = f"pushups = {self.num_pushups}"
      draw_text(img, 20, 30, pushup_str, BLACK)

      return {}