import json
import csv
import pathlib
import os
parent_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
### Collect statistics of fixations and jumps - all against on problematic words ###

setn = [1,2,3,4,5,6,7,8,9,10]
name_set = {'participant1': [1,3,4,5,6,7,8,9,10], 'participant2': [1,2,4,5,6,7,8,9,10], 'participant3': [1,2,3,4,5,6,7,9,10], 
            'participant4': [1,2,3,4,6,7,8,9,10], 'participant5': [1,2,3,5,6,7,8,9,10], 'participant6': [1,2,3,4,5,6,8,9,10], 
            'participant7': [1,2,3,4,5,7,8,9,10], 'participant8': [2,3,4,5,6,7,8,9,10]}
nums = [1,2,3,4,5,6,7,8,9,10]
names = ['participant1', 'participant2', 'participant3', 'participant4', 'participant5', 'participant6', 'participant7', 'participant8']

def check_fixations():
    for name in names:
        w = parent_folder + r'/mappings/{}/problematic_words.json'.format(name)
        f = open(w, 'r')
        words = json.load(f)
        result = parent_folder + r'/mappings/{}/fixations_stats.csv'.format(name)
        res = open(result, 'w', encoding='UTF8', newline='')
        header = ['set', 'screen', 'num_of_fixes', 'intersections']
        writer = csv.writer(res)
        writer.writerow(header)
        for s in name_set[name]:
            for num in nums:
                    fixes = parent_folder + r'/mappings/{}/set{}/corrected/traces/output/coords_with_time{}_fixations.json'.format(name,s,num)
                    if not pathlib.Path(fixes).is_file():
                        continue
                    fi = open(fixes, 'r')
                    fixations = json.load(fi)
                    
                    if not str(s) in words.keys():
                        continue
                    if str(num) in words[str(s)].keys():
                        words_coords = words[str(s)][str(num)]
                    else:
                        continue
                    row = []
                    row.append(s)
                    row.append(num)
                    row.append(len(fixations))
                    intrsc = 0
                    for fix in fixations:
                        for word in words_coords:
                            if fix[2] <= word[0] or word[2] <= fix[0]:
                                continue
                            if word[1] >= fix[3] or word[3] <= fix[1]:
                                continue
                            intrsc += 1
                    
                    row.append(intrsc)
                    
                    writer.writerow(row)
                        
def check_saccades():
    for name in names:
        w = parent_folder + r'/mappings/{}/problematic_words.json'.format(name)
        f = open(w, 'r')
        words = json.load(f)
        result = parent_folder + r'/mappings/{}/saccades_stats.csv'.format(name)
        res = open(result, 'w', encoding='UTF8', newline='')
        header = ['set', 'screen', 'num_of_jumps', 'intersections']
        writer = csv.writer(res)
        writer.writerow(header)
        for s in name_set[name]:
            for num in nums:
                ju = parent_folder + r'/mappings/{}/set{}/corrected/traces/output/coords_with_time{}_saccades.json'.format(name,s,num)
                if not pathlib.Path(ju).is_file():
                    continue
                j = open(ju, 'r')
                jumps = json.load(j)
                
                if not str(s) in words.keys():
                    continue
                if str(num) in words[str(s)].keys():
                    words_coords = words[str(s)][str(num)]
                else:
                    continue
                row = []
                row.append(s)
                row.append(num)
                row.append(len(jumps))
                intrsc = 0
                
                for jump in jumps:
                    for word in words_coords:
                        if float(jump[0]) >= word[0] - 50 and float(jump[0]) <= word[2] + 50 and float(jump[1]) >= word[1] - 40 and float(jump[1]) <= word[3] + 40:
                            intrsc += 1
                        #if float(jump[1][1]) >= word[0] - 50 and float(jump[1][1]) <= word[2] + 50 and float(jump[1][2]) >= word[1] - 40 and float(jump[1][2]) <= word[3] + 40:
                        #    intrsc += 1
                            
                row.append(intrsc)
                
                writer.writerow(row)