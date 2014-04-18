#!/usr/bin/env python2

#
# Webcam-based entropy source
#
# Usage:
#   1) Run:
#        webcam-rng.py <video capture device number (default: 0)>
#        (Note: Python opencv2 bindings must be installed)
#
#   2) Point your webcam at a stationary object, like a wall
#
#   3) Bask in all the glorious entropy!
#

import numpy as np
import cv2
import hashlib


def amplify_noise(noise):
  """ Make the noise easy to see (for the visual output) """
  min, max      = noise.min(), noise.max()
  amplification = 255.0 / (max - min)

  return (noise * amplification).astype("uint8")


def extract_noise(a, b):
  """
  CCD noise detector

  TODOs:
    * ignore large differences (low-pass filter) to ensure
      that noise is being captured
  """
  return cv2.absdiff(a, b)


old_rands = set()

def noise_to_rand(noise):
  """ Output a stream of random bytes """

  global old_rands

  # TODO: This should be done in an information-theoretic way.
  #       (eg: determine noise distribution, use chaotic mixing, etc.)
  rand = hashlib.sha256(noise.tostring()).hexdigest()

  if rand in old_rands:
    print "Duplicate random numbers!!!"
  else:
    old_rands.add(rand)

  return rand


def webcam_noise(devicenum=0):
  cap = cv2.VideoCapture(devicenum)

  lastframe = None

  while(True):
    # Capture a frame
    ret, currentframe = cap.read()

    if lastframe is not None:
      noise = extract_noise(lastframe, currentframe)

      cv2.imshow('Video entropy collector (q to quit)', amplify_noise(noise))

      print noise_to_rand(noise) # random bytes

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
