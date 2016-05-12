import Cards
import time
import argparse
import os
import random
from math import ceil
from copy import copy

try:
	# for Python2
	from Tkinter import *
except ImportError:
	# for Python3
	from tkinter import *
try:
	from PIL import Image, ImageTk
except ImportError:
	print("Bullshit Game requires Python Imaging Library package. Exiting.")
	exit(0)

class Bullshit_Game:
	def __init__(self, player_list):
		self.game_deck = Cards.Deck()
		self.game_pile = Cards.Pile()
		self.player_list = player_list
		self.turn_counter = 0
		self.winner_flag = False
		self.current_player = player_list[0]
		self.current_card = "Ace"

	def deal_game(self):
		self.game_deck.shuffle()
		self.game_deck.deal(self.player_list)

	def print_deck(self):
		self.game_deck.print_deck()

	def print_pile(self):
		self.game_pile.print_pile()

	def take_turn(self, toPlay):
		
		self.current_player.take_turn(self.current_card, self.game_pile, self.player_list, toPlay)
		
		bs = self.current_player.bs_check(self.current_card, self.game_pile, self.player_list)
		self.updateTurnCounter()
		return bs

	def updateTurnCounter(self):
		self.turn_counter += 1
		if self.turn_counter % 14 == 0:
			self.turn_counter += 1 #This skips over the case where turn_counter % 14 == 0, allowing us to accurately line up values		
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
		self.current_card = current_card_name
		self.prev_player = self.current_player
		self.current_player = self.player_list[(self.turn_counter % len(self.player_list)) - 1]



class Player:
	def __init__(self, name, PlayerType):
		self.PlayerType = PlayerType
		self.name = name
		self.hand = Cards.Hand(name, [])

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

	def take_turn(self, current_card, pile, player_list, toPlay):
		# self.print_hand()
		# turnDescription = "It is currently " + self.name + "'s turn and the card needed is: " + current_card
		# print(turnDescription)
		# print("")
		# play = -1
		# cards_to_play = []
		# indicies_chosen = []
		# while True:
		# 	card_to_play = input("Type the index of the card you wish to play (or type \"stop\" to end card selection phase): ")
		# 	print("")
		# 	if card_to_play == "Stop" or card_to_play == "stop":
		# 		if len(cards_to_play) == 0:
		# 			print("You must play at least one card per turn\n")
		# 			continue
		# 		break
		# 	else:
		# 		try:
		# 			card_to_play = int(card_to_play)
		# 		except (ValueError,KeyboardInterrupt):
		# 			print("That is not a valid index. Please try again.")
		# 			print("")
		# 			continue
		# 		if card_to_play < 0 or card_to_play >= self.hand.number_of_cards:
		# 			print("That is not a valid index. Please try again.")
		# 			print("")
		# 			continue
		# 		if card_to_play in indicies_chosen:
		# 			print("You have alreday added that card.")
		# 			print("")
		# 			continue
		# 		cards_to_play.append(self.hand.cards[card_to_play])
		# 		indicies_chosen.append(card_to_play)
		print(self.PlayerType)
		if self.PlayerType == "Human":
			cards_to_play = toPlay
		else:
			cards_to_play = []
			cards_to_play.append(self.hand.cards[0])
		print(cards_to_play)
		self.play_cards(cards_to_play, pile)
		self.number_cards_played = len(cards_to_play)

	def bs_check(self,current_card,pile,player_list):
		bs_list = copy(player_list)
		bs_list.remove(self)
		for player in bs_list:
			# prompt = player.name + ", do you wish to call bullshit on " + self.name + "? Type \"BS\" if you do and \"No\" if you don't: "
			# bullshit = input(prompt)
			# print("")
			if player.PlayerType != "Human":
			# if bullshit == "BS" or bullshit == "bs" or bullshit == "Bs":
				sample = random.random()
				if sample > .5:
					tell_truth = pile.check_cards(self.number_cards_played, current_card)
					if tell_truth == True:
						# print(self.name, "was telling the truth,", player.name, "must pick up")
						# print("")
						player.pick_up_pile(pile)
						return (player.name, 0)
					else:
						# print(self.name, "was lying,", self.name, "must pick up")
						# print("")
						self.pick_up_pile(pile)
						return (player.name, 1)
				else:
					continue
			else:
				if player.BSHuman == 1:
					tell_truth = pile.check_cards(self.number_cards_played, current_card)
					if tell_truth == True:
						# print(self.name, "was telling the truth,", player.name, "must pick up")
						# print("")
						player.pick_up_pile(pile)
						return (player.name, 0)
					else:
						# print(self.name, "was lying,", self.name, "must pick up")
						# print("")
						self.pick_up_pile(pile)
						return (player.name, 1)					
				if player.BSHuman == 0:
					continue
		return (None, -1)


