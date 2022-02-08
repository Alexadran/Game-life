import pygame
import time

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.map = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.cell_size = 20

    def view(self, top, left, cell_size):
        self.top = top
        self.left = left
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j] == 1:
                    pygame.draw.rect(screen, GREEN, (
                        j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
                    pygame.draw.rect(screen, WHITE, (
                        j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size), 1)
                else:
                    pygame.draw.rect(screen, WHITE, (
                        j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size), 1)
                self.board[i][j] = (
                    j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        for num1, i in enumerate(self.board):
            for num2, j in enumerate(i):
                if (j[0] <= x <= j[2] + j[0]) and (j[1] <= y <= j[3] + j[1]):
                    return num2, num1
        return None

    def on_click(self, cell_cords):
        x, y = cell_cords
        self.map[y][x] = 1

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


class Life(Board):
    def __init__(self, width, height):
        super().__init__(width, height)

    def next_move(self):
        deleted = list()
        new = list()

        """ подготавливаем список клеток для удаления и создания,
        ведь иначе клетки удалятся раньше(соседи исчезнут) 
        или создадутся раньше(появятся соседиБ которых ранее не было) """

        for y, cells in enumerate(self.map):
            for x, cell in enumerate(cells):
                if cell == 0:
                    # print(self.map[y][x - 1])
                    # [print(i) for i in self.map]
                    # print("\n")
                    # print(x, y, "x, y")
                    # print("[y][x + 1]", self.map[y][x + 1], ' this')
                    # print("[y][x - 1]", self.map[y][x - 1], ' this')
                    # print("[y + 1][x + 1]", self.map[y + 1][x + 1], ' this')
                    # print("[y + 1][x - 1]", self.map[y + 1][x - 1], ' this')
                    # print("[y + 1][x]", self.map[y + 1][x], ' this')
                    # print("self.map[y - 1][x]", self.map[y - 1][x], ' this')
                    # print("[y - 1][x + 1]", self.map[y - 1][x + 1], "this")
                    # print("[y - 1][x - 1]", self.map[y - 1][x - 1], "this\n\n")
                    col = 0  # количество живых соседей
                    if x + 1 < len(self.map[y]) and self.map[y][x + 1]:
                        col += 1
                    if x - 1 >= 0 and self.map[y][x - 1]:
                        col += 1
                    if y + 1 < len(self.map) and x + 1 < len(self.map[y + 1]) and self.map[y + 1][x + 1]:
                        col += 1
                    if y + 1 < len(self.map) and x - 1 >= 0 and self.map[y + 1][x - 1]:
                        col += 1
                    if y + 1 < len(self.map) and self.map[y + 1][x]:
                        col += 1
                    if y - 1 >= 0 and self.map[y - 1][x]:
                        col += 1
                    if y - 1 >= 0 and x + 1 < len(self.map[y - 1]) and self.map[y - 1][x + 1]:
                        col += 1
                    if y - 1 >= 0 and x - 1 >= 0 and self.map[y - 1][x - 1]:
                        col += 1

                    """ Проверка всех 8 соседей """

                    if col == 3:  # рождается
                        new.append((y, x))
                elif cell == 1:
                    col = 0  # количество живых соседей
                    if x + 1 < len(self.map[y]) and self.map[y][x + 1]:
                        col += 1
                    if x - 1 >= 0 and self.map[y][x - 1]:
                        col += 1
                    if y + 1 < len(self.map) and x + 1 < len(self.map[y + 1]) and self.map[y + 1][x + 1]:
                        col += 1
                    if y + 1 < len(self.map) and x - 1 >= 0 and self.map[y + 1][x - 1]:
                        col += 1
                    if y + 1 < len(self.map) and self.map[y + 1][x]:
                        col += 1
                    if y - 1 >= 0 and self.map[y - 1][x]:
                        col += 1
                    if y - 1 >= 0 and x + 1 < len(self.map[y - 1]) and self.map[y - 1][x + 1]:
                        col += 1
                    if y - 1 >= 0 and x - 1 >= 0 and self.map[y - 1][x - 1]:
                        col += 1

                    """ Проверка всех 8 соседей """

                    if col > 3 or col < 2:  # умирает
                        deleted.append((y, x))

        for y, x in new:
            self.map[y][x] = 1

        for y, x in deleted:
            self.map[y][x] = 0


class Game:
    def __init__(self, height: int, weight: int, fps: int):
        self.__size = self.height, self.weight = height, weight  # разрешение экрана
        self.__fps = fps  # fps
        pygame.init()
        self.__screen = pygame.display.set_mode(self.__size)  # отрисовка рабочего окна
        self.__clock = pygame.time.Clock()  # fps
        self.life = Life(30, 30)
        self.time_for_sleep = 0.025

    def run(self) -> None:
        """
        Основной цикл игры
        :return: None
        """
        start = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not start:
                        self.life.get_click(event.pos)
                    elif event.button == 3:  # right click
                        start = True
                    elif event.button == 4 and start:  # scroll up
                        if self.time_for_sleep > 0:
                            self.time_for_sleep -= 0.05
                    elif event.button == 5 and start:  # scroll down
                        if self.time_for_sleep < 0.5:
                            self.time_for_sleep += 0.05

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start = not start

            self.__screen.fill('black')
            if start:
                self.life.next_move()
                time.sleep(self.time_for_sleep)
            self.life.render(self.__screen)
            pygame.display.flip()
            self.__clock.tick(self.__fps)


game = Game(600, 600, 30)
game.run()
