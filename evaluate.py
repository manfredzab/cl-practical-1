def accuracy(ref_file, hyp_file):
	# Collect counts of (token,tag) pairs
	correct_count = 0
	total_count = 0
	
	for ref_sentence,hyp_sentence in zip(open(ref_file), open(hyp_file)):
		ref_tags = [x.rsplit('/',1)[1] for x in ref_sentence.split()]
		hyp_tags = [x.rsplit('/',1)[1] for x in hyp_sentence.split()]
		for ref_tag,hyp_tag in zip(ref_tags, hyp_tags):
			if ref_tag == hyp_tag:
				correct_count += 1
			total_count += 1

	accuracy = float(correct_count)/total_count
	print "Accuracy: %f (%d/%d)" % (accuracy, correct_count, total_count)
	
	return accuracy
