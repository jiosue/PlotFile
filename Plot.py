"""
Plot data from file.
Files should be of the form:

plot_type
**kwargs for plot 1
**kwargs for plot 2
...
# "#" indicates that the data is starting
1 1 2 3...
2 4 4 5...
...
...
# (Optional) "#" indicates that the data has ended.
(Any specific things you want to do are put here)
title("Title")
xlabel("x")
legend(loc="Upper Left")
xlim(-1, 1)
...
"""

import pylab, sys
from tkinter.filedialog import askopenfilenames
import tkinter as tk


ICON = "ploticon.ico"


def points_from_columns(xs):
    """
    Takes a list of rows and converts it into
    a list of columns. For example,
        xs = [[1, 2, 3], [4, 5, 6], [1], [2, 4]]
    will return
        x = [[1, 4, 1, 2], [2, 5, 4], [3, 6]]
    xs: list of rows (lists).
    returns: list of columns (lists).
    """
    x = []
    for row in xs:
        while len(x) < len(row): x.append([])
        for i in range(len(row)): x[i].append(row[i])
    return x


def display_error(error):
    """
    Create new window, display error message.
    error: any object that inherits from Exception.
    """
    name, message = error.__class__.__name__, str(error)
    root = tk.Tk()
    root.resizable(0, 0)
    root.bell()
    color = "#ffe6e6"
    root.config(bg=color)
    root.title(name)
    root.attributes("-toolwindow", 1)
    tk.Message(root, text=message, bg=color, width=400).pack()
    tk.Button(root, text="Okay", command=root.destroy, width=7).pack()
#    root.eval("tk::PlaceWindow %s center"%root.winfo_pathname(root.winfo_id()))
    root.bind("<Return>", lambda e: root.destroy())
    root.mainloop()


class File(object):
    """
    Reads from a file and compiles the information.
    path: str, the full filename (i.e. 'C:/Documents/.../helloworld.txt').
    """
    def __init__(self, path):
        xs, ys = [], []
        self.kwargs, self.to_evaluate = [], []
        with open(path) as f:
            self.plot_type = eval("pylab." + f.readline().strip())
            line = f.readline()
            while "#" not in line.strip():
                self.kwargs.append(eval("dict(%s)" % line))
                line = f.readline()
            for line in f:
                if line.strip():
                    l = line.split()
                    if "#" in l: break
                    xs.append([float(l[i]) for i in range(0, len(l), 2)])
                    ys.append([float(l[i]) for i in range(1, len(l), 2)])
            for line in f: self.to_evaluate.append("pylab." + line.strip())

        self.x, self.y = points_from_columns(xs), points_from_columns(ys)

    def plot(self):
        """ Plots the data with extracted specifications """
        assert len(self.x) == len(self.y), "Must have columns x1 y1 x2 y2 ..."
        for i in range(len(self.x)):
            kwargs = self.kwargs[i] if i < len(self.kwargs) else {}
            self.plot_type(self.x[i], self.y[i], **kwargs)
        pylab.legend()
        for e in self.to_evaluate: eval(e)


def plot(paths):
    """
    Plot data from paths.
    paths: iterable; with file path contents.
    """
    try:
        for i in range(len(paths)):
            pylab.figure(i)
            File(paths[i]).plot()
        pylab.show()
    except Exception as e:
        pylab.close("all")
        display_error(e)


def ask_open():
    """ Asks for filenames to plot, then calls plot """
    options = dict(
        defaultextension=".plt",
        filetype=[("PLOT files", ".plt"), ("All Files", "*.*")],
        initialdir="C:/Documents",
        title="Choose files to plot"
    )
    paths = askopenfilenames(**options)
    if paths: plot(paths)


def main():
    """ Create window with button that invokes plot """
    root = tk.Tk()
    try: root.iconbitmap(ICON)
    except tk.TclError: pass
    root.resizable(0, 0)
    tk.Button(root, text="PLOT", command=ask_open, width=20, height=10).pack()
    # root.eval("tk::PlaceWindow %s center"%root.winfo_pathname(root.winfo_id()))
    root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        plot([" ".join(sys.argv[1:])])
    else:
        main()