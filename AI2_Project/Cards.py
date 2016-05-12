import random

class Card:
	def __init__(self, value, suit):
		self.value = value #value of card
		self.suit = suit #suit of card

		if self.value == 1:
			self.name = "Ace"
		elif self.value == 2:
			self.name = "Two"
		elif self.value == 3:
			self.name = "Three"
		elif self.value == 4:
			self.name = "Four"
		elif self.value == 5:
			self.name = "Five"
		elif self.value == 6:
			self.name = "Six"
		elif self.value == 7:
			self.name = "Seven"
		elif self.value == 8:
			self.name = "Eight"
		elif self.value == 9:
			self.name = "Nine"
		elif self.value == 10:
			self.name = "Ten"
		elif self.value == 11:
			self.name = "Jack"
		elif self.value == 12:
			self.name = "Queen"
		elif self.value == 13:
			self.name = "King"
		else:
			print("Not a valid value")
			return -1

class Deck:
	def __init__(self):
		numDecks = 1
		self.number_of_cards = 52*numDecks
		self.cards = []
		for i in range(1, 14):
			for d in range(numDecks):
				self.cards.append(Card(i, "Clubs"))
		for i in range(1, 14):
			for d in range(numDecks):
				self.cards.append(Card(i, "Spades"))
		for i in range(1, 14):
			for d in range(numDecks):
				self.cards.append(Card(i, "Hearts"))
		for i in range(1, 14):
			for d in range(numDecks):
				self.cards.append(Card(i, "Diamonds"))


	def draw_card(self, hand): #Put one version of this here, but I think it may be better in the "Hand" class
		if len(self.cards) == 0:
			print("Deck is empty")
			return -1
		card_drawn = self.cards.pop()
		hand.cards.append(card_drawn)

	def shuffle(self):
		i = 0
		while(i <31):
			for i in range(len(self.cards)):
				current_card = self.cards[i]
				random_int = random.randint(0, len(self.cards) - 1)
				self.cards[i] = self.cards[random_int]
				self.cards[random_int] = current_card
			i+=1
	
	def print_deck(self):
		print("Deck")
		if self.number_of_cards == 0:
			print("Empty")
		else:
			for i in range(self.number_of_cards):
				print(self.cards[i].name, " of ", self.cards[i].suit)
		print("")

	def deal(self, player_list):
		i = 0
		while self.number_of_cards != 0:
			player_list[i].draw_card(self)
			i = (i + 1)%(len(player_list))
			
class Hand:
	def __init__(self, player_name, cards):
		self.player_name = player_name
		self.cards = cards
		self.number_of_cards = len(cards)

	def draw_card(self, source): #Draw from some source
		if(source.number_of_cards == 0):
				print("Source has no cards left")
				return -1
		new_card = source.cards.pop() #Note, this take the card from the "end" of the source, not the front
		source.number_of_cards -= 1
		self.cards.append(new_card)
		self.number_of_cards += 1
		self.cards.sort(key=lambda x: x.value) #lets keep the cards in hands sorted for easier ux and algorithm for the AI

	def draw_cards(self, source, number_cards): #Draw some number of cards 
		new_cards = []
		for i in range(number_cards):
			if(source.number_of_cards == 0):
				print("Source has no cards left")
				break
			new_cards.append(source.cards.pop())
			source.number_of_cards -= 1
		self.cards.extend(new_cards)
		self.number_of_cards += len(new_cards)
		self.cards.sort(key=lambda x: x.value) #lets keep the cards in hands sorted for easier ux and algorithms for the AI

	def play_card(self, card, destination):
		if self.cards.count(card) == 0:
			print("This card is not in your hand")
			return -1
		self.cards.remove(card)
		self.number_of_cards -= 1
		destination.cards.append(card)
		destination.number_of_cards += 1

	def play_cards(self, cards, destination):
		for i in range(len(cards)):
			self.play_card(cards[i], destination)

	def print_hand(self):
		print(self.player_name)
		if self.number_of_cards == 0:
			print("Empty")
		else:
			for i in range(self.number_of_cards):
				cardString = str(i) + ". " + self.cards[i].name + " of " + self.cards[i].suit			
				print(cardString)
		print("")

class Pile:
	def __init__(self):
		self.cards = []
		self.number_of_cards = 0

	def check_cards(self, number_played, required_value): #returns False if cards don't match value, otherwise True
		if self.number_of_cards < number_played:
			print("There are less cards in the pile than being checked")
			return False
		cards_to_check = []
		for i in range(number_played):
			card_to_check = self.cards.pop()
			cards_to_check.append(card_to_check)
			if card_to_check.name != required_value:
				self.cards.extend(cards_to_check)
				return False
		self.cards.extend(cards_to_check)
		return True

	def print_pile(self):
		print("Pile")
		if self.number_of_cards == 0:
			print("Empty")
		else:
			for i in range(self.number_of_cards):
				print(self.cards[i].name, " of ", self.cards[i].suit)
		print("")

