from pyevolve import *
import math

rmse_accum = Util.ErrorAccumulator()

#@GTree.gpdec(representation="+", color="red")
def gp_add(a, b): return a+b

#@GTree.gpdec(representation="-")
def gp_sub(a, b): return a-b

#@GTree.gpdec(representation="*")
def gp_mul(a, b): return a*b

#@GTree.gpdec(representation="sqrt")
def gp_sqrt(a):   return math.sqrt(abs(a))
   
def eval_func(chromosome):
   global rmse_accum
   rmse_accum.reset()
   code_comp = chromosome.getCompiledCode()
   
   for a in xrange(0, 80):
      for b in xrange(0, 80):
         evaluated     = eval(code_comp)
         target        = math.sqrt((a*a)+(b*b))
         rmse_accum   += (target, evaluated)
   return rmse_accum.getRMSE()

def callback_draw(ga_engine):
   if ga_engine.getCurrentGeneration() == 0:
      GTree.GTreeGP.writePopulation(ga_engine, "full.jpg", 0, 10)
   return False


def main_run():
   genome = GTree.GTreeGP()
   genome.setParams(max_depth=4, method="ramped")
   genome.evaluator += eval_func
   genome.mutator.set(Mutators.GTreeGPMutatorSubtree)

   ga = GSimpleGA.GSimpleGA(genome, seed=666)
   ga.setParams(gp_terminals       = ['a', 'b'],
                gp_function_prefix = "gp")

   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setGenerations(20)
   #ga.stepCallback.set(callback_draw)
   ga.setCrossoverRate(1.0)
   ga.setMutationRate(0.08)
   ga.setPopulationSize(800)
   ga.setMultiProcessing(False)
   
   ga(freq_stats=5)
   best = ga.bestIndividual()
   #print best

if __name__ == "__main__":
   main_run()
