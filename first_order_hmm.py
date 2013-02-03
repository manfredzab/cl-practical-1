#!/usr/bin/env python
import collections

tag_count = None
current_tag_previous_tag_count = None
token_tag_count = None

def train(train_file): 
    global tag_count, current_tag_previous_tag_count, token_tag_count
    
    tag_count = collections.defaultdict(int)
    current_tag_previous_tag_count = collections.defaultdict(int)
    token_tag_count = collections.defaultdict(int)
        
    # Collect counts of (current_tag, previous_tag) pairs
    for line in open(train_file):
        token_tag_line = line.split()
        
        for token, tag in [token_tag.rsplit('/', 1) for token_tag in token_tag_line]:
            token_tag_count[(token, tag)] += 1
            tag_count[tag] += 1
        
        tag_line = [token_tag.rsplit('/', 1)[1] for token_tag in token_tag_line].insert(0, '.')
        for (current_tag, previous_tag) in zip(tag_line[1:], tag_line[:-1]):
            current_tag_previous_tag_count[(current_tag, previous_tag)] += 1
    
    # TODO: for correct tagging, append './.' to the beginning of the test file

def test(test_file, readable, output_file):           
    # Output the most frequent tag for each test word. 
    # If the word is unknown, output the most frequent tag
    with open(output_file, 'w') as f_out:
        for line in open(test_file):
            sigma = []
            psi = []
            
            first_token = True;
            for token in line.split():
                sigma.append(collections.defaultdict(float));
                psi.append(collections.defaultdict(str));
            
                if (first_token):
                    for tag in tag_count:
                        sigma[-1][tag] = (current_tag_previous_tag_count[(tag, '.')] / tag_count[tag]) * (token_tag_count[(token, tag)] / tag_count[tag]) 
                        psi[-1][tag] = ''
                    
                    first_token = False
                else:
                    for tag in tag_count:
                        sigma[-1][tag] = (current_tag_previous_tag_count[(tag, '.')] / tag_count[tag]) * (token_tag_count[(token, tag)] / tag_count[tag]) 
                        psi[-1][tag] = ''                
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