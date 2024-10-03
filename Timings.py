import CombatSim
import timeit


# tm = timeit.Timer('stmt=CombatSim.startSimulator()')
print(timeit.repeat('MonteCarloCombatSim.startSimulator()', number=100, setup='import MonteCarloCombatSim'))
# CombatSim.startSimulator()