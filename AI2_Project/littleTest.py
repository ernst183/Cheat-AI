import Player as P
import PlayerType as PT
from BullshitGame import *
import random

fd = open('dolphin_v_lynx_v_owl.txt','w')
DavisWins = 0
MarlWins = 0
SvenWins = 0
JorgeWins = 0
JesusWins = 0
JimWins = 0
TerminatorWins = 0
ter_num_won_BS = 0
ter_num_lost_BS = 0

butts = 100000
for x in range(butts):
	player_list = []


	thisPlayer = P.Player("Davis", PT.Frog(random.uniform(.05,.3)))
	player_list.append(thisPlayer)
	thisPlayer = P.Player("Marl", PT.Fish(random.uniform(.05,.3)))
	player_list.append(thisPlayer)
	thisPlayer = P.Player("Sven", PT.Eel(random.uniform(.05,.3)))
	player_list.append(thisPlayer)	
	thisPlayer = P.Player("Jorge", PT.Eel(random.uniform(.05,.3)))
	#thisPlayer = P.Player("Terminator", PT.Fish(0.2))
	player_list.append(thisPlayer)
	thisPlayer = P.Player("Terminator", PT.Lynx(0.08,0.98,0.02,"Terminator"))
	#thisPlayer = P.Player("Terminator", PT.Owl(1,.01))
	player_list.append(thisPlayer)
	game = Bullshit_Game(player_list)
	random.shuffle(player_list)
	game.deal_game()


	#Initialize tracker of player moves and evidence for AI agents to use:
	for player in player_list:
		tracker = PlayerTracker(player.name, len(player.hand.cards))
		#tracker.probability_given_card = tracker.num_cards/52.0
		game.players_tracker[player.name] = tracker
		#print ("Player " + player.name + " has " +str(tracker.num_cards) + " cards")
		

	winner = game.play_game()
	if winner == "Davis":
		DavisWins += 1
	if winner == "Marl":
		MarlWins += 1
	if winner == "Sven":
		SvenWins += 1
	if winner == "Jorge":
		JorgeWins += 1
	if winner == "Terminator":
		TerminatorWins+=1

	ter_num_won_BS += game.players_tracker["Terminator"].num_won_BS
	ter_num_lost_BS += game.players_tracker["Terminator"].num_lost_BS


stringy = (str(TerminatorWins)+","+str(ter_num_won_BS)+","+str(ter_num_lost_BS)+"\n")
fd.write(stringy)
DavisWins = 0
MarlWins = 0
SvenWins = 0
JorgeWins = 0
JesusWins = 0
JimWins = 0
TerminatorWins = 0
ter_num_won_BS = 0
ter_num_lost_BS = 0


for x in range(butts):
	player_list = []

	
	thisPlayer = P.Player("Davis", PT.Frog(random.uniform(.05,.3)))
	player_list.append(thisPlayer)
	thisPlayer = P.Player("Marl", PT.Fish(random.uniform(.05,.3)))
	player_list.append(thisPlayer)
	thisPlayer = P.Player("Sven", PT.Eel(random.uniform(.05,.3)))
	player_list.append(thisPlayer)	
	thisPlayer = P.Player("Jorge", PT.Eel(random.uniform(.05,.3)))
	#thisPlayer = P.Player("Terminator", PT.Fish(0.2))
	player_list.append(thisPlayer)
	thisPlayer = P.Player("Terminator", PT.Owl(1,0.08))
	#thisPlayer = P.Player("Terminator", PT.Owl(1,.01))
	player_list.append(thisPlayer)
	game = Bullshit_Game(player_list)
	random.shuffle(player_list)
	game.deal_game()


	#Initialize tracker of player moves and evidence for AI agents to use:
	for player in player_list:
		tracker = PlayerTracker(player.name, len(player.hand.cards))
		#tracker.probability_given_card = tracker.num_cards/52.0
		game.players_tracker[player.name] = tracker
		#print ("Player " + player.name + " has " +str(tracker.num_cards) + " cards")
		

	winner = game.play_game()
	if winner == "Davis":
		DavisWins += 1
	if winner == "Marl":
		MarlWins += 1
	if winner == "Sven":
		SvenWins += 1
	if winner == "Jorge":
		JorgeWins += 1
	if winner == "Terminator":
		TerminatorWins+=1

	ter_num_won_BS += game.players_tracker["Terminator"].num_won_BS
	ter_num_lost_BS += game.players_tracker["Terminator"].num_lost_BS


stringy = (str(TerminatorWins)+","+str(ter_num_won_BS)+","+str(ter_num_lost_BS)+"\n")
fd.write(stringy)
DavisWins = 0
MarlWins = 0
SvenWins = 0
JorgeWins = 0
JesusWins = 0
JimWins = 0
TerminatorWins = 0
ter_num_won_BS = 0
ter_num_lost_BS = 0


for x in range(butts):
	player_list = []

	
	thisPlayer = P.Player("Davis", PT.Frog(random.uniform(.05,.3)))
	player_list.append(thisPlayer)
	thisPlayer = P.Player("Marl", PT.Fish(random.uniform(.05,.3)))
	player_list.append(thisPlayer)
	thisPlayer = P.Player("Sven", PT.Eel(random.uniform(.05,.3)))
	player_list.append(thisPlayer)	
	thisPlayer = P.Player("Jorge", PT.Eel(random.uniform(.05,.3)))
	#thisPlayer = P.Player("Terminator", PT.Fish(0.2))
	player_list.append(thisPlayer)
	thisPlayer = P.Player("Terminator", PT.Dolphin(1,0.08,0.98,0.02,"Terminator"))
	#thisPlayer = P.Player("Terminator", PT.Owl(1,.01))
	player_list.append(thisPlayer)
	game = Bullshit_Game(player_list)
	random.shuffle(player_list)
	game.deal_game()


	#Initialize tracker of player moves and evidence for AI agents to use:
	for player in player_list:
		tracker = PlayerTracker(player.name, len(player.hand.cards))
		#tracker.probability_given_card = tracker.num_cards/52.0
		game.players_tracker[player.name] = tracker
		#print ("Player " + player.name + " has " +str(tracker.num_cards) + " cards")
		

	winner = game.play_game()
	if winner == "Davis":
		DavisWins += 1
	if winner == "Marl":
		MarlWins += 1
	if winner == "Sven":
		SvenWins += 1
	if winner == "Jorge":
		JorgeWins += 1
	if winner == "Terminator":
		TerminatorWins+=1

	ter_num_won_BS += game.players_tracker["Terminator"].num_won_BS
	ter_num_lost_BS += game.players_tracker["Terminator"].num_lost_BS


stringy = (str(TerminatorWins)+","+str(ter_num_won_BS)+","+str(ter_num_lost_BS)+"\n")
fd.write(stringy)
	

	#print("best vale for upper bound in probability is: ", str(maxI))
	#print("max number of wins: ", str(maxWins))
