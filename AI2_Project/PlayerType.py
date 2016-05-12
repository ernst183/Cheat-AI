import random
import time
from math import floor
from copy import copy
import Cards
import Player

class Human:
	def __init__(self):
		self.x = 1

	def chooseCards(self,hand,current_card,player_trackers, numturns, current_card_value):
		hand.print_hand()
		indicies_chosen = []
		cards_to_play = []
		while True:
			card_to_play = input("Type the index of the card you wish to play (or type \"stop\" to end card selection phase): ")
			print("")
			if card_to_play == "Stop" or card_to_play == "stop":
				if len(cards_to_play) == 0:
					print("You must play at least one card per turn\n")
					continue
				break
			else:
				try:
					card_to_play = int(card_to_play)
				except (ValueError,KeyboardInterrupt):
					print("That is not a valid index. Please try again.")
					print("")
					continue
				if card_to_play < 0 or card_to_play >= hand.number_of_cards:
					print("That is not a valid index. Please try again.")
					print("")
					continue
				if card_to_play in indicies_chosen:
					print("You have alreday added that card.")
					print("")
					continue
				cards_to_play.append(hand.cards[card_to_play])
				indicies_chosen.append(card_to_play)
		return cards_to_play

	def callBS(self,hand,num_cards,curr_card,current_card_value,curr_player,numturns,player_trackers=None):
		print("This is your hand:")
		hand.print_hand()
		print(curr_player + " says he has " + str(num_cards) + " " + curr_card + "s\n")
		prompt = "Do you wish to call bullshit on " + curr_player + "? Type 'BS' if you do and 'No' if you don't: "
		bullshit = input(prompt)
		print("")
		if bullshit == "BS" or bullshit == "bs" or bullshit == "Bs":
			return True
		else:
			return False 
		



class Fish:
	def __init__(self, percentCallBs,player_trackers=None):
		self.bsPer = percentCallBs
		self.keepTrack = False

	def chooseCards(self, hand, current_card, player_trackers, numturns, current_card_value):
		cards_to_play = []
		handsize = len(hand.cards)
		# pick a random number of random cards to play
		y = random.randint(1,handsize)
		xArr = random.sample(range(0,handsize), y)
		for x in xArr:
			cards_to_play.append(hand.cards[x])
		return cards_to_play


	def callBS(self,hand,num_cards,curr_card,current_card_value,curr_player,numturns,player_trackers=None):
		# sample to call BS
		if random.random() < self.bsPer:
			return True
		else:
			return False

class Frog:
	def __init__(self, percentCallBs,player_trackers=None):
		self.bsPer = percentCallBs
		self.keepTrack = False

	def chooseCards(self, hand, current_card, player_trackers, numturns, current_card_value):
		cards_to_play = [];
		haveMatch = False;
		# play honestly
		for card in hand.cards:	
			if card.name == current_card:
				cards_to_play.append(card)
				haveMatch = True				
		# if no match play a single bluff card
		if not haveMatch:
			handsize = len(hand.cards)
			x = random.randint(0,handsize -1)
			cards_to_play.append(hand.cards[x])
		return cards_to_play


	def callBS(self,hand,num_cards,curr_card,current_card_value,curr_player,numturns,player_trackers):
		if random.random() < self.bsPer:
			return True
		else:
			return False	

class Eel:
	def __init__(self, percentCallBs):
		self.bsPer = percentCallBs
		self.keepTrack = False
		self.numDecks = 1

	def chooseCards(self, hand, current_card, player_trackers, numturns, current_card_value):
		cards_to_play = [];
		haveMatch = False;
		# play honestly
		for card in hand.cards:	
			if card.name == current_card:
				cards_to_play.append(card)
				haveMatch = True				
		# sample for number of bluff cards 1 - 3 if no match
		if not haveMatch:
			handsize =  len(hand.cards)
			if 3 < handsize:
				sample = random.random()
				if sample > 0 and sample <= 0.7:
					y = 1
				elif sample > 0.7 and sample <= 0.9:
					y = 2
				else:
					y = 3
			else:
				y = 1
			xArr = random.sample(range(0,handsize), y)
			for x in xArr:
				cards_to_play.append(hand.cards[x])
		return cards_to_play


	def callBS(self,hand,num_cards,curr_card,current_card_value,curr_player,numturns,player_trackers):
		num_cards_hand = player_trackers[curr_player].num_cards
		# call BS on last card
		if num_cards_hand == 0:
			return True
		# call BS if more than 4 cards played
		if num_cards > 4*self.numDecks:
			return True
		# else sample for BS
		if random.random() < self.bsPer:
			return True
		else:
			return False

