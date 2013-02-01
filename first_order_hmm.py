#!/usr/bin/env python
import collections

tags = None
token_tag_count = None
global_max_tag = None

def train(train_file): 
    global tags, token_tag_count, global_max_tag
    
    tags = collections.defaultdict(int)
    token_tag_count = collections.defaultdict(int)
        
    # Collect counts of (token,tag) pairs
    for line in open(train_file):
        for token, tag in [x.rsplit('/', 1) for x in line.split()]:
            token_tag_count[(token, tag)] += 1
            tags[tag] += 1
    
    # find the most frequent tag
    global_max_tag_frequency = 0
    for tag in tags:
        if tags[tag] > global_max_tag_frequency:
            global_max_tag_frequency = tags[tag]
            global_max_tag = tag


def test(test_file, readable, output_file):    
    # Output the most frequent tag for each test word. 
    # If the word is unknown, output the most frequent tag
    with open(output_file, 'w') as f_out:
        for line in open(test_file):
            tokenized_line = []
            for token in line.split():
                max_tag = None
                max_tag_frequency = 0
                for tag in tags:
                    if token_tag_count[(token, tag)] > max_tag_frequency:
                        max_tag_frequency = token_tag_count[(token, tag)]
                        max_tag = tag
                if max_tag == None:
                    max_tag = global_max_tag
                if readable:
                    tokenized_line.append("%s/%s" % (token, max_tag))
                else:
                    f_out.write(max_tag + "\n")
            if readable:
                f_out.write(' '.join(tokenized_line) + "\n")