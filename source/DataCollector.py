import pandas as pd
import numpy as np

from Team import Team
from Event import Event
from Player import Player
from Position import Position
from PlotData import PlotData

#Constants
TOTAL_NUMBER_OF_PLAYERS = 22
NUMBER_OF_PLAYERS_PER_TEAM = TOTAL_NUMBER_OF_PLAYERS/2
PLAYER_L1_COUNTING_KICK_LOG_DATA_FRAME_COLUMN_POSITION = 34
FIRST_COUNTING_KICK_COLUMN_L = 34
NUMBER_OF_COLUMNS_BETWEEN_COUNTING_KICKS_PLUS_ONE = 31
NUMBER_OF_COLUMNS_BETWEEN_PLAYER_X_POS_AND_PLAYER_COUNTING_KICKS_PLUS_ONE = 16
NUMBER_OF_COLUMNS_BETWEEN_PLAYER_Y_POS_AND_PLAYER_COUNTING_KICKS_PLUS_ONE = 15

class DataCollector():
	def __init__(self): #sem log_path
		
		self.__log_path = './files/t1.rcg.csv'
		self.__data_frame = None	

		self.__team_l = None # By instanciating the team, all the computing is scored inside the __init__ of the class Team()
		self.__team_r = None
		self.__teams = []
		self.__all_events = []
		self.__all_faults = []
		self.__all_goals = []
		self.__all_penalties = []

		# calls for data computing
		self.initialize()

	
	# Creates the Setters and Getters methods   

	def set_team_l(self, team):
		self.__team_l = team
	
	def set_log_path(self,log_path):
		self.__log_path = log_path 		

	def set_all_goals(self, all_goals):
		self.__all_goals = all_goals

	def set_all_faults(self, all_faults):
		self.__all_faults =	all_faults

	def set_all_penalties(self, all_penalties):
		self.__all_penalties = all_penalties
	
	# Getters
	
	def get_team(self, team_side):
		
		if(team_side == "l"):
			return self.__team_l
		else:
			return self.__team_r
	
	def get_team_name(self, team_side):
		if(team_side == "l"):
			return self.__team_l.get_name()
		else:
			return self.__team_r.get_name()
		
	
	# Does the general initialization
	def initialize(self):
		
		# The data will be collected from this dataframe
		self.__data_frame = pd.read_csv(self.__log_path)

		# Getting teams names from the Data Frame
		team_left_name = self.__data_frame.iloc[0].team_name_l
		team_right_name = self.__data_frame.iloc[0].team_name_r
		
		# Players are initialized before the Teams because they are an attribute of them.
		# -> All Teams have an array of Players 
		left_players = self.starting_players(team_left_name, "l")
		right_players = self.starting_players(team_right_name, "r")
		
		# Teams:
		self.starting_teams(team_left_name, team_right_name, left_players, right_players)

		# Saving both teams in this DataCollector
		self.__teams.append(self.__team_l)
		self.__teams.append(self.__team_r)

	# Definition of computing functions

	def find_unique_event_count(self, event):
		
		simplified_dataframe = self.data_frame[['playmode']]

	def statChanged(self, logDataFrame, rowNumber, columnNumber):
		if(logDataFrame.iloc[rowNumber, columnNumber] == logDataFrame.iloc[rowNumber-1, columnNumber]):
			return False
		else:
			return True
	
	def starting_teams(self, team_left_name, team_right_name, left_players, right_players):
	
		self.__team_l = Team()
		self.__team_l.set_side("left")

		self.__team_r = Team()
		self.__team_r.set_side("right")
		
		# Setting team names from the Data Frame
		self.__team_l.set_name(team_left_name)
		self.__team_r.set_name(team_right_name)
		
		# Goals:

		self.__score = [self.__data_frame['team_score_l'].max(),self.__data_frame['team_score_r'].max()]
		
		self.__team_l.set_goals_scored = [] # need implementation
		self.__team_r.set_goals_scored = [] # need implementation

		self.__team_l.set_number_of_goals_scored(self.__score[0])
		self.__team_r.set_number_of_goals_scored(self.__score[1])
		
		self.__team_l.set_players(left_players)
		self.__team_r.set_players(right_players)
		
		# Setting goals scored
		l_goals = self.__data_frame['team_score_l'].max()
		r_goals = self.__data_frame['team_score_r'].max()
		
		self.__team_l.set_number_of_goals_scored(l_goals)
		self.__team_r.set_number_of_goals_scored(r_goals)
		
		# Setting free kicks
		r_free_kicks = self.__data_frame['playmode'].str.count('free_kick_l').sum()
		l_free_kicks = self.__data_frame['playmode'].str.count('free_kick_r').sum()
		
		self.__team_r.set_number_of_free_kicks(r_free_kicks)
		self.__team_l.set_number_of_free_kicks(l_free_kicks)

		#TODO: IMPLEMENTAR FUNÇÃO find_unique_event_count, e usá-la no lugar disto:
		#solução alternativa com output correto (mas mais lenta...)
		l_foul_charge = 0
		r_foul_charge = 0
		for i in range(len(self.__data_frame)):
			if(self.__data_frame.iloc[i,1] == "foul_charge_l" and self.__data_frame.iloc[i-1,1] != "foul_charge_l"):
				l_foul_charge += 1
			elif(self.__data_frame.iloc[i,1] == "foul_charge_r" and self.__data_frame.iloc[i-1,1] != "foul_charge_r"):
				r_foul_charge += 1

		self.__team_l.set_number_of_faults_commited(l_foul_charge)
		self.__team_r.set_number_of_faults_commited(r_foul_charge)

		# Setting foul_charges
			#TODO

		
		# Penalties:
		pen_r = self.__data_frame['team_pen_score_r'].max()
		pen_l = self.__data_frame['team_pen_score_l'].max()		
		
		self.__team_r.set_penaltis_scored(pen_r)
		self.__team_l.set_penaltis_scored(pen_l)

	def starting_players(self, team, side):	  
		players_array = [Player(team,side,1), Player(team,side,2), Player(team,side,3), Player(team,side,4), Player(team,side,5), Player(team,side,6), Player(team,side,7), Player(team,side,8), Player(team,side,9), Player(team,side,10), Player(team,side,11)]
		i = 1

		if side[0] == 'l' or side[0] == 'L':
			side = 'l'
		elif side[0] == 'r' or side[0] == 'R':
			side = 'r'
		
		for player in players_array:
			column = "player_{}{}_type".format(side,i)
			position = self.__data_frame.iloc[0][column] 
			player.set_pos(position)
			i = i + 1

		return players_array
		
		# Functions that command the plotting of graphs