class Salamander: 
	def __init__(self):
		self.keepTrack = False
		self.numDecks = 1

	def chooseCards(self, hand, current_card, player_trackers, numturns, current_card_value):
		cards_to_play = [];
		haveMatch = False;
		# play honestly
		for card in hand.cards:	
			if card.name == current_card:
				cards_to_play.append(card)
				haveMatch = True				

		# bluff a single card if no match
		if not haveMatch:
			handsize = len(hand.cards)
			x = random.randint(0,handsize -1)
			cards_to_play.append(hand.cards[x])
		return cards_to_play


	def callBS(self,hand,num_cards,curr_card,current_card_value,curr_player,numturns,player_trackers):
		num_cards_hand = player_trackers[curr_player].num_cards
		# call BS if last card played
		if num_cards_hand == 0:
			return True
		# call BS if more than 4 cards played
		if num_cards > 4*self.numDecks:
			return True
		else:
			return False

		

class Owl:
	def __init__(self, beta, alpha):
		self.alpha = alpha
		self.keep_track = True
		self.enemies_known_cards = {}
		self.beta = beta

	def chooseCards(self, hand, current_card, player_trackers, numturns, current_card_value):
		cards_to_play = [];
		haveMatch = False;
		# play honestly
		for card in hand.cards:	
			if card.name == current_card:
				cards_to_play.append(card)
				haveMatch = True				
		# bluff one card if no match
		if not haveMatch:
			handsize = len(hand.cards)
			x = random.randint(0,handsize - 1)
			cards_to_play.append(hand.cards[x])
		return cards_to_play


	def callBS(self,hand,num_cards,curr_card,current_card_value,curr_player,numturns,player_trackers):
		
		num_cards_hand = player_trackers[curr_player].num_cards + num_cards
		# call be if last or second to last card
		if num_cards_hand == 0:
			return True
		if num_cards_hand == 1:
			return True
		# calculate probability that player has what they claim
		prob_has_card = player_trackers[curr_player].probability_having_cards[current_card_value]
		if prob_has_card == 0.0:
			prob_has_card = Player.getProbabilityMove(num_cards, num_cards_hand, hand, current_card_value)
		# if prob < threshold call BS
		if prob_has_card < self.alpha:
			return True
		else:
			return False


class Lynx:
	def __init__(self, prob_saying_truth, gamma, del_gamma, name):
		self.bsPer = prob_saying_truth
		self.del_gamma = del_gamma
		self.keep_track = True
		self.enemies_known_cards = {}
		self.alpha = prob_saying_truth
		self.gamma = gamma
		self.name = name
		self.numDecks = 1
		self.beta = 1

	def changeGamma(self, by):
		self.gamma += by*self.del_gamma


	def chooseCards(self, hand, current_card, player_trackers, numturns, current_card_value):
		handsize = len(hand.cards)
		nextCardsNeeded = []
		nextNeed = current_card_value
		for i in range(13):
			nextNeed = ((nextNeed + len(player_trackers)) % 13)
			if nextNeed == 0:
				nextNeed = 13
			nextCardsNeeded.append(nextNeed)

		sortedHand = []
		#sort hand in order of the soonest needed
		for z in range(len(nextCardsNeeded)):
			for x in range(handsize):
				if hand.cards[x].value == nextCardsNeeded[z]:
					sortedHand.append(hand.cards[x])

		bs = 0
		# calculate the rate at which opponents bluff
		numturns = floor(numturns * ((len(player_trackers) - 1) / len(player_trackers)))
		for key in player_trackers.keys():
			if key != self.name:
				bs += player_trackers[key].number_BS
		if numturns != 0:
			percenBS = bs / numturns
		else:
			percenBS = 0
		cards_to_play = [];
		haveMatch = False; 
		
		#initially play honestly
		for card in hand.cards:	
			if card.name == current_card:
				cards_to_play.append(card)
				haveMatch = True				

		# bluff a single card
		if not haveMatch:
			y = 1
			for x in range(1,y+1):
				cards_to_play.append(sortedHand[-x])
		#lets add extra bluff cards if bs rate is low overall
		etta = 1 - percenBS - self.gamma
		while etta > 0 and len(cards_to_play) < 4*self.numDecks and handsize > len(cards_to_play):
			
			x = 1
			#make sure to add them in the same order as before
			while sortedHand[-x] in cards_to_play:
				x += 1
			cards_to_play.append(sortedHand[-x]);
			etta = etta - (self.gamma / 10);
		return cards_to_play


	def callBS(self,hand,num_cards,curr_card,current_card_value,curr_player,numturns,player_trackers):

		#call bs if the cards they say they have plus
		#the number of cards we have of that same vaue
		#is greater than the total number fo that card
		num_cards_i_have = 0
		for c in hand.cards:
			if c.name == curr_card:
				num_cards_i_have += 1
		if num_cards + num_cards_i_have > 4*self.numDecks:
			return True
		num_cards_hand = player_trackers[curr_player].num_cards
		# call BS if last card played
		if num_cards_hand == 0:
			return True
		# call BS if more than  cards played
		if num_cards > 4*self.numDecks:
			return True
		# sample to call BS
		if random.random() < self.bsPer:
			return True
		else:
			return False


