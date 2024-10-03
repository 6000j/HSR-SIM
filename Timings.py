import CombatSim
import MonteCarloCombatSim
import timeit
import cProfile
import pstats
from pstats import SortKey


# tm = timeit.Timer('stmt=CombatSim.startSimulator()')
# print(timeit.repeat('MonteCarloCombatSim.startSimulator()', number=100, setup='import MonteCarloCombatSim'))
# CombatSim.startSimulator()

cProfile.run('CombatSim.startSimulator()', 'Output/statss')

p = pstats.Stats('Output/statss')
p.strip_dirs().sort_stats('tottime').print_stats()