class Game_window(Tk, Bullshit_Game):
	def __init__(self, parent,  bsGame):
		Tk.__init__(self, parent,)
		self.parent = parent
		bsGame.deal_game()
		initializeWindow(self,bsGame)



class WindowedGame(Bullshit_Game):
	def __init__(self,bsGame):
		self.toPlay = []
		self.game = bsGame
		self.BSCaller = None

	def select(self, cardPos, card):
		oldx = cardPos.winfo_x()
		oldy = cardPos.winfo_y()
		if oldy == 738:
			cardPos.place(x=oldx,y=oldy-40)
			self.toPlay.append(card)
		else:
			cardPos.place(x=oldx,y=oldy+40)
			self.toPlay.remove(card)

	



class NameWindow():
	def __init__(self):
		self.txt = ""

	def askname(self,root):
		dialogWdw = Frame(root, borderwidth=2, relief=RAISED)
		Label(dialogWdw, text='Enter Your Name:').pack(side=TOP, padx=20, pady=4)
		dialogTxt = Entry(dialogWdw)
		dialogTxt.pack()
		root.bind('<Return>', lambda x:self.destroyDialog(dialogWdw,dialogTxt))
		dialogBtn = Button(dialogWdw,text='OK',command=lambda:self.destroyDialog(dialogWdw,dialogTxt)).pack(side=TOP, padx=20, pady=4)
		dialogWdw.place(relx=0.5, rely=0.5, anchor=CENTER)
		dialogWdw.mainloop()
		return self.txt

	def destroyDialog(self,dialogWdw,dialogTxt):
		self.txt = dialogTxt.get()
		dialogWdw.destroy()
		dialogWdw.quit()


def refreshAndMoveOn(root,wg,bsval):

	print(wg.toPlay)

	
	wg.game.player_list[0].BSHuman = bsval
	#if wg.game.turn_counter == 0:
	#	wg.game.updateTurnCounter()	
	if wg.game.current_player.PlayerType == "Human": 
		print(str(1))
		wg.game.current_player.take_turn(wg.game.current_card, wg.game.game_pile, wg.game.player_list, wg.toPlay)
		bs = wg.game.current_player.bs_check(wg.game.current_card, wg.game.game_pile, wg.game.player_list)
		wg.game.updateTurnCounter()

		wg.BSCaller = bs[0]
		wg.BSValue = bs[1]
	elif (bsval == -1) or (bsval == 0) or (bsval == 1):
		print(str(2))
		wg.game.current_player.take_turn(wg.game.current_card, wg.game.game_pile, wg.game.player_list, wg.toPlay)
	else:
		print(str(3))
		bs = wg.game.current_player.bs_check(wg.game.current_card, wg.game.game_pile, wg.game.player_list)
		wg.game.updateTurnCounter()

		wg.BSCaller = bs[0]
		wg.BSValue = bs[1]
	
	print(wg.game.game_pile.cards)

	wg.toPlay = []
	winFlg = True
	for player in wg.game.player_list:
		if len(player.hand.cards) == 0:
			drawWin(root,wg,player)
			winFlg = False
	if winFlg:
		reDraw(root,wg)

		if wg.game.current_player.PlayerType == "Human":
			#wg.game.updateTurnCounter()
			selButton = Button(root,text="Play Cards",command=lambda:refreshAndMoveOn(root,wg,-1),font=("Purisa",14),bg="pink")
			selButton.place(x=(650-selButton.winfo_reqwidth()/2),y=600)
	
		elif bsval == (bsval == -1) or (bsval == 0) or (bsval == 1):
			contButton = Button(root,text="Continue",command=lambda:refreshAndMoveOn(root,wg,-2),font=("Purisa",14),bg="pink")
			contButton.place(x=(650-contButton.winfo_reqwidth()/2),y=600)

		else:
			#wg.game.updateTurnCounter()
			bsButton = Button(root,text="Call BS!",command=lambda:refreshAndMoveOn(root,wg,1),font=("Purisa",14),bg="pink")
			bsButton.place(x=650,y=600)
			nobsButton = Button(root,text="No BS!",command=lambda:refreshAndMoveOn(root,wg,0),font=("Purisa",14),bg="pink")
			nobsButton.place(x=(650-bsButton.winfo_reqwidth()),y=600)


