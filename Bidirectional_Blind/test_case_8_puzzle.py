import b_hash
import timeit
from collections import Counter
import csv
from itertools import izip
from operator import itemgetter
import collections
from matplotlib.pyplot import stem


'''
setting up the initial matrix from database
'''
a = 0
total_time = 0


def csv_formater(fw_list,bw_list,opt_path,initial_matrix,csvfile):
    count_fw = 0
    count_bw = 0
    
    writer_3 =csv.writer(csvfile,quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
    writer_3.writerow(['PROBLEM: '] + [initial_matrix])
    writer_3.writerow(['Forwards'])
    writer=csv.writer(csvfile,quoting=csv.QUOTE_NONNUMERIC, lineterminator=',') 
    sortedlist_fw = sorted(fw_list, key=itemgetter(1,2))
    sortedlist_bw = sorted(bw_list, key=itemgetter(1,2))
    
    writer.writerow([])
    for i in range(opt_path + 1):
        writer.writerow([i])
    writer_2 = csv.writer(csvfile,quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
    writer_2.writerow([])
    for i in range(opt_path,-1,-1):
        row = [i]
        for j in sortedlist_fw:
            if(j[1] == i):
                row += [j[3]]
        writer_2.writerow(row)
        
    writer_3.writerow(['Backwards'])
    writer.writerow([])
    for i in range(opt_path + 1):
        writer.writerow([i])
    writer_2.writerow([])
    for i in range(opt_path,-1,-1):
        row = [i]
        for j in sortedlist_bw:
            if(j[1] == i):
                row += [j[3]]
        writer_2.writerow(row)
        
def graph_maker(graph_dict,csvfile,opt_path,before_opt_mean,after_opt_mean):    
    #od = collections.OrderedDict(sorted(graph_dict.items()))
    writer =csv.writer(csvfile,quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
    writer.writerow([])
    #for key,value in sorted(graph_dict):
    writer.writerow([opt_path] + [before_opt_mean])
    writer.writerow([opt_path] + [after_opt_mean])
    
        
def mean_calc(graph_dict,opt_path): 
    before_val = 0
    after_val = 0
    for key,value in graph_dict.items():
        if key != str(opt_path):
            before_val += value
        after_val += value
            
    return before_val,after_val
    
def stu(matrix_initial,char, number):
    if char == 'a':
        matrix_initial[0][0] = number
    if char == 'b':
        matrix_initial[0][1] = number
    if char == 'c':
        matrix_initial[0][2] = number
    if char == 'd':
        matrix_initial[1][0] = number
    if char == 'e':
        matrix_initial[1][1] = number
    if char == 'f':
        matrix_initial[1][2] = number
    if char == 'g':
        matrix_initial[2][0] = number
    if char == 'h':
        matrix_initial[2][1] = number
    if char == 'i':
        matrix_initial[2][2] = number
         
        
'''
Here we input our database file
'''
with open('fgchart_blind.csv','wb') as csvfile:  
    for z in range(1,32):
        count = 0
        before_opt_mean = 0 
        after_opt_mean = 0
        with open('EightPuzzle_' + str(z) + '.txt','r') as file1:
        
            lines = [i.strip() for i in file1]
            matrix_initial = [[0]*3 for i in range(3)]
            matrix_goal = [[0]*3 for i in range(3)]
             
            matrix_goal[0][0] = '1'
            matrix_goal[0][1] = '2'
            matrix_goal[0][2] = '3'
            matrix_goal[1][0] = '4'
            matrix_goal[1][1] = '5'
            matrix_goal[1][2] = '6'
            matrix_goal[2][0] = '7'
            matrix_goal[2][1] = '8'
            matrix_goal[2][2] = '0'

            
            ########################### Just change the number and it will generate new csv file of n optimal path ####################
            for i in range(len(lines)):
                fieldnames = ['Direction','Gvalue','Fvalue','Count']
                writer = csv.writer(csvfile,quoting=csv.QUOTE_NONNUMERIC, lineterminator=',')
                fw_list = []
                bw_list = []
                str1 = lines[i]
                str2 = str1[223:]
                str3 = str2.replace('at','')
                str4 = str3[:-12]
                str5 = str4.replace('(','')
                str6 = str5.replace(')','')
                str7 = str6.replace(',','')
            
                stu(matrix_initial, str7[1], str7[0])
                stu(matrix_initial, str7[3], str7[2])
                stu(matrix_initial, str7[5], str7[4])
                stu(matrix_initial, str7[7], str7[6])
                stu(matrix_initial, str7[9], str7[8])
                stu(matrix_initial, str7[11], str7[10])
                stu(matrix_initial, str7[13], str7[12])
                stu(matrix_initial, str7[15], str7[14])
                stu(matrix_initial, str7[-1], '0')
                    
                matrix_initial_1 = [item for sublist in matrix_initial for item in sublist] 
                matrix_goal_1 = [item for sublist in matrix_goal for item in sublist]
                
                start = timeit.default_timer()
                opt_path,nodes = b_hash.b_hash(matrix_initial_1, matrix_goal_1)
                b_hash.flim = 1
                stop = timeit.default_timer()
                time_taken = round(stop - start,6)
                result = 'Optimal Path: ' + str(opt_path) + ', Nodes Expanded: ' + str(len(nodes)) + ', Time Taken: ' + str(time_taken)    #if(opt_path != 15):
                print(result)
                x,y = mean_calc(b_hash.f_level_nodes,opt_path) 
                before_opt_mean += x
                after_opt_mean += y
                total_time += time_taken
                new_list,zero_list = b_hash.csv_format(matrix_initial_1)
                cnter = Counter(new_list) #counts all the element occurences
                
                for key, value in cnter.items():
                    line = list(key) + [value]
                    if(line[0] == 'bw'):
                        bw_list.append(line)
                    elif(line[0] == 'fw'):
                        fw_list.append(line)     
            
                for i in zero_list:
                    if(i[2] <= opt_path):
                        line = list(i) + [0]
                        if(line[0] == 'bw'):
                            bw_list.append(line)
                        elif(line[0] == 'fw'):
                            fw_list.append(line)
                            
                csv_formater(fw_list, bw_list,opt_path,matrix_initial_1,csvfile)
                b_hash.temp_nodes[:] = []
                cnter.clear()
                zero_list[:] = []
                count += 1
        avg_bef_opt = before_opt_mean/count
        avg_aft_opt = after_opt_mean/count
        #graph_maker(b_hash.f_level_nodes,csvfile2,opt_path,avg_bef_opt,avg_aft_opt)    

print "Total time taken =", total_time
file1.close()