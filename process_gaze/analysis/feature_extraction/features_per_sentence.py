import csv
import json
import pathlib
import os
parent_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

setn = [1,2,3,4,5,6,7,8,9,10]
nums = [1,2,3,4,5,6,7,8,9,10]
names = ['participant1', 'participant2', 'participant3', 'participant4', 'participant5', 'participant6', 'participant7', 'participant8']

def fixations_per_sentence():
    for name in names:
        for s in setn:
            stat = parent_folder + r'\mappings\{}\set{}\fixations-per-sentence.csv'.format(name,s)
            statistics = open(stat, 'w', newline='')
            header = ['src', 'tgt1', 'tgt2']
            writer = csv.writer(statistics)
            writer.writerow(header)
            for num in nums:
                sent = parent_folder + r'\mappings\sentence_rectangulars\rects-coords{}.csv'.format(s)
                f = parent_folder + r'\mappings\{}\set{}\corrected\traces\output\coords_with_time{}_fixations.json'.format(name,s,num)
                if not pathlib.Path(f).is_file():
                    continue
                sentences = open(sent, 'r')
                f_json = open(f, 'r')
                fixes = json.load(f_json)
                sentences_reader = csv.reader(sentences, delimiter=',')

                src = 0
                tgt1 = 0
                tgt2 = 0

                sentence_rects = []
                for row in sentences_reader:
                    if row[0] == str(num):
                        sentence_rects.append(row[2:])
                
                
                
                src_x1 = float(sentence_rects[0][0])
                src_y1 = float(sentence_rects[0][1])
                src_x2 = float(sentence_rects[0][2])
                src_y2 = float(sentence_rects[0][3])

                tgt1_x1 = float(sentence_rects[1][0])
                tgt1_y1 = float(sentence_rects[1][1])
                tgt1_x2 = float(sentence_rects[1][2])
                tgt1_y2 = float(sentence_rects[1][3])

                tgt2_x1 = float(sentence_rects[2][0])
                tgt2_y1 = float(sentence_rects[2][1])
                tgt2_x2 = float(sentence_rects[2][2])
                tgt2_y2 = float(sentence_rects[2][3])
                
                for word in fixes:
                    if word[0] >= src_x1 and word[2] <= src_x2 and word[1] >= src_y1 and word[3] <= src_y2:
                        src += 1
                    if word[0] >= tgt1_x1 and word[2] <= tgt1_x2 and word[1] >= tgt1_y1 and word[3] <= tgt1_y2:
                        tgt1 += 1
                    if word[0] >= tgt2_x1 and word[2] <= tgt2_x2 and word[1] >= tgt2_y1 and word[3] <= tgt2_y2:
                        tgt2 += 1

                row = []
                row.append(src)
                row.append(tgt1)
                row.append(tgt2)
                writer.writerow(row)
    
def saccades_per_sentence():
    for name in names:
        for s in setn:
            stat = parent_folder + r'\mappings\{}\set{}\saccades-per-sentence.csv'.format(name,s)
            statistics = open(stat, 'w', newline='')
            header = ['src', 'tgt1', 'tgt2']
            writer = csv.writer(statistics)
            writer.writerow(header)
            for num in nums:
                sent = parent_folder + r'\mappings\sentence_rectangulars\rects-coords{}.csv'.format(s)
                f = parent_folder + r'\mappings\{}\set{}\corrected\traces\output\coords_with_time{}_saccades.json'.format(name,s,num)
                if not pathlib.Path(f).is_file():
                    continue
                sentences = open(sent, 'r')
                f_json = open(f, 'r')
                jumps = json.load(f_json)
                sentences_reader = csv.reader(sentences, delimiter=',')

                src = 0
                tgt1 = 0
                tgt2 = 0

                sentence_rects = []
                for row in sentences_reader:
                    if row[0] == str(num):
                        sentence_rects.append(row[2:])
                
                src_x1 = float(sentence_rects[0][0])
                src_y1 = float(sentence_rects[0][1])
                src_x2 = float(sentence_rects[0][2])
                src_y2 = float(sentence_rects[0][3])

                tgt1_x1 = float(sentence_rects[1][0])
                tgt1_y1 = float(sentence_rects[1][1])
                tgt1_x2 = float(sentence_rects[1][2])
                tgt1_y2 = float(sentence_rects[1][3])

                tgt2_x1 = float(sentence_rects[2][0])
                tgt2_y1 = float(sentence_rects[2][1])
                tgt2_x2 = float(sentence_rects[2][2])
                tgt2_y2 = float(sentence_rects[2][3])
                
                for jump in jumps:
                    x = float(jump[0])
                    y = float(jump[1])
                    if x >= src_x1 and x <= src_x2 and y >= src_y1 and y <= src_y2:
                        src += 1
                    if x >= tgt1_x1 and x <= tgt1_x2 and y >= tgt1_y1 and y <= tgt1_y2:
                        tgt1 += 1
                    if x >= tgt2_x1 and x <= tgt2_x2 and y >= tgt2_y1 and y <= tgt2_y2:
                        tgt2 += 1

                row = []
                row.append(src)
                row.append(tgt1)
                row.append(tgt2)
                writer.writerow(row)