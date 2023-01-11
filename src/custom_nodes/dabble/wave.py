from typing import Any, Dict, List, Tuple
import cv2
import math
from peekingduck.pipeline.nodes.abstract_node import AbstractNode

# setup global constants
FONT = cv2.FONT_HERSHEY_SIMPLEX
WHITE = (255, 255, 255)       # opencv loads file in BGR format
YELLOW = (0, 0,0)
THRESHOLD = 0.3               # ignore keypoints below this threshold
KP_RIGHT_EAR = 4              # PoseNet's skeletal keypoints
KP_RIGHT_SHOULDER = 6         
KP_RIGHT_WRIST = 10
KP_RIGHT_ELBOW = 8
KP_RIGHT_HIP = 12
KP_RIGHT_KNEE = 14
keypointList = [4,6,10,8,12,14]


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

# we are gonna do a simple check that only tests for an updown motion
class Node(AbstractNode):
   def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
      super().__init__(config, node_path=__name__, **kwargs)
      # setup object working variables
      self.right_shoulder = None
      self.right_ear = None
      self.right_hip = None

      self.direction = None
      self.num_direction_changes = 0
      self.num_pushups = 0

   def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
      # get required inputs from pipeline
      img = inputs["img"]
      keypoints = inputs["keypoints"]
      keypoint_scores = inputs["keypoint_scores"]

      img_size = (img.shape[1], img.shape[0])  # image width, height


      the_keypoints = keypoints[0]              # image only has one person
      the_keypoint_scores = keypoint_scores[0]  # only one set of scores
      right_shoulder = None
      right_ear = None
      right_hip = None

      for i, keypoints in enumerate(the_keypoints):
         keypoint_score = the_keypoint_scores[i]

         if keypoint_score >= THRESHOLD:
            x, y = map_keypoint_to_image_coords(keypoints.tolist(), img_size)
            x_y_str = f"({x}, {y})"
            if i == KP_RIGHT_SHOULDER:
               right_shoulder = keypoints
            if i == KP_RIGHT_EAR:
               right_ear = keypoints
            if i == KP_RIGHT_HIP:
               right_hip = keypoints
            if i in keypointList:
               draw_text(img, x, y, x_y_str, WHITE)

      if right_shoulder is not None and right_hip is not None and right_ear is not None:
         # only count number pushups after we have gotten the keypoints for the shoulder from the code above
         if self.right_shoulder is None:
            self.right_shoulder = right_shoulder           # first shoulder data point
         if self.right_ear is None:
            self.right_ear = right_ear
         if self.right_hip is None:
            self.right_hip = right_hip
         else:
            # if you want, can add a check that person is doing pushup before even counting the rep 
            if right_shoulder[1] < self.right_shoulder[1] and right_ear[1]<self.right_ear[1] and right_hip[1]<self.right_hip[1]:
               direction = "down"
            else:
               direction = "up"

            if self.direction is None:
               self.direction = direction          # first direction data point
            else:
               # check if hand changes direction
               if direction != self.direction:
                  self.num_direction_changes += 1
               # every two hand direction changes == one wave
               if self.num_direction_changes >= 2:
                  self.num_pushups += 1
                  self.num_direction_changes = 0   # reset direction count

            self.right_hip = right_hip
            self.right_ear = right_ear
            self.right_shoulder = right_shoulder         # save last position
            self.direction = direction

         wave_str = f"pushups = {self.num_pushups}"
         draw_text(img, 20, 30, wave_str, YELLOW)

      return {}