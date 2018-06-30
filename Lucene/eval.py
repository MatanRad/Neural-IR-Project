#################################################################
#               IR project evaluation script                    #
#################################################################

import json
import sys

#!python2

def bsearch(sequence, value):
    lo, hi = 0, len(sequence) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sequence[mid]['id'] < value:
            lo = mid + 1
        elif value < sequence[mid]['id']:
            hi = mid - 1
        else:
            return mid
    return None

for arg in sys.argv:
	if arg == "-h":
		print("Usage: eval.py <qrels filepath> <questions filepath> <answers filepath>")
		sys.exit()

qrls = sorted(json.load(open(sys.argv[1],'r')), key=lambda k: k['id'])
questions = [line.rstrip('\n') for line in open(sys.argv[2],'r')]
answers = sorted(json.load(open(sys.argv[3],'r')), key=lambda k: k['id'])

sumAccuracy = 0.0;
sumMRR = 0.0;

for q in questions:
	qrl = qrls[bsearch(qrls, q.split('\t')[0])]
	relanswers = set(qrl['nbestanswers'])
	inx = bsearch(answers, qrl['id'])
	if inx is None:
		print("No answers for question id: "+qrl['id']+". This counts as no match!")
		continue
	#eval questions
	qanswers = sorted(answers[inx]['answers'], key=lambda k: k['score'], reverse=True)
	rank = 1
	matchFound = False
	for asw in qanswers:
		if asw['answer'] in relanswers:
			matchFound = True
			break
		rank += 1
		if rank == 6:
			break
	if matchFound:
		if rank == 1:
			sumAccuracy += 1
		sumMRR += 1.0 / rank

meanAcc = sumAccuracy / len(questions);
meanMRR = sumMRR / len(questions);
print("Accuracy: {}".format(meanAcc))
print("MRR@5: {}".format(meanMRR))
		
			
	
