import tkinter as tk
from idlelib.configdialog import font_sample_text
from sys import maxsize
from tkinter import ttk
from venv import logger

import customtkinter as ctk
import ctypes
import random
import json

from src.algorithms.recursive_best_first_search import recursive_best_first_search, FAILURE

WINDOW_WIDTH = round(927*1.75)
WINDOW_HEIGHT = round(695*1.75)
NODE_COLOR = "#784794"

ctypes.windll.shcore.SetProcessDpiAwareness(1)

class Visualizer:
    def __init__(self, problem, node_canvas_data_file):

        self.paused = True
        self.problem = problem

        # load node positions
        node_canvas_data = json.loads(open(node_canvas_data_file).read())
        self.node_positions = {node["nodeName"]: ({"x": node["position"]["x"], "y": node["position"]["y"]})
                               for node in node_canvas_data["nodes"]}

        # create widgets
        # ==============
        self.window = tk.Tk()
        self.window.title("RBFS Visualizer")
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.center()

        self.main_frame = tk.Frame(
            self.window,
            background="#C4C4C4",
            relief="ridge",
            padx=51,
            pady=20
        )
        self.main_frame.grid(column=0, row=0, sticky="nsew")
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        self.narration_box = tk.Frame(
            self.main_frame,
            background="#E1E1E1",
        )
        self.narration_box.grid(row=0, column=0, sticky="nsew", pady=(0, 26))

        self.narration_text = tk.Label(
            self.narration_box,
            foreground="black",
            background=self.narration_box["background"],
            font=("Inter Bold", 18),
            text="Narration"
        )
        self.narration_text.pack(expand=True, fill="both")

        self.graph_canvas = tk.Canvas(
            self.main_frame,
            background="white",
            bd=10,
            highlightthickness=5,
            highlightbackground="black",
        )
        self.graph_canvas.grid(row=1, column=0, sticky="nsew", pady=(0, 26))

        self.bottom_frame = tk.Frame(
            self.main_frame,
            background=self.main_frame["background"]
        )
        self.bottom_frame.grid(row=2, column=0, sticky="nsew", pady=(10, 10))
        self.bottom_frame.columnconfigure(0, weight=4)  # First column (wider)
        self.bottom_frame.columnconfigure(1, weight=1)  # Second column (narrower)
        self.bottom_frame.rowconfigure(0, weight=1)

        self.nodes_in_memory_frame = tk.Frame(
            self.bottom_frame,
            background=self.narration_box["background"],
            padx=13,
            pady=8
        )
        self.nodes_in_memory_frame.grid(row=0, column=0, sticky="nsew")

        self.nodes_in_memory_frame.rowconfigure(0, weight=0)
        self.nodes_in_memory_frame.rowconfigure(1, weight=3)
        self.nodes_in_memory_frame.columnconfigure(0, weight=1)

        self.nodes_in_memory_label = tk.Label(
            self.nodes_in_memory_frame,
            text="Nodes in memory",
            font=("Inter Bold", 14),
            background=self.narration_box["background"],
        )
        self.nodes_in_memory_label.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        self.nodes_view_frame = tk.Frame(
            self.nodes_in_memory_frame,
            background=self.narration_box["background"],
        )
        self.nodes_view_frame.grid(row=1, column=0, sticky="nsew")

        self.play_button = tk.Button(
            self.bottom_frame,
            text="Start",
            background="#1D1D1D",
            foreground="white",
            font=("Inter Bold", 18),
            command=self.toggle_pause
        )
        self.play_button.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        self.bottom_frame.rowconfigure(0, weight=1)

        self.main_frame.rowconfigure(0, weight=1)  # narration_box
        self.main_frame.rowconfigure(1, weight=5)  # graph_canvas
        self.main_frame.rowconfigure(2, weight=1)  # play_button
        # make column take up all available space
        self.main_frame.columnconfigure(0, weight=1)
        # ==============

        self.CANVAS_WIDTH = self.graph_canvas.winfo_width()
        self.CANVAS_HEIGHT = self.graph_canvas.winfo_height()

        self.draw_graph()
        self.set_narration_text("Press the start button to begin.")
        self.started = False

    def start(self):
        self.window.mainloop()

    def toggle_pause(self):
        """
        Switch the state of the button between "Play" and "Pause".
        """
        if self.started:
            self.paused = not self.paused
            self.play_button.config(text="Play" if self.paused else "Pause")
        else:
            self.started = True
            self.paused = False
            self.play_button.config(text="Pause")
            self.animate(recursive_best_first_search(self.problem))

    def highlight_node(self, node_state, color="red", tag="node"):
        """
        Highlight a node on the graph canvas.
        """

        x, y = self.node_positions[node_state]["x"], self.node_positions[node_state]["y"]

        self.draw_node(x, y, node_state, outline=color, tag=tag)
        logger.info(f"Highlighting node {node_state}")

        self.main_frame.update()

    def highlight_edge(self, u, v, color="red", tag="edge"):
        """
        Highlight an edge on the graph canvas.
        """

        x1, y1 = self.node_positions[u]["x"], self.node_positions[u]["y"]
        x2, y2 = self.node_positions[v]["x"], self.node_positions[v]["y"]

        self.graph_canvas.create_line(
            x1, y1, x2, y2,
            fill=color,
            width=3,
            tags=tag
        )

        self.main_frame.update()

    def set_narration_text(self, text):
        """
        Add a text to the narration box.
        """

        self.narration_text["text"] = text
        self.main_frame.update()

    def center(self):
        """ gets the coordinates of the center of the screen """
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        # coordinates of the upper left corner of the window to make the window appear in the center
        x_coord = int((screen_width / 2) - (WINDOW_WIDTH / 2))
        y_coord = int((screen_height / 2) - (WINDOW_HEIGHT / 2))
        self.window.geometry("{}x{}+{}+{}".format(WINDOW_WIDTH, WINDOW_HEIGHT, x_coord, y_coord))

    def draw_graph(self):

        # draw nodes
        for node in self.node_positions.keys():
            self.draw_node(self.node_positions[node]["x"], self.node_positions[node]["y"], node)

        # draw edges (and label their weights)
        edge_weight_dictionary = self.problem.get_edges_and_weight()
        for (u, v) in edge_weight_dictionary.keys():
            self.draw_edge(u, v, edge_weight_dictionary[(u, v)])

        # set node labels to be on top
        self.graph_canvas.tag_raise("label")
        # set nodes to be on top of edges
        self.graph_canvas.tag_raise("node")

    def draw_edge(self, u, v, weight):
        self.graph_canvas.create_line(
            self.node_positions[u]["x"],
            self.node_positions[u]["y"],
            self.node_positions[v]["x"],
            self.node_positions[v]["y"],
            fill="black",
            width=3
        )

        # determine the mid point of edge, where the weight label will be displayed
        mid_x, mid_y = (((self.node_positions[u]["x"] + self.node_positions[v]["x"]) // 2),
                        ((self.node_positions[u]["y"] + self.node_positions[v]["y"]) // 2))
        self.draw_label_with_background(mid_x, mid_y, str(weight), tag="weight_label", font_size=6)

    def draw_node(self, x, y, name, outline="black", tag="node"):

        self.graph_canvas.create_oval(
            x-15,
            y-15,
            x+15,
            y+15,
            fill=NODE_COLOR,
            outline=outline,
            width=2,
            tags=tag
        )
        self.draw_label_with_background(x, y+30, name)

    def draw_label_with_background(self, x, y, text, tag="label", font_size=10, padding=5):
        text_width = (font_size * len(text)) // 1.5
        text_height = font_size + 4

        self.graph_canvas.create_rectangle(
            x - text_width - padding, y - text_height - padding,
            x + text_width + padding, y + text_height + padding,
            fill="white", outline="white",
            tags=tag
        )
        self.graph_canvas.create_text(
            x,
            y,
            text=text,
            font=("Inter Bold", font_size),
            fill="black",
            tags=tag
        )

    def animate(self, rbfs_generator):

        if self.paused:
            return # do nothing (pause)

        try:
            # generator yields a node or a message string
            yielded = next(rbfs_generator)

            if yielded == FAILURE:
                # TODO: backtracking?
                # potentially clear current_node_highlight tagged nodes
                print("Failure, no solution found.")
                return

            if type(yielded) is str:
                self.set_narration_text(yielded)
            else: # yielded a node

                # check if goal node reached
                if yielded.state == self.problem.goal_state:
                    print("Goal state reached.")
                    self.highlight_node(yielded.state, color="green")
                    return

                # highlight current node
                self.highlight_node(yielded.state, color="orange", tag="current_node_highlight")
                # clear all potential edges highlighted
                self.graph_canvas.delete("potential_edge_highlight")
                # highlight the edge between the current node and its predecessor
                if yielded.predecessor is not None:
                    self.highlight_edge(yielded.state, yielded.predecessor.state, color="orange")

            if not self.paused:
                self.window.after(2000, lambda: self.animate(rbfs_generator))

        except StopIteration:
            print("Algorithm finished.")
            return




    '''
    # chatgpt answer
    def draw_graph(self):
        """Draw the graph with nodes and edges."""
        self.canvas.delete("all")  # Clear canvas before redrawing

        # Draw edges (roads)
        for u, v in self.graph.edges:
            x1, y1 = self.positions[u]
            x2, y2 = self.positions[v]
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
            weight = self.graph[u][v]['weight']
            mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
            self.canvas.create_text(mid_x, mid_y, text=str(weight), font=("Arial", 10))

        # Draw nodes (cities)
        for node, (x, y) in self.positions.items():
            self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="lightgray", outline="black",
                                    width=2)
            self.canvas.create_text(x, y, text=node, font=("Arial", 12))

    # stefan answer
    def plotPoint(city, canvas, color="blue", size=12):
        # Compute the coordinates relative to the canvas center
        canvas_x = CENTER_X + city.x * MULTIPLIER
        canvas_y = CENTER_Y - city.y * MULTIPLIER

        canvas.create_oval(canvas_x + size / 2, canvas_y + size / 2, canvas_x - size / 2, canvas_y - size / 2,
                           fill=color)
        canvas.create_text(canvas_x - 10, canvas_y - 15, text=city.getName())
        canvas.create_text(canvas_x - 20, canvas_y + 20, text=city.fScore)

    def plotCityPoints(cities, canvas):
        for city in cities.values():
            plotPoint(city, canvas)

    def drawLine(city1, city2, canvas, color="black", width=1):
        canvas_x1 = CENTER_X + city1.x * MULTIPLIER
        canvas_y1 = CENTER_Y - city1.y * MULTIPLIER
        canvas_x2 = CENTER_X + city2.x * MULTIPLIER
        canvas_y2 = CENTER_Y - city2.y * MULTIPLIER

        canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2, fill=color, width=width)

    def plotCityConnections(connections, canvas):

        for city in connections:
            for connection in connections[city]:
                drawLine(city, connection, canvas)

    def drawCurrentPath(path, canvas):
        for i in range(1, len(path)):
            drawLine(path[i - 1], path[i], canvas, color="blue", width=2)

    def visualiser(generator, canvas, cities, connections):
        # This will update the canvas at each step.

        try:
            arg1, arg2, arg3 = next(generator)  # Get the next step in the algorithm
            # Codes: arg1 = None => arg2 is a path to be drawn
            #   arg2 = None => algorithm finished.
            #   else: arg1 = current point, arg2 = neighbor
            #   arg3 is used to draw the shortest path known so far

            canvas.delete("all")
            plotCityConnections(connections, canvas)
            plotCityPoints(cities, canvas)

            if arg2 is None:
                # Get in this case when the A* is done with a path.
                for i in range(1, len(arg1)):
                    drawLine(arg1[i - 1], arg1[i], canvas, color="green", width=3)
                print("A* Algorithm Finished!")
                return


            elif arg1 is None:
                # This draws the path
                drawCurrentPath(arg2, canvas)

            else:

                plotPoint(arg1, canvas, color="yellow")
                drawCurrentPath(arg3, canvas)
                drawLine(arg1, arg2, canvas, "red", 3)

            canvas.after(1000, visualiser, generator, canvas, cities, connections)

        except StopIteration:

            print("A* Algorithm Finished!")

    # Helper functions
    def modifyDistanceByPercentage(percentage):
        # relative to 0,0
        with open('Heuristics.csv', 'r', newline='\n') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                new_row = row[0] + "," + row[1] + "," + str(float(row[2]) * percentage) + "," + str(
                    float(row[3]) * percentage)
                print(new_row)

    def shiftPositionOnAxis(axis, distance):
        if axis == 'x' or axis == 'X':
            with open('Heuristics.csv', 'r', newline='\n') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    new_row = row[0] + "," + row[1] + "," + str(float(row[2]) + distance) + "," + row[3]
                    print(new_row)
        if axis == 'y' or axis == 'Y':
            with open('Heuristics.csv', 'r', newline='\n') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    new_row = row[0] + "," + row[1] + "," + row[2] + "," + str(float(row[3]) + distance)
                    print(new_row)
    '''