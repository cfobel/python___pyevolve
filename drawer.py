from pyevolve import GSimpleGA, GAllele
from pyevolve.G1DList import G1DList
from pyevolve import Mutators, Crossovers, Initializators
from pyevolve import Consts, Util
from pyevolve.GenomeBase import GenomeBase

import Image
import aggdraw

import random, copy

def G1DListCrossoverSPSafe(genome, **args):
   sister = None
   brother = None
   gMom = args["mom"]
   gDad = args["dad"]
   
   cut = random.randint(1, len(gMom)-1)

   if args["count"] >= 1:
      sister = gMom.clone()
      sister.resetStats()
      sister[cut:] = copy.deepcopy(gDad[cut:])

   if args["count"] == 2:
      brother = gDad.clone()
      brother.resetStats()
      brother[cut:] = copy.deepcopy(gMom[cut:])

   return (sister, brother)


class G1DListSafe(G1DList):
   def __init__(self, size):
      G1DList.__init__(self, size)

   def copy(self, g):
      GenomeBase.copy(self, g)
      g.listSize = self.listSize
      g.genomeList = copy.deepcopy(self.genomeList)
   
   def clone(self):
      newcopy = G1DListSafe(self.listSize)
      self.copy(newcopy)
      return newcopy

imgOriginal = Image.open("monalisa_small.jpg")
size_tuple = imgOriginal.size

POLY_MAX_POINTS = 8

def randomAlpha(begin=10, end=60):
   return random.randint(begin, end)

def randomColor(begin=0, end=255):
   return [random.randint(begin, end), random.randint(begin, end), random.randint(begin, end)]

def randomXY(size):
   return (random.randint(0, size[0]), random.randint(0, size[1]))

def randomAngle():
   return random.randint(10, 360)

def G1DListMutatorDrawer(genome, **args):
   if args["pmut"] <= 0.0: return 0
   listSize = len(genome) - 1

   mutations = 0
   for it in xrange(listSize+1):
      if Util.randomFlipCoin(args["pmut"]):
         genome[it].mutate()
         mutations+=1

   return mutations

class DrawPolygon:
   def __init__(self, size):
      self.point_list = []
      self.size = size

      num_points = random.randint(3, POLY_MAX_POINTS)
      for i in xrange(num_points):
         x, y = randomXY(size)
         self.point_list.append(x)
         self.point_list.append(y)
      self.color = randomColor()
      self.alpha = randomAlpha()

   def drawTo(self, imgDraw):
      brush = aggdraw.Brush(tuple(self.color), self.alpha)
      imgDraw.polygon(tuple(self.point_list), brush)

   def mutate(self):
      for i in xrange(len(self.point_list)):
         self.point_list[i] += int(random.gauss(0, 5))
         self.point_list[i] = max(self.point_list[i], 0)

      for i in xrange(len(self.color)):
         self.color[i] += int(random.gauss(0, 5))
         self.color[i] = min(max(0, self.color[i]), 255)
        
      self.alpha += int(random.gauss(0, 5))
      self.alpha = min(max(10, self.alpha), 60)

class DrawChord:
   def __init__(self, size):
      self.seq_list = []
      self.angle_start = randomAngle()
      self.angle_end = randomAngle()
      self.color = randomColor()
      self.alpha = randomAlpha()

      for i in xrange(2):
         x, y = randomXY(size)
         self.seq_list.append(x), self.seq_list.append(y)

   def drawTo(self, imgDraw):
      brush = aggdraw.Brush(tuple(self.color), self.alpha)
      imgDraw.chord(tuple(self.seq_list), self.angle_start, self.angle_end, brush)

   def mutate(self):
      for i in xrange(len(self.seq_list)):
         self.seq_list[i] += int(random.gauss(0, 5))
         self.seq_list[i] = max(self.seq_list[i], 0)

      self.alpha += int(random.gauss(0, 5))
      self.alpha = min(max(10, self.alpha), 60)

      self.angle_start += int(random.gauss(0, 5))
      self.angle_start = min(max(0, self.angle_start), 360)

      self.angle_end += int(random.gauss(0, 5))
      self.angle_end = min(max(0, self.angle_end), 360)

      for i in xrange(len(self.color)):
         self.color[i] += int(random.gauss(0, 5))
         self.color[i] = min(max(0, self.color[i]), 255)
        

class DrawEllipse:
   def __init__(self, size):
      self.seq_list = []
      self.color = randomColor()
      self.alpha = randomAlpha()

      for i in xrange(2):
         x, y = randomXY(size)
         self.seq_list.append(x), self.seq_list.append(y)

   def drawTo(self, imgDraw):
      brush = aggdraw.Brush(tuple(self.color), self.alpha)
      imgDraw.ellipse(tuple(self.seq_list), brush)

   def mutate(self):
      for i in xrange(len(self.seq_list)):
         self.seq_list[i] += int(random.gauss(0, 5))
         self.seq_list[i] = max(0, self.seq_list[i])

      self.alpha += int(random.gauss(0, 5))
      self.alpha = min(max(10, self.alpha), 60)

      for i in xrange(len(self.color)):
         self.color[i] += int(random.gauss(0, 5))
         self.color[i] = min(max(0, self.color[i]), 255)

