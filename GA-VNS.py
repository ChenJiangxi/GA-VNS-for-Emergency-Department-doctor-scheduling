"""
Time: 2022-11-21
Author: Chen Jiangxi
Describe: Hybrid variable neighborhood search by genetic algorithm
"""

import copy
import random
from operator import attrgetter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import gen_solution
from gen_solution import Doctor, Solution
import VNS
import GVNS
            

def GAVNS(popsize, cr, mr, generation, kmax, iteration):
    epoch = 0
    interval = generation/2
    #init
    solution_set = gen_pop(popsize)
    best_solution = copy.deepcopy(solution_set.pop(0))
    while (epoch < generation):
        #crossover
        do_crossover = cr * popsize
        for i in range(0, int(do_crossover/2)):
            child1, child2 = crossover(solution_set[random.randint(0, popsize-1)], solution_set[random.randint(0, popsize-1)])
            solution_set.append(child1)
            solution_set.append(child2)
            
        #mutation
        do_mutation = mr * popsize
        for i in range(0, round(do_mutation)):
            solution_set.append(mutation(solution_set[random.randint(0, popsize-1)]))
        
        #VNS
        if (epoch % 2 == 0 or epoch == generation-1):
            n_repair = len(solution_set) - popsize
            for i in range (0, n_repair):
                solution_set[popsize + i] = VNS.VNS(solution_set[popsize + i], l_max = kmax, k_max = 1, iteration = iteration)
        
        #selection
        solution_set = selection(solution_set, popsize)

        cmpfun = attrgetter('obj')
        solution_set.sort(key = cmpfun)
        temp_best_solution = copy.deepcopy(solution_set.pop(0))
        if temp_best_solution.obj < best_solution.obj:
            best_solution = copy.deepcopy(temp_best_solution)
            objection_list.append(best_solution.obj)
            plot_obj(objection_list)
            gen_solution.plot_len(best_solution.length)
            gen_solution.store(best_solution, best_solution.obj, 'temp store week1/')

        epoch = epoch + 1
    #GVNS
    best_solution = GVNS.VNS(best_solution)
    objection_list.append(best_solution.obj)
    plot_obj(objection_list)
    gen_solution.plot_len(best_solution.length)
    gen_solution.store(best_solution, best_solution.obj, 'temp store week1/')


def plot_obj(y):
    x = [i for i in range(len(y))]
    plt.figure(figsize=(10,6),dpi=100)
    plt.plot(x, y, 'o-', alpha=0.5, linewidth=1, label='objection')
    plt.legend() 
    plt.xlabel('iteration')
    plt.ylabel('obj')
    plt.savefig("./obj-week1.png")
    plt.close()

def gen_pop(popsize):
    week1, week2 = gen_solution.read_data('lambda.csv')
    Doc_list = gen_solution.initial(10)
    solution = Solution(Doc_list, week1)
    solution.get_objection()
    best_sol = copy.deepcopy(solution)
    solution_set = []
    count = 0
    num = 0
    while(count < 4):
        if num > 100:
            num = 0
            solution = copy.deepcopy(best_sol)
            solution.doc_list.append(Doctor(random.randint(0,6)))
            count = solution.__len__() - 10
        solution = gen_solution.gen_init(solution)
        # solution.gen_code()
        solution_set.append(solution)
        if solution.get_objection() < best_sol.get_objection():
            best_sol = copy.deepcopy(solution)
        else:
            num += 1
            if solution.__len__() > 10:
                doctor = solution.doc_list[random.randint(10, solution.__len__() - 1)]
                doctor.__init__(random.randint(0,6))
    cmpfun = attrgetter('obj') #按照obj进行排序
    solution_set.sort(key = cmpfun)
    solution_set = copy.deepcopy(solution_set[0:popsize])
    print('solution_set_size', len(solution_set))
    return solution_set


#锦标赛选择法
def selection(solution_set, popsize):
    p = 0
    new_sol_set = []
    while p < (popsize + 1):
        sol_ind_list = random.sample(range(0, len(solution_set)), 5)
        temp_set = []
        for ind in sol_ind_list:
            temp_set.append(solution_set[ind])
        cmpfun = attrgetter('obj') 
        temp_set.sort(key = cmpfun)
        new_sol_set.append(temp_set.pop(0))
        p += 1
    new_sol_set.sort(key = cmpfun)
    return new_sol_set


def crossover(parent1, parent2):
    ind = random.randint(0, min(parent1.__len__(), parent2.__len__()) - 1)
    doc1 = copy.deepcopy(parent1.doc_list[ind])
    doc2 = copy.deepcopy(parent2.doc_list[ind])
    parent1.doc_list[ind] = copy.deepcopy(doc2)
    parent2.doc_list[ind] = copy.deepcopy(doc1)
    parent1.get_objection()
    parent2.get_objection()
    return parent1, parent2


#reduce doctor
def mutation(solution):
    solution = VNS.reduce_doc(solution)
    return solution

if __name__ == '__main__':
    objection_list = []

    populationsize = 20
    cr = 0.4
    mr = 0.3
    generation = 30
    kmax = 3
    iteration = 1

    GAVNS(populationsize, cr, mr, generation, kmax, iteration)