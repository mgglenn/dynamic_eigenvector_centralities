# Dynamic Eigenvector Centralities
## Paper / Purpose
This code serves as an implementation of the work on calculating keywords and their emerging importance outlined here: https://people.cs.clemson.edu/~isafro/papers/dynamic-centralities.pdf

## Requirements
1. All code is run in Python 3.6 (Anaconda 4.3.0)
2. Data to be processed should be stored in ordered text files (i.e., file1.txt, file2.txt, ... fileN.txt for N intervals, or some other numbered format.)
3. Text files should contain one-document (i.e., one tweet) per line

## Usage
* Ensure all requirements are satisfied. The program can be run as follows.
```
# after repo has been downloaded
cd dynamic_eigenvector_centralities
python dec_main.py --input_folder /home/username/time_series_data/ --P 6 --output_folder /home/username/dec_results/
```

## Files
* `dec_main.py` Runs the full algorithm to compute DEC values described in the 
* `dec_graph.py` contains code for the graph logic of the algorithm
* `dec_text.py` contains code for preprocessing and cleaning the data
* `break_files.py` a useful script for dividing time-series CSV data