class Dolphin:
	def __init__(self, beta,alpha, gamma, del_gamma, name):
		self.del_gamma = del_gamma
		self.keep_track = True
		self.enemies_known_cards = {}
		self.beta = beta
		self.alpha = alpha
		self.gamma = gamma
		self.name = name
		self.numDecks = 1

	def changeGamma(self, by):
	
		self.gamma += by*self.del_gamma


	def chooseCards(self, hand, current_card, player_trackers, numturns, current_card_value):
		handsize = len(hand.cards)
		nextCardsNeeded = []
		nextNeed = current_card_value
		for i in range(13):
			nextNeed = ((nextNeed + len(player_trackers)) % 13)
			if nextNeed == 0:
				nextNeed = 13
			nextCardsNeeded.append(nextNeed)

		sortedHand = []
		#sort hand in order of the soonest needed
		for z in range(len(nextCardsNeeded)):
			for x in range(handsize):
				if hand.cards[x].value == nextCardsNeeded[z]:
					sortedHand.append(hand.cards[x])

		bs = 0
		# calculate the rate at which opponents bluff
		numturns = floor(numturns * ((len(player_trackers) - 1) / len(player_trackers)))
		for key in player_trackers.keys():
			if key != self.name:
				bs += player_trackers[key].number_BS
		if numturns != 0:
			percenBS = bs / numturns
		else:
			percenBS = 0
		cards_to_play = [];
		haveMatch = False; 
		
		#initially play honestly
		for card in hand.cards:	
			if card.name == current_card:
				cards_to_play.append(card)
				haveMatch = True				

		# bluff a single card
		if not haveMatch:
			y = 1
			for x in range(1,y+1):
				cards_to_play.append(sortedHand[-x])
		#lets add extra bluff cards if bs rate is low overall
		etta = 1 - percenBS - self.gamma
		while etta > 0 and len(cards_to_play) < 4*self.numDecks and handsize > len(cards_to_play):
			
			x = 1
			#make sure to add them in the same order as before
			while sortedHand[-x] in cards_to_play:
				x += 1
			cards_to_play.append(sortedHand[-x]);
			etta = etta - (self.gamma / 10);
		return cards_to_play


	def callBS(self,hand,num_cards,curr_card,current_card_value,curr_player,numturns,player_trackers):

		#call bs if the cards they say they have plus
		#the number of cards we have of that same vaue
		#is greater than the total number fo that card
		num_cards_deck_match = 0
		num_cards_i_have = 0
		for c in hand.cards:
			if c.name == curr_card:	
				num_cards_i_have += 1
		# if matched in hand + matched in deck + number they claim > 4 call BS
		for c in range(1,14):
			if current_card_value == c:
				num_card_deck_match = player_trackers[self.name].known_cards_deck[c]
		if num_cards + num_cards_i_have + num_card_deck_match > 4*self.numDecks:
			return True
		num_cards_hand = player_trackers[curr_player].num_cards
		# if player plays last card call BS
		if num_cards_hand == 0:
			return True
		# if player caims mre than 4 cards call BS
		if num_cards > 4*self.numDecks:
			return True
		# else calculate probability player has what they claim
		prob_has_card = player_trackers[curr_player].probability_having_cards[current_card_value]
		if prob_has_card == 0.0:
			prob_has_card = Player.getProbabilityMove(num_cards, num_cards_hand, hand, current_card_value)

		#calculates the rate at which other players bluff
		numturns = floor(numturns * ((len(player_trackers) - 1) / len(player_trackers)))
		bs = 0
		for key in player_trackers.keys():
			if key != self.name:
				bs += player_trackers[key].number_BS
		if numturns != 0:
			percenBS = bs / numturns
		else:
			percenBS = 0
		
		#adjust alpha to be higher if bs rate is high, lower if low
		if percenBS < 0.2:
			adjust_alpha = (percenBS - 0.4) / 3.8
		else:
			adjust_alpha = 0
		if prob_has_card < self.alpha + adjust_alpha:
			return True
		else:
			return False


