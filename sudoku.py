import pygame, sys, requests
import pygame, sys
import requests
from bs4 import BeautifulSoup
from main_settings import *
from button_settings import *

class Sudoku:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((win_width, win_height))
        self.running = True
        self.grid = finishedBoard
        self.selected = None
        self.mouse_position = None
        self.state = "playing"
        self.compleated = False
        self.blocks_changed = False
        self.button_present = []
        self.fixedcells = []
        self.wrongcells = []
        self.font = pygame.font.SysFont("arial", block_size//2)
        self.grid = []
        self.getPuzzle("4")
        self.load()
    def run(self):
        while self.running:
            if self.state == "playing":
                self.running_events()
                self.running_update()
                self.running_drawing()
        pygame.quit()
        sys.exit()

# required
    def allCellsDone(self):
        for row in self.grid:
            for number in row:
                if number == 0:
                    return False
        return True

    def checkAllCells(self):
        self.checkRows()
        self.checkCols()
        self.checkSmallGrid()

    def checkSmallGrid(self):
        for x in range(3):
            for y in range(3):
                possibles = [1,2,3,4,5,6,7,8,9]
                # print("re-setting possibles")
                for i in range(3):
                    for j in range(3):
                        # print(x*3+i, y*3+j)
                        x_index = x*3+i
                        y_index = y*3+j
                        if self.grid[y_index][x_index] in possibles:
                            possibles.remove(self.grid[y_index][x_index])
                        else:
                            if [x_index, y_index] not in self.fixedcells and [x_index, y_index] not in self.wrongcells:
                                self.wrongcells.append([x_index, y_index])
                            if [x_index, y_index] in self.fixedcells:
                                for k in range(3):
                                    for l in range(3):
                                        xidx2 = x*3+k
                                        yidx2 = y*3+l
                                        if self.grid[yidx2][xidx2] == self.grid[y_index][x_index] and [xidx2, yidx2] not in self.fixedcells:
                                            self.wrongcells.append([xidx2, yidx2])

    def checkRows(self):
        for y_index, row in enumerate(self.grid):
            possibles = [1,2,3,4,5,6,7,8,9]
            for x_index in range(9):
                if self.grid[y_index][x_index] in possibles:
                    possibles.remove(self.grid[y_index][x_index])
                else:
                    if [x_index, y_index] not in self.fixedcells and [x_index, y_index] not in self.wrongcells:
                        self.wrongcells.append([x_index, y_index])
                    if [x_index, y_index] in self.fixedcells:
                        for k in range(9):
                            if self.grid[y_index][k] == self.grid[y_index][x_index] and [k, y_index] not in self.fixedcells:
                                self.wrongcells.append([k, y_index])


    def checkCols(self):
        for x_index in range(9):
            possibles = [1,2,3,4,5,6,7,8,9]
            for y_index, row in enumerate(self.grid):
                if self.grid[y_index][x_index] in possibles:
                    possibles.remove(self.grid[y_index][x_index])
                else:
                    if [x_index, y_index] not in self.fixedcells and [x_index, y_index] not in self.wrongcells:
                        self.wrongcells.append([x_index, y_index])
                    if [x_index, y_index] in self.fixedcells:
                        for k, row in enumerate(self.grid):
                            if self.grid[k][x_index] == self.grid[y_index][x_index] and [x_index, k] not in self.fixedcells:
                                self.wrongcells.append([x_index, k])

##### HELPER FUNCTIONS #####
    def getPuzzle(self, difficulty):
        html_doc = requests.get("https://nine.websudoku.com/?level={}".format(difficulty)).content
        soup = BeautifulSoup(html_doc)
        ids = ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f10', 'f11',
        'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f20', 'f21', 'f22', 'f23',
        'f24', 'f25', 'f26', 'f27', 'f28', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35',
        'f36', 'f37', 'f38', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47',
        'f48', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f60',
        'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68', 'f70', 'f71', 'f72',
        'f73', 'f74', 'f75', 'f76', 'f77', 'f78', 'f80', 'f81', 'f82', 'f83', 'f84',
        'f85', 'f86', 'f87', 'f88']
        data = []
        for cid in ids:
            data.append(soup.find('input', id=cid))
        board = [[0 for x in range(9)] for x in range(9)]
        for index, cell in enumerate(data):
            try:
                board[index//9][index%9] = int(cell['value'])
            except:
                pass
        self.grid = board
        self.load()

    def shadeIncorrectCells(self, window, incorrect):
        for cell in incorrect:
            pygame.draw.rect(window, error_color, (cell[0]*block_size+grid_position[0], cell[1]*block_size+grid_position[1], block_size, block_size))

    def shadeLockedCells(self, window, locked):
        for cell in locked:
            pygame.draw.rect(window, fixedcells_color, (cell[0]*block_size+grid_position[0], cell[1]*block_size+grid_position[1], block_size, block_size))

    def drawNumbers(self, window):
        for y_index, row in enumerate(self.grid):
            for x_index, num in enumerate(row):
                if num != 0:
                    pos = [(x_index*block_size)+grid_position[0], (y_index*block_size)+grid_position[1]]
                    self.textToScreen(window, str(num), pos)

    def drawSelection(self, window, pos):
        pygame.draw.rect(window, lightblue, ((pos[0]*block_size)+grid_position[0], (pos[1]*block_size)+grid_position[1], block_size, block_size))

    def drawGrid(self, window):
        pygame.draw.rect(window, black, (grid_position[0], grid_position[1], win_width-150, win_height-150), 2)
        for x in range(9):
            pygame.draw.line(window, black, (grid_position[0]+(x*block_size), grid_position[1]), (grid_position[0]+(x*block_size), grid_position[1]+450), 2 if x % 3 == 0 else 1)
            pygame.draw.line(window, black, (grid_position[0], grid_position[1]+(x*block_size)), (grid_position[0]+450, grid_position[1]++(x*block_size)), 2 if x % 3 == 0 else 1)

    def mouseOnGrid(self):
        if self.mouse_position[0] < grid_position[0] or self.mouse_position[1] < grid_position[1]:
            return False
        if self.mouse_position[0] > grid_position[0]+gridsize or self.mouse_position[1] > grid_position[1]+gridsize:
            return False
        return ((self.mouse_position[0]-grid_position[0])//block_size, (self.mouse_position[1]-grid_position[1])//block_size)

    def loadButtons(self):
        self.button_present.append(Button(  20, 40, win_width//7, 40,function=self.checkAllCells,colour=(27,142,207),text="Submit"))
        self.button_present.append(Button(  140, 40, win_width//7, 40,colour=(117,172,112),function=self.getPuzzle,params="1",text="Easy"))
        self.button_present.append(Button(  win_width//2-(win_width//7)//2, 40, win_width//7, 40,colour=(204,197,110),function=self.getPuzzle,params="2",text="Medium"))
        self.button_present.append(Button( 380, 40, win_width//7, 40,colour=(199,129,48),function=self.getPuzzle,params="3",text="Hard"))
        self.button_present.append(Button(  500, 40, win_width//7, 40,colour=(207,68,68),function=self.getPuzzle,params="4",text="Evil"))

    def textToScreen(self, window, text, pos):
        font = self.font.render(text, False, black)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (block_size-fontWidth)//2
        pos[1] += (block_size-fontHeight)//2
        window.blit(font, pos)

    def load(self):
        self.button_present = []
        self.loadButtons()
        self.fixedcells = []
        self.wrongcells = []
        self.compleated = False

        # Setting locked cells from original board
        for y_index, row in enumerate(self.grid):
            for x_index, num in enumerate(row):
                if num != 0:
                    self.fixedcells.append([x_index, y_index])

    def isInt(self, string):
        try:
            int(string)
            return True
        except:
            return False

    



    def running_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # User clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()
                if selected:
                    self.selected = selected
                else:
                    self.selected = None
                    for button in self.button_present:
                        if button.highlighted:
                            button.click()

            # User types a key
            if event.type == pygame.KEYDOWN:
                if self.selected != None and self.selected not in self.fixedcells:
                    if self.isInt(event.unicode):
                        # cell changed
                        self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
                        self.blocks_changed = True

    def running_update(self):
        self.mouse_position = pygame.mouse.get_pos()
        for button in self.button_present:
            button.update(self.mouse_position)

        if self.blocks_changed:
            self.wrongcells = []
            if self.allCellsDone():
                # Check if board is correct
                self.checkAllCells()
                if len(self.wrongcells) == 0:
                    self.compleated = True


    def running_drawing(self):
        self.window.fill(white)

        for button in self.button_present:
            button.draw(self.window)

        if self.selected:
            self.drawSelection(self.window, self.selected)

        self.shadeLockedCells(self.window, self.fixedcells)
        self.shadeIncorrectCells(self.window, self.wrongcells)

        self.drawNumbers(self.window)

        self.drawGrid(self.window)
        pygame.display.update()
        self.blocks_changed = False


    