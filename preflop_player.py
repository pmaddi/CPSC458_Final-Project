import cards
import hands
import preflop_sim
import afterflop_sim
import afterturn_sim
import afterriver_sim

import random

# returns bet size of small blind, with -1 being fold
# small_blind is true if small blind, false if big blind or reraise
# position is False if small blind player, True if big blind player
# stack size is smallest stack on the table
# money in is money already on the table (small blind)
# money required is how much to call
# write this later to include a random factor
def randomPermute(value, random_factor):
  factor = 1
  if random.random() < .5:
    factor = -1

  return (random.random() * random_factor * factor + 1) * value

def play_preflop(hand, money_in, money_required, big_blind, stack_size, position = False, small_blind = True):
  kPositionAdvantage = .025
  kPositionDisadvantage = .025
  kRandomFactor = .1 # max value of random factor
  kUndercut = .33 # chance that hero bets small with a really good hand
  kLimp = .2 # chance that hero limps in with a poor hand
  kGoodHand = .1 # really good hand differential
  kBetFactor = 4
  kConstantBetFactor = .75
  kCallPercent = .3 # percent of big blind that the raise is for us just to call
  kLowHandConstant = .08 # makes it more likely to play beter hands
  kStretchFactor = 1.2
  kGoodRatio = .60
  kReallyGoodRatio = .66
  final_bet = 0

  hand_strength = preflop_sim.getPreflopStrength(hand)
  win_ratio = hand_strength[0] / (hand_strength[0] + hand_strength[2])
  cost_benefit_ratio = (money_required - money_in) / float(money_required)

  # correcting for advantageous position
  if position:
    win_ratio = win_ratio * (1 + kPositionAdvantage)
  else:
    win_ratio = win_ratio * (1 - kPositionDisadvantage)

  if small_blind:
    if win_ratio > cost_benefit_ratio:
      # 'bluff' by calling with a really good hand
      if random.random() < kUndercut:
        final_bet = money_required - money_in

      else:
        bet = (win_ratio + kConstantBetFactor) * big_blind + money_required - money_in
        bet = randomPermute(bet, kRandomFactor)
        if bet - money_required < kCallPercent * big_blind:
          final_bet = money_required - money_in
        else:
          final_bet = int(bet) - money_in
    else:
      win_ratio = randomPermute(win_ratio, kRandomFactor)
      if win_ratio + kLowHandConstant > cost_benefit_ratio or random.random() < kLimp:
        final_bet = money_required - money_in
      else:
        final_bet = -1
  else:
    # use random_permute to sometimes play slightly worse hands as good hands
    if randomPermute(win_ratio, kRandomFactor) > kGoodRatio:
      if random.random() < kUndercut:
        final_bet = money_required - money_in
      else:
        tentative_bet = (win_ratio + kConstantBetFactor) * big_blind + win_ratio * (money_required - money_in) * kBetFactor
        if tentative_bet < money_required - money_in:
          if win_ratio > kReallyGoodRatio:
            final_bet = (money_required - money_in) * 2
          else:
            final_bet = money_required - money_in
        else:
          final_bet = int(tentative_bet)
    else:
      # kStretchFactor to err on the side of calling a bit
      if cost_benefit_ratio < randomPermute(win_ratio, kRandomFactor) * kStretchFactor:
        final_bet = money_required - money_in
      else:
        final_bet = -1

  # this is just to make sure we're not overambitious with betting
  if final_bet > (stack_size - money_in):
    return stack_size - money_in
  else:
    return final_bet

# note: money_in == money_required when first_bet == True
def play_afterflop(hand, table, money_in, money_required, big_blind, stack_size, position = False, first_bet = True):
  # find flags here - like multiple suited and straight draws
  # find straight and flush outs
  # find what i have w/ win percentages
  cost_benefit_ratio = (money_required - money_in) / float(money_required)

  hand_strength = afterflop_sim.getStrength(hand, table)
  win_ratio = hand_strength[0] / (hand_strength[0] + hand_strength[2])
  print win_ratio
  
  return money_required - money_in

def play_turn(hand, table, money_in, money_required, big_blind, stack_size, position = False, first_bet = True):
  hand_strength = afterturn_sim.getStrength(hand, table)
  win_ratio = hand_strength[0] / (hand_strength[0] + hand_strength[2])
  print win_ratio

  return money_required - money_in

def play_river(hand, table, money_in, money_required, big_blind, stack_size, position = False, first_bet = True):
  hand_strength = afterriver_sim.getStrength(hand, table)
  win_ratio = hand_strength[0] / (hand_strength[0] + hand_strength[2])
  print win_ratio

  return money_required - money_in


#central tenant #1 - aggressive AI is better than passive AI
#central tenant #2 - AI is good because of randomness
#central tenant #3 - AI is good because of monte carlo

#theDeck = cards.Deck()
#theDeck.shuffle()
#hand = cards.Hand()
#table = cards.Hand()
#hand.add_card(theDeck.deal_card())
#hand.add_card(theDeck.deal_card())
#
#for j in range(5):
#  table.add_card(theDeck.deal_card())
#
#print hand, table
#print play_river(hand, table, 20, 40, 10, 300, False, False)