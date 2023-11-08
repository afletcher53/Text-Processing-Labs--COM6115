"""\
------------------------------------------------------------
USE: python <PROGNAME> (options) file1...fileN
OPTIONS:
    -h : print this help message
    -s FILE : use stoplist file FILE
    -p : use Porter stemming (default: no stemming)
    -b : use BINARY weights (default: count weighting)
------------------------------------------------------------\
"""

import sys, re, getopt
import glob
from nltk.stem import PorterStemmer
opts, args = getopt.getopt(sys.argv[1:], 'hs:pbI:')
opts = dict(opts)

##############################
# HELP option

if '-h' in opts:
    progname = sys.argv[0]
    progname = progname.split('/')[-1] # strip out extended path
    help = __doc__.replace('<PROGNAME>', progname, 1)
    print(help, file=sys.stderr)
    sys.exit()



##############################
# Identify input files, when "-I" option used

print(sys.argv)
if '-I' in opts:
    # get all files matching pattern
    filenames = glob.glob(opts['-I'])
else:
    filenames = args

# Check if filenames are being found 
# (comment out after checking)
print('INPUT-FILES:', filenames, file=sys.stderr)

##############################
# STOPLIST option

stops = set()
if '-s' in opts:
    with open(opts['-s'], 'r') as stop_fs:
        for line in stop_fs :
            stops.add(line.strip())
            


##############################
# Stemming function

stemmer = PorterStemmer().stem

def stem_word(word):
    return stemmer(word)

##############################
# Port stemming function

if '-p' in opts:
    stops = set([stem_word(x) for x in stops])

##############################
# COUNT-WORDS function. 
# Takes 2 inputs: 1= FILE-NAME, 2= stoplist
# Returns a dictionary of word counts
import re
def count_words(filename, stops):
    counts = {}
    file_words = open(filename, 'r')

   
    for line in file_words:
        if '-p' in opts:
            # stem each word in line and return as string
            line = ' '.join([stem_word(x) for x in line.split()])
        for element in line.split():
            element = re.sub(r'[^\w\s]', '', element)
            element = element.lower()
            if element not in stops:
                counts[element] = counts.get(element, 0) + 1
    return counts
    

##############################
# Compute counts for individual documents

docs = [ ]


for infile in filenames:
    docs.append(count_words(infile, stops))


##############################
# Compute similarity score for document pair
# Inputs are dictionaries of counts for each doc
# Returns similarity score
import numpy as np
def jaccard(doc1, doc2):
    """Calculates the Jaccard similarity coefficient between two documents.

    Args:
        doc1: A dictionary mapping words to their counts.
        doc2: A dictionary mapping words to their counts.

    Returns:
        The Jaccard similarity coefficient between the two documents.
    """
    doc1_set = set(doc1.keys())
    doc2_set = set(doc2.keys())
    if '-b' in opts:
        doc1 = set(doc1.keys())
        doc2 = set(doc2.keys())
   
        numerator = len(doc1_set.intersection(doc2_set))
        demoninator = len(doc1_set.union(doc2_set))

    else:
        
        w = doc1_set.union(doc2_set)
        #map dictionaries so that only words in both dictionaries are counted
        doc1 = {k: doc1.get(k, 0) for k in w}
        doc2 = {k: doc2.get(k, 0) for k in w}

    
        #calculate minumum value of each dictionary

        doc1_min_count = np.array(list(doc1.values()))
        doc2_min_count = np.array(list(doc2.values()))
        #calculate maximum value of each dictionary
        doc1_max_count = np.array(list(doc1.values()))
        doc2_max_count = np.array(list(doc2.values()))

        #calculate numerator and denominator
        numerator = np.sum(np.minimum(doc1_min_count, doc2_min_count))
        demoninator = np.sum(np.maximum(doc1_max_count, doc2_max_count))

    return numerator/demoninator

##############################
# Compute scores for all document pairs

results = {}
for i in range(len(docs)-1):
    for j in range(i+1, len(docs)):        
        pair_name = '%s <> %s' % (filenames[i], filenames[j])
        results[pair_name] = jaccard(docs[i], docs[j])

##############################
# Sort, and print top N results

top_N = 20

pairs = list(results) # DUMMY CODE LINE 

# Replace with code to sort results based on scores.
# Have only results for highest "top_N" scores printed.

# Printing
c = 0

for pair in pairs:
    c += 1
    print('[%d] %s = %.3f' % (c, pair, results[pair]), file=sys.stdout)

##############################

