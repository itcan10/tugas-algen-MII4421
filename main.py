import ga

from pyevolve import (
    G2DBinaryString,
    Selectors,
    Crossovers,
    Mutators,
    Consts
)
from random import choice as rand_choice

OFF_COEF = 0.4
STD_COEF = 0.6
PEAK_COEF = 1

OFF_RANGE = range(0, 11) + range(42, 47)
STD_RANGE = range(20, 29)
PEAK_RANGE = range(12, 19) + range(30, 41)
LIGHTS_OFF_RANGE = range(12, 35)
LIGHTS_ON_RANGE = range(0, 11) + range(36, 47)

LIGHTS_POWER = 0.25
TV_POWER = 0.114
DISHWASHER_POWER = 0.75
COMP_POWER = 0.05
POOL_PUMP_POWER = 1
WASHING_MACHINE_POWER = 0.75
STOVE_POWER = 1.5
MICROWAVE_POWER = 0.5

PENALTY = 999
POP_SIZE = 50
GENERATIONS = 100


def generate_chromosome(genome):
    genome.clearString()

    for i in xrange(genome.getHeight()):
        for j in xrange(genome.getWidth()):
            random_gene = rand_choice((0, 1))
            genome.setItem(i, j, random_gene)
            for u in LIGHTS_OFF_RANGE:
                genome.setItem(0, u, 0)
    return genome


def eval_func(chromosome):
    score = 0.0

    for w in xrange(chromosome.getWidth()):
        if sum(x.count(1) for x in [chromosome[1]]) >= 2:
            if chromosome[1][w] == 1 and w in OFF_RANGE:
                score += TV_POWER * OFF_COEF
            if chromosome[1][w] == 1 and w in STD_RANGE:
                score += TV_POWER * STD_COEF
            if chromosome[1][w] == 1 and w in PEAK_RANGE:
                score += TV_POWER * PEAK_COEF
        if sum(x.count(1) for x in [chromosome[2]]) >= 1:
            if chromosome[2][w] == 1 and w in OFF_RANGE:
                score += DISHWASHER_POWER * OFF_COEF
            if chromosome[2][w] == 1 and w in STD_RANGE:
                score += DISHWASHER_POWER * STD_COEF
            if chromosome[2][w] == 1 and w in PEAK_RANGE:
                score += DISHWASHER_POWER * PEAK_COEF
        if sum(x.count(1) for x in [chromosome[3]]) >= 5:
            if chromosome[3][w] == 1 and w in OFF_RANGE:
                score += COMP_POWER * OFF_COEF
            if chromosome[3][w] == 1 and w in STD_RANGE:
                score += COMP_POWER * STD_COEF
            if chromosome[3][w] == 1 and w in PEAK_RANGE:
                score += COMP_POWER * PEAK_COEF
        if sum(x.count(1) for x in [chromosome[4]]) >= 2:
            if chromosome[4][w] == 1 and w in OFF_RANGE:
                score += POOL_PUMP_POWER * OFF_COEF
            if chromosome[4][w] == 1 and w in STD_RANGE:
                score += POOL_PUMP_POWER * STD_COEF
            if chromosome[4][w] == 1 and w in PEAK_RANGE:
                score += POOL_PUMP_POWER * PEAK_COEF
        if sum(x.count(1) for x in [chromosome[5]]) >= 1:
            if chromosome[5][w] == 1 and w in OFF_RANGE:
                score += WASHING_MACHINE_POWER * OFF_COEF
            if chromosome[5][w] == 1 and w in STD_RANGE:
                score += WASHING_MACHINE_POWER * STD_COEF
            if chromosome[5][w] == 1 and w in PEAK_RANGE:
                score += WASHING_MACHINE_POWER * PEAK_COEF
        if sum(x.count(1) for x in [chromosome[6]]) >= 2:
            if chromosome[6][w] == 1 and w in OFF_RANGE:
                score += STOVE_POWER * OFF_COEF
            if chromosome[6][w] == 1 and w in STD_RANGE:
                score += STOVE_POWER * STD_COEF
            if chromosome[6][w] == 1 and w in PEAK_RANGE:
                score += STOVE_POWER * PEAK_COEF
        if sum(x.count(1) for x in [chromosome[7]]) >= 1:
            if chromosome[7][w] == 1 and w in OFF_RANGE:
                score += MICROWAVE_POWER * OFF_COEF
            if chromosome[7][w] == 1 and w in STD_RANGE:
                score += MICROWAVE_POWER * STD_COEF
            if chromosome[7][w] == 1 and w in PEAK_RANGE:
                score += MICROWAVE_POWER * PEAK_COEF
        else:
            score += PENALTY

    for i in LIGHTS_OFF_RANGE:
        for j in LIGHTS_ON_RANGE:
            if sum(row.count(1) for row in [chromosome[0]]) >= 6:
                if chromosome[0][i] == 1:
                    score += PENALTY
                if chromosome[0][j] == 1:
                    score += LIGHTS_POWER
            else:
                score += PENALTY

    return score


def run_main():
    chromosome = G2DBinaryString.G2DBinaryString(8, 48)
    chromosome = generate_chromosome(chromosome)

    chromosome.crossover.set(Crossovers.G2DBinaryStringXUniform)
    chromosome.mutator.set(Mutators.G2DBinaryStringMutatorSwap)
    chromosome.evaluator.set(eval_func)

    ga_instance = ga.GeneticAlgorithm(chromosome)
    ga_instance.setMinimax(Consts.minimaxType["minimize"])
    ga_instance.selector.set(Selectors.GRankSelector)
    ga_instance.setPopulationSize(POP_SIZE)
    ga_instance.setGenerations(GENERATIONS)
    ga_instance.evolve(freq_stats=1)

    print ga_instance.bestIndividual()

if __name__ == "__main__":
    run_main()

