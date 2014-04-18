#!/usr/bin/env python2

#
# Webcam-based entropy source
#
# Usage:
#   1) Run:
#        webcam-rng.py <video capture device number (default: 0)> [<output file for random bytes>]
#        (Note: Python opencv2 bindings must be installed)
#
#   2) Point your webcam at a stationary object, like a wall
#
#   3) Bask in all the glorious entropy!
#
# 
# TODOs:
# ----------------
#
# Statistical tests for entropy
#   => dieharder: http://www.phy.duke.edu/~rgb/General/dieharder.php
#   => ent:       https://www.fourmilab.ch/random/
#   => diehard:   https://en.wikipedia.org/wiki/Diehard_tests
#   => https://en.wikipedia.org/wiki/Randomness_test
#
# Entropy pool
#   => How to Eat Your Entropy and Have it Too (Fortuna): http://eprint.iacr.org/2014/167
#   => Hash chain: https://en.wikipedia.org/wiki/Hash_chain
#   => On entropy and randomness: http://lwn.net/Articles/261804/
#

import numpy as np
import cv2
import hashlib


def extract_noise(frame1, frame2):
  """
  CCD noise detector

  TODOs:
    * ignore large differences (low-pass filter) to ensure
      that noise is being captured
  """
  return cv2.absdiff(frame1, frame2)


def amplify_noise(noise):
  """ Amplifly the noise to make it more apparent in the GUI display """

  min, max      = noise.min(), noise.max()
  amplification = 255.0 / (max - min)

  return (noise * amplification).astype("uint8")


def write_noise_to_file(noise, count):
  filename = "noise-%0.4d.dat" % count

  file = open(filename, "wb")
  file.write(noise)
  file.close()


def write_noise_to_image(noise, count):
  filename = "noise-%0.4d.png" % count

  noisefile = cv2.imwrite(filename, noise)


def webcam_rng(devicenum=0, rand_filename="rand.dat"):
  hash       = hashlib.sha512()
  cap        = cv2.VideoCapture(devicenum)
  randfile   = open(rand_filename, "wb")
  old_rands  = set()
  lastframe  = None
  framecount = 0
  collected  = 0

  while True:
    # Capture a frame
    ret, currentframe = cap.read()

    if lastframe is not None:
      framecount += 1

      noise     = extract_noise(lastframe, currentframe)
      amp_noise = amplify_noise(noise)

      cv2.imshow('Video entropy collector (q to quit)', amp_noise)

      # write_noise_to_file(noise, framecount)
      write_noise_to_image(amp_noise, framecount)

      # hash the noise to generate random bytes
      hash.update(noise.tostring())
      randbytes = hash.digest()

      collected += len(randbytes)
      randfile.write(randbytes)

      print "%0.40s... (%d bytes) -- %d collected" % (randbytes.encode("hex"), len(randbytes), collected)

      if randbytes in old_rands:
        print "!!!Duplicate random number!!!"
      else:
        old_rands.add(randbytes)

      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    lastframe = currentframe

  randfile.close()
  cap.release()
  cv2.destroyAllWindows()


if __name__ == '__main__':
  import sys

  args = sys.argv

  if len(args) > 1:
    devicenum = int(args[1])
  else:
    devicenum = 0

  if len(args) > 2:
    randfile = args[2]
  else:
    randfile = "rand.dat"

  print "Using video capture device #%d" % devicenum
  print "Writing random bytes to %s" % randfile

  webcam_rng(devicenum, randfile)
