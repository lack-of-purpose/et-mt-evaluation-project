# eye-tracking-mt-evaluation-project
Code for eye tracking MT evalution project (without actual eye tracking tool - Eyewarebeam was used). 

index.html - homepage, run on localhost:8000

# Project structure

./collected_data/raw_data contains all data collected for each participant: 
 - /participant{}/clicked_words - _clicked problematic words for each set of screens with their coordinates_
 - /participant{}/timestamps - _timestamps of the beginning and the end of reading each screen + chosen best translation_
 - /participant{}/track - _raw data from eye tracker_

./collected_data/results _contains tables for each set of screens with chosen best translation for each screen by each participant_

./data - _sentences for each set of screens (used for calling it from frontend part)_

./process_gaze/analysis _contains code used for data processing and analysis_

./process_gaze/mapping _contains the following data per participant:_
 - /participant{}/fix_stats_h.csv - _statistics for fixations: number of fixations per screen and number of intersections between fixations and problematic words_
 - /participant{}/jump_stats_h.csv - _statistics for jumps(saccades): number of jumps per screen and number of intersections between jumps and problematic words_
   - /participant{}/set{}/corrected/screen{}_map_corrected.jpg - _mapping of gaze trace corrected along the y-axis_
   - /participant{}/set{}/map_fixations_and_problem_words - _each screen with mapped fixations (green) and problematic words (red)_
   - /participant{}/set{}/h-fixes-per-sentence.csv - _number of fixations per each sentence on each screen_
   - /participant{}/set{}/jumps-per-sentence.csv - _number of jumps per each sentence on each screen_
   - /participant{}/set{}/src{}.txt - _raw data from eye tracker_
   - /participant{}/set{}/screen{}_map.jpg - _mapping of the trace to the screen_