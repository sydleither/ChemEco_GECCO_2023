import numpy as np
import pandas as pd
import sys
import os
from analyze_final_pop import get_final_pop
from copy import deepcopy
from ydata_profiling import ProfileReport

def find_pareto(pops, fitnesses):
    fitness_names = [x for x in fitnesses[0].keys() if 'Score' in x]
    for index, fit in enumerate(fitnesses):
        for fit2 in fitnesses:
            if(fit['Biomass_Score'] < fit2['Biomass_Score'] and fit['Growth_Rate_Score'] < fit2['Growth_Rate_Score'] and fit['Heredity_Score'] < fit2['Heredity_Score'] and fit['Invasion_Ability_Score'] < fit2['Invasion_Ability_Score'] and fit['Resiliance_Score'] < fit2['Resiliance_Score']):
                pops[index] = 0
    final_pops = []
    final_fit = []
    for i in range(len(pops)):
        if pops[i] != 0 and fitnesses[i]['Biomass'] > 5000:
            pos_count = 0
            for f in fitness_names:
                if fitnesses[i][f] > 0:
                    pos_count += 1
            if pos_count > 1:
                final_pops.append(pops[i])
                final_fit.append(fitnesses[i])
                print(fitnesses[i])
    return final_pops, final_fit


def main():
    user = os.getlogin()
    root_path = f"/mnt/home/{user}/grant/chemical-ecology/results/"
    pops = []
    fitnesses = []
    for i in range(10):
        full_path = root_path + str(i)
        population, fitness = get_final_pop(full_path+'/evolve')
        pops.append(population)
        fitnesses.append(fitness)
    pareto_pops = []
    for i in range(10):
        ppops, pfits = find_pareto(deepcopy(pops[i]), deepcopy(fitnesses[i]))
        pareto_pops.append(ppops)
    for i, replicate in enumerate(pareto_pops):
        print(len(pareto_pops[i]), "genomes found on the pareto front for replicate", i)

    all_pops = [val for sublist in pareto_pops for val in sublist]
    df = pd.DataFrame(all_pops, columns=['diffusion', 'seeding', 'clear', 'clique_linkage', 'pct_pos_in', 'pct_pos_out', 'muw', 'beta', 'clique_size'])
    profile = ProfileReport(df, title="Profiling Report")
    profile.to_file("filtered_profile_report.html")


main()