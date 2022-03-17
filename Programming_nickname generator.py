#Random nickname generator

#How the code works: the code accepts user input and assigns two random numbers, first number corresponds to color
#and another to an animal. Mix of color and animal is our nickname. No two nicknames can be the same.
#The code then saves the output to the .csv file. Once the code is run again, it checks the content of .csv file and makes sure
#that nicknames will be unique for new batch of inputs.


color={0:"white",1:"black",2:"brown",3:"pink",4:"orange",5:"red",6:"blue",7:"purple",8:"gray",9:"green",10:"yellow"}
animal={0:"seal",1:"dog",2:"cat",3:"mouse",4:"fish",5:"dolphin",6:"snake",7:"parrot",8:"camel",9:"turtle", 10:"spider"}

import re
import random

name_lst = list()

#the code for name input does not allow numbers nor does it accept short inputs
while True:
    user_inp = input("Please enter the name. Press q or Q to exit: ")
    if user_inp.upper() == "Q":
        break
    if len(user_inp) < 3:
        print("Name is too short, try again.")
        continue
    else:
        if re.findall("[0-9]+", user_inp):
            print("Name should not contain numbers, try again.")
            continue
        else:
            name_lst.append(user_inp)

def nickn_generator_and_filewriter(name_lst):
    #the code checks wehther we already have nickname.csv file and treats each case separately
    try:
        fh = open("nickname.csv","r")
        lines = fh.readlines()
        print("The file detected. Appending to a file...\n")
        fh_a = open("nickname.csv","a")
        new_file = False
    except:
        print("Creating a new file...\n")
        fh_w = open("nickname.csv","w")
        new_file = True

    if new_file:
        #nickname.csv file doesn't exist
        '''unique number combinations generator'''
        nam_num = dict() #dictionary of name and numbers
        for nam in name_lst:
            key = nam
            val = random.randint(0,10), random.randint(0,10)
            #we want to make sure that there are no the same number combinations within the tranche of names that is currently being input
            while val in nam_num.values():
                #if the combination of numbers repeats within the same tranche the loop runs until it finds a unique one for the tranche
                val = random.randint(0,10), random.randint(0,10)
                continue
            #when we finally get unique combinations value (combination of 2 numbers) is created to the key (name)
            nam_num[key] = val

        '''numbers to words translator and file writer'''
        nam_nn = dict() #dictionary of name and words
        for key,val in nam_num.items():
            nam_nn[key] = str(color[val[0]] + " " + animal[val[1]])
        for key,val in nam_nn.items():
            line = (key + "," + val + "\n")
            fh_w.write(line)
        fh_w.close()

    else:
        #nickname.csv file was already created. We create a list of nicknames from this file; nicknames that are already taken (taken_nicknames_lst)
        taken_nn_lst = list() #take nicknames in a word form
        taken_num_lst= list() #taken number combinations

        fh = open("nickname.csv","r")
        lines = fh.readlines()
        for line in lines:
            #first we extract nicknames in word form from the file (ex: white seal)
            record = line.rstrip().split(",")
            act_name = record[0] #actual name (ex. Jane Doe)
            taken_nn = record[1] #nickname (ex. white seal)
            taken_nn_lst.append(taken_nn)
        print("Taken nicknames:", taken_nn_lst,"\n")
            #next, we split those nicknames into separate components (ex.(white,seal))
        for t_nn in taken_nn_lst:
            #print("Nickname:", t_nn)
            t_nn_words = t_nn.split()
            t_nn_col = t_nn_words[0]
            #print("Taken color:", t_nn_col)
            t_nn_anim = t_nn_words[1]
            #print("Taken animal:", t_nn_anim)
            #lastly, we change the word form into appropriate numerical form (ex.(0,0))
            for key,val in color.items():
                if t_nn_col == val:
                    wanted_num_col = key
            for key,val in animal.items():
                if t_nn_anim == val:
                    wanted_num_anim = key
            #print(t_nn, "translates into",(wanted_num_col,wanted_num_anim)) we end up with a list of numbers that the nickname from the file was composed of
            taken_num_lst.append((wanted_num_col,wanted_num_anim))
        print("Taken combinations:",taken_num_lst,"\n")

        '''unique number combinations generator'''
        #we proceed to create a combination of 2 unique numbers (value) for a given name (key)
        nam_num = dict() #dictionary of name and numbers
        for nam in name_lst:
            key = nam
            val = random.randint(0,10), random.randint(0,10)
            print("To be added:",key,val)
            print("Combination in the current tranche?",val in nam_num.values())
            print("Combination in the previous tranches (file)?",val in taken_num_lst)
            #we want to make sure that there are no the same number combinations within a current tranche of names that is now being input also, since some nicknames were already assigned, we want to make sure we won't have doubles
            while val in nam_num.values() or val in taken_num_lst:
                val = random.randint(0,10), random.randint(0,10)
                continue
            nam_num[key] = val
        print(nam_num)

        '''numbers to words translator and file writer'''
        nam_nn = dict() #dictionary of name and words
        for key,val in nam_num.items():
            nam_nn[key] = str(color[val[0]] + " " + animal[val[1]])
        for key,val in nam_nn.items():
            line = (key + "," + val + "\n")
            fh_a.write(line)
        fh_a.close()
        fh.close()
    return nam_nn

print(nickn_generator_and_filewriter(name_lst))