def drawWin(root, wg, player):
	for widget in root.winfo_children():
		widget.destroy()


	root.columnconfigure(0, weight=1)
	root.title('BULLSHIT')
	root.geometry("1300x866")
	bkg=Label(root,image = wg.backImage)
	bkg.place(x=0, y=0, relwidth=1, relheight=1)
	winStr = player.name + " WINS!!!"
	winLbl = Label(root,text=winStr,font=("Putrisa",100))
	winLbl.place(x=(650-winLbl.winfo_reqwidth()/2),y=(400-winLbl.winfo_reqheight()/2))
	#time.sleep(5)
	#exit(1)

	menubar = Menu(root)
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="Exit", command=root.quit)
	filemenu.add_command(label="New Game", command=lambda:newGame(root))
	menubar.add_cascade(label="File", menu=filemenu)

	helpmenu = Menu(menubar, tearoff=0)
	helpmenu.add_command(label="About")
	menubar.add_cascade(label="Help")

	# display the menu
	root.config(menu=menubar)

def reDraw(root,wg):
	for widget in root.winfo_children():
		widget.destroy()



	root.columnconfigure(0, weight=1)
	root.title('BULLSHIT')
	root.geometry("1300x866")
	bkg=Label(root,image = wg.backImage)
	bkg.place(x=0, y=0, relwidth=1, relheight=1)
	placeCards(root,wg)
	if wg.BSCaller is not None:
		bsStr = wg.BSCaller + " called BS!"
		if wg.BSValue == 1:
			bsStr += "\n" + wg.game.prev_player.name + " has to pick up pile!"
		if wg.BSValue == 0:
			bsStr += "\n" + wg.BSCaller + " was wrong, and has to pick up pile!"
		bsBox = Label(root,text=bsStr,font=("Purisa",18))
		bsBox.place(x=200,y=500)

	menubar = Menu(root)
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="Exit", command=root.quit)
	filemenu.add_command(label="New Game", command=lambda:newGame(root))
	menubar.add_cascade(label="File", menu=filemenu)

	helpmenu = Menu(menubar, tearoff=0)
	helpmenu.add_command(label="About")
	menubar.add_cascade(label="Help")
	# display the menu
	root.config(menu=menubar)





def initializeWindow(root,game):
	

	root.columnconfigure(0, weight=1)
	root.title('BULLSHIT')
	root.geometry("1300x866")
	feltImage = Image.open("img/felt.jpg")
	tkimage = ImageTk.PhotoImage(feltImage)
	bkg=Label(root,image = tkimage)
	bkg.place(x=0, y=0, relwidth=1, relheight=1)
	cardBack = Image.open("img/CARDS/Red_Back.jpg")
	imageBack = cardBack.crop((54,54,231,303))
	w,h = imageBack.size
	imageBack = imageBack.resize((ceil(w/2) , ceil(h/2)),Image.ANTIALIAS)
	cardBack = ImageTk.PhotoImage(imageBack)

	for player in game.player_list:
		for card in player.hand.cards:
			cardImg = card.image.crop((34,34,211,283))
			w,h = cardImg.size
			cardImg = cardImg.resize((ceil(w/2) , ceil(h/2)),Image.ANTIALIAS)
			card.image = ImageTk.PhotoImage(cardImg)
	
	#root.after_idle(root.lower)
	nam = NameWindow()
	playerName = ""
	while playerName == "":
		playerName = nam.askname(root)
	
	#playerName = "jarvis"
	game.player_list[0].name = playerName
	wg = WindowedGame(game)
	wg.cardBack = cardBack
	wg.backImage = tkimage
	placeCards(root,wg)
	refreshAndMoveOn(root,wg,-1)
	root.resizable(width=FALSE,height=FALSE)
	menubar = Menu(root)
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="Exit", command=root.quit)
	filemenu.add_command(label="New Game", command=lambda:newGame(root))
	menubar.add_cascade(label="File", menu=filemenu)

	helpmenu = Menu(menubar, tearoff=0)
	helpmenu.add_command(label="About")
	menubar.add_cascade(label="Help")

	# display the menu
	root.config(menu=menubar)
	root.mainloop()


