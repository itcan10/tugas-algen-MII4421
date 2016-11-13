from pyevolve import (
    G2DBinaryString,
    GSimpleGA,
    Selectors,
    Crossovers,
    Mutators,
    Consts
)
from random import choice as rand_choice


def generate_chromosome(genome):
    genome.clearString()

    for i in xrange(genome.getHeight()):
        for j in xrange(genome.getWidth()):
            random_gene = rand_choice((0, 1))
            genome.setItem(i, j, random_gene)
            for u in range(12, 35):
                genome.setItem(0, u, 0)
    return genome


def eval_func(chromosome):
    score = 0.0

    for w in xrange(chromosome.getWidth()):
        if sum(x.count(1) for x in [chromosome[1]]) >= 2:
            if chromosome[1][w] == 1:
                score += 1
        if sum(x.count(1) for x in [chromosome[2]]) >= 1:
            if chromosome[2][w] == 1:
                score += 1
        if sum(x.count(1) for x in [chromosome[3]]) >= 5:
            if chromosome[3][w] == 1:
                score += 1
        if sum(x.count(1) for x in [chromosome[4]]) >= 2:
            if chromosome[4][w] == 1:
                score += 1
        if sum(x.count(1) for x in [chromosome[5]]) >= 1:
            if chromosome[5][w] == 1:
                score += 1
        if sum(x.count(1) for x in [chromosome[6]]) >= 2:
            if chromosome[6][w] == 1:
                score += 1
        if sum(x.count(1) for x in [chromosome[7]]) >= 1:
            if chromosome[7][w] == 1:
                score += 1

    for i in range(12, 35):
        for j in range(0, 11) + range(36, 47):
            if sum(row.count(1) for row in [chromosome[0]]) >= 6:
                if chromosome[0][i] == 1:
                    score += 999
                if chromosome[0][j] == 1:
                    score += 1
            else:
                score += 999

    return score


def run_main():
    chromosome = G2DBinaryString.G2DBinaryString(8, 48)
    chromosome.crossover.set(Crossovers.G2DBinaryStringXSingleHPoint)
    chromosome.mutator.set(Mutators.G2DBinaryStringMutatorSwap)

    # Generate chromosome
    chromosome = generate_chromosome(chromosome)

    # The evaluator function (objective function)
    chromosome.evaluator.set(eval_func)

    # Genetic Algorithm Instance
    ga = GSimpleGA.GSimpleGA(chromosome)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.selector.set(Selectors.GRankSelector)
    ga.setPopulationSize(20)
    ga.setGenerations(200)

    # Do the evolution
    ga.evolve(freq_stats=10)

    # Best individual
    print ga.bestIndividual()

if __name__ == "__main__":
    run_main()

