def generate_10_fold_corpus(train_file, output_file_prefix):
    
    line_count = file_len(train_file)
    lines_per_section = line_count / 10.0;  
    
    for section in range(10):
        with open(train_file) as f_in:
            # Generate section boundaries (as floats, to ensure that all data is used)
            first_train_section_start = 0
            first_train_section_end = section * lines_per_section
            
            eval_section_start = first_train_section_end
            eval_section_end = eval_section_start + lines_per_section
            
            second_train_section_start = eval_section_end
            second_train_section_end = line_count
            
            # Generate training and evaluation cross-folds
            with open("train/" + output_file_prefix + str(section), 'w') as f_train_out:
                # First training section              
                for _ in range(int(round(first_train_section_start)), int(round(first_train_section_end))):
                    f_train_out.write(f_in.readline())
                
                # Evaluation section
                with open("eval/" + output_file_prefix + str(section), 'w') as f_eval_out:
                    with open("test/" + output_file_prefix + str(section), 'w') as f_test_out:
                        for _ in range(int(round(eval_section_start)), int(round(eval_section_end))):
                            line = f_in.readline()
                            
                            f_eval_out.write(line)
                            f_test_out.write(' '.join(map(lambda x: x[0], [x.rsplit('/', 1) for x in line.split()])) + "\n")
                
                # Second training section
                for _ in range(int(round(second_train_section_start)), int(round(second_train_section_end))):
                    f_train_out.write(f_in.readline())
                                            
            
def file_len(file_name):
    with open(file_name) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1            