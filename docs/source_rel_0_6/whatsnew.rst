
What's new ?
============================================================

What's new on the release |release|:

**Function Slots - Functions now have weights**
   
   Added a new `weight` parameter to the `add` method of the
   :class:`FunctionSlot.FunctionSlot` class. This parameter is
   used when you enable the *random apply* of the slot. See
   the class for more information.

**Multiprocessing - the use of multiprocessign module**

   Added a new method to the :class:`GSimpleGA.GSimpleGA` class, the
   :meth:`GSimpleGA.GSimpleGA.setMultiProcessing` method. With this
   method you can enable the use of **multiprocessing** python module.
   When you enable this option, Pyevolve will check if you have
   more than one CPU core and if there is support to the multiprocessing
   use. You **must** see the warning on the :meth:`GSimpleGA.GSimpleGA.setMultiProcessing`
   method.

**Scaling Scheme - the Boltzmann scaling**

   Added the Boltzmann scaling scheme, this scheme uses a temperature which is reduced
   each generation by a small amount. As the temperature decreases, the difference
   spread between the high and low fitnesses increases. See the description
   on the :func:`Scaling.BoltzmannScaling` function.


**Selectors - the alternative Tournament Selection**
   
   Added an alternative Tournament selection method, the :func:`Selectors.GTournamentAlternative`.
   This new Tournament Selector **don't uses** the Roulette Wheel method to pick individuals.


**Statistisc - two new statistical measures**
   
   Added the **fitTot** and the **rawTot** parameters to the :class:`Statistics.Statistics`
   class. See the class documentation for more information.

**Elitism - replacement option**
   
   Added the method :meth:`GSimpleGA.GSimpleGA.setElitismReplacement`. This method is used to set
   the number of individuals cloned on the elitism.

**String representation - resumeString**

   Added the method *resumeString* to all native chromosomes. This method returns a 
   small as possible string representation of the chromosome.

**Optimizations and bug-fixes**

   Added some general optimizations and bug-fixes.