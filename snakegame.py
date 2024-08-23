from tkinter import *
import random

# Constants (Naming convention = All uppercase)
GAME_WIDTH = 700
GAME_HEIGHT = 600
SPEED = 100
SPACE_SIZE = 35
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# Handles the snake
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = [(0,0)] * BODY_PARTS
        self.squares = []
    
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR, tag = "snake")
            self.squares.append(square)

# Handles the food
class Food:
    def __init__(self):
        x = random.randint(0,int((GAME_WIDTH/SPACE_SIZE))-1) * SPACE_SIZE
        y = random.randint(0,int((GAME_HEIGHT/SPACE_SIZE))-1) * SPACE_SIZE

        self.coordinates = [x,y]

        canvas.create_rectangle(x, y, x + SPACE_SIZE//3, y + SPACE_SIZE, fill = FOOD_COLOR, tag = "food")
        canvas.create_rectangle(x + SPACE_SIZE//1.5, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = FOOD_COLOR, tag = "food")



# Handles each "round"
def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    head = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR)
    snake.squares.insert(0, head)

    update_snake_head(snake)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text = "Score:{}" .format(score))
        canvas.delete("food")
        food = Food()

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)

# Handles changing directions
def change_direction(new_direction):

    global direction

    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction 
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction       

# Handles collisions
def check_collisions(snake):
    x, y = snake.coordinates[0]

    """
    if x < 0 or x >= GAME_WIDTH: 
        print("GAME OVER")
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        print("GAME OVER")
        return True
    """

    if x < 0:
        x=GAME_WIDTH
    elif x >= GAME_WIDTH:
        x=0
    
    if y < 0:
        y=GAME_HEIGHT
    elif y >= GAME_HEIGHT:
        y=0

    snake.coordinates[0]=(x,y)
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True
        
    return False

def update_snake_head(snake):
    x, y = snake.coordinates[0]
    canvas.delete(snake.squares[0])

    if direction == "up":
        head = canvas.create_polygon(x + SPACE_SIZE//2, y, x, y + SPACE_SIZE, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    elif direction == "down":
        head = canvas.create_polygon(x, y, x + SPACE_SIZE, y, x + SPACE_SIZE//2, y + SPACE_SIZE, fill=SNAKE_COLOR)
    elif direction == "left":
        head = canvas.create_polygon(x + SPACE_SIZE, y, x + SPACE_SIZE, y + SPACE_SIZE, x, y + SPACE_SIZE//2, fill=SNAKE_COLOR)
    elif direction == "right":
        head = canvas.create_polygon(x, y, x, y + SPACE_SIZE, x + SPACE_SIZE, y + SPACE_SIZE//2, fill=SNAKE_COLOR)

    snake.squares[0] = head

# Handles the end of a game
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font = ("consolas", 70), text = "GAME OVER", fill = "red", tag = "gameover")

window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = "down"

label = Label(window,text = "Score:{}".format(score), font = ("consolas", 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

window.bind("<a>", lambda event: change_direction("left"))
window.bind("<d>", lambda event: change_direction("right"))
window.bind("<w>", lambda event: change_direction("up"))
window.bind("<s>", lambda event: change_direction("down"))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()