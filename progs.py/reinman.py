##########################################
# Name: Kris Yotam                       #
# Program: Reinman                       #
# Date: 10/11/2024                       #
# Description: This program visualizes   #
# the Riemann surface for the square     #
# root function and allows dynamic       #
# interaction, multiple surfaces,        #
# critical points analysis, and a basic  #
# GUI interface.                         #
##########################################

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider
import tkinter as tk

# Create a mesh grid for complex numbers (z = x + iy)
theta = np.linspace(0, 2 * np.pi, 100)
r = np.linspace(0.01, 2, 50)  # Start from 0.01 to avoid singularity at 0
theta, r = np.meshgrid(theta, r)
x = r * np.cos(theta)
y = r * np.sin(theta)

# Define the function to plot the surface
def plot_surface(exponent):
    # Compute the square root of complex numbers z = x + iy
    z = x + 1j * y
    w = z ** exponent

    # Real and imaginary parts of the surface
    X1 = np.real(w)
    Y1 = np.imag(w)
    Z1 = np.log(r)  # Using log(r) to make visualization more informative

    ax.clear()  # Clear previous plots
    # Color map based on height (Z1)
    cmap = plt.get_cmap('coolwarm')  # Blue to light blue gradient

    # Plot the first branch of the square root with the updated color scheme
    ax.plot_surface(x, y, X1, rstride=1, cstride=1,
                    facecolors=cmap((Z1 - Z1.min()) / (Z1.max() - Z1.min())),
                    alpha=0.9, edgecolor='k')

    # Plot the second branch (negative square root)
    ax.plot_surface(x, y, -X1, rstride=1, cstride=1,
                    facecolors=cmap((Z1 - Z1.min()) / (Z1.max() - Z1.min())),
                    alpha=0.9, edgecolor='k')

    # Labels and title
    ax.set_xlabel('Re(z)')
    ax.set_ylabel('Im(z)')
    ax.set_zlabel('Re(z^n)')
    ax.set_title(f'Riemann Surface for z^{exponent} with Custom Colors')
    plt.draw()

# Function to calculate critical points
def critical_points(exponent):
    # Calculate critical points based on the derivative
    # For z^n, critical points occur at z=0 for n > 1
    if exponent > 1:
        return [0]  # Critical point at origin
    return []

# Create sliders for interactive control
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': '3d'})
plt.subplots_adjust(left=0.1, bottom=0.25)

# Create slider for exponent
ax_exponent = plt.axes([0.1, 0.1, 0.65, 0.03])  # [left, bottom, width, height]
slider_exponent = Slider(ax_exponent, 'Exponent', 1, 5, valinit=2)

# Update function for slider
def update(val):
    plot_surface(slider_exponent.val)
    cp = critical_points(slider_exponent.val)
    print("Critical Points:", cp)

slider_exponent.on_changed(update)
plot_surface(slider_exponent.val)

# Basic GUI setup using tkinter
def create_gui():
    root = tk.Tk()
    root.title("Riemann Surface Visualizer")

    label = tk.Label(root, text="Welcome to the Riemann Surface Visualizer!")
    label.pack()

    instruction = tk.Label(root, text="Use the slider to change the exponent.")
    instruction.pack()

    # Add a button to close the GUI
    close_button = tk.Button(root, text="Close", command=root.quit)
    close_button.pack()

    root.mainloop()

# Show GUI in a separate thread
import threading

gui_thread = threading.Thread(target=create_gui)
gui_thread.start()

plt.show()  # Show the plot