def placeCards(root,wg):
	#place player 1 hand

	i = 150
	handlen = len(wg.game.player_list[0].hand.cards)
	if handlen > 10:
		SPACING = 1000 / handlen
	else: SPACING = 75
	for card in wg.game.player_list[0].hand.cards:
		cardVar=Button(root,image=card.image, width = "87")
		cardVar.config(command= lambda cardPos=cardVar,card=card:wg.select(cardPos,card))
		cardVar.place(x=i,y=738)
		i += SPACING
	nameVar = Label(root,text=wg.game.player_list[0].name)
	nameVar.place(relx=0.5, y=675, anchor=CENTER)

	#place player 2 hand
	i = 150
	handlen = len(wg.game.player_list[1].hand.cards)
	if handlen > 10:
		SPACING = 1000 / handlen
	else: SPACING = 75
	#hide other player's hands
	


	for card in wg.game.player_list[1].hand.cards:

		cardVar=Label(root,image=wg.cardBack, width = "87")
		cardVar.place(x=i,y=0)
		i += SPACING

	nameVar = Label(root,text=wg.game.player_list[1].name)
	nameVar.place(relx=0.5, y=150, anchor=CENTER)

	#place player 3 hand
	i = 50
	handlen = len(wg.game.player_list[2].hand.cards)
	if handlen > 10:
		SPACING = 685 / handlen
	else: SPACING = 75
	#hide other player's hands

	for card in wg.game.player_list[2].hand.cards:

		cardVar=Label(root,image=wg.cardBack, width = "87")
		cardVar.place(x=1212,y=i)
		i += SPACING

	nameVar = Label(root,text=wg.game.player_list[2].name)
	nameVar.place(rely=0.5, x=150, anchor=CENTER)

	#place player 4 hand
	i = 50
	handlen = len(wg.game.player_list[3].hand.cards)
	if handlen > 10:
		SPACING = 685 / handlen
	else: SPACING = 75
	#hide other player's hands

	for card in wg.game.player_list[3].hand.cards:

		cardVar=Label(root,image=wg.cardBack, width = "87")
		cardVar.place(x=0,y=i)
		i += SPACING

	nameVar = Label(root,text=wg.game.player_list[3].name)
	nameVar.place(rely=0.5, x=1150, anchor=CENTER)

	if len(wg.game.game_pile.cards) > 0:
		cardVar=Label(root,image=wg.cardBack, width = "87")
		cardVar.place(x=605,y=375)

	playStr = "Current card needed: " + wg.game.current_card + "\nCards in pile: " + str(len(wg.game.game_pile.cards)) + "\nPlayer's Turn: " + wg.game.current_player.name +wg.game.current_player.PlayerType
	playBox = Label(root,text=playStr,font=("Purisa",18))
	playBox.place(x=200,y=200)


def newGame(root):
	
	root.destroy()
	root.quit()
	main()	




def main():

	numPlayers = 4
	player_list = []
	thisPlayer = Player("Player 1", "Human")
	player_list.append(thisPlayer)
	thisPlayer = Player("Sven", "Fish")
	player_list.append(thisPlayer)
	thisPlayer = Player("Davis", "Fish")
	player_list.append(thisPlayer)
	thisPlayer = Player("Jorge", "Fish")
	player_list.append(thisPlayer)

	game = Bullshit_Game(player_list)
	gameWindow = Game_window(None,game)
		
main()
