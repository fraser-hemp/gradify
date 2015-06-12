from operator import itemgetter
import sys, os, argparse
from PIL import Image, ImageFilter

""" Image Gradients
Module for analysing images for their 4 most
prominant colors, and creating a CSS gradient.
"""

class Gradify():
  """ Image Analyser
  Main class to do the analysis
  """
  
  # Cross browser prefixes.
  BROWSER_PREFIXES = ["", "-webkit-", "-moz-", "-o-", "-ms-"]

  def __init__(self, black_sensitivity=4.3, white_sensitivity = 3, num_colors=4, resize=55, uniformness=7, webkit_only=False):

    self.MAX_COLORS = num_colors

    self.RESIZE_VAL = resize

    self.UNIFORMNESS = uniformness

    self.spread_quadrants = True

    self.pairs = []

    self.num_done = 0

    if webkit_only:
      self.BROWSER_PREFIXES= ["-webkit-"]

    self.IGNORED_COLORS = {
      "BLACK": {
        "col": (0,0,0),
        "radius": black_sensitivity
      },
      "WHITE": {
        "col": (255,255,255),
        "radius": white_sensitivity
      }
    }
    self.init_CLI_args()
    
    if self.args.demo:
      self.demo_file = "demo.html"
      open(self.demo_file, "w").close()
    if self.args.file:
      self.get_file(self.args.file)
    if self.args.dir:
      self.get_dir(self.args.dir)
    if not self.args.file:
      self.get_dir("")
    if self.args.demo:
      # TODO: Sorry windows, will fix later
      os.system("open " + self.demo_file)
    else:
      self.printRules()

  def init_CLI_args(self):
    self.parser = argparse.ArgumentParser()
    self.parser.add_argument("--single", help="1 color background (no gradient)", action="store_true")
    self.parser.add_argument("--spread", help="Uses color's spread in each quadrant rather than it's strength: flattens bell curve of accuracy", action="store_true")
    self.parser.add_argument("-d", "--dir", help="Gradify contents of this directory")
    self.parser.add_argument("-f", "--file", help="Gradify single file")
    self.parser.add_argument("-c", "--classname", help="Specific classname of CSS to add gradients to (default is 'gradify')")
    self.parser.add_argument("--demo", help="Create example HTML file displaying results, opens when completed", action="store_true")
    self.args = self.parser.parse_args()
    return

  def get_directions(self, fn):

    foo = Image.open(fn)
    foo = foo.resize((100, 100), Image.ANTIALIAS)
    self.image = foo
    
    col = self.get_colors()

    if self.args.single:
      if self.args.demo:
        self.printExampleCSS(col)
      self.pairs.append((self.num_done, col))
      return
    quad_cols = [0]*4
    taken = [0] * 4
    cols_quads = [0]*4

    for i in range(len(col)):
      count = 0
      # 0 - left, 1 - bottom, 2 - right, 3 - top 
      a = [0]*4
      for pix in foo.getdata():
        if self.get_RGB_diff(pix,col[i])<4.2:
          if int((count%100)/50)==1:
            a[2] += 1
          else :
            a[0] += 1
          if int((count/100.0)/50) == 0:
            a[3] += 1
          else:
            a[1] += 1
        count += 1
      cols_quads[i] = a
      while 0 in taken and not self.args.spread:
        best_quad = a.index(max(a))
        if max(a)==0:
          best_quad = taken.index(0)
        if taken[best_quad]==0:
          taken[best_quad] = 1
          col[i] = list(col[i])
          col[i].append(best_quad * 90)
          quad_cols[i] = col[i]
          break
        else:
          a[best_quad] = 0

    if self.args.spread:
      quad_cols = self.calculate_spread(cols_quads, col)

    if self.args.demo:
      self.printExampleCSS(quad_cols)
    self.pairs.append((self.num_done, quad_cols))

  def calculate_spread(self, spread_quads, col):
    strength_spread = []
    quad_cols = [0] * 4
    taken_col = [0] * 4
    taken_quads = [0] * 4
    for quad in spread_quads:
      top = quad[3]*1.0/(quad[1]+0.01)
      left = quad[2]*1.0/(quad[0]+0.01)
      if left < 1:
        left = 1/(left+0.01)
      if top < 1:
        top = 1/(top+0.01)
      strength_spread.append(top)
      strength_spread.append(left)
    # TODO: Make more readable
    while 0 in taken_col:
      best_col = int(strength_spread.index(max(strength_spread))/2)
      if max(strength_spread) is 0:
        best_col = taken_col.index(0)
      if taken_col[best_col] is 0:
        best_quad = spread_quads[best_col].index(max(spread_quads[best_col]))
        if max(spread_quads[best_col]) is 0:
          sys.stderr.write(str(spread_quads))
          best_quad = taken_quads.index(0)
        if taken_quads[best_quad] is 0:
          taken_quads[best_quad] = 1
          taken_col[best_col] = 1
          col[best_col] = list(col[best_col])
          col[best_col].append(best_quad * 90)
          quad_cols[best_col] = col[best_col]
        spread_quads[best_col][best_quad] = 0
      strength_spread[strength_spread.index(max(strength_spread))] = 0

    return quad_cols

  def printRules(self):
    for pair in self.pairs:
      i = 0
      if self.args.classname:
        print(".%s-%d {" % (self.args.classname, pair[0]))
      else:
        print(".gradify-%d {" % (pair[0]))
      print("background:")
      if self.args.single:
        print "rgb(" + str(pair[1][0])+"," + str(pair[1][1]) +"," + str(pair[1][2]) +");"
      else:
        print "rgb(" + str(pair[1][0][0])+"," + str(pair[1][0][1]) +"," + str(pair[1][0][2]) +");"
      if not self.args.single:
        print("background:")
        for prefix in self.BROWSER_PREFIXES:
          for color in pair[1]:
            print prefix + "linear-gradient("+str(color[3])+"deg, rgba(" + str(color[0])+"," + str(color[1]) +"," + str(color[2]) +","+str(1)+") 0%, rgba(" + str(color[0])+"," + str(color[1]) +"," + str(color[2]) +",0) 100%)"
            i += 1
            if i==self.MAX_COLORS:
              print ";"
              break
            print ","
      print("}")

  def get_file(self, filen):
    self.image = Image.open(filen)
    self.imageFileName = filen
    self.get_directions(filen)

  def get_dir(self, dir):
    dir = dir + "/"
    self.num_files = len(os.listdir(dir))
    for fn in os.listdir(dir):
      fn = dir + fn
      if os.path.isfile(fn) and ".jpg" in fn:
        self.image = Image.open(fn)
        self.imageFileName = fn
        self.get_directions(fn)
        self.num_done += 1
        sys.stderr.write("Done " + str(self.num_done) + "/" + str(self.num_files) + " images\n")

  def printExampleCSS(self, colors):
    i = 0
    with open(self.demo_file, "a") as df:
      df.write("<div class='example-img-0' style='width:300px;height:300px;float:left;background:")
      if self.args.single:
        sys.stderr.write(str(colors))
        df.write("rgb(" + str(colors[0])+"," + str(colors[1]) +"," + str(colors[2]) +");")
      else:
        for prefix in self.BROWSER_PREFIXES:
          for color in colors:
            df.write(prefix + "linear-gradient("+str(color[3])+"deg, rgba(" + str(color[0])+"," + str(color[1]) +"," + str(color[2]) +","+str(1)+") 0%, rgba(" + str(color[0])+"," + str(color[1]) +"," + str(color[2]) +",0) 100%)")
            i += 1
            if i == self.MAX_COLORS:
              break
            df.write(",")
          df.write(";")
      df.write("'></div>")
      df.write("<div class='example-img-0' style='width:300px;height:300px;float:left;'><img src='" + self.imageFileName + "' style='width:300px;float:left;height:300px;' class='blah'/>")
      df.write("</div>")


  def printShowCase(self, colors):
    i = 0
    print "<div class='example-container'>"
    print "<div class='grad lol-" + str(self.numDone) + "'>"
    for color in reversed(colors):
      #print "-webkit-linear-gradient("+str(90 - i*90)+"deg, rgba(128,0,0,0) 0%, rgba(" + str(color[0])+"," + str(color[1]) +"," + str(color[2]) +",1) 100%, rgba(" + str(color[0])+"," + str(color[1]) +"," + str(color[2]) +",1) 100%)"
      i+=1
      if (i==self.MAX_COLORS):
        break
      #print ","
    print "</div><img src='" + self.imageFileName + "' class='photo'/>"
    print "</div>"

  def get_colors(self):
    self.image = self.image.resize((55,55), Image.ANTIALIAS)

    h = self.image.filter(ImageFilter.BLUR)
    h = h.histogram()
    self.colors = []
    # split into red, green, blue
    r = h[0:256]
    g = h[256:256*2]
    b = h[256*2: 256*3]
    # Rank the histogram in order of appearance
    self.ranked_colors = sorted(self.image.getcolors(self.image.size[0]*self.image.size[1]), key = itemgetter(0))
    for i in range(len(self.ranked_colors)):
      self.colors.append(self.ranked_colors[len(self.ranked_colors)- 1 - i])
    if self.MAX_COLORS is 1:
      return self.colors[0]
    else:
      return self.findBestColors()

  def get_RGB_diff(self, old, new):
    # Currently an approximation of LAB colorspace
    return abs(1.4*abs(old[0]-new[0])**(1/2.0) + .8*abs(old[1]-new[1])**(1/2.0) + .8*abs(old[2]-new[2])**(1/2.0))**(1/2.0)

  def find_single_color(self):
    for i in range(len(self.colors)):
      diffB = self.get_RGB_diff(self.IGNORED_COLORS["BLACK"]["col"], self.colors[i][1])
      diffW = self.get_RGB_diff(self.IGNORED_COLORS["WHITE"]["col"], self.colors[i][1])
      if diffB > 4 and diffW> 3.5:
        # IF too close to Black or White, ignore this color
        sys.stderr.write(str(diffB) + "\n")
        sys.stderr.write(str(self.colors[i][1]) + "\n")
        return self.colors[i][1]
    # Worst-case return first color
    return self.colors[0][1]


  def findBestColors(self):
    selectedColors = []
    bad_color = False
    sensitivity = self.UNIFORMNESS
    ignored_radius = 0
    if self.args.single:
      return self.find_single_color()
    while (len(selectedColors) < self.MAX_COLORS):
      selectedColors = []
      for i in range(len(self.colors)):
        bad_color = False
        for col, col_dict in self.IGNORED_COLORS.iteritems():
          diff = self.get_RGB_diff(col_dict["col"], self.colors[i][1])
          if diff < col_dict["radius"] - ignored_radius:
            # IF too close to Black or White, ignore this color
            bad_color = True
            break
        for j in range(len(selectedColors)):
          diff = self.get_RGB_diff(self.colors[i][1], selectedColors[j])
          if (diff < sensitivity):
            # IF too close to any other selected color, ignore.
            bad_color = True
            break
        if bad_color:
          continue
        selectedColors.append(self.colors[i][1])
      if ignored_radius < 2:
        ignored_radius += 1
      else :
        sensitivity -= 1
        ignored_radius = 0

    return selectedColors[0:4]

foo = Gradify()
