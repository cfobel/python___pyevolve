from pyevolve import GSimpleGA
from pyevolve import G1DList, GAllele
from pyevolve import Mutators, Crossovers, Initializators
from pyevolve import Consts, Util
import Image
import aggdraw
import math
import operator
import random

imgOriginal = Image.open("monalisa_small.jpg")
size_tuple = imgOriginal.size

def G1DListPolyMutator(genome, **args):
   if args["pmut"] <= 0.0: return 0
   listSize = len(genome) - 1
   mutations = 0

   allele = genome.getParam("allele", None)
   if allele is None:
      Util.raiseException("to use the G1DListPolyMutator, you must specify the 'allele' parameter", TypeError)

   for it in xrange(listSize+1):
      if Util.randomFlipCoin(args["pmut"]):
         choice = [1,2,3]
         key = random.choice(choice)
         if key == 1:
            # mutate every parameter
            tar = genome[it]
            point_list = tar[0]
            rgb = tar[1]
            alpha = tar[2]

            plist_temp = []
            for i in point_list:
               plist_temp.append(i + random.gauss(0, 5))
            point_list = tuple(plist_temp)

            rgb_temp = []
            for i in rgb:
               v = i + int(random.gauss(0, 5))
               v = min(255, v)
               v = max(0, v)
               rgb_temp.append(v)
            rgb = tuple(rgb_temp)

            alpha += int(random.gauss(0,5))

            genome[it] = (point_list, rgb, alpha)
            mutations+=1

         elif key == 2: # swap
            Util.listSwapElement(genome, it, random.randint(0, listSize))
            mutations+=1

         elif key == 3: # mutate allele
            new_val = allele[it].getRandomAllele()
            genome[it] = new_val
            mutations+=1

   return mutations


class PolygonAllele:
   def __init__(self, size, max_points=5):
      self.max_points = max_points
      self.maxX = size[0]
      self.maxY = size[1]

   def getRandomAllele(self):
      num_points = random.randint(3, self.max_points)
      point_list = []
      for i in xrange(num_points):
         x, y = random.randint(0, self.maxX), random.randint(0, self.maxY)
         point_list.append(x)
         point_list.append(y)
      point_list = tuple(point_list)
      rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
      alpha = random.randint(10, 60)
      return (point_list, rgb, alpha)


def createImage(individual):
   imgInd = Image.new("RGB", size_tuple)
   imgDraw = aggdraw.Draw(imgInd)

   for i in xrange(len(individual)):
      poly_list = individual[i][0]
      color = individual[i][1]
      alpha = individual[i][2]
      brush = aggdraw.Brush(color, alpha)
      imgDraw.polygon(poly_list, brush)

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

   size = 20

   genome = G1DList.G1DList(size)
   genome.evaluator.set(eval_func)

   genome.crossover.set(Crossovers.G1DListCrossoverUniform)
   genome.initializator.set(Initializators.G1DListInitializatorAllele)
   genome.mutator.set(G1DListPolyMutator)

   pallele = PolygonAllele(size_tuple, 6)
   alleleSet = GAllele.GAlleles([pallele], homogeneous=True)
   
   genome.setParams(allele=alleleSet)
   ga = GSimpleGA.GSimpleGA(genome)
   ga.setGenerations(50000)
   ga.setMutationRate(0.2)
   ga.setCrossoverRate(0.9)
   ga.setPopulationSize(50)
   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.evolve(freq_stats=10)

   best =  ga.bestIndividual()
   a = createImage(best)
   a.show()


