"""
  ----------------------------------------
     Tombola - prob. cards are identical
  ----------------------------------------
  ----------------------------------------
  Python Version: 3.8.2
  ----------------------------------------
  
"""

import os
import csv
import yaml
import numpy as np

conf_file_path = 'config.yaml'

# -------------------------------------

# parse config from YAML file
with open(conf_file_path) as f:
  yaml_conf = yaml.load(f, Loader = yaml.FullLoader)

# total number of tests
n_tests = yaml_conf["n_tests"]

# minumum number extracted
min_extr = yaml_conf["min_extr"]

# maximum number extracted
max_extr = yaml_conf["max_extr"]

# numbers per card
num_extr = yaml_conf["num_extr"]

# cards per player
num_cards = yaml_conf["num_cards"]


output_base_path = '.'
output_folder_name = 'output'
output_folder_path = os.path.join(output_base_path, output_folder_name)

if not os.path.exists(output_folder_path): os.mkdir(output_folder_path)

# -------------------------------------

if __name__ == "__main__":
  
  # sanity check: maximum number of cards is bound by num_cards*num_extr <= max_extr - min_extr + 1
  assert(num_cards * num_extr <= 90)
  
  print("\n --- RUN CONFIG ---")
  print("Number of cards per player:", num_cards)
  print("Minimum extracted number:", min_extr)
  print("Minimum extracted number:", max_extr)
  print("Numbers extracted per cards:", num_extr)
  print("Number of tests:", n_tests, "\n")

  print("\n --- RUN OUTPUT ---\n")
  
  
  extr_identical = 0
  
  # with numbers (randomly) shared by different cards
  for test in range(n_tests):
    
    print("Sampling with replacement - running test: %g/%g"%(test + 1, n_tests), end = "\r")
    
    cards = dict()
    card_name_list = list()
  
    identical_cards = True
  
    while identical_cards:
      # extract "num_cards * num_extr" numbers between "min_extr" and "min_extr"
      # from a uniform distribution with replacement 
      extr_with = np.random.choice(a = range(min_extr, max_extr + 1),
                                   size = num_cards * num_extr,
                                   replace = True)
      
      
      extr_with_unique, max_recurrences = np.unique(extr_with, return_counts = True)
      
      # if all the numbers are repeated across all the cards, which means the unique vector
      # has length which is 1/num_cards of "len(extr_with)", reshuffle
      identical_cards = True if len(extr_with_unique) == num_extr else False
      
      if len(extr_with_unique) == num_extr:
        extr_identical += 1 
        
  print("Recurrences of the limit case 'all cards are identical': %d/%d"%(extr_identical, n_tests))
      
          
    
  
  
  
  