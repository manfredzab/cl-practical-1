#!/usr/bin/env python
import collections, math

tag_count = None
token_count = None
current_tag_previous_tag_count = None
token_tag_count = None
singleton_tag_tag_count = None
singleton_tag_word_count = None

def train(train_file): 
    global tag_count, token_count, current_tag_previous_tag_count, token_tag_count, singleton_tag_tag_count, singleton_tag_word_count 
    
    # Initialize count dictionaries
    tag_count = collections.defaultdict(int)
    token_count = collections.defaultdict(int)
    current_tag_previous_tag_count = collections.defaultdict(int)
    token_tag_count = collections.defaultdict(int)
    singleton_tag_tag_count = collections.defaultdict(int)
    singleton_tag_word_count = collections.defaultdict(int)
        
    # Collect various counts
    for line in open(train_file):
        token_tag_line = line.split()
        
        # Count t_i's, w_i's and (w_i, t_i) pairs
        for token, tag in [token_tag.rsplit('/', 1) for token_tag in token_tag_line]:
            token_tag_count[(token, tag)] += 1
            tag_count[tag] += 1
            token_count[token] += 1
        
        tag_line = [token_tag.rsplit('/', 1)[1] for token_tag in token_tag_line]
        # Add '.' as a start symbol
        tag_line.insert(0, '.')
        
        #  Count (t_i, t_i-1) pairs
        for (current_tag, previous_tag) in zip(tag_line[1:], tag_line[:-1]):
            current_tag_previous_tag_count[(current_tag, previous_tag)] += 1
    
    
    # Gather singleton counts
    for current_tag in tag_count:
        # Tag-tag singletons
        for next_tag in tag_count:
            if (current_tag_previous_tag_count[(next_tag, current_tag)] == 1):
                singleton_tag_tag_count[current_tag] += 1
                
        # Tag-word singletons
        for current_token in token_count:
            if (token_tag_count[(current_token, current_tag)] == 1):
                singleton_tag_word_count[current_tag] += 1
        
        
    
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
                        sigma[-1][tag] = log_pi(tag) + log_pr_tw(token, tag) 
                        psi[-1][tag] = ''
                    
                    first_token = False
                else:
                    for tag_k in tag_count:
                        max_tag = None
                        log_max_tag_prob = float("-inf")
                        
                        for tag_i in tag_count:
                            log_prob = sigma[-2][tag_i] + log_pr_tt(tag_k, tag_i) + log_pr_tw(token, tag_k)
                            if (log_prob > log_max_tag_prob):
                                log_max_tag_prob = log_prob
                                max_tag = tag_i
                        
                        sigma[-1][tag_k] = log_max_tag_prob  
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
                    log_max_tag_prob = float("-inf")
                    
                    for tag in tag_count:
                        log_prob = sigma[-1][tag]                        
                        if (log_prob > log_max_tag_prob):
                            log_max_tag_prob = log_prob
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
                f_out.write(' '.join(output_line) + "\n"),
            else:
                f_out.write(''.join(output_line))
                
def log_pi(tag):
    return log_pr_tt(tag, '.') 

def log_pr_tt(t_i, t_i_minus_1):
    lambda_tt = singleton_tag_tag_count[t_i_minus_1] + math.exp(-100)
     
    return math.log(current_tag_previous_tag_count[(t_i, t_i_minus_1)] + lambda_tt * pr_tt_backoff(t_i, t_i_minus_1)) \
           - math.log(tag_count[t_i_minus_1] + lambda_tt)

def log_pr_tw(w_i, t_i):
    lambda_wt = singleton_tag_word_count[t_i] + math.exp(-100)
    
    return math.log(token_tag_count[(w_i, t_i)] + lambda_wt * pr_tw_backoff(w_i, t_i))                                    \
           - math.log(tag_count[t_i] + lambda_wt)

def pr_tt_backoff(t_i, t_i_minus_1):
    return tag_count[t_i] / float(len(tag_count) - 1)

def pr_tw_backoff(w_i, t_i):
    return (token_count[w_i] + 1) / float(len(tag_count) + len(token_count) - 1)
    