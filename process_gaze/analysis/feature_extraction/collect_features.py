import csv
import json
import pathlib
import os
parent_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

setn = [1,2,3,4,5,6,7,8,9,10]
nums = [1,2,3,4,5,6,7,8,9,10]
names = ['participant1', 'participant2', 'participant3', 'participant4', 'participant5', 'participant6', 'participant7', 'participant8']

def collect_fixations():
    for name in names:
        for s in setn:
            print(s)
            for num in nums:
                tr = parent_folder + r'\mappings\{}\set{}\corrected\traces\coords_with_time{}.csv'.format(name,s,num)
                senten = parent_folder + r'\mappings\sentence_rects\rects-coords{}.csv'.format(s)
                if not pathlib.Path(tr).is_file():
                    continue
                sentences = open(senten, 'r')
                sentences_reader = csv.reader(sentences, delimiter=',')
                sent_coords = []
                for row in sentences_reader:
                    if row[0] == str(num):
                        sent_coords.append(row[2:])
                
                trace = open(tr, 'r')
                trace_reader = csv.reader(trace, delimiter=',')
                all_points = []
                line_count = 0
                for row in trace_reader:
                    if line_count == 0:
                        line_count += 1
                        continue
                    all_points.append(row)
                fixations = []
                i = 0
                for sent in sent_coords:
                    win_x1 = float(sent[0])
                    win_y1 = float(sent[1]) + 20
                    win_x2 = win_x1 + 224
                    win_y2 = win_y1 + 70
                    
                    while win_y2 <= float(sent[3])-20 and win_y1 < win_y2:
                        while win_x2 <= float(sent[2]) and win_x1 < win_x2:
                            gaze_collection = []
                            for row in all_points:
                                x = float(row[1])
                                y = float(row[2])
                                if x >= win_x1 and x <= win_x2 and y >= win_y1 and y <= win_y2:
                                    gaze_collection.append(row)

                            if len(gaze_collection) > 0:
                                init = 0
                                for item in gaze_collection:
                                    if init == 0:
                                        init = float(item[0])
                                    else:
                                        diff = float(item[0]) - init
                                        if diff <= 0.5 and diff >= 0.480: 
                                            fixations.append([win_x1, win_y1, win_x2, win_y2])
                                        elif diff > 0.5:
                                            init = float(item[0])
                            if win_x2 + 224 <= float(sent[2]):
                                win_x2 += 224
                            else: 
                                win_x2 = float(sent[2])
                            win_x1 += 224
                        if win_y2 + 70 <= float(sent[3]) - 20:
                            win_y2 += 70
                        else: 
                            win_y2 = float(sent[3]) - 20
                        win_y1 += 70
                        win_x1 = float(sent[0])
                        win_x2 = win_x1 + 224
                
                list_of_fixes = []
                if len(fixations) == 0:
                    continue
                start = fixations[0]
                x1 = start[0]
                y1 = start[1]
                x2 = start[2]
                y2 = start[3]
                prev_x1 = x1
                prev_x2 = x2
                for item in fixations:
                    if item[1] == y1 and item[3] == y2:
                        if item[0] - prev_x1 == 30 or item[0] - prev_x1 == 0:
                            prev_x1 = item[0]
                            prev_x2 = item[2]
                        else:
                            fix = [x1,y1,prev_x2,y2]
                            list_of_fixes.append(fix)
                            x1 = item[0]
                            y1 = item[1]
                            x2 = item[2]
                            y2 = item[3]
                            prev_x1 = x1
                            prev_x2 = x2
                    else:
                        fix = [x1,y1,prev_x2,y2]
                        list_of_fixes.append(fix)
                        x1 = item[0]
                        y1 = item[1]
                        x2 = item[2]
                        y2 = item[3]
                        prev_x1 = x1
                        prev_x2 = x2
                
                fix = [x1,y1,prev_x2,y2]
                list_of_fixes.append(fix)
                
                processed_fix = parent_folder + r'\mappings\{}\set{}\corrected\fixations\processed-fix{}.json'.format(name,s,num)
                out_file = open(processed_fix, "w")
                json.dump(list_of_fixes, out_file)
                out_file.close()
    
def collect_jumps():
    for name in names:
        for s in setn:
            for num in nums:
                print(num)
                tr = parent_folder + r'\mappings\{}\set{}\corrected\traces\coords_with_time{}.csv'.format(name,s,num)
                if not pathlib.Path(tr).is_file():
                    continue
                trace = open(tr, 'r', newline='')
                trace_reader = csv.reader(trace, delimiter=',')
                all_points = []
                line_count = 0
                for row in trace_reader:
                    if line_count == 0:
                        line_count += 1
                        continue
                    all_points.append(row)
                    
                start = []
                jumps = []
                jump = []
                for row in all_points:
                    if start == []:
                        start = row
                        continue
                    else:
                        if float(row[2]) - float(start[2]) >= 200 or float(row[2]) - float(start[2]) <= -200:
                            jump.append(start)
                            jump.append(row)
                            jumps.append(jump)
                            jump = []
                            start = row
                
                jumps_f = parent_folder + r'\mappings\{}\set{}\corrected\jumps\jumps{}.json'.format(name,s,num)
                out_file = open(jumps_f, "w")

                json.dump(jumps, out_file)

                out_file.close()