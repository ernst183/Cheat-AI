import Player as P
import PlayerType as PT
from BullshitGame import *
import random

#Running tests against most basic agents (Fish)

ppst = 0.01 #Probability people say truth (actually play the cards the claim they are)
pub = 0.01 #Upper bound in the probability (used for calling BS)

fd = open("owl_vs_all.txt","w")

for i in range(1, 21):
	pub = i/100.0
	for j in range(1, 11):
		ppst = j/10.0
		TerminatorWins = 0
		ter_num_won_BS = 0
		ter_num_lost_BS = 0
		ter_total_BS = 0

		for x in range(500):
			player_list = []
		
			thisPlayer = P.Player("Davis", PT.Fish(random.uniform(0.05,0.5)))
			player_list.append(thisPlayer)
			thisPlayer = P.Player("Marl", PT.Frog(random.uniform(0.05, 0.5)))
			player_list.append(thisPlayer)
			thisPlayer = P.Player("Sven", PT.Eel(random.uniform(0.05, 0.5)))
			player_list.append(thisPlayer)
			thisPlayer = P.Player("Jorge", PT.Salamander(random.uniform(0.05,0.5)))
			player_list.append(thisPlayer)
			thisPlayer = P.Player("Terminator", PT.Owl(ppst,pub))
			player_list.append(thisPlayer)
			game = Bullshit_Game(player_list)
			random.shuffle(player_list)
			game.deal_game()
			#Initialize tracker of player moves and evidence for AI agents to use:
			for player in player_list:
				tracker = PlayerTracker(player.name, len(player.hand.cards))
				game.players_tracker[player.name] = tracker

			winner = game.play_game()
			if winner == "Terminator":
				TerminatorWins+=1
			ter_num_won_BS += game.players_tracker["Terminator"].num_won_BS
			ter_num_lost_BS += game.players_tracker["Terminator"].num_lost_BS
			ter_total_BS += game.players_tracker["Terminator"].number_BS

		data_string = str(ppst) + "," +str(pub)+","+str(TerminatorWins)+","+str(ter_num_won_BS)+","+str(ter_num_lost_BS)+"\n"
		fd.write(data_string)


fd.close()
