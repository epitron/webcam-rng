
# webcam-rng

A random number generator that uses your webcam's CCD noise as an entropy source.

(__NOTE:__ This is a work in progress, and should not be used for mission critical applications like protecting nuclear secrets or shuffling poker decks. That said, [preliminary testing](https://github.com/epitron/webcam-rng/tree/master/tests) has shown that, even at this early stage, we're generating good random numbers!)


## Requirements

* Python 2.7
* OpenCV 2.x Python bindings


## Installation

First, clone the git repo:

  ```git clone https://github.com/epitron/webcam-rng```

Next, install the python opencv2 bindings (if you haven't yet)...

#### Ubuntu:

  ```$ apt-get install python-opencv```

#### Fedora:

   ```$ dnf install python2-opencv```

#### RHEL7/CentOS7/Scientific Linux 7:

Note: ensure to have `optional` repo enabled:

    ```$ yum install opencv-python```

#### Arch:
  
  ```$ pacman -S opencv```

#### Everyone else:

Sorry, you're on your own!


## Usage

1. Run: 

  ```$ ./webcam-rng.py 0```

  (`0` is the first video device, `1` is the second, etc.)

2. Point your webcam at a stationary object, like a wall
3. Bask in the glorious entropy!


Random nubmers will be written to `rand.dat`. You can set the filename by passing an extra commandline argument:

  ```$ ./webcam-rng.py 0 really-random.dat```


## TODOs

### Statistical tests of generated entropy:

* [Dieharder statistical tests](http://www.phy.duke.edu/~rgb/General/dieharder.php)
* [ent entropy estimator](https://www.fourmilab.ch/random/)
* [Diehard statistical tests](https://en.wikipedia.org/wiki/Diehard_tests)
* [Randomness tests (Wikipedia)](https://en.wikipedia.org/wiki/Randomness_test)

### Use the CCD noise more effectively:

We should be able to get much more than 64-bytes of entropy out
of each webcam frame (depending on how crappy the webcam is).

Doing a very crude test, 256 frames of webcam noise (235 MB of data)
compresses down to 55 MB using LZMA. This means that there is potentially
about 200k of entropy in each frame (a firehose of entropy, compared to the
64 bytes it's currently getting.)

__Related Research:__

* [Webcam Random Number Generator](https://pthree.org/2016/06/12/webcam-random-number-generation/) (using pyblake2 to hash the images)
* [Hardware RNG (Wikipedia)](https://en.wikipedia.org/wiki/Hardware_random_number_generator#Using_observed_events)
* [video_entropyd](http://www.vanheusden.com/ved/)
  
### Entropy pool:

* [How to Eat Your Entropy and Have it Too (Fortuna)](http://eprint.iacr.org/2014/167)
* [Hash chains](https://en.wikipedia.org/wiki/Hash_chain)
* [On entropy and randomness](http://lwn.net/Articles/261804/)

## License

  WTFPL2, as usual. :)

## Copyright

(c) 2014 by Chris Gahan (chris@ill-logic.com)
