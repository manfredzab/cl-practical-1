import zeroth_order_hmm, cross_validation, evaluate

cross_validation.generate_10_fold_corpus("danish.train", "danish")

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

avg_accuracy = 0.0
for section in range(10):
    zeroth_order_hmm.train("train/danish" + str(section))
    zeroth_order_hmm.test("test/danish" + str(section), True, "hyp/danish" + str(section))
    avg_accuracy += evaluate.accuracy("eval/danish" + str(section), "hyp/danish" + str(section))
    
print "Average accuracy: " + str(avg_accuracy / 10.0) 