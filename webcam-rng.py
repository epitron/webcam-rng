#!/usr/bin/env python2

#
# Webcam-based entropy source
#
# Usage:
#   1) Run:
#        webcam-rng.py <video capture device number (default: 0)>
#
#   2) Point your webcam at a stationary object, like a wall
#
#   3) Bask in all the glorious entropy!
#

import numpy as np
import cv2

def extract_frame_noise(a, b):
  """ Detect CCD noise """

  diff          = cv2.absdiff(a, b)
  min, max      = diff.min(), diff.max()
  amplification = 255 / (max - min)

  return diff * amplification


def webcam_noise(devicenum=0):
  cap = cv2.VideoCapture(devicenum)

  lastframe = None

  while(True):
    # Capture frame-by-frame
    ret, currentframe = cap.read()

    if lastframe is not None:
      noise = extract_frame_noise(lastframe, currentframe)

      cv2.imshow('Video entropy collector (q to quit)', noise)

      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    lastframe = currentframe

  cap.release()
  cv2.destroyAllWindows()


if __name__ == '__main__':
  import sys

  args = sys.argv

  if len(args) > 1:
    devicenum = int(args[1])
  else:
    devicenum = 0

  print "Using video capture device #%d" % devicenum

  webcam_noise(devicenum)
