# eye-tracking-mt-evaluation-project
Code for eye tracking MT evalution project (without actual eye tracking tool - Eyewarebeam was used). 

index.html - homepage, run on localhost:8000

# Project structure

./collected_data/raw_data contains all data collected for each participant: 
    /participant{}/clicked_words - clicked problematic words for each set of screens with their coordinates  
    /participant{}/timestamps - timestamps of the beginning and the end of reading each screen + chosen best translation
    /participant{}/track - raw data from eye tracker

./collected_data/results contains tables for each set of screens with chosen best translation for each screen by each participant

./data - sentences for each set of screens (used for calling it from frontend part)

./process_gaze/analysis contains code used for data processing and analysis

./process_gaze/mapping contains the following data per participant:
    /participant{}/fix_stats_h.csv - statistics for fixations: number of fixations per screen and number of intersections between fixations and problematic words
    /participant{}/jump_stats_h.csv - statistics for jumps(saccades): number of jumps per screen and number of intersections between jumps and problematic words
        /participant{}/set{}/corrected/screen{}_map_corrected.jpg - mapping of gaze trace corrected along the y-axis
        /participant{}/set{}/map_fixations_and_problem_words - each screen with mapped fixations (green) and problematic words (red)
        /participant{}/set{}/h-fixes-per-sentence.csv - number of fixations per each sentence on each screen
        /participant{}/set{}/jumps-per-sentence.csv - number of jumps per each sentence on each screen
        /participant{}/set{}/src{}.txt - raw data from eye tracker
        /participant{}/set{}/screen{}_map.jpg - mapping of the trace to the screen