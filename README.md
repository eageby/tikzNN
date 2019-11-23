# tikzNN
TikzNN (Tikz Neural Network) is a tool to generate data files for visualizing Neural Networks with the LaTeX package [tikz-network](https://ctan.org/pkg/tikz-network?lang=en).

# Usage
The script is used by inputting an arbitrary number of network layer widths
```bash
tikznn 5 5 3 8
```
which generates two csv files in the default directory "./network".

The latex template file can be created automatically by using the flag --latex/-l.
```latex
\documentclass[tikz]{standalone}
\usepackage{tikz-network}

\begin{document}
	\begin{tikzpicture}
		\Vertices{./network/vertices.csv}
		\Edges{./network/edges.csv}
	\end{tikzpicture}
\end{document}
```
Compilation of that file will render a visualization.

![Example of tikzNN](/example.png)

## Separation
The interface provides options for customizing the distance between layers (x) and nodes (y).
```bash
 -x, --x_separation FLOAT
 -y, --y_separation FLOAT
 
```
# Installation
```bash
pip install git+https://github.com/eliasageby/tikzNN
```
