import Cards
import Player as P
import PlayerType as PT
import time


class Bullshit_Game:
	def __init__(self, player_list):
		self.i = 0
		self.game_deck = Cards.Deck()
		self.game_pile = Cards.Pile()
		self.player_list = player_list
		self.turn_counter = 0
		self.winner_flag = False
		self.verbose = False	
		self.players_tracker = {}
		self.possible_cards_in_pile = [-1,0,0,0,0,0,0,0,0,0,0,0,0,0]
		#example:	cards_played_probabilities[1] --> probability associated with an A
		self.cards_played_probabilities = [-1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]


	def deal_game(self):
		self.game_deck.shuffle()
		self.game_deck.deal(self.player_list)

	def print_deck(self):
		self.game_deck.print_deck()

	def print_pile(self):
		self.game_pile.print_pile()

	def take_turn(self):
		if self.turn_counter % 14 == 0:
			self.turn_counter += 1 #This skips over the case where turn_counter % 14 == 0, allowing us to accurately line up values
		current_player = self.player_list[(self.turn_counter % len(self.player_list)) - 1]
		current_card = self.turn_counter % 14
		if current_card == 1:
			current_card_name = "Ace"
		elif current_card == 2:
			current_card_name = "Two"
		elif current_card == 3:
			current_card_name = "Three"
		elif current_card == 4:
			current_card_name = "Four"
		elif current_card == 5:
			current_card_name = "Five"
		elif current_card == 6:
			current_card_name = "Six"
		elif current_card == 7:
			current_card_name = "Seven"
		elif current_card == 8:
			current_card_name = "Eight"
		elif current_card == 9:
			current_card_name = "Nine"
		elif current_card == 10:
			current_card_name = "Ten"
		elif current_card == 11:
			current_card_name = "Jack"
		elif current_card == 12:
			current_card_name = "Queen"
		elif current_card == 13:
			current_card_name = "King"
		current_player.take_turn(current_card_name, current_card, self.game_pile, self.player_list,
			 self.players_tracker, self.possible_cards_in_pile, self.cards_played_probabilities, self.i)
		# keep track of current turn
		self.turn_counter += 1
		# keep track of total hands played
		self.i += 1

	def play_game(self):
		while True:
			self.take_turn()
			for i in range(len(self.player_list)):
				if self.player_list[i].hand_empty() == True:
					if self.verbose:
						print(self.player_list[i].name, "WINS!!")
					return self.player_list[i].name
			time.sleep(0)

# main method to track player activity and probabilities
class PlayerTracker:
	def __init__(self, adversary_name, num_cards):
		self.name = adversary_name
		self.num_cards = num_cards
		self.number_BS = 0
		self.num_won_BS = 0
		self.num_lost_BS = 0
		self.cards_played = []
		self.picked_up_cards = []
		self.probability_given_card = 0.0
		self.probability_having_cards = [-1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
		self.picked_up_cards = [-1,0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.known_cards_deck = [-1,0,0,0,0,0,0,0,0,0,0,0,0,0]

	def toString(self):
		msg = "name: " + str(self.name) + "\nnumCards: " + str(self.num_cards) 
		+ "\nprob given card: " + str(self.probability_given_card) + "\nprob cards: " + str(self.probability_having_cards)
		return msg

	def update(self,picked_up_cards, known_cards,cards_played_probabilities, last_card_played_value, num_cards_played):
		for x in range(1,14):
			self.picked_up_cards[x] += picked_up_cards[x]

		if len(picked_up_cards) == 0 or known_cards == None:
			#Current player made his move and nobody called BS, so we remove the probability 
			# associated wth the card he just played if he picked it up before from pile
			self.probability_having_cards[last_card_played_value] = 0.0
			self.picked_up_cards[last_card_played_value] = 0
			return
		else:
			#Current player has to pick up from pile, meaning he lost a BS challenge
			#We know the last cards played with probability 1:
			for card in known_cards:
				self.picked_up_cards[card.value] +=1
				self.probability_having_cards[card.value] = 1
				#Remove cards known from the pile, so we are only left with uncertain cards:
				picked_up_cards[card.value] = 0
				cards_played_probabilities[card.value] = 0.0
			for i in range(1,14):
				if picked_up_cards[i] != 0:
					if self.picked_up_cards[i] == 0 and self.probability_having_cards[i] == 0.0:					
						self.probability_having_cards[i] += cards_played_probabilities[i]
					else:
						self.probability_having_cards[i] += cards_played_probabilities[i]
		#remember to clear list of possible cards in pile and associated probabilities
		del picked_up_cards[:]
		picked_up_cards.extend([-1,0,0,0,0,0,0,0,0,0,0,0,0,0])
		del cards_played_probabilities[:]
		cards_played_probabilities.extend([-1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])

