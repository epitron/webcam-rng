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
# 
# TODOs:
# - Statistical tests for entropy
#   => dieharder: http://www.phy.duke.edu/~rgb/General/dieharder.php
#   => ent:       https://www.fourmilab.ch/random/
#   => diehard:   https://en.wikipedia.org/wiki/Diehard_tests
#   => https://en.wikipedia.org/wiki/Randomness_test
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


def hash_noise(noise):
  """ Cheap stream of random bytes """

  # TODO: This should be done in an information-theoretic way.
  #       (eg: determine noise distribution, use chaotic mixing, etc.)
  return hashlib.sha256(noise.tostring()).hexdigest()


def webcam_noise(devicenum=0):
  cap       = cv2.VideoCapture(devicenum)
  old_rands = set()
  lastframe = None

  while(True):
    # Capture a frame
    ret, currentframe = cap.read()

    if lastframe is not None:
      noise = extract_noise(lastframe, currentframe)

      cv2.imshow('Video entropy collector (q to quit)', amplify_noise(noise))

      rand = hash_noise(noise) # random bytes
      print rand

      if rand in old_rands:
        print "Duplicate random number!!!"
      else:
        old_rands.add(rand)


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
