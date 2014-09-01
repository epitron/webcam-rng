#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import sys
import fcntl
import struct

RNDADDENTROPY = 1074287107        # from /usr/include/linux/random.h

def add_entropy(rnd):
    fd = os.open("/dev/random", os.O_WRONLY)
    # struct rand_pool_info {
    # int entropy_count;
    # int buf_size;
    # __u32 buf[0];
    # };
    fmt = 'ii%is' % len(rnd)
    rand_pool_info = struct.pack(fmt, 8 * len(rnd), len(rnd), rnd)
    fcntl.ioctl(fd, RNDADDENTROPY, rand_pool_info)
    os.close(fd)

while True:
	add_entropy(sys.stdin.read(512))