class DrawPieslice:
   def __init__(self, size):
      self.seq_list = []
      self.angle_start = randomAngle()
      self.angle_end = randomAngle()
      self.color = randomColor()
      self.alpha = randomAlpha()

      for i in xrange(2):
         x, y = randomXY(size)
         self.seq_list.append(x), self.seq_list.append(y)

   def drawTo(self, imgDraw):
      brush = aggdraw.Brush(tuple(self.color), self.alpha)
      imgDraw.pieslice(tuple(self.seq_list), self.angle_start, self.angle_end, brush)


   def mutate(self):
      for i in xrange(len(self.seq_list)):
         self.seq_list[i] += int(random.gauss(0, 5))
         self.seq_list[i] = max(0, self.seq_list[i])

      self.alpha += int(random.gauss(0, 5))
      self.alpha = min(max(10, self.alpha), 60)

      for i in xrange(len(self.color)):
         self.color[i] += int(random.gauss(0, 5))
         self.color[i] = min(max(0, self.color[i]), 255)

      self.angle_start += int(random.gauss(0, 5))
      self.angle_start = min(max(0, self.angle_start), 360)

      self.angle_end += int(random.gauss(0, 5))
      self.angle_end = min(max(0, self.angle_end), 360)



class DrawRectangle:
   def __init__(self, size):
      self.seq_list = []
      self.color = randomColor()
      self.alpha = randomAlpha()

      for i in xrange(2):
         x, y = randomXY(size)
         self.seq_list.append(x), self.seq_list.append(y)

   def drawTo(self, imgDraw):
      brush = aggdraw.Brush(tuple(self.color), self.alpha)
      imgDraw.rectangle(tuple(self.seq_list), brush)
    
   def mutate(self):
      for i in xrange(len(self.seq_list)):
         self.seq_list[i] += int(random.gauss(0, 5))
         self.seq_list[i] = max(0, self.seq_list[i])

      self.alpha += int(random.gauss(0, 5))
      self.alpha = min(max(10, self.alpha), 60)

      for i in xrange(len(self.color)):
         self.color[i] += int(random.gauss(0, 5))
         self.color[i] = min(max(0, self.color[i]), 255)

class DrawerAllele:
   def __init__(self, size):
      self.size = size
      self.drawers = [DrawPolygon, DrawChord, DrawEllipse, DrawPieslice, DrawRectangle]

   def getRandomAllele(self):
      drawerClass = random.choice(self.drawers)
      drawerInstance = drawerClass(self.size)
      return drawerInstance
      
def createImage(individual):
   imgInd = Image.new("RGB", size_tuple)
   imgDraw = aggdraw.Draw(imgInd)

   for f in individual:
      f.drawTo(imgDraw)
      
   imgDraw.flush()
   return imgInd

def eval_func(chromosome):
   global imgOriginal
   score = 0.0

   imgInd = createImage(chromosome)

   oR, oG, oB = imgOriginal.split()
   nR, nG, nB = imgInd.split()

   olR, olG, olB = oR.load(), oG.load(), oB.load()
   nlR, nlG, nlB = nR.load(), nG.load(), nB.load()

   for x in xrange(0, size_tuple[0]):
      for y in xrange(0, size_tuple[1]):
         dRed   = olR[x,y] - nlR[x,y]
         dGreen = olG[x,y] - nlG[x,y]
         dBlue  = olB[x,y] - nlB[x,y]
         pixelFitness = dRed * dRed + dGreen * dGreen + dBlue * dBlue
         score += pixelFitness

   return score

if __name__ == "__main__":

   size = 150

   genome = G1DListSafe(size)
   genome.evaluator.set(eval_func)

   genome.crossover.set(G1DListCrossoverSPSafe)
   genome.initializator.set(Initializators.G1DListInitializatorAllele)
   genome.mutator.set(G1DListMutatorDrawer)

   pallele = DrawerAllele(size_tuple)
   alleleSet = GAllele.GAlleles([pallele], homogeneous=True)
   
   genome.setParams(allele=alleleSet)
   ga = GSimpleGA.GSimpleGA(genome)
   ga.setGenerations(20000)
   ga.setMutationRate(0.03)
   ga.setCrossoverRate(0.9)
   #ga.setPopulationSize(50)
   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.evolve(freq_stats=10)

   best =  ga.bestIndividual()
   imgCreate = createImage(best)
   imgCreate.show()


