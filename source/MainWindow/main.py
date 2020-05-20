import sys

from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QWidget, QDialog, QGroupBox, QHBoxLayout, QVBoxLayout, QListWidget, QLabel, QMenuBar, QAction
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

import numpy as np
import pandas as pd

STATISTICS = "EXTRACTION_FIELDS"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.VIEW_FILLED = False

        ##### SCREEN INILIALIZATION #####
        #getting CURRENT monitor screen size
        #CHANGE:self.dimensions = QApplication(sys.argv)
        self.application = QApplication(sys.argv)
        self.screen = self.application.primaryScreen()
        self.rect = self.screen.availableGeometry()
        
        #declaring variables that holds the screen title and dimensions   
        self.title = 'RobôCIn statistics extractor'
        self.width = self.rect.width()
        self.height = self.rect.height()
        self.top = (self.rect.height()/2) - (self.height/2) 
        self.left = (self.rect.width()/2) -  (self.width/2) 
        
        #setting the title, icon image, dimensions(geometry), statusBar
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon('robocin-03-small.png'))
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.statusBar().showMessage("Statusbar - awaiting user control")
        ##### END OF SCREEN INITIALIZATION #####

        #setting the main layout to be horizontal
        self.main_hbox = QHBoxLayout()

        #creating the elements of the window (calling custom functions)
        self.init_Menu() # main menu at the top of the screen
        self.init_List() # left side list
        self.create_View("Escolha uma das opções na lista à esquerda") # right side graph area

        #creating central widget and putting it in the main window as a central widget
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_hbox)
        self.setCentralWidget(self.main_widget)
        
        #turns main window visible
        self.show()

    ##### Definition of custom functions #####
    def init_Menu(self):
        '''
        Creates the main menu and connects its actions to
        the respective function calls
        '''
        #creates the main menu at the top 
        self.mainMenu = self.menuBar()
        fileMenu = self.mainMenu.addMenu("File")
        editMenu = self.mainMenu.addMenu("Edit")
        selectionMenu = self.mainMenu.addMenu("Selection")
        viewMenu = self.mainMenu.addMenu("View")
        terminalMenu = self.mainMenu.addMenu("Terminal")
        helpMenu = self.mainMenu.addMenu("Help")
        #creates the "clear" action inside the "edit" option on the main menu 
        clearAction = QAction("Clear", self)
        editMenu.addAction(clearAction)
        #connects the "clear" action to the clear_View() function 
        clearAction.triggered.connect(self.clear_View) # when calling clear_View without specifying parameters, title hold a '0' int value
 

    def init_List(self):
        '''
        Creates the selection list
        '''
        # creates the selection list
        self.main_list = QListWidget()
        # defines the maximum and minimum dimensions of the list
        self.main_list.setMinimumHeight(300)
        self.main_list.setMaximumHeight(600)
        self.main_list.setMaximumWidth(181)
        self.main_list.setMinimumWidth(180)
        # creates the list items
        self.main_list.insertItem(0,"pie")
        self.main_list.insertItem(1,"bar")
        self.main_list.insertItem(2,STATISTICS)
        self.main_list.insertItem(3,STATISTICS)
        self.main_list.insertItem(4,STATISTICS)
        self.main_list.insertItem(5,STATISTICS)
        self.main_list.insertItem(6,STATISTICS)
        self.main_list.insertItem(7,STATISTICS)
        self.main_list.insertItem(8,STATISTICS)
        self.main_list.insertItem(9,STATISTICS)
        # adds the list to the main_hbox
        self.main_hbox.addWidget(self.main_list)
        # when an item is clicked on, sends a signal to the itemSelected() function 
        self.main_list.itemClicked.connect(self.itemSelected)
    
    def itemSelected(self, item):
        stat = item.text()
        self.create_View(stat)

    def create_View(self, title):  
        '''
        Creates the area, on the right side of the screen, where the plot the graphs on.
        '''
        # creates the view_groupBox (area where to plot the graphs on)
        self.view_groupBox = QGroupBox()
        # creates the layout of view_groupBox 
        self.layout = QVBoxLayout()
        # cleans the graph area, if there's already a graph being displayed  
        if self.VIEW_FILLED == True:
            self.clear_View(title)
        # creates the area where to plot the graphs
        self.plot_Area = self.create_Plot(title)
        # defines the layout of view_groupBox
        self.view_groupBox.setLayout(self.plot_Area)
        # adds the view_groupBox to the main_hbox 
        self.main_hbox.addWidget(self.view_groupBox) 
        self.VIEW_FILLED = True



    #TODO: ENTENDER O FUNCIONAMENTO INERNO DE CLEAR_VIEW
    def clear_View(self, title):
        for i in reversed(range(self.main_hbox.count())): 
            if i > 0:
                self.main_hbox.itemAt(i).widget().setParent(None)  
        self.VIEW_FILLED = False
        # if the clear_View function was called by a signal from: MainMenu -> edit -> clear, 
        if (title == 0):
            self.create_View("Escolha uma das opções na lista à esquerda")
    
    def create_Plot(self, title):
        '''
        Creates figure, cavas, navigationToolbar, and configures the layout.
        Calls the function to plot the graph.
        '''
        # creates a 'figure', where to plot the graphs on 
        self.figure = Figure()

        # creates a canvas widget, which displays the figure 
        self.canvas = FigureCanvas(self.figure)

        # creates and customize the graph title
        self.view_title = QLabel(title) 
        #self.view_title.setSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Minimum) 
        self.view_title.setAlignment(Qt.AlignCenter)
        self.view_title.setFont(QtGui.QFont("Arial",25,QtGui.QFont.Bold))

        # creates the navigationToolbar widget  
        if(title != "Escolha uma das opções na lista à esquerda"): 
            self.toolbar = NavigationToolbar(self.canvas, self)

        #(code snippet to plot a graph by pressing a button) 
        # Just some button connected to `plot` method
        #self.button = QPushButton('Plot')
        #self.button.clicked.connect(self.plot)

        # customizes the toolbar and canvas layout 
        space = QVBoxLayout()

        space.addWidget(self.view_title)
        if(title != "Escolha uma das opções na lista à esquerda"):
            space.addWidget(self.toolbar)
        space.addWidget(self.canvas) 

        # calls the function responsable of plotting the graph 
        if(title == "pie"):
            self.plot_Pie()
        elif(title == "bar"):
            self.plot_Bar()
        elif(title == "empty"):
            pass

        return space


    def plot_Bar(self):
        
        data = [50,50]

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.clear()

        # plot data
        ax.bar(data,2)

        # refresh canvas
        self.canvas.draw()


    def plot_Pie(self):

        data = [50,50]
        label = ["A", "B"]

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.clear()

        # plot data
        ax.pie(data, labels = label)

        # refresh canvas
        self.canvas.draw()
   
    def define_Log(self):
        self.log = pd.read_csv('./t1.rcg.csv1')

    def get_Score(self): 
        placar = [self.log['team_score_l'].max(),self.log['team_score_r'].max()]
        team_left = self.log.iloc[0].team_name_l
        team_right = self.log.iloc[0].team_name_r
        equipes = [team_left,team_right]
        eixox = np.arange(len(equipes))
    
    def getOut(self):
        sys.exit()


if __name__ == "__main__":
    Application = QApplication(sys.argv)
    Main = MainWindow()
    sys.exit(Application.exec())
