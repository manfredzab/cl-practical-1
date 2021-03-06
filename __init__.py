import pos_tagger_unigram, pos_tagger_hmm, cross_validation, evaluate

# Cross-validation corpus generation
# cross_validation.generate_10_fold_corpus("danish.train", "danish")

# Cross-validation corpus print-out (for debugging purposes)
#for section in range(10):
#    print "==================================="
#    print "Training file " + str(section) + ":"
#    print "-----------------------------------"
#    
#    for line in open("train/temp" + str(section)):
#        print line,
#    print
#    
#    print "-----------------------------------"
#    print "Evaluation file " + str(section) + ":"
#    
#    for line in open("eval/temp" + str(section)):
#        print line,
#    print
#
#    print "-----------------------------------"
#    print "Testing file " + str(section) + ":"
#    
#    for line in open("test/temp" + str(section)):
#        print line,
#    print
#    
#    print "==================================="
#    print

# Training and testing
avg_accuracy = 0.0
for section in range(10):
    pos_tagger_hmm.train("train/danish" + str(section))
    pos_tagger_hmm.test("test/danish" + str(section), True, "hyp/danish" + str(section))
    avg_accuracy += evaluate.accuracy("eval/danish" + str(section), "hyp/danish" + str(section))
    
print "Average accuracy: " + str(avg_accuracy / 10.0)

#pos_tagger_hmm.train("danish.train")
#pos_tagger_hmm.test("danish.test", False, "output.csv")

#pos_tagger_hmm.train("train/hmm_testing0")
#pos_tagger_hmm.test("test/hmm_testing0", True, "out.txt")