#TODO: GENERALIZAR PLOTTING FUNCTIONS 
	def plot_graph(self, mainWindowObject, graph_type, title, data):
		#Create an matplotlib.axes object
		axes = mainWindowObject.figure.add_subplot(111)

		if (graph_type == "bar"):
			# sets axis labels
			axes.set_xlabel(data.get_x_label()) 
			axes.set_ylabel(data.get_y_label())
			colors = ["#7da67d","#ffa1a1"]
			# set title
			axes.set_title(title)
			# plot each bar
			for barIndex in range(0,len(data.get_entries())):
				axes.bar(data.get_entry(barIndex).get_x_coordinate(), data.get_entry(barIndex).get_value(), width = data.get_entry(barIndex).get_width(), color = colors[barIndex])
		
			#Attach a text label above each bar in *rects*, displaying its height.
			#adapted from matplotlib documentation
			aux = 0
			for entry in data.get_entries():
				height = entry.get_value()
				axes.annotate('{}'.format(height), xy=(aux, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
				aux += 1

		if (graph_type == "pie"):
			axes.set_title(title)
			# plot the graph
			axes.pie([data.get_entry(0).get_value(), data.get_entry(1).get_value()], explode =(0.06, 0), labels = data.get_sector_labels(), colors = ["#7da67d", "#ffa1a1"], autopct='%1.1f%%', shadow=True, startangle=90)

		#TODO: SOLUÇÃO PALIATIVA
		if (graph_type == "scatter"):
			axes.set_title("Posição das faltas")
			axes.set_xlabel('X')
			axes.set_ylabel('Y')																# TODO: na solução definitiva, não fazer hardcoded assim como está aqui.
			axes.scatter(data.get_entry(0).get_x_positions(), data.get_entry(0).get_y_positions(), color = "#7da67d", label = "RobôCin")
			axes.scatter(data.get_entry(1).get_x_positions(), data.get_entry(1).get_y_positions(), color = "#ffa1a1", label = "Razi")
			axes.legend()


		#TODO: TERMINAR IMPLEMENTAÇÃO QUANDO O MESMO PROBLEMA DE _plot_faults_position FOR
		#      RESOLVIDO.
		if (graph_type == "_scatter"):
			# set title
			axes.set_title('Posição das faltas')
			# set axis labels
			axes.set_xlabel('X')
			axes.set_ylabel('Y')

			#Xrc = [20,50,70]
			#Yrc = [20,50,70]
			#Xother = [26,58,74]
			#Yother = [26,58,74]
			#axes.scatter(Xrc, Yrc, color='r')
			#axes.scatter(Xother, Yother, color='b')

			axes.scatter(data.get_entry(0).get_x_positions(), data.get_entry(0).get_y_positions(), color="#7da67d")
			axes.scatter(data.get_entry(1).get_x_positions(), data.get_entry(1).get_y_positions(), color="#ffa1a1")

		#TODO: is this necessary?
		# discards the old graph
		#axes.clear()

		#TODO: is this necessary?
		# refresh canvas
		#self.canvas.draw()

	def plot_faults_quantity(self, mainWindowObject, title):
		data_to_plot = PlotData("bar",2)
			
			# sets data for graph
		data_to_plot.set_x_label("Team name")
		data_to_plot.set_y_label("Number of fouls commited")
			
			# sets data for bar 1 
		bar1 =  data_to_plot.get_entry(0)
		bar1.set_x_coordinate(self.get_team("l").get_name())
		bar1.set_value(self.get_team("l").get_number_of_faults_commited()) 
			
			# sets data for bar 2 
		bar2 = data_to_plot.get_entry(1) 
		bar2.set_x_coordinate(self.get_team("r").get_name())
		bar2.set_value(self.get_team("r").get_number_of_faults_commited()) 
		
			# calls the function to plot the graph 
		self.plot_graph(mainWindowObject, "bar", title, data_to_plot)

	def plot_faults_percentage(self, mainWindowObject, title):
		data_to_plot = PlotData("pie",2)

		# sets labels for each sector
			#TODO: está hardcoded, corrigir depois.
		data_to_plot.set_sector_labels(["RobôCin","Razi"])

		# aux variables for readability
		fouls_commited_by_l = self.get_team("l").get_number_of_faults_commited()
		fouls_commited_by_r = self.get_team("r").get_number_of_faults_commited()
		total_number_of_fouls = fouls_commited_by_l + fouls_commited_by_r

		# sets data for sector 1
		sector1 = data_to_plot.get_entry(0)
		sector1.set_value( (fouls_commited_by_l*100)/total_number_of_fouls)

		# sets data for sector 2
		sector2 = data_to_plot.get_entry(1)
		sector2.set_value( (fouls_commited_by_r*100)/total_number_of_fouls)


		self.plot_graph(mainWindowObject, "pie", title, data_to_plot)

	#TODO: SOLUÇÃO PALIATIVA, ELIMINAR QUANDO A DE BAIXO ESTIVER
	#	   PRONTA. (define a posição da falta pela posição da bola no momento em que a falta ocorreu)
	def plot_faults_position(self, mainWindowObject, title):
		data_to_plot = PlotData("scatter",2)
		
		teamL = data_to_plot.get_entry(0)
		teamL_x_positions = []
		teamL_y_positions = []

		teamR = data_to_plot.get_entry(1)
		teamR_x_positions = []
		teamR_y_positions = []
		
		for i in range(len(self.__data_frame)):
			if(self.__data_frame.iloc[i,1] == "foul_charge_l" and self.__data_frame.iloc[i-1,1] != "foul_charge_l"):
				teamL_x_positions.append(int(self.__data_frame.iloc[i,10]))
				teamL_y_positions.append(int(self.__data_frame.iloc[i,11]))
			elif(self.__data_frame.iloc[i,1] == "foul_charge_r" and self.__data_frame.iloc[i-1,1] != "foul_charge_r"):
				teamR_x_positions.append(int(self.__data_frame.iloc[i,10]))
				teamR_y_positions.append(int(self.__data_frame.iloc[i,11]))

		teamL.set_x_positions(teamL_x_positions)
		teamL.set_y_positions(teamL_y_positions)
		teamR.set_x_positions(teamR_x_positions)
		teamR.set_y_positions(teamR_y_positions)

		self.plot_graph(mainWindowObject, "scatter", title, data_to_plot)
	
	#TODO: TERMINAR IMPLEMENTAÇÃO, DEPOIS QUE RESOLVER O PROBLEMA
	#      DE DESCOBRIR QUEM FEZ A FALTA
	def _plot_faults_position(self, mainWindowObject, title):
		data_to_plot = PlotData("scatter",2)
		# sets data for team1
		team1 = data_to_plot.get_entry(0)
			# for each fault made by team "l", appends it to the data_to_plot's entry of the team it belongs to
		for fault in self.get_team("l").get_faults_commited():
			team1.append_fault(fault)
		# sets data for team 2
		team2 = data_to_plot.get_entry(1)
		for fault in self.get_team("r").get_faults_commited():
			team2.append_fault(fault)
		self.plot_graph(mainWindowObject, "scatter", title, data_to_plot)

	def plot_goals_quantity(self, mainWindowObject, title):
		data_to_plot = PlotData("bar",2)

		# sets data for graph
		data_to_plot.set_x_label("Team name")
		data_to_plot.set_y_label("Number of goals scored")
			
			# sets data for bar 1 
		bar1 =  data_to_plot.get_entry(0)
		bar1.set_x_coordinate(self.get_team("l").get_name())
		bar1.set_value(self.get_team("l").get_number_of_goals_scored()) 
			
			# sets data for bar 2 
		bar2 = data_to_plot.get_entry(1) 
		bar2.set_x_coordinate(self.get_team("r").get_name())
		bar2.set_value(self.get_team("r").get_number_of_goals_scored()) 
		
			# calls the function to plot the graph 
		self.plot_graph(mainWindowObject, "bar", title, data_to_plot)
	
	def plot_goals_percentage(self, mainWindowObject, title):
		data_to_plot = PlotData("pie",2)
		
		data_to_plot.set_sector_labels(["RobôCin","Razi"])

		# aux variables for readability
		goals_scored_l = self.get_team("l").get_number_of_goals_scored()
		goals_scored_r = self.get_team("r").get_number_of_goals_scored()
		total_number_of_goals = goals_scored_l + goals_scored_r
		print(total_number_of_goals)

		# sets data for sector 1
		sector1 = data_to_plot.get_entry(0)
		sector1.set_value( (goals_scored_l*100)/total_number_of_goals)

		# sets data for sector 2
		sector2 = data_to_plot.get_entry(1)
		sector2.set_value( (goals_scored_r*100)/total_number_of_goals)

		self.plot_graph(mainWindowObject, "pie", title, data_to_plot)


	#TODO: ESTE É O LOCAL, NO GOL, ONDE A BOLA ENTROU (LEMBRAR DE FAZER O GRÁFICO DA POSIÇÃO DE QUEM CHUTOU A BOLA Q RESULTOU EM GOL)
	def plot_goals_position(self, mainWindowObject, title):

		data_to_plot = PlotData("scatter",2)
		
		teamL = data_to_plot.get_entry(0)
		teamL_x_positions = []
		teamL_y_positions = []

		teamR = data_to_plot.get_entry(1)
		teamR_x_positions = []
		teamR_y_positions = []
		
		for i in range(len(self.__data_frame)):
			if(self.__data_frame.iloc[i,1] == "goal_l" and self.__data_frame.iloc[i-1,1] != "goal_l"):
				teamL_x_positions.append(int(self.__data_frame.iloc[i,10]))
				teamL_y_positions.append(int(self.__data_frame.iloc[i,11]))
			elif(self.__data_frame.iloc[i,1] == "goal_r" and self.__data_frame.iloc[i-1,1] != "goal_r"):
				teamR_x_positions.append(int(self.__data_frame.iloc[i,10]))
				teamR_y_positions.append(int(self.__data_frame.iloc[i,11]))

		teamL.set_x_positions(teamL_x_positions)
		teamL.set_y_positions(teamL_y_positions)
		teamR.set_x_positions(teamR_x_positions)
		teamR.set_y_positions(teamR_y_positions)

		self.plot_graph(mainWindowObject, "scatter", title, data_to_plot)