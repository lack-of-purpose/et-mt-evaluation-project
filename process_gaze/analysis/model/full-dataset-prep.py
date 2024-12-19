import csv
import os
import numpy as np
parent_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

setn = [1,2,3,4,5,6,7,8,9,10]
#setn = [3]
names = ['participant1', 'participant2', 'participant3', 'participant4', 'participant5', 'participant6', 'participant7', 'participant8']
#names = ['participant3']
columns = [2,3,8,6,4,5,7,1]
#columns = [8]

for name, column in zip(names,columns):
    all_data = parent_folder + r'\analysis\model\all-data-{}.csv'.format(name)
    f = open(all_data, 'w', newline='')
    header = ['fixations_tgt1', 'jumps_tgt1', 'time_tgt1', 'fixations_tgt2', 'jumps_tgt2', 'time_tgt2', 'choice']
    writer = csv.writer(f)
    writer.writerow(header)
    for s in setn:
        fixes = parent_folder + r'\mappings\{}\set{}\fixations-per-sentence.csv'.format(name,s)
        fixations = open(fixes, 'r')
        fixations_reader = csv.reader(fixations, delimiter=',')
        j = parent_folder + r'\mappings\{}\set{}\saccades-per-sentence.csv'.format(name,s)
        jumps = open(j, 'r')
        jumps_reader = csv.reader(jumps, delimiter=',')
        st = parent_folder + r'\mappings\{}\set{}\stats.csv'.format(name,s)
        stats = open(st, 'r')
        stats_reader = csv.reader(stats, delimiter=',')
        res = parent_folder + r'\analysis\model\set{}_results.csv'.format(s)
        results = open(res, 'r')
        results_reader = csv.reader(results, delimiter=',')
        choice = [2]
        for r in results_reader:
            if r[0] == 'num':
                continue
            if r[column] == 'NaN':
                choice.append(None)
            if r[column] == '1':
                choice.append(0)
            if r[column] == '2':
                choice.append(1)
        count = 0
        for fix,jum,sta,ch in zip(fixations_reader,jumps_reader,stats_reader,choice):
            if count == 0:
                count += 1
                continue
            row = []
            if fix[1] == 'NaN':
                row.append(np.nan)
            else: 
                row.append(int(fix[1]))
            if jum[1] == 'NaN':
                row.append(np.nan)
            else: 
                row.append(int(jum[1]))
            if sta[1] == 'NaN':
                row.append(np.nan)
            else: 
                row.append(int(sta[1]))
            if fix[2] == 'NaN':
                row.append(np.nan)
            else: 
                row.append(int(fix[2]))
            if jum[2] == 'NaN':
                row.append(np.nan)
            else: 
                row.append(int(jum[2]))
            if sta[2] == 'NaN':
                row.append(np.nan)
            else: 
                row.append(int(sta[2]))
            if ch == None:
                row.append(np.nan)
            else: 
                row.append(ch)
            writer.writerow(row)
            
            