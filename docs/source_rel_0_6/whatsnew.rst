
What's new ?
============================================================

What's new on the release |release|:

**Optimizations and bug-fixes**

   Added some general optimizations and bug-fixes. The code is more *pythonic* now.

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

**Statistics - two new statistical measures**
   
   Added the **fitTot** and the **rawTot** parameters to the :class:`Statistics.Statistics`
   class. See the class documentation for more information.

**Elitism - replacement option**
   
   Added the method :meth:`GSimpleGA.GSimpleGA.setElitismReplacement`. This method is used to set
   the number of individuals cloned on the elitism.

**String representation - resumeString**

   Added the method *resumeString* to all native chromosomes. This method returns a 
   small as possible string representation of the chromosome.

**DB Adapter - XML RPC**
   
   Added a new DB Adapter to send Pyevolve statistics, the XML RPC, to see more information,
   access the docs of the :class:`DBAdapters.DBXMLRPC`.

**DB Adapters - OO redesigned**

   The DB Adapters were redesigned and now there is a super class for all DB Adapters, you
   can create your own DB Adapters subclassing the :class:`DBAdapters.DBBaseAdapter` class.

**The Network module - lan/wan networking**
   
   Added the :mod:`Network` module, this module is used to keep all the
   networking related classes, currently it contains the threaded UDP client/server.
   
**The Migration module - distributed GA**
   
   Added the :mod:`Migration` module, this module is used to control the
   migration of the distributed GA.

**The G2DBinaryString module - the 2D Binary String**

   Added the :mod:`G2DBinaryString` module. This module contains
   the 2D Binary String chromosome representation.

**1D chromosomes - new base class**

   All the 1D choromsomes representation is now extending the
   :class:`GenomeBase.G1DBase` base class.

**Tree chromosome - new Tree representation chromosome**

   Added the module :mod:`GTree`, this module contains the
   new GTree chromosome representation and all tree related
   functions.