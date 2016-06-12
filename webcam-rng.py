#!/usr/bin/env python2
# -*- coding: utf8 -*-

#
# webcam-rng
#
# A random number generator that uses your webcam's CCD noise as an entropy source.
# (c) 2014 by Chris Gahan (chris@ill-logic.com)
#

import numpy as np
import cv2
import hashlib
import os
import sys
import fcntl
import struct


RNDADDENTROPY = 1074287107        # from /usr/include/linux/random.h

def add_to_entropy_pool(data):
    """
    Add entropy to Linux's PRNG entropy pool.
    """

    fd = os.open("/dev/random", os.O_WRONLY)

    try:
      # struct rand_pool_info {
      #   int entropy_count;
      #   int buf_size;
      #   __u32 buf[0];
      # };
      fmt = 'ii%is' % len(data)
      rand_pool_info = struct.pack(fmt, 8 * len(data), len(data), data)
      fcntl.ioctl(fd, RNDADDENTROPY, rand_pool_info)

    finally:
      os.close(fd)


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


def webcam_rng(devicenum=0, rand_filename=None):
  hash       = hashlib.sha512()
  cap        = cv2.VideoCapture(devicenum)

  if rand_filename:
    randfile = open(rand_filename, "wb")
  else:
    randfile = None

  old_rands  = set()
  lastframe  = None
  framecount = 0
  collected  = 0
  warmup     = 10

  can_write_to_dev_random = True

  while True:
    # Capture a frame
    ret, currentframe = cap.read()

    if lastframe is not None :
      framecount += 1

      noise     = extract_noise(lastframe, currentframe)
      amp_noise = amplify_noise(noise)

      cv2.imshow('Video entropy collector (q to quit)', amp_noise)

      # write_noise_to_file(noise, framecount)
      # write_noise_to_image(amp_noise, framecount)

      if framecount < warmup:
        print "* Warming up..."

      else:
        # hash the noise to generate random bytes
        hash.update(noise.tostring())
        randbytes = hash.digest()
        collected += len(randbytes)

        if can_write_to_dev_random:
          try:
            add_to_entropy_pool(randbytes)
            print "* %d bytes added to entropy pool... (%d bytes total)" % (len(randbytes), collected)
          except IOError:
            print "Error: Can't write to /dev/random; entropy won't be gathered."
            can_write_to_dev_random = False

        if randfile:
          randfile.write(randbytes)
          print "%0.35s... (%d bytes) -- %d bytes generated" % (randbytes.encode("hex"), len(randbytes), collected)

        # if randbytes in old_rands:
        #   print "!!!Duplicate random number!!!"
        # else:
        #   old_rands.add(randbytes)

      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    lastframe = currentframe

  # randfile.close()
  cap.release()
  cv2.destroyAllWindows()


if __name__ == '__main__':
  import sys

  args = sys.argv

  if len(args) == 1:
    print "usage:"
    print "  ./webcam-rng.py <video device number> [<output file (default: 'rand.dat')>]"
    sys.exit(1)

  if len(args) > 1:
    devicenum = int(args[1])

  if len(args) > 2:
    randfile = args[2]
  else:
    randfile = None

  print "Using video capture device #%d" % devicenum

  if randfile:
    print "Writing random bytes to %s" % randfile

  webcam_rng(devicenum, randfile)
