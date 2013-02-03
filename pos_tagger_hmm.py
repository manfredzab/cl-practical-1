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
        
        tag_line = [token_tag.rsplit('/', 1)[1] for token_tag in token_tag_line]
        # Add '.' as a start symbol
        tag_line.insert(0, '.')
        
        for (current_tag, previous_tag) in zip(tag_line[1:], tag_line[:-1]):
            current_tag_previous_tag_count[(current_tag, previous_tag)] += 1
    
    # TODO: for correct tagging, append './.' to the beginning of the test file

def test(test_file, readable, output_file):           
    # Output the most frequent tag for each test word. 
    # If the word is unknown, output the most frequent tag
    with open(output_file, 'w') as f_out:
        if (not readable):
            f_out.write("Tag\n")
            
        for line in open(test_file):
            sigma = []
            psi = []
            
            tokenized_line = line.split()
            
            first_token = True
            for token in tokenized_line:
                sigma.append(collections.defaultdict(float));
                psi.append(collections.defaultdict(str));
            
                if (first_token):
                    for tag in tag_count:
                        sigma[-1][tag] = (current_tag_previous_tag_count[(tag, '.')] / float(tag_count['.'])) * (token_tag_count[(token, tag)] / float(tag_count[tag])) 
                        psi[-1][tag] = ''
                    
                    first_token = False
                else:
                    for tag_k in tag_count:
                        max_tag = None
                        max_tag_prob = -1.0;
                        
                        for tag_i in tag_count:
                            prob = sigma[-2][tag_i] * (current_tag_previous_tag_count[(tag_k, tag_i)] / float(tag_count[tag_i])) * (token_tag_count[(token, tag_k)] / float(tag_count[tag_k]))
                            if (prob > max_tag_prob):
                                max_tag_prob = prob
                                max_tag = tag_i
                        
                        sigma[-1][tag_k] = max_tag_prob  
                        psi[-1][tag_k] = max_tag
                        
            
            # Output holder
            output_line = []
            
            # Start backtracking the tags
            tokenized_line.reverse()
            
            i = 0
            max_tag = None            
            last_token = True
            
            for token in tokenized_line:               
                
                if (last_token):
                    max_prob = -1.0
                    
                    for tag in tag_count:
                        prob = sigma[-1][tag]                        
                        if (prob > max_prob):
                            max_prob = prob
                            max_tag = tag
                                   
                    last_token = False                     
                
                else:
                    max_tag = psi[-i][max_tag]
                
                i = i + 1
                
                if readable:
                    output_line.insert(0, "%s/%s" % (token, max_tag))
                else:
                    output_line.insert(0, max_tag + "\n")
                    
            if readable:
                print (' '.join(output_line) + "\n"),
            else:
                f_out.write(''.join(output_line))