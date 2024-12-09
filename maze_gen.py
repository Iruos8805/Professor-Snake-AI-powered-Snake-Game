import tkinter as tk

CELL_SIZE = 20
GRID_ROWS = 30
GRID_COLS = 30
OUTPUT_FILE = "maze.txt"

def draw_grid():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x1, y1 = col * CELL_SIZE, row * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            canvas.create_rectangle(x1, y1, x2, y2, outline="gray")

def draw_wall(event):
    col = event.x // CELL_SIZE
    row = event.y // CELL_SIZE
    if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
        x1, y1 = col * CELL_SIZE, row * CELL_SIZE
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, fill="black")
        maze[row][col] = "#"

def erase_wall(event):
    col = event.x // CELL_SIZE
    row = event.y // CELL_SIZE
    if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
        x1, y1 = col * CELL_SIZE, row * CELL_SIZE
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")
        maze[row][col] = "_"

def start_draw(event):
    global drawing_mode
    drawing_mode = "draw"
    draw_wall(event)

def start_erase(event):
    global drawing_mode
    drawing_mode = "erase"
    erase_wall(event)

def on_drag(event):
    if drawing_mode == "draw":
        draw_wall(event)
    elif drawing_mode == "erase":
        erase_wall(event)

def save_maze():
    with open(OUTPUT_FILE, "w") as file:
        for row in maze:
            file.write("".join(row) + "\n")
    print(f"Maze saved to {OUTPUT_FILE}")

root = tk.Tk()
root.title("Interactive Maze Drawer")

canvas = tk.Canvas(root, width=GRID_COLS * CELL_SIZE, height=GRID_ROWS * CELL_SIZE, bg="white")
canvas.pack()

maze = [["_" for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
drawing_mode = None

canvas.bind("<Button-1>", start_draw)
canvas.bind("<Button-3>", start_erase)
canvas.bind("<B1-Motion>", on_drag)
canvas.bind("<B3-Motion>", on_drag)

tk.Button(root, text="Save Maze", command=save_maze).pack()

draw_grid()
root.mainloop()
