import tkinter as tk
from idlelib.configdialog import font_sample_text
from sys import maxsize
from tkinter import ttk
from venv import logger

import customtkinter as ctk
import ctypes
import random
import json

from src.classes.problem_state import Color

from src.algorithms.recursive_best_first_search import recursive_best_first_search, FAILURE
from src.classes.edge import Edge

WINDOW_WIDTH = round(927*1.75)
WINDOW_HEIGHT = round(695*1.75)
NODE_COLOR = "#784794"

ctypes.windll.shcore.SetProcessDpiAwareness(1)

class Visualizer:
    def __init__(self, problem, node_canvas_data_file):

        self.paused = True
        self.problem = problem
        self.rbfs_generator = None
        self.extensions = 0

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
        self.nodes_view_frame.rowconfigure(0, weight=1) # single row

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
            print("Paused" if self.paused else "Playing")
            self.play_button.config(text="Play" if self.paused else "Pause")
            if not self.paused:
                self.animate(self.rbfs_generator)
        else:
            self.started = True
            self.paused = False
            self.play_button.config(text="Pause")
            self.clear_highlights()
            self.clear_nodes_in_memory()
            self.rbfs_generator = recursive_best_first_search(self.problem)
            self.animate(self.rbfs_generator)

    def highlight_node(self, node_state, color: Color, tag: str):
        """
        Highlight a node on the graph canvas.
        """

        x, y = self.node_positions[node_state]["x"], self.node_positions[node_state]["y"]

        self.draw_node(
            x, y,
            node_state,
            outline=color.value,
            width=10,
            tag=tag
        )

    def highlight_edge(self, u_state, v_state, color: Color, tag: str):
        """
        Highlight an edge on the graph canvas.
        """

        x1, y1 = self.node_positions[u_state]["x"], self.node_positions[u_state]["y"]
        x2, y2 = self.node_positions[v_state]["x"], self.node_positions[v_state]["y"]

        self.graph_canvas.create_line(
            x1, y1, x2, y2,
            fill=color.value,
            width=10,
            tags=tag
        )

    def set_narration_text(self, text):
        """
        Add a text to the narration box.
        """

        self.narration_text["text"] = text

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
        self.draw_label_with_background(mid_x, mid_y,
                                        str(weight),
                                        color="white",
                                        tag="weight_label",
                                        font_size=6)

    def draw_node(self, x, y, name, outline="black", width=3, tag="node"):

        self.graph_canvas.create_oval(
            x-15,
            y-15,
            x+15,
            y+15,
            fill=NODE_COLOR,
            outline=outline,
            width=width,
            tags=tag
        )
        self.draw_label_with_background(x, y+30, name)

    def draw_label_with_background(self, x, y, text, color="", tag="label", font_size=10, padding=5):
        text_width = (font_size * len(text)) // 1.5
        text_height = font_size + 4

        self.graph_canvas.create_rectangle(
            x - text_width - padding, y - text_height - padding,
            x + text_width + padding, y + text_height + padding,
            fill=color, outline=color,
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

    def update_window(self, problem_state):

        # clear all previous highlights
        self.clear_highlights()

        # iterate in problem_state.highlighted
        for node_state_tuple, color in problem_state.highlighted.items():
            # highlight elements with dark green
            if color == Color.DARK_GREEN:
                if len(node_state_tuple) == 1:
                    self.highlight_node(node_state_tuple[0], color, tag="expanded_node_highlight")
                else:
                    self.highlight_edge(node_state_tuple[0], node_state_tuple[1], color, tag="path_highlight")

            # highlight elements with orange
            elif color == Color.ORANGE:
                if len(node_state_tuple) == 1:
                    self.highlight_node(node_state_tuple[0], color, tag="successor_highlight")
                else:
                    self.highlight_edge(node_state_tuple[0], node_state_tuple[1], color,
                                        tag="successor_edge_highlight")

            elif color == Color.GRAY:
                self.highlight_node(node_state_tuple[0], color, tag="no_successors_highlight")

            elif color == Color.GREEN:
                if len(node_state_tuple) == 1:
                    self.highlight_node(node_state_tuple[0], color, tag="best_successor_highlight")
                else:
                    self.highlight_edge(node_state_tuple[0], node_state_tuple[1],
                                        color,
                                        tag="best_successor_edge_highlight")

            elif color == Color.BLUE:
                self.highlight_node(node_state_tuple[0], color, tag="alternative_successor_highlight")

        # have node outlines on top
        self.graph_canvas.tag_raise("label")

        # have nodes on top
        self.graph_canvas.tag_raise("node")

        self.graph_canvas.tag_raise("expanded_node_highlight")
        self.graph_canvas.tag_raise("successor_highlight")
        self.graph_canvas.tag_raise("no_successors_highlight")
        self.graph_canvas.tag_raise("best_successor_highlight")
        self.graph_canvas.tag_raise("alternative_successor_highlight")

        # have edge labels on top
        self.graph_canvas.tag_raise("weight_label")

        # update displayed message
        self.set_narration_text(problem_state.displayed_message)

        # display nodes in memory
        self.display_nodes_in_memory(problem_state.in_memory_nodes)

    def animate(self, rbfs_generator):

        next_wait_time_ms = 2000

        if self.paused:
            return # do nothing (pause)

        try:
            # generator yields a problem state
            problem_state = next(rbfs_generator)

            self.update_window(problem_state)

            if not self.paused:
                self.window.after(next_wait_time_ms, lambda: self.animate(rbfs_generator))

        except StopIteration:
            self.set_narration_text("Algorithm finished. Press the start button to restart.")
            self.play_button.config(text="Start")
            self.paused = True
            self.started = False
            self.rbfs_generator = None
            return

    def display_nodes_in_memory(self, in_memory_nodes):
        """
        Display the nodes in memory.
        """

        # clear the previous nodes in memory
        for widget in self.nodes_view_frame.winfo_children():
            widget.destroy()

        # display the nodes in memory
        for i, tup in enumerate(in_memory_nodes):
            node = tup[0]

            if tup[1] == None:
                node_label = tk.Label(
                    self.nodes_view_frame,
                    text=f"{node.state}",
                    font=("Inter Bold", 12),
                    padx=0,
                    background=self.narration_box["background"]
                )
            else:
                node_label = tk.Label(
                    self.nodes_view_frame,
                    text=f"{node.state} {tup[1]}",
                    font=("Inter Bold", 8),
                    padx=0,
                    background=self.narration_box["background"]
                )
            node_label.grid(row=0, column=i)

            self.nodes_view_frame.columnconfigure(i, weight=1)


    def clear_highlights(self):
        # the green highlight of the expanded nodes
        self.graph_canvas.delete("expanded_node_highlight")
        # the green highlight of the edges between the initial node and the expanded node
        self.graph_canvas.delete("path_highlight")
        # the orange highlight of a successor node
        self.graph_canvas.delete("successor_highlight")
        # the orange highlight of the edge between the current node and its successor
        self.graph_canvas.delete("successor_edge_highlight")
        # the gray highlight of a node with no successors
        self.graph_canvas.delete("no_successors_highlight")
        # the green highlight of the best successor node
        self.graph_canvas.delete("best_successor_highlight")
        # the green highlight of the edge between the current node and the best successor
        self.graph_canvas.delete("best_successor_edge_highlight")
        # the blue highlight of the alternative successor node
        self.graph_canvas.delete("alternative_successor_highlight")

        # nodes on top
        self.graph_canvas.tag_raise("node")

    def clear_nodes_in_memory(self):
        for widget in self.nodes_view_frame.winfo_children():
            print(widget)
            widget.destroy()
        self.nodes_view_frame.update()