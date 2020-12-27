"""
  ----------------------------------------
      Tombola - prob. to win if overlap
  ----------------------------------------
  ----------------------------------------
  Python Version: 3.8.2
  ----------------------------------------
  
"""

"""
hypothesis: every card is generated at random (probably not the case in the actual game but whatever)

read from config:
  - number of cards per player
  
run tests:
  - win if overlap is set to True and if it isn't

export results on csv

graph results

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

  print("\n --- RUN OUTPUT ---")
  
  winning_round_without = list() 
  # without numbers shared by different cards
  for test in range(n_tests):
    
    print("Sampling without replacement - running test: %g/%g"%(test + 1, n_tests), end = "\r")
    
    cards = dict()
    card_name_list = list()
  
    # extract "num_cards * num_extr" numbers between "min_extr" and "min_extr"
    # from a uniform distribution without replacement 
    extr_without = np.random.choice(a = range(min_extr, max_extr + 1),
                                    size = num_cards * num_extr,
                                    replace = False)
      
    for card_num in range(num_cards):
      tmp = extr_without[card_num * num_extr : (card_num + 1) * num_extr]
  
      card_name = "card_%d"%(card_num + 1)
      card_name_list.append(card_name)
      cards[card_name] = tmp
    
    # FIXME: debug   
    #print(cards)
    
    # extract all the numbers between "min_extr" and "min_extr" from a uniform distr w/out replacement
    # emulating what the dealer would do
    extr_dealer = np.random.choice(a = range(min_extr, max_extr + 1),
                                   size = max_extr - min_extr + 1,
                                   replace = False)
    
    # FIXME: debug 
    #print("extr_dealer:", extr_dealer, "\n")
    round_num = 0
    
    # while the dealer doesn't extract every number
    while len(extr_dealer) > 0:
      
      round_num += 1
      # FIXME: debug 
      #print("Round", round_num)
      #print(cards)
      
      # pop one number from the dealer picks (the last)
      last, extr_dealer = extr_dealer[-1], extr_dealer[:-1]
      
      # FIXME: debug 
      #print("Extracted:", last)
      
      # for each card, remove the number if found
      for card_num, card_name in enumerate(card_name_list):  
        
        current = cards[card_name]
        new = np.delete(current, np.where(current == last))
        cards[card_name] = new
        
        # if the card is empty, the player wins - otherwise, continue
        if len(cards[card_name]) == 0:
          # FIXME: debug
          #print("\nSampling without replacement: win at round %d with card number %d"%(round_num, card_num))
          winning_round_without.append(round_num)
          extr_dealer = np.array([])
          break
        
  # -------------------------------------
  # -------------------------------------
  
  print()
  
  winning_round_with = list() 
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
      identical_cards = True if len(extr_with_unique) == len(extr_with)/num_cards else False
        
    for card_num in range(num_cards):
      tmp = extr_without[card_num * num_extr : (card_num + 1) * num_extr]
  
      card_name = "card_%d"%(card_num + 1)
      card_name_list.append(card_name)
      cards[card_name] = tmp
      
      
      
      
    # FIXME: debug  
    #print(cards)
    
    # extract all the numbers between "min_extr" and "min_extr" from a uniform distr w/out replacement
    # emulating what the dealer would do
    extr_dealer = np.random.choice(a = range(min_extr, max_extr + 1),
                                   size = max_extr - min_extr + 1,
                                   replace = False)
    
    # FIXME: debug 
    #print("extr_dealer:", extr_dealer, "\n")
    round_num = 0
    
    # while the dealer doesn't extract every number
    while len(extr_dealer) > 0:
      
      round_num += 1
      # FIXME: debug 
      #print("Round", round_num)
      #print(cards)
      
      # pop one number from the dealer picks (the last)
      last, extr_dealer = extr_dealer[-1], extr_dealer[:-1]
      
      # FIXME: debug 
      #print("Extracted:", last)
      
      # for each card, remove the number if found
      for card_num, card_name in enumerate(card_name_list):  
        
        current = cards[card_name]
        new = np.delete(current, np.where(current == last))
        cards[card_name] = new
        
        # if the card is empty, the player wins - otherwise, continue
        if len(cards[card_name]) == 0:
          # FIXME: debug
          #print("\nSampling with replacement: win at round %d with card number %d\n"%(round_num, card_num))
          winning_round_with.append(round_num)
          extr_dealer = np.array([])
          break
  
  winning_round_without = np.array(winning_round_without)  
  winning_round_with = np.array(winning_round_with)
  
  print("\n\nWithout replacement (no shared numbers between cards): avg win at round", np.mean(winning_round_without))
  print("With replacement (shared numbers between cards): avg win at round", np.mean(winning_round_with))
      
          
    
  
  
  
  