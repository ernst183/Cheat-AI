import Cards
from copy import copy 
import random
import time
import PlayerType as PT
import math

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)


def getProbabilityMove(num_wanted, hand_size, hand, current_card_value):
	# calculate stats about agents's own hand
	if hand == None:
		num_cards_hand_match = 0
		my_hand_size = 0
	else:
		my_hand_size = len(hand.cards)
		num_cards_hand_match = 0
		for card in hand.cards:
			if card.value == current_card_value:
					num_cards_hand_match += 1
	numDecks  = 1
	if num_wanted > hand_size:
		return hand_size/52.0*numDecks

	# probability is 0 if player tries to play more than 4 cards
	if num_wanted > 4*numDecks:
		return 0.0

	# probability is 0 if the play tries to play cards such that
	# our matches + his attempted matches > 4
	if 4*numDecks - num_cards_hand_match < num_wanted:
		return 0.0

	# probability is 1 if the opposing player has this many cards and we don't have matches
	if 52*numDecks - my_hand_size - (4*numDecks - num_cards_hand_match) < hand_size-num_wanted:
		return 1.0

	# if none of the above applies, calculate probability that that
	# player has what he says he does
	numerator = nCr(4*numDecks - num_cards_hand_match, num_wanted)*nCr(52*numDecks - my_hand_size - (4*numDecks - num_cards_hand_match), hand_size-num_wanted)
	denominator = nCr(52*numDecks - my_hand_size, hand_size)
	return float(numerator)/float(denominator)
	
class Player:
	def __init__(self, name, PlayerType):
		self.PlayerType = PlayerType
		self.name = name
		self.hand = Cards.Hand(name, [])
		self.verbose = False

	def hand_empty(self):
		if self.hand.number_of_cards == 0:
			return True
		else:
			return False

	def return_name(self):
		return self.name

	def pick_up_pile(self, pile):
		self.hand.draw_cards(pile, pile.number_of_cards)

	def draw_card(self, source):
		self.hand.draw_card(source)

	def draw_cards(self, source, number_cards):
		self.hand.draw_cards(source, number_cards)

	def play_card(self, card, destination):
		self.hand.play_card(card, destination)

	def play_cards(self, cards, destination):
		self.hand.play_cards(cards, destination)

	def print_hand(self):
		self.hand.print_hand()

	def take_turn(self, current_card,current_card_value, pile, player_list, players_tracker
				, possible_cards_in_pile,cards_played_probabilities, numturns):
		if self.verbose:
			turnDescription = "\nIt is currently " + self.name + "'s turn and the card needed is: " + current_card
			print(turnDescription)
			print("")
			print(self.name, "has", self.hand.number_of_cards, "cards in hand")
			print("")
			print( "Cards in pile: " + str(len(pile.cards))+ "\n")
		cards_to_play = self.PlayerType.chooseCards(self.hand, current_card, players_tracker, numturns, current_card_value);
		
		# Update info in public game tracker
		players_tracker[self.name].cards_played.extend(cards_to_play)
		self.play_cards(cards_to_play, pile)
		
		number_cards_played = len(cards_to_play)

		value = current_card_value
		probability_move = 0.0
		#Add probability of the card just played to per game table of probabilities:
		agent = None
		for player in player_list:
			if type(player.PlayerType) is PT.Dolphin:
				agent = player
		if agent:
			probability_move = getProbabilityMove(number_cards_played, players_tracker[self.name].num_cards,agent.hand,current_card_value)
		else:
			probability_move = getProbabilityMove(number_cards_played, players_tracker[self.name].num_cards,None,current_card_value)

		beta = 1
			
		if type(self.PlayerType) is PT.Owl:
			beta = self.PlayerType.beta

		if type(self.PlayerType) is PT.Lynx:
			beta = self.PlayerType.beta

		if type(self.PlayerType) is PT.Dolphin:
			beta = self.PlayerType.beta

		# use beta paramater as a filter
		for card in cards_to_play:
			effective_prob = (beta*probability_move)+((1-beta)*(1-probability_move))
			if possible_cards_in_pile[value] == 0:
				cards_played_probabilities[value] += (effective_prob)
			else:	
				cards_played_probabilities[value] *= (effective_prob)

			possible_cards_in_pile[current_card_value] += 1
			players_tracker[self.name].known_cards_deck[card.value] += 1

		players_tracker[self.name].num_cards -= number_cards_played

		bs_list = copy(player_list)
		# players can't call bs on themselves
		bs_list.remove(self)
		# always let players call BS in random order, because in the
		# real game, anyone may cal BS at any time
		random.shuffle(bs_list)
		called_BS = False
		won_BS = False

		# bs_list is the opponents
		for player in bs_list:
			# give all a chance to call BS
			if player.PlayerType.callBS(player.hand,number_cards_played,current_card, current_card_value,self.name, numturns, players_tracker):
				
				if self.verbose:
					print("Player " + str(player.name) + " just called BS!")

				# were they lying?
				tell_truth = pile.check_cards(number_cards_played, current_card)
				called_BS = True
				players_tracker[player.name].number_BS += 1

				# reset the deck tracker when cards are picked up
				players_tracker[self.name].known_cards_deck = [-1,0,0,0,0,0,0,0,0,0,0,0,0,0]
				for p in bs_list:
					players_tracker[p.name].known_cards_deck = [-1,0,0,0,0,0,0,0,0,0,0,0,0,0]
				if tell_truth == True:
					won_BS= True
					if self.verbose:
						print(self.name, "was telling the truth,", player.name, "must pick up")
						print("")
					
					#Update info in public game tracker
					players_tracker[player.name].num_lost_BS += 1
					players_tracker[player.name].num_cards += len(pile.cards)
					players_tracker[player.name].update(possible_cards_in_pile, cards_to_play,cards_played_probabilities, current_card_value, number_cards_played)
					player.pick_up_pile(pile)
					break

				else:
					won_BS= False
					if self.verbose:
						print(self.name, "was lying,", self.name, "must pick up")
						print("")

					#Update info in public game tracker
					players_tracker[player.name].num_won_BS += 1
					players_tracker[self.name].num_cards += len(pile.cards)
					players_tracker[self.name].update(possible_cards_in_pile, cards_to_play, cards_played_probabilities, current_card_value, number_cards_played)
					self.pick_up_pile(pile)
					break
			else:
				continue

		#lynx and dolphin update gamma depending on if bluff was called or not
		if type(self.PlayerType) is PT.Lynx or type(self.PlayerType) is PT.Dolphin:
			if called_BS == True:
				self.PlayerType.changeGamma(1)
			else:
				self.PlayerType.changeGamma(-1) 

		# update probabilities
		if not called_BS or won_BS:
			for card in cards_to_play:
				possible_cards_in_pile[current_card_value] += 1
			players_tracker[self.name].update([-1,0,0,0,0,0,0,0,0,0,0,0,0,0], None, cards_played_probabilities, current_card_value, number_cards_played)


			






