import logging
import pyevolve

import code
from pyevolve import(
    GSimpleGA,
    Consts,
)
from time import time
from sys import platform as sys_platform

if sys_platform[:3] == "win":
    from pyevolve import msvcrt


class GeneticAlgorithm(GSimpleGA.GSimpleGA):
    def evolve(self, freq_stats=0):
        """ Do all the generations until the termination criteria, accepts
        the freq_stats (default is 0) to dump statistics at n-generation

        :param freq_stats: if greater than 0, the statistics will be
                           printed every freq_stats generation.
        :rtype: returns the best individual of the evolution

        .. versionadded:: 0.6
           the return of the best individual

        """

        stopFlagCallback = False
        stopFlagTerminationCriteria = False

        self.time_init = time()

        logging.debug("Starting the DB Adapter and the Migration Adapter if any")
        if self.dbAdapter: self.dbAdapter.open(self)
        if self.migrationAdapter: self.migrationAdapter.start()

        if self.getGPMode():
            gp_function_prefix = self.getParam("gp_function_prefix")
            if gp_function_prefix is not None:
                self.__gp_catch_functions(gp_function_prefix)

        self.initialize()
        self.internalPop.evaluate()
        self.internalPop.sort()
        logging.debug("Starting loop over evolutionary algorithm.")

        try:
            while True:
                if self.migrationAdapter:
                    logging.debug("Migration adapter: exchange")
                    self.migrationAdapter.exchange()
                    self.internalPop.clearFlags()
                    self.internalPop.sort()

                if not self.stepCallback.isEmpty():
                    for it in self.stepCallback.applyFunctions(self):
                        stopFlagCallback = it

                if not self.terminationCriteria.isEmpty():
                    for it in self.terminationCriteria.applyFunctions(self):
                        stopFlagTerminationCriteria = it

                if freq_stats:
                    if (self.currentGeneration % freq_stats == 0) or (self.getCurrentGeneration() == 0):
                        self.printStats()
                        for i in range(0, 10):
                            print self.internalPop.bestFitness(i)
                if self.dbAdapter:
                    if self.currentGeneration % self.dbAdapter.getStatsGenFreq() == 0:
                        self.dumpStatsDB()

                if stopFlagTerminationCriteria:
                    logging.debug("Evolution stopped by the Termination Criteria !")
                    if freq_stats:
                        print "\n\tEvolution stopped by Termination Criteria function !\n"
                    break

                if stopFlagCallback:
                    logging.debug("Evolution stopped by Step Callback function !")
                    if freq_stats:
                        print "\n\tEvolution stopped by Step Callback function !\n"
                    break

                if self.interactiveMode:
                    if sys_platform[:3] == "win":
                        if msvcrt.kbhit():
                            if ord(msvcrt.getch()) == Consts.CDefESCKey:
                                print "Loading modules for Interactive Mode...",
                                logging.debug("Windows Interactive Mode key detected ! generation=%d",
                                              self.getCurrentGeneration())
                                from pyevolve import Interaction
                                print " done !"
                                interact_banner = "## Pyevolve v.%s - Interactive Mode ##\nPress CTRL-Z to quit interactive mode." % (
                                pyevolve.__version__,)
                                session_locals = {"ga_engine": self,
                                                  "population": self.getPopulation(),
                                                  "pyevolve": pyevolve,
                                                  "it": Interaction}
                                print
                                code.interact(interact_banner, local=session_locals)

                    if (self.getInteractiveGeneration() >= 0) and (
                        self.getInteractiveGeneration() == self.getCurrentGeneration()):
                        print "Loading modules for Interactive Mode...",
                        logging.debug("Manual Interactive Mode key detected ! generation=%d",
                                      self.getCurrentGeneration())
                        from pyevolve import Interaction
                        print " done !"
                        interact_banner = "## Pyevolve v.%s - Interactive Mode ##" % (pyevolve.__version__,)
                        session_locals = {"ga_engine": self,
                                          "population": self.getPopulation(),
                                          "pyevolve": pyevolve,
                                          "it": Interaction}
                        print
                        code.interact(interact_banner, local=session_locals)

                if self.step(): break  # exit if the number of generations is equal to the max. number of gens.

        except KeyboardInterrupt:
            logging.debug("CTRL-C detected, finishing evolution.")
            if freq_stats: print "\n\tA break was detected, you have interrupted the evolution !\n"

        if freq_stats != 0:
            self.printStats()
            self.printTimeElapsed()

        if self.dbAdapter:
            logging.debug("Closing the DB Adapter")
            if not (self.currentGeneration % self.dbAdapter.getStatsGenFreq() == 0):
                self.dumpStatsDB()
            self.dbAdapter.commitAndClose()

        if self.migrationAdapter:
            logging.debug("Closing the Migration Adapter")
            if freq_stats: print "Stopping the migration adapter... ",
            self.migrationAdapter.stop()
            if freq_stats: print "done !"

        return self.bestIndividual()
