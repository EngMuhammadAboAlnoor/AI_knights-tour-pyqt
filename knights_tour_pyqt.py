# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 01:11:25 2024

@author: msi
"""
import sys
from PyQt5.QtWidgets import QSlider, QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QRadioButton, QGridLayout, QPushButton, QButtonGroup
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, pyqtSignal
import heapq, time
from collections import deque

##########################################################
##   Creating clickable Label class to represen         ##
##   the square on the chessboard                       ##
##########################################################
class ClickableLabel(QLabel):
    clicked = pyqtSignal(int, int)

    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col

    def mousePressEvent(self, event):
        self.clicked.emit(self.row, self.col)
        
##########################################################
##                   Program GUI class                  ##
##########################################################        
        
class ChessBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.board_size = 8
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Knight\'s Tour')
        self.setGeometry(350, 150, 600, 750) 
        self.start_position=(0,0)
        self.speedify = 15
        self.delay = 1/self.speedify
        self.stop_flag = False
        
        self.font_size = 30
        self.font = QFont('Arial', self.font_size)
        
        layout = QVBoxLayout()
        
        # Controls
        size_control_layout = QHBoxLayout()

        # Radio buttons to choose the size
        self.radio55 = QRadioButton("5x5")
        size_control_layout.addWidget(self.radio55)

        self.radio88 = QRadioButton("8x8")
        self.radio88.setChecked(True)
        self.radio88.toggled.connect(self.changeSize)
        size_control_layout.addWidget(self.radio88)

        # Add radio buttons to a group
        self.size_group = QButtonGroup()
        self.size_group.addButton(self.radio55)
        self.size_group.addButton(self.radio88)
        
        self.expanded_label = QLabel('Expanded Nodes: 0')
        size_control_layout.addWidget(self.expanded_label)
        
        layout.addLayout(size_control_layout)
    
        # Chessboard
        mid_layout = QHBoxLayout()
        self.board_widget = QWidget()
        self.board_color = QColor('#4565bf')
        self.board_widget.setStyleSheet("background-color: %s; " % self.board_color.name())
        self.grid_layout = QGridLayout(self.board_widget)
        self.labels = []
        
        self.drawBoard()
        
        mid_layout.addWidget(self.board_widget)
        # indicators and controls
        mid_right_layout = QVBoxLayout()
        
        self.speed_label = QLabel('Speed:\n100%')
        mid_right_layout.addWidget(self.speed_label)
        
        self.slider = QSlider(Qt.Vertical)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setTickInterval(10)
        self.slider.setValue(100)
        self.slider.setTickPosition(QSlider.TicksLeft)  
        self.slider.valueChanged.connect(self.sliderMoved)
        
        mid_right_layout.addWidget(self.slider)
        
        mid_layout.addLayout(mid_right_layout)
        
        layout.addLayout(mid_layout)
        # layout.addWidget(self.board_widget)
        
        # Controls
        control_layout = QHBoxLayout()
        
        self.iters_label = QLabel('Iterations: ')
        control_layout.addWidget(self.iters_label)
        
        self.iters_txt = QLineEdit('2500')
        control_layout.addWidget(self.iters_txt)
        
        self.start_lbl = QLabel('Start Position: ')
        control_layout.addWidget(self.start_lbl)
        
        self.start_position = [0, 0]
        self.start_pos_edit = QLineEdit(f'{self.start_position[0]},{self.start_position[1]}')
        self.start_pos_edit.setEnabled(False)
        self.start_pos_edit.setStyleSheet('background-color: white; color: black;')
        control_layout.addWidget(self.start_pos_edit)

        self.radioBFS = QRadioButton("BFS")
        self.radioDFS = QRadioButton("DFS")
        self.radioGreedy = QRadioButton("Greedy")
        self.radioAStar = QRadioButton("A*")
        self.radioWarnsdroff = QRadioButton("Warnsdorff")
        self.radioBFS.setChecked(True)

        control_layout.addWidget(self.radioBFS)
        control_layout.addWidget(self.radioDFS)
        control_layout.addWidget(self.radioGreedy)
        control_layout.addWidget(self.radioAStar)
        control_layout.addWidget(self.radioWarnsdroff)

        
        layout.addLayout(control_layout)
        
        # Add Buttons
        go_button = QPushButton("Go")
        go_button.clicked.connect(self.solve)
        # control_layout.addWidget(go_button)
        layout.addWidget(go_button)
        
        stop_button = QPushButton("Stop")
        stop_button.clicked.connect(self.stop_solving)
        # control_layout.addWidget(stop_button)
        layout.addWidget(stop_button)
        
        self.setLayout(layout)
        self.show()
        
    
    
    ## to control animation speed  ##
    #################################
    def sliderMoved(self):
        # pass
        self.delay = (11-self.slider.value()//10)/self.speedify
        self.speed_label.setText(f"Speed:\n{self.slider.value()} %")


    ##    choosing start square    ##
    #################################
    def labelClicked(self, row, col):
        self.start_pos_edit.setText(f"{row},{col}")
        self.start_position = [row, col]
        self.update_chessboard()
    
    
    ##  start solving by clicking  ##
    ##  on "Go" button             ##
    #################################
    def solve(self):
        self.board_color = QColor('#4565bf')
        self.stop_flag = False
        self.changeSize()
        N = self.board_size
        start_row, start_col = 0, 0
        position = window.start_pos_edit.text().strip().split(',')
        if position:
            start_row, start_col = list(map(int, position))
        state = [[-1 for _ in range(N)] for _ in range(N)]

        knightTour = KnightTour(state, start_row, start_col)
        
        solution = []
        if window.radioAStar.isChecked():
            solution = knightTour.solve_Astar()
        if window.radioDFS.isChecked():
            solution = knightTour.solve_DFS()
        if window.radioBFS.isChecked():
            solution = knightTour.solve_BFS()
        if window.radioGreedy.isChecked():
            solution = knightTour.solve_greedy()
        if window.radioWarnsdroff.isChecked():
            solution = knightTour.solve_warnsdorff()
        
        if solution !=None:
            color = '#9ce890' if len(solution) == N*N else '#f7d9ba'
            self.board_color = QColor(color)
            for label in self.labels: label.setText('')
            self.simulate(solution, start_row, start_col)
            
        
    ##  simulate solving process   ##
    ##  according to strategy      ##
    #################################
    def simulate(self, moves, start_row, start_col):
        
        ##  Inner function to get a square   ##
        ##  from chessboard                  ##
        #######################################
        def getSquare(row, col):
            return self.grid_layout.itemAtPosition(row, col).widget()
        
        row = start_row
        col = start_col
        pixmap = QPixmap("knight.png")
        label = getSquare(row, col)
        pixmap = pixmap.scaled(label.size(), aspectRatioMode=True)
        label.setPixmap(pixmap)
        previous_label = label
        self.update_chessboard()
        for order, move in enumerate(moves):
            if order == 0: continue
            dx = move[0]
            dy = move[1]
            time.sleep(self.delay)
            previous_label.setText(str(order))
            
            previous_label = getSquare(row+dx, col+dy)
            previous_label.setPixmap(pixmap)
            self.update_chessboard()
            row +=dx
            col +=dy
            if self.stop_flag: break
            
    
    
    ##  To update squares drawing on chessboard  ##
    ##  to simulate solution process             ##
    ###############################################
    def update_chessboard(self):
        size = 75 if self.board_size == 8 else 100
        self.board_widget.setStyleSheet("background-color: %s; " % self.board_color.name())
        for i in range(self.board_size):
            for j in range(self.board_size):
                label = self.grid_layout.itemAtPosition(i, j).widget()
                
                label.setFont(self.font)
                back_color = 'white' if (i + j) % 2 == 0 else 'grey'
                for_color = 'black' if (i + j) % 2 == 0 else 'white'
                if [i, j]==self.start_position:
                    back_color = '#48ba36'
                label.setStyleSheet(f"background-color: {back_color}; color: {for_color};")
                
                label.setFixedSize(size, size)
                label.setAlignment(Qt.AlignCenter)
                label.clicked.connect(self.labelClicked)
                label.lower()
                self.grid_layout.addWidget(label, i, j)
                self.labels.append(label)
        QApplication.processEvents()


    ##  To update only values on squares  ##
    ##  without deleting previous objects ##
    ########################################
    def update_gui(self, node):
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                label = self.grid_layout.itemAtPosition(i, j).widget()
                if node.state[i][j] != -1:
                    label.setText(str(node.state[i][j]))
                else:
                    label.setText('')
        QApplication.processEvents()

    

    ##  Change the board size                    ##
    ##  and recreate the chessboard             ##
    ###############################################
    def changeSize(self):
        self.board_color = QColor('#4565bf')
        self.board_size = 5 if self.radio55.isChecked() else 8
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)
        self.drawBoard()
    
    
    
    ##  to draw the chessboard at the prog       ##
    ##  launching and when changing size         ##
    ###############################################
    def drawBoard(self):
        self.labels.clear()
        self.board_widget.setStyleSheet("background-color: %s; " % self.board_color.name())
        size = 75 if self.radio88.isChecked() else 100
        for i in range(self.board_size):
            for j in range(self.board_size):
                label = ClickableLabel(i, j)
                
                label.setFont(self.font)
                back_color = 'white' if (i + j) % 2 == 0 else 'grey'
                for_color = 'black' if (i + j) % 2 == 0 else 'white'
                if (i, j)==self.start_position:
                    back_color = '#48ba36'
                label.setStyleSheet(f"background-color: {back_color}; color: {for_color};")

                
                label.setFixedSize(size, size) 
                label.setAlignment(Qt.AlignCenter)
                label.clicked.connect(self.labelClicked)
                label.lower()
                self.grid_layout.addWidget(label, i, j)
                self.labels.append(label)



    ## change stop flag enabling forced stopping ##
    ###############################################
    def stop_solving(self):
        self.stop_flag = True


    ## when closing the GUI, force stop kernel too ##
    #################################################
    def closeEvent(self, event):
        self.stop_flag = True
        event.accept()        

##########################################################
##  Class Node which represents each state and          ##

class Node:

    def __init__(self, state, row=0, column=0, order=1, parent=None, action=(0,0), depth=0):
        
        self.state=state
        self.row=row
        self.column=column
        self.order=order
        self.parent=parent
        self.action=action
        self.depth=depth
        self.heuristic = self.warnsdorff_heuristic()
        self.score = self.depth + self.heuristic

    def __lt__(self, other):
        return self.score < other.score

    def warnsdorff_heuristic(self):
        moves = self.get_moves()
        #if not moves:
            #return float('inf')
        #counts = [len(n.get_moves()) for n in moves]
        
        #return counts
       # print(len(moves))
        return len(moves)
    
    def get_moves(self):
        moves = []
        for dx, dy in [ (2, 1), (1, 2), (-1, -2),(-2, -1), (-1, 2), (1, -2), (2, -1), (-2, 1)]:
            row, col = self.row + dx, self.column + dy
            if 0 <= row < len(self.state) and 0 <= col < len(self.state[0]) and self.state[row][col] == -1:
                moves.append((dx, dy))
                #print(moves)
        return  moves
    #------------
    def move_knight(self, move, ignore_gn=False):
        new_row, new_col = self.row + move[0], self.column + move[1]
        new_state = [row[:] for row in self.state]
        new_state[new_row][new_col] = self.order +1
        return Node(new_state, new_row, new_col, self.order +1, self, move, self.depth + 1)
     #---------------
    def __eq__(self, other):
        return str(self.state) == str(other.state)
     #--------------
    def __hash__(self):
        return hash(str(self.state))
class KnightTour:
    def __init__(self, iput_state, start_row=0, start_col=0):
        self.initial_state = iput_state
        self.start_row = start_row
        self.start_col = start_col
        self.initial_state[self.start_row][self.start_col] = 1
#-----

    def solve_BFS(self):
      start_node = Node(self.initial_state )
      print ('iii',start_node)
      if start_node.heuristic == 0:
        return start_node
      #ننشئ رتل فارغ
      queue = []
      #العقد التي تم زيارتها
      visited = set()
      queue.append(start_node)
      #عداد العقد الموسعة
      expanded_nodes = 0
      iterations = int(window.iters_txt.text())
      while queue: 
        if window.stop_flag:
            return
        #يحذف العقدة الحالية
        current_node = queue.pop(0) 
       #نضيف العقدة الحالية إلى قائمة العقد المزارة
        visited.add(current_node)
        N=len(self.initial_state)
        if current_node.heuristic ==N*N or iterations==expanded_nodes:
           #ننشئ قائمة فارغة لتخزين المسار
            path = []
            node = current_node
            
            # for row in node.state: print(row)
            while node.parent:
                path.append(node.action)
                node = node.parent
            path.append(node.action)
            #نعكس قائمة المسار
            path.reverse()
            #print('path===',path)
            
            return path
        #زيد عداد العقد الموسعة بواحد
        expanded_nodes+=1
        window.expanded_label.setText(f'Expanded Nodes: {expanded_nodes}')
        window.update_gui(current_node) # Node should be replaced
        time.sleep(window.delay/process_faster)
        for move in current_node.get_moves():
              child_node = current_node.move_knight(move)

              if child_node not in visited:
                queue.append(child_node)
#------
    

    def solve_DFS(self):
        start_node = Node(self.initial_state)
        if start_node.heuristic == 0:
            return start_node
        stack = []
        visited = set()
        stack.append(start_node)
        expanded_nodes = 0
        iterations = int(window.iters_txt.text())
        while stack: # some condition required here
            if window.stop_flag:
                return
            current_node = stack.pop()
           
            visited.add(current_node)
            N=len(self.initial_state)
            if current_node.heuristic ==N*N or iterations==expanded_nodes:
                path = []
                node = current_node
            
                # for row in node.state: print(row)
                while node.parent:
                    path.append(node.action)
                    node = node.parent
                path.append(node.action)
                path.reverse()
                # print(path)
                return path
            expanded_nodes+=1
            window.expanded_label.setText(f'Expanded Nodes: {expanded_nodes}')
            window.update_gui(current_node) # Node should be replaced
            time.sleep(window.delay/process_faster)
            for move in current_node.get_moves():
                new_row, new_col = current_node.row + move[0], current_node.column + move[1]
                if 0 <= new_row < N and 0 <= new_col < N:
                 child_node = current_node.move_knight(move)
                 if child_node not in visited:
                    stack.append(child_node)
                  
    
   
    def solve_Astar(self):
        start_node = Node(self.initial_state)
        if start_node.heuristic == 0:
            return start_node
        open_list = []
        closed_list = set()
        heapq.heappush(open_list, start_node)
        expanded_nodes = 0
        iterations = int(window.iters_txt.text())
        while open_list: 
            if window.stop_flag:
                return
            current_node = heapq.heappop(open_list) 
            closed_list.add(current_node)
            N=len(self.initial_state)
            if current_node.heuristic ==N*N or iterations==expanded_nodes:
                path = []
                node = current_node
            
                # for row in node.state: print(row)
                while node.parent:
                    path.append(node.action)
                    node = node.parent
                path.append(node.action)
                path.reverse()
                # print(path)
                return path
            expanded_nodes+=1
            window.expanded_label.setText(f'Expanded Nodes: {expanded_nodes}')
            window.update_gui(current_node) # Node should be replaced
            time.sleep(window.delay/process_faster)
            for move in current_node.get_moves():
                child_node = current_node.move_knight(move)

                if child_node not in closed_list:
                    heapq.heappush(open_list, child_node)  

    def solve_greedy(self):
        start_node = Node(self.initial_state)
        if start_node.heuristic == 0:
            return start_node
        current_node = start_node
        expanded_nodes = 0
        iterations = int(window.iters_txt.text())
        while True: 
            if window.stop_flag:
                return
            N=len(self.initial_state)
            if current_node.heuristic ==N*N or iterations==expanded_nodes:
                path = []
                node = current_node
                
                # for row in node.state: print(row)
                while node.parent:
                    path.append(node.action)
                    node = node.parent
                path.append(node.action)
                path.reverse()
                # print(path)
                return path
            expanded_nodes+=1
            window.expanded_label.setText(f'Expanded Nodes: {expanded_nodes}')
            window.update_gui(current_node) # Node should be replaced
            time.sleep(window.delay/process_faster)
            
            moves = current_node.get_moves()
            if not moves:
                break
            best_move = min(moves, key=lambda move: current_node.move_knight(move).heuristic)
            current_node = current_node.move_knight(best_move)            
    def solve_warnsdorff(self):
        start_node = Node(self.initial_state, self.start_row, self.start_col, 1)
        if start_node.heuristic == 0:
            return start_node
        open_list = []
        closed_list = set()
        heapq.heappush(open_list, start_node)
        expanded_nodes = 0
        iterations = int(window.iters_txt.text())
        while open_list: 
            if window.stop_flag:
                return
            current_node = heapq.heappop(open_list) 
            closed_list.add(current_node)
            N=len(self.initial_state)
            if current_node.heuristic ==N*N or iterations==expanded_nodes:
                path = []
                node = current_node
                
                # for row in node.state: print(row)
                while node.parent:
                    path.append(node.action)
                    node = node.parent
                path.append(node.action)
                path.reverse()
                # print(path)
                return path
            expanded_nodes+=1
            window.expanded_label.setText(f'Expanded Nodes: {expanded_nodes}')
            window.update_gui(current_node) # Node should be replaced
            time.sleep(window.delay/process_faster)
            moves = current_node.get_moves()
            if not moves:
                continue
            best_move = min(moves, key=lambda move: current_node.move_knight(move).heuristic)
            child_node = current_node.move_knight(best_move)
            if child_node in closed_list:
                continue
            heapq.heappush(open_list, child_node)  

app = QApplication(sys.argv)
process_faster = 7
window = ChessBoard()
sys.exit(app.exec_())
