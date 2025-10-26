from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

@dataclass
class Style:
    accent = "#2266cc"
    box_kwargs = dict(boxstyle="round,pad=0.3,rounding_size=8", linewidth=1)

def box(ax, xy, text, face="#ffffff"):
    x, y = xy
    rect = FancyBboxPatch((x, y), 2.8, 0.9, fc=face, ec="black", **Style.box_kwargs)
    ax.add_patch(rect)
    ax.text(x+1.4, y+0.45, text, ha="center", va="center")
    return rect

def arrow(ax, src_xy, dst_xy):
    (x1,y1), (x2,y2) = src_xy, dst_xy
    ax.add_patch(FancyArrowPatch((x1+2.8, y1+0.45), (x2, y2+0.45),
                                 arrowstyle="->", mutation_scale=12, lw=1, color=Style.accent))

def bridge_diagram(ax, left, right, caption=None):
    ax.axis("off")
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 3)
    box(ax, (0.5, 1.1), "\n".join(left))
    box(ax, (5.7, 1.1), "\n".join(right))
    arrow(ax, (0.5,1.1), (5.7,1.1))
    if caption:
        ax.text(4.5, 0.2, caption, ha="center", va="center", fontsize=10)

