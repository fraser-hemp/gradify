# gradify
A module to produce CSS gradients as placeholders for images.

[gradify showcase](http://gradifycss.com "gradify")

0.1 (beta)

The JS version was quickly written to use as an example on the website, and needs futher work.
The python source also needs some optimization/styling, especially deep cross-browser support and PNG support.

Currently only accepts JPG images

# Getting Started

For a quick demo of gradify, simply place some images within the same directory and run:

`$ python gradify.py --demo --spread`

# Usage

To see the flags and their uses

`python gradify.py help`

`--demo`

DEMO (opt) - this flag will display the images next to their gradient on a webpage on completion.

`--spread`

SPREAD (opt) - this flag will give the color which has the least spread over the image the highest priority when assigning directions (opposed to most dominant color). This feature improves overall accuracy, however adds complexity and in unique cases it produces counter-intuitive results

`--single`

SINGLE (opt) - Only produce a single, uniform background color - this is much quicker and has all browser support

`-c --classname`

CLASSNAME (opt) - custom classname for the CSS rules to be assigned to (needs work)

`-f --file`

FILE (opt) specify a single image file to be used

`-d --dir`

DIR (opt) - specify a directory to be used. If not used (and not -f), current dir will be used. Only files with "jpg" extension will be used.

Other important notes:
There are constants you can tweak which will later be flags (Black/White sensitivity, image resolution, uniformness of colors) although generally the default vals are generally best.

My only suggestion is increasing the uniformness (by lowering it's val) can improve the general case, improve speed, but decrease the upper limits of accuracy. Increasing sensitivity to black will do the same.


# Requirements

Gradify depends on Pillow, which you may install using
`pip install Pillow`

In case you get the error message `ImportError: No module named PIL`, you need to install Pillow first.


# License MIT

Copyright (c) 2015 Fraser Hemphill

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
