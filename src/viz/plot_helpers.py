"""
plot_helpers.py
---------------
Shared matplotlib/seaborn utilities for consistent figure styling.
"""

import matplotlib.pyplot as plt

PALETTE = ["#1f4e79", "#2e86c1", "#85c1e9", "#f39c12", "#e74c3c"]

def set_style():
    plt.rcParams.update({
        "figure.dpi": 150,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.family": "sans-serif",
    })
