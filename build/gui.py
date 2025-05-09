from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font as tkFont, Label, Frame, messagebox, filedialog, Scrollbar, RIGHT, Y, Toplevel
import pyglet, os
import sympy as sp
from integration import parse_user_function, process_user_integration
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.figure import Figure
import datetime


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Mark Limpahan\Documents\Visual Studio Code\CSMATH221_CALC\finmain\build\assets\frame0")

TEXT_COLOR = "#273C8B"

def format_pi_display(text):
    """Format pi display to 2 decimal places while preserving full precision for calculations"""
    # Replace full pi value with 2 decimal places in display
    return text.replace('3.141592653589793', '3.14')

def add_placeholder(widget, placeholder_text, is_entry=True):
    poppins_font = tkFont.Font(family="Poppins Medium", size=10)
    if is_entry:
        widget.config(font=poppins_font)
    else:
        widget.config(font=tkFont.Font(family="Poppins Medium", size=12))  # Increased font size by 2
        widget.config(state='normal')  # Temporarily enable to set placeholder
        widget.delete("1.0", "end")
        widget.insert("1.0", placeholder_text)
        widget.config(fg='gray')
        widget.config(state='disabled')  # Make non-editable
        return  # Skip binding events for Text widgets since they're non-editable
    if is_entry:
        widget.insert(0, placeholder_text)
        widget.config(fg='gray')
        def on_entry_focus_in(event):
            if widget.get() == placeholder_text:
                widget.delete(0, "end")
                widget.config(fg=TEXT_COLOR, font=poppins_font)
        def on_entry_focus_out(event):
            if widget.get() == "":
                widget.insert(0, placeholder_text)
                widget.config(fg='gray', font=poppins_font)
        widget.bind("<FocusIn>", on_entry_focus_in)
        widget.bind("<FocusOut>", on_entry_focus_out)
    else:
        widget.insert("1.0", placeholder_text)
        widget.config(fg='gray')
        def on_text_focus_in(event):
            if widget.get("1.0", "end-1c") == placeholder_text:
                widget.delete("1.0", "end")
                widget.config(fg=TEXT_COLOR, font=poppins_font)
        def on_text_focus_out(event):
            if widget.get("1.0", "end-1c") == "":
                widget.insert("1.0", placeholder_text)
                widget.config(fg='gray', font=poppins_font)
        widget.bind("<FocusIn>", on_text_focus_in)
        widget.bind("<FocusOut>", on_text_focus_out)

# Function to insert text into the active entry widget
def insert_to_entry(text):
    """Insert text into the currently focused entry widget"""
    # Get the currently focused widget
    focused_widget = window.focus_get()
    
    # Check if the focused widget is an Entry
    if isinstance(focused_widget, Entry):
        # If the current text is the placeholder, clear it first
        if focused_widget.get() == "Enter your function here" or \
           focused_widget.get() == "Input order of derivative" or \
           focused_widget.get() == "Upper limit" or \
           focused_widget.get() == "Lower Limit":
            focused_widget.delete(0, "end")
            focused_widget.config(fg=TEXT_COLOR)
        
        # Insert the new text at the cursor position
        focused_widget.insert("insert", text)
    # If no entry is focused, focus on the main function entry
    else:
        entry_1.focus_set()
        if entry_1.get() == "Enter your function here":
            entry_1.delete(0, "end")
            entry_1.config(fg=TEXT_COLOR)
        entry_1.insert("insert", text)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1440x1024")
window.configure(bg = "#4268FB")

# Set window title and icon
window.title("F'Prime: Python-Based Function Calculator")
try:
    window.iconbitmap(str(OUTPUT_PATH / "icon.ico"))
except:
    print("Warning: icon.ico not found in build directory")

canvas = Canvas(
    window,
    bg = "#4268FB",
    height = 1024,
    width = 1440,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    720.0,
    512.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    719.0,
    511.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    722.0,
    178.9996337890625,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    95.0,
    96.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    346.0,
    361.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    240.0,
    466.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    404.0,
    466.0,
    image=image_image_7
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    502.0,
    466.0,
    image=image_image_8
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    346.5,
    361.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#F3F3F3",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=161.0,
    y=347.0,
    width=371.0,
    height=27.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    212.5,
    466.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#F3F3F3",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=158.0,
    y=452.0,
    width=170.0,
    height=27.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    400.0,
    466.5,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#F3F3F3",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=375.0,
    y=452.0,
    width=65.0,
    height=27.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    502.0,
    466.5,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#F3F3F3",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=469.0,
    y=452.0,
    width=65.0,
    height=27.0
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    218.0,
    308.0,
    image=image_image_9
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    240.0,
    421.0,
    image=image_image_10
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    374.0,
    421.0,
    image=image_image_11
)

image_image_12 = PhotoImage(
    file=relative_to_assets("image_12.png"))
image_12 = canvas.create_image(
    472.0,
    421.0,
    image=image_image_12
)

# Function to preprocess mathematical expressions
def preprocess_expression(expr_str):
    # Replace common mathematical notations with sympy-compatible format
    expr_str = expr_str.replace('^', '**')  # Replace ^ with ** for exponentiation
    expr_str = expr_str.replace('π', '3.141592653589793')  # Replace π with numerical value
    expr_str = expr_str.replace('pi', '3.141592653589793')  # Replace pi with numerical value
    expr_str = expr_str.replace('×', '*')   # Replace × with *
    expr_str = expr_str.replace('÷', '/')   # Replace ÷ with /
    
    # Add * between number and variable (e.g., 3x -> 3*x)
    import re
    expr_str = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', expr_str)
    
    return expr_str

# Function to adjust text size and wrapping
def adjust_text_size(text_widget, text):
    # Configure text widget to wrap text
    text_widget.config(wrap="word")
    
    # Insert the text
    text_widget.delete("1.0", "end")
    text_widget.insert("1.0", text)

# Function to calculate the first derivative
def calculate_first_derivative():
    func_str = entry_1.get()
    if func_str == "" or func_str == "Enter your function here":
        entry_6.config(state='normal')
        entry_6.delete("1.0", "end")
        entry_6.insert("1.0", "Please enter a function")
        entry_6.config(fg=TEXT_COLOR)
        entry_6.config(state='disabled')
        return
    
    try:
        x = sp.Symbol('x')
        processed_func = preprocess_expression(func_str)
        expr = sp.sympify(processed_func)
        derivative = sp.diff(expr, x)
        entry_6.config(state='normal')
        result_text = format_pi_display(f"f'(x) = {str(derivative).replace('**', '^')}")
        adjust_text_size(entry_6, result_text)
        entry_6.config(fg=TEXT_COLOR)
        entry_6.config(state='disabled')
    except Exception as e:
        entry_6.config(state='normal')
        entry_6.delete("1.0", "end")
        entry_6.insert("1.0", f"Error: {str(e)}")
        entry_6.config(fg=TEXT_COLOR)
        entry_6.config(state='disabled')

# Function to calculate nth derivative
def calculate_nth_derivative():
    func_str = entry_1.get()
    order_str = entry_2.get()
    
    if func_str == "" or func_str == "Enter your function here":
        entry_8.config(state='normal')
        entry_8.delete("1.0", "end")
        entry_8.insert("1.0", "Please enter a function")
        entry_8.config(fg=TEXT_COLOR)
        entry_8.config(state='disabled')
        return
    
    try:
        order = int(order_str) if order_str else 1
        x = sp.Symbol('x')
        processed_func = preprocess_expression(func_str)
        expr = sp.sympify(processed_func)
        derivative = expr
        for _ in range(order):
            derivative = sp.diff(derivative, x)
        
        entry_8.config(state='normal')
        result_text = format_pi_display(f"f^({order})(x) = {str(derivative).replace('**', '^')}")
        adjust_text_size(entry_8, result_text)
        entry_8.config(fg=TEXT_COLOR)
        entry_8.config(state='disabled')
    except Exception as e:
        entry_8.config(state='normal')
        entry_8.delete("1.0", "end")
        entry_8.insert("1.0", f"Error: {str(e)}")
        entry_8.config(fg=TEXT_COLOR)
        entry_8.config(state='disabled')

# Function to calculate indefinite integral
def calculate_indefinite_integral():
    func_str = entry_1.get()
    if func_str == "" or func_str == "Enter your function here":
        entry_5.config(state='normal')
        entry_5.delete("1.0", "end")
        entry_5.insert("1.0", "Please enter a function")
        entry_5.config(fg=TEXT_COLOR)
        entry_5.config(state='disabled')
        return
    
    try:
        x = sp.Symbol('x')
        processed_func = preprocess_expression(func_str)
        expr = sp.sympify(processed_func)
        integral = sp.integrate(expr, x)
        entry_5.config(state='normal')
        result_text = format_pi_display(f"∫f(x)dx = {str(integral).replace('**', '^')} + C")
        adjust_text_size(entry_5, result_text)
        entry_5.config(fg=TEXT_COLOR)
        entry_5.config(state='disabled')
    except Exception as e:
        entry_5.config(state='normal')
        entry_5.delete("1.0", "end")
        entry_5.insert("1.0", f"Error: {str(e)}")
        entry_5.config(fg=TEXT_COLOR)
        entry_5.config(state='disabled')

# Function to calculate definite integral
def calculate_definite_integral():
    func_str = entry_1.get()
    lower_str = entry_3.get()
    upper_str = entry_4.get()
    
    if func_str == "" or func_str == "Enter your function here":
        entry_7.config(state='normal')
        entry_7.delete("1.0", "end")
        entry_7.insert("1.0", "Please enter a function")
        entry_7.config(fg=TEXT_COLOR)
        entry_7.config(state='disabled')
        return
    
    try:
        # Convert limits to float, handling pi and e
        def parse_limit(limit_str):
            if not limit_str:
                return 0
            limit_str = limit_str.lower().strip()
            if limit_str == 'pi':
                return float(sp.pi)
            elif limit_str == 'e':
                return float(sp.E)
            return float(limit_str)
            
        lower = parse_limit(lower_str)
        upper = parse_limit(upper_str)
        
        x = sp.Symbol('x')
        processed_func = preprocess_expression(func_str)
        expr = sp.sympify(processed_func)
        
        # Try symbolic integration first
        try:
            integral = sp.integrate(expr, (x, lower, upper))
            # Convert symbolic result to float, handling symbolic constants
            if isinstance(integral, sp.Float):
                result = float(integral)
            else:
                # Substitute pi and e with their numerical values
                result = float(integral.subs({sp.pi: float(sp.pi), sp.E: float(sp.E)}))
            
            entry_7.config(state='normal')
            # Format the display of pi in the limits
            lower_display = "3.14" if lower == float(sp.pi) else str(lower)
            upper_display = "3.14" if upper == float(sp.pi) else str(upper)
            result_text = f"∫f(x)dx from {lower_display} to {upper_display} = {result:.2f}"
            adjust_text_size(entry_7, result_text)
            entry_7.config(fg=TEXT_COLOR)
            entry_7.config(state='disabled')
        except:
            # Fall back to numerical integration
            result = process_user_integration(func_str, lower, upper)
            entry_7.config(state='normal')
            if result["success"]:
                # Format the display of pi in the limits
                lower_display = "3.14" if lower == float(sp.pi) else str(lower)
                upper_display = "3.14" if upper == float(sp.pi) else str(upper)
                result_text = f"∫f(x)dx from {lower_display} to {upper_display} ≈ {result['result']:.2f}"
                adjust_text_size(entry_7, result_text)
            else:
                entry_7.delete("1.0", "end")
                entry_7.insert("1.0", f"Error: {result['message']}")
            entry_7.config(fg=TEXT_COLOR)
            entry_7.config(state='disabled')
    except Exception as e:
        entry_7.config(state='normal')
        entry_7.delete("1.0", "end")
        entry_7.insert("1.0", f"Error: {str(e)}")
        entry_7.config(fg=TEXT_COLOR)
        entry_7.config(state='disabled')

# Create frames for the graphs
graph_frame_1 = Frame(window, bg="#4268FB", width=187, height=159)
graph_frame_1.place(x=700, y=563)

graph_frame_2 = Frame(window, bg="#4268FB", width=187, height=159)
graph_frame_2.place(x=1020, y=563)

graph_frame_3 = Frame(window, bg="#4268FB", width=187, height=159)
graph_frame_3.place(x=700, y=768)

graph_frame_4 = Frame(window, bg="#4268FB", width=187, height=159)
graph_frame_4.place(x=1020, y=768)

# Function to create a placeholder graph
def create_placeholder_graph(canvas, frame, title="Graph"):
    # Create figure and axis with smaller size
    fig = Figure(figsize=(1.87, 1.59), dpi=100, facecolor="#3159EE")  # Increased by 0.05 inches
    ax = fig.add_subplot(111)
    
    # Set up the graph with matching style from oldgui.py
    ax.set_facecolor("#3159EE")
    ax.grid(True, linestyle='--', alpha=0.7, color='white')
    ax.axhline(y=0, color='white', linestyle='-', alpha=0.3)
    ax.axvline(x=0, color='white', linestyle='-', alpha=0.3)
    ax.set_title(title, fontsize=8, color='white')  # Reduced font size
    ax.set_xlabel('x', fontsize=6, color='white')   # Reduced font size
    ax.set_ylabel('y', fontsize=6, color='white')   # Reduced font size
    ax.tick_params(colors='white', labelsize=6)     # Reduced font size
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    
    # Create a sample plot
    x_vals = np.linspace(-10, 10, 100)
    y_vals = np.zeros_like(x_vals)
    ax.plot(x_vals, y_vals, color='#FFAB4C', linewidth=1.5)  # Reduced line width
    
    # Embed the figure in the canvas
    canvas_widget = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack(fill='both', expand=True)
    
    # Add coordinate display on hover
    coord_text = ax.text(0.02, 0.98, '', transform=ax.transAxes,
                        fontsize=6, color='white', alpha=0.8,
                        verticalalignment='top',
                        bbox=dict(facecolor='#3159EE', alpha=0.7, edgecolor='white'))
    coord_text.set_visible(False)
    
    def hover(event):
        if event.inaxes == ax:
            coord_text.set_visible(True)
            coord_text.set_text(f'x: {event.xdata:.2f}\ny: {event.ydata:.2f}')
            canvas_widget.draw_idle()
        else:
            coord_text.set_visible(False)
            canvas_widget.draw_idle()
    
    canvas_widget.mpl_connect('motion_notify_event', hover)
    
    return fig, ax, canvas_widget

# Create placeholder graphs
def setup_placeholder_graphs():
    # Graph 1: First Derivative (top left)
    fig1, ax1, canvas1 = create_placeholder_graph(canvas, graph_frame_1, "Original Function")
    
    # Graph 2: Nth Derivative (top right)
    fig2, ax2, canvas2 = create_placeholder_graph(canvas, graph_frame_2, "First Derivative")
    
    # Graph 3: Indefinite Integral (bottom left)
    fig3, ax3, canvas3 = create_placeholder_graph(canvas, graph_frame_3, "Nth Derivative")
    
    # Graph 4: Definite Integral (bottom right)
    fig4, ax4, canvas4 = create_placeholder_graph(canvas, graph_frame_4, "Numerical Integration")
    
    return (fig1, ax1, canvas1), (fig2, ax2, canvas2), (fig3, ax3, canvas3), (fig4, ax4, canvas4)

# Add the background images for graphs
image_image_21 = PhotoImage(
    file=relative_to_assets("image_21.png"))
image_21 = canvas.create_image(
    790.0,
    639.0,
    image=image_image_21
)

image_image_22 = PhotoImage(
    file=relative_to_assets("image_22.png"))
image_22 = canvas.create_image(
    790.0,
    844.0,
    image=image_image_22
)

image_image_23 = PhotoImage(
    file=relative_to_assets("image_23.png"))
image_23 = canvas.create_image(
    1110.0,
    639.0,
    image=image_image_23
)

image_image_24 = PhotoImage(
    file=relative_to_assets("image_24.png"))
image_24 = canvas.create_image(
    1110.0,
    844.0,
    image=image_image_24
)

# Function to update graphs based on calculations
def update_graphs(func_str, derivative1, derivative_n, integral_indef, integral_def, lower=0, upper=1):
    try:
        x = np.linspace(-10, 10, 1000)  # Increased resolution for smoother curves
        x_sym = sp.Symbol('x')
        
        # Convert sympy expressions to numpy functions with proper evaluation
        def create_numpy_func(expr):
            if isinstance(expr, sp.Derivative):
                # For derivatives, evaluate them first
                expr = expr.doit()
            elif isinstance(expr, sp.Integral):
                # For integrals, evaluate them first
                expr = expr.doit()
            
            # Replace symbolic constants with their numerical values
            expr = expr.subs({sp.pi: np.pi, sp.E: np.e})
            
            # Handle Piecewise expressions
            if isinstance(expr, sp.Piecewise):
                # Take the first condition (usually the main case)
                expr = expr.args[0][0]
            
            return sp.lambdify(x_sym, expr, 'numpy')
        
        # Create numpy functions for each expression
        func = create_numpy_func(sp.sympify(preprocess_expression(func_str)))
        deriv1 = create_numpy_func(derivative1)
        deriv_n = create_numpy_func(derivative_n)
        integ_indef = create_numpy_func(integral_indef)
        
        # Update each graph
        for fig, ax, canvas in graphs:
            ax.clear()
            ax.set_facecolor("#3159EE")
            ax.grid(True, linestyle='--', alpha=0.7, color='white')
            ax.axhline(y=0, color='white', linestyle='-', alpha=0.3)
            ax.axvline(x=0, color='white', linestyle='-', alpha=0.3)
            ax.set_xlabel('x', fontsize=6, color='white')
            ax.set_ylabel('y', fontsize=6, color='white')
            ax.tick_params(colors='white', labelsize=6)
            ax.spines['top'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            
            try:
                if fig == graphs[0][0]:  # Original Function
                    # Plot the main function
                    ax.plot(x, func(x), color='#69FF8A', linewidth=1.5)
                    
                    # Add shading between bounds
                    x_bounds = np.linspace(lower, upper, 200)
                    y_bounds = func(x_bounds)
                    ax.fill_between(x_bounds, y_bounds, alpha=0.3, color='#69FF8A')
                    
                    ax.axvline(x=lower, color='white', linestyle='--', alpha=0.5)
                    ax.axvline(x=upper, color='white', linestyle='--', alpha=0.5)
                    ax.set_title("Original Function", fontsize=8, color='white')
                    # Add function expression as text with LaTeX formatting
                    expr = sp.sympify(preprocess_expression(func_str))
                    # Format pi display in bounds
                    lower_display = "3.14" if lower == float(sp.pi) else str(lower)
                    upper_display = "3.14" if upper == float(sp.pi) else str(upper)
                    ax.text(0.05, 0.95, f'$f(x) = {sp.latex(expr)}$\nBounds: [{lower_display}, {upper_display}]', 
                           transform=ax.transAxes, fontsize=7, color='white',
                           verticalalignment='top', bbox=dict(facecolor='#3159EE', alpha=0.7, edgecolor='white'))
                elif fig == graphs[1][0]:  # First Derivative
                    ax.plot(x, deriv1(x), color='#ff8568', linewidth=1.5)
                    ax.set_title("First Derivative", fontsize=8, color='white')
                    # Add derivative expression as text with LaTeX formatting
                    deriv_expr = derivative1.doit()
                    # Format pi display in LaTeX
                    latex_str = sp.latex(deriv_expr)
                    latex_str = latex_str.replace('3.141592653589793', '3.14')
                    ax.text(0.05, 0.95, f"$f'(x) = {latex_str}$", 
                           transform=ax.transAxes, fontsize=7, color='white',
                           verticalalignment='top', bbox=dict(facecolor='#3159EE', alpha=0.7, edgecolor='white'))
                elif fig == graphs[2][0]:  # Nth Derivative
                    ax.plot(x, deriv_n(x), color='#ffc253', linewidth=1.5)
                    ax.set_title("Nth Derivative", fontsize=8, color='white')
                    # Add nth derivative expression as text with LaTeX formatting
                    deriv_n_expr = derivative_n.doit()
                    # Format pi display in LaTeX
                    latex_str = sp.latex(deriv_n_expr)
                    latex_str = latex_str.replace('3.141592653589793', '3.14')
                    ax.text(0.05, 0.95, f"$f^({entry_2.get()})(x) = {latex_str}$", 
                           transform=ax.transAxes, fontsize=7, color='white',
                           verticalalignment='top', bbox=dict(facecolor='#3159EE', alpha=0.7, edgecolor='white'))
                elif fig == graphs[3][0]:  # Numerical Integration
                    # Plot the indefinite integral
                    ax.plot(x, integ_indef(x), color='#f9f871', linewidth=1.5)
                    
                    # Add shading between bounds
                    x_bounds = np.linspace(lower, upper, 200)
                    y_bounds = integ_indef(x_bounds)
                    ax.fill_between(x_bounds, y_bounds, alpha=0.3, color='#f9f871')
                    
                    # Add vertical lines for bounds
                    ax.axvline(x=lower, color='white', linestyle='--', alpha=0.5)
                    ax.axvline(x=upper, color='white', linestyle='--', alpha=0.5)
                    ax.set_title("Numerical Integration", fontsize=8, color='white')
                    # Add indefinite integral expression as text with LaTeX formatting
                    integ_expr = integral_indef.doit()
                    if isinstance(integ_expr, sp.Piecewise):
                        integ_expr = integ_expr.args[0][0]  # Take the first condition
                    # Format pi display in LaTeX and add bounds
                    latex_str = sp.latex(integ_expr)
                    latex_str = latex_str.replace('3.141592653589793', '3.14')
                    # Format pi display in bounds
                    lower_display = "3.14" if lower == float(sp.pi) else str(lower)
                    upper_display = "3.14" if upper == float(sp.pi) else str(upper)
                    ax.text(0.05, 0.95, 
                           f"$\\int {sp.latex(sp.sympify(preprocess_expression(func_str)))} dx = {latex_str}$\nBounds: [{lower_display}, {upper_display}]", 
                           transform=ax.transAxes, fontsize=7, color='white',
                           verticalalignment='top', bbox=dict(facecolor='#3159EE', alpha=0.7, edgecolor='white'))
            except Exception as plot_error:
                # If plotting fails, display the result expression in the middle of the graph
                if fig == graphs[0][0]:  # Original Function
                    ax.set_title("Original Function", fontsize=8, color='white')
                    expr = sp.sympify(preprocess_expression(func_str))
                    # Format pi display in LaTeX
                    latex_str = sp.latex(expr)
                    latex_str = latex_str.replace('3.141592653589793', '3.14')
                    ax.text(0.5, 0.5, f'$f(x) = {latex_str}$\nBounds: [{lower}, {upper}]', 
                           transform=ax.transAxes, fontsize=10, color='white',
                           verticalalignment='center', horizontalalignment='center',
                           bbox=dict(facecolor='#3159EE', alpha=0.7, edgecolor='white'))
                elif fig == graphs[1][0]:  # First Derivative
                    ax.set_title("First Derivative", fontsize=8, color='white')
                    deriv_expr = derivative1.doit()
                    # Format pi display in LaTeX
                    latex_str = sp.latex(deriv_expr)
                    latex_str = latex_str.replace('3.141592653589793', '3.14')
                    ax.text(0.5, 0.5, f"$f'(x) = {latex_str}$", 
                           transform=ax.transAxes, fontsize=10, color='white',
                           verticalalignment='center', horizontalalignment='center',
                           bbox=dict(facecolor='#3159EE', alpha=0.7, edgecolor='white'))
                elif fig == graphs[2][0]:  # Nth Derivative
                    ax.set_title("Nth Derivative", fontsize=8, color='white')
                    deriv_n_expr = derivative_n.doit()
                    # Format pi display in LaTeX
                    latex_str = sp.latex(deriv_n_expr)
                    latex_str = latex_str.replace('3.141592653589793', '3.14')
                    ax.text(0.5, 0.5, f"$f^({entry_2.get()})(x) = {latex_str}$", 
                           transform=ax.transAxes, fontsize=10, color='white',
                           verticalalignment='center', horizontalalignment='center',
                           bbox=dict(facecolor='#3159EE', alpha=0.7, edgecolor='white'))
                elif fig == graphs[3][0]:  # Numerical Integration
                    ax.set_title("Numerical Integration", fontsize=8, color='white')
                    # Format pi display in bounds
                    lower_display = "3.14" if lower == float(sp.pi) else str(lower)
                    upper_display = "3.14" if upper == float(sp.pi) else str(upper)
                    ax.text(0.5, 0.5, f"Not Supported\nBounds: [{lower_display}, {upper_display}]", 
                           transform=ax.transAxes, fontsize=12, color='white',
                           verticalalignment='center', horizontalalignment='center',
                           bbox=dict(facecolor='#3159EE', alpha=0.7, edgecolor='white'))
            
            canvas.draw()
    except Exception as e:
        print(f"Error updating graphs: {str(e)}")

# Modify calculate_all to update graphs
def calculate_all():
    calculate_first_derivative()
    calculate_nth_derivative()
    calculate_indefinite_integral()
    calculate_definite_integral()
    
    # Get the results and update graphs
    func_str = entry_1.get()
    if func_str and func_str != "Enter your function here":
        try:
            x = sp.Symbol('x')
            processed_func = preprocess_expression(func_str)
            expr = sp.sympify(processed_func)
            
            # Calculate all expressions
            deriv1 = sp.diff(expr, x)
            order = int(entry_2.get()) if entry_2.get() else 1
            deriv_n = expr
            for _ in range(order):
                deriv_n = sp.diff(deriv_n, x)
            integ_indef = sp.integrate(expr, x)
            
            # Get limits for definite integral
            lower = float(entry_3.get()) if entry_3.get() else 0
            upper = float(entry_4.get()) if entry_4.get() else 1
            
            # Update graphs
            update_graphs(func_str, deriv1, deriv_n, integ_indef, expr, lower, upper)
        except Exception as e:
            print(f"Error updating graphs: {str(e)}")

# Initialize graphs
graphs = setup_placeholder_graphs()

# Show all result to the text areas
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=calculate_all,
    relief="flat"
)

button_image_hover_1 = PhotoImage(
    file=relative_to_assets("button_hover_1.png"))

def button_1_hover(e):
    button_1.config(
        image=button_image_hover_1
    )
def button_1_leave(e):
    button_1.config(
        image=button_image_1
    )

button_1.bind('<Enter>', button_1_hover)
button_1.bind('<Leave>', button_1_leave)

button_1.place(
    x=365.0,
    y=879.8250732421875,
    width=189.63,
    height=54.0
)

# Function to save graph as image
def save_graph_as_image(fig, default_filename):
    """Save the matplotlib figure as an image file with user-selected location"""
    try:
        # Ask user where to save the file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile=default_filename,
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        # If user cancels the dialog, return False
        if not file_path:
            return False, None
        
        # Create a temporary file with the specified name
        fig.savefig(file_path, dpi=300, bbox_inches='tight', facecolor="#3159EE", edgecolor='white')
        return True, file_path
    except Exception as e:
        print(f"Error saving graph: {str(e)}")
        return False, None

# Function to save first derivative graph
def save_first_derivative_graph():
    """Save the first derivative graph as an image"""
    # Generate a filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    default_filename = f"first_derivative_{timestamp}.png"
    
    # Save the graph
    success, file_path = save_graph_as_image(graphs[0][0], default_filename)
    if success:
        # Show success message
        messagebox.showinfo("Success", f"Graph saved as {file_path}")
    else:
        # Show error message only if user didn't cancel
        if file_path is None:
            messagebox.showerror("Error", "Failed to save graph")

# Function to save nth derivative graph
def save_nth_derivative_graph():
    """Save the nth derivative graph as an image"""
    # Generate a filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    default_filename = f"nth_derivative_{timestamp}.png"
    
    # Save the graph
    success, file_path = save_graph_as_image(graphs[1][0], default_filename)
    if success:
        # Show success message
        messagebox.showinfo("Success", f"Graph saved as {file_path}")
    else:
        # Show error message only if user didn't cancel
        if file_path is None:
            messagebox.showerror("Error", "Failed to save graph")

# Function to save indefinite integral graph
def save_indefinite_integral_graph():
    """Save the indefinite integral graph as an image"""
    # Generate a filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    default_filename = f"indefinite_integral_{timestamp}.png"
    
    # Save the graph
    success, file_path = save_graph_as_image(graphs[2][0], default_filename)
    if success:
        # Show success message
        messagebox.showinfo("Success", f"Graph saved as {file_path}")
    else:
        # Show error message only if user didn't cancel
        if file_path is None:
            messagebox.showerror("Error", "Failed to save graph")

# Function to save definite integral graph
def save_definite_integral_graph():
    """Save the definite integral graph as an image"""
    # Generate a filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    default_filename = f"definite_integral_{timestamp}.png"
    
    # Save the graph
    success, file_path = save_graph_as_image(graphs[3][0], default_filename)
    if success:
        # Show success message
        messagebox.showinfo("Success", f"Graph saved as {file_path}")
    else:
        # Show error message only if user didn't cancel
        if file_path is None:
            messagebox.showerror("Error", "Failed to save graph")

# Function to create a zoomed graph window
def create_zoomed_graph(fig, title):
    """Create a new window with a zoomed version of the graph"""
    # Create a new window
    zoom_window = Toplevel(window)
    zoom_window.title(title)
    zoom_window.configure(bg="#4268FB")
    
    # Set window size to be larger than original
    zoom_window.geometry("800x600")
    
    # Create a new figure with larger size
    zoom_fig = Figure(figsize=(10, 8), dpi=100, facecolor="#3159EE")
    
    # Copy the data and settings from original figure
    orig_ax = fig.axes[0]
    zoom_ax = zoom_fig.add_subplot(111)
    
    # Copy the plot data and properties
    for line in orig_ax.lines:
        zoom_ax.plot(line.get_xdata(), line.get_ydata(), 
                    color=line.get_color(), 
                    linewidth=2.0)  # Increased line width for better visibility
    
    # Copy axis properties
    zoom_ax.set_facecolor("#3159EE")
    zoom_ax.grid(True, linestyle='--', alpha=0.7, color='white')
    zoom_ax.axhline(y=0, color='white', linestyle='-', alpha=0.3)
    zoom_ax.axvline(x=0, color='white', linestyle='-', alpha=0.3)
    zoom_ax.set_title(title, fontsize=12, color='white')
    zoom_ax.set_xlabel('x', fontsize=10, color='white')
    zoom_ax.set_ylabel('y', fontsize=10, color='white')
    zoom_ax.tick_params(colors='white', labelsize=10)
    
    # Copy spines properties
    for spine in zoom_ax.spines.values():
        spine.set_color('white')
    
    # Copy shading and bounds if they exist in the original plot
    if "Original Function" in title or "Numerical Integration" in title:
        try:
            lower = float(entry_3.get()) if entry_3.get() and entry_3.get() != "Upper li..." else 0
            upper = float(entry_4.get()) if entry_4.get() and entry_4.get() != "Lower li.." else 1
            
            # Handle pi values
            if entry_3.get().lower().strip() == 'pi':
                lower = float(sp.pi)
            if entry_4.get().lower().strip() == 'pi':
                upper = float(sp.pi)
            
            # Get the function data
            x_bounds = np.linspace(lower, upper, 200)
            if "Original Function" in title:
                func_str = entry_1.get()
                if func_str and func_str != "Enter your function here":
                    x_sym = sp.Symbol('x')
                    expr = sp.sympify(preprocess_expression(func_str))
                    func = sp.lambdify(x_sym, expr, 'numpy')
                    y_bounds = func(x_bounds)
                    zoom_ax.fill_between(x_bounds, y_bounds, alpha=0.3, color='#69FF8A')
            elif "Numerical Integration" in title:
                func_str = entry_1.get()
                if func_str and func_str != "Enter your function here":
                    x_sym = sp.Symbol('x')
                    expr = sp.integrate(sp.sympify(preprocess_expression(func_str)), x_sym)
                    func = sp.lambdify(x_sym, expr, 'numpy')
                    y_bounds = func(x_bounds)
                    zoom_ax.fill_between(x_bounds, y_bounds, alpha=0.3, color='#f9f871')
            
            # Add vertical lines for bounds
            zoom_ax.axvline(x=lower, color='white', linestyle='--', alpha=0.5)
            zoom_ax.axvline(x=upper, color='white', linestyle='--', alpha=0.5)
        except Exception as e:
            print(f"Warning: Could not add shading to zoomed graph: {str(e)}")
    
    # Copy text annotations with larger font size
    for text in orig_ax.texts:
        if not text.get_text().startswith('x:'): # Skip coordinate display text
            text_str = text.get_text()
            zoom_ax.text(text.get_position()[0], text.get_position()[1],
                        text_str,
                        transform=zoom_ax.transAxes,
                        fontsize=10, color='white',
                        verticalalignment=text.get_verticalalignment(),
                        horizontalalignment=text.get_horizontalalignment(),
                        bbox=dict(facecolor='#3159EE', alpha=0.7, edgecolor='white'))
    
    # Create canvas and add to window
    canvas_widget = FigureCanvasTkAgg(zoom_fig, master=zoom_window)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack(fill='both', expand=True)
    
    # Enable zooming with mouse wheel
    def on_scroll(event):
        # Get the current x and y limits
        cur_xlim = zoom_ax.get_xlim()
        cur_ylim = zoom_ax.get_ylim()
        
        # Get the current mouse position
        if event.inaxes:
            xdata = event.xdata  # Mouse x position in data coordinates
            ydata = event.ydata  # Mouse y position in data coordinates
        else:
            # If mouse is not over the plot, zoom around the center
            xdata = sum(cur_xlim) / 2
            ydata = sum(cur_ylim) / 2
        
        # Get the direction of scroll
        if event.button == 'up':
            # Zoom in
            scale_factor = 0.9
        elif event.button == 'down':
            # Zoom out
            scale_factor = 1.1
        else:
            # No zoom if it's not a scroll event
            return
        
        # Calculate new limits
        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
        
        # Calculate new centers based on mouse position
        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])
        
        # Set new limits
        zoom_ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * relx])
        zoom_ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * rely])
        
        # Redraw the canvas
        canvas_widget.draw_idle()
    
    # Connect the scroll event
    canvas_widget.mpl_connect('scroll_event', on_scroll)
    
    # Add coordinate display on hover for zoomed graph
    coord_text = zoom_ax.text(0.02, 0.98, '', transform=zoom_ax.transAxes,
                            fontsize=10, color='white', alpha=0.8,
                            verticalalignment='top',
                            bbox=dict(facecolor='#3159EE', alpha=0.7, edgecolor='white'))
    coord_text.set_visible(False)
    
    def hover(event):
        if event.inaxes == zoom_ax:
            coord_text.set_visible(True)
            coord_text.set_text(f'x: {event.xdata:.2f}\ny: {event.ydata:.2f}')
            canvas_widget.draw_idle()
        else:
            coord_text.set_visible(False)
            canvas_widget.draw_idle()
    
    canvas_widget.mpl_connect('motion_notify_event', hover)
    
    # Add a close button
    close_button = Button(zoom_window, text="Close", command=zoom_window.destroy,
                         bg="#273C8B", fg="white", font=("Poppins Medium", 10))
    close_button.pack(pady=10)
    
    # Make window resizable
    zoom_window.resizable(True, True)
    
    # Center the window on screen
    window_width = 800
    window_height = 600
    screen_width = zoom_window.winfo_screenwidth()
    screen_height = zoom_window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    zoom_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Functions to zoom each type of graph
def zoom_first_derivative():
    """Create a zoomed window for the first derivative graph"""
    create_zoomed_graph(graphs[0][0], "Original Function (Zoomed)")

def zoom_nth_derivative():
    """Create a zoomed window for the nth derivative graph"""
    create_zoomed_graph(graphs[1][0], "First Derivative (Zoomed)")

def zoom_indefinite_integral():
    """Create a zoomed window for the indefinite integral graph"""
    create_zoomed_graph(graphs[2][0], "Nth Derivative (Zoomed)")

def zoom_definite_integral():
    """Create a zoomed window for the definite integral graph"""
    create_zoomed_graph(graphs[3][0], "Numerical Integration (Zoomed)")

# Save first derivative graph as image
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=save_first_derivative_graph,  # Save first derivative graph
    relief="flat"
)
button_2.place(
    x=911.0,
    y=702.0,
    width=57.0,
    height=39.0
)

zoom_button_image = PhotoImage(
    file=relative_to_assets("ZoomButton.png"))
# Duplicate button for first derivative graph - now for zooming
button_2_dup = Button(
    image=zoom_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=zoom_first_derivative,  # Changed to zoom function
    relief="flat"
)
button_2_dup.place(
    x=911.0,
    y=650.0,  # Positioned above the original
    width=57.0,
    height=39.0
)

zoom_button_image_hover = PhotoImage(
    file=relative_to_assets("ZoomButtonHover.png"))

button_image_hover_2 = PhotoImage(
    file=relative_to_assets("button_hover_2.png"))

def button_2_hover(e):
    button_2.config(
        image=button_image_hover_2
    )
def button_2_leave(e):
    button_2.config(
        image=button_image_2
    )

button_2.bind('<Enter>', button_2_hover)
button_2.bind('<Leave>', button_2_leave)

# Apply hover effect to duplicate button
button_2_dup.bind('<Enter>', lambda e: button_2_dup.config(image=zoom_button_image_hover))
button_2_dup.bind('<Leave>', lambda e: button_2_dup.config(image=zoom_button_image))

# Save nth derivative graph as image
button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=save_nth_derivative_graph,  # Save nth derivative graph
    relief="flat"
)
button_3.place(
    x=1234.0,
    y=702.0,
    width=57.0,
    height=39.0
)

# Duplicate button for nth derivative graph - now for zooming
button_3_dup = Button(
    image=zoom_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=zoom_nth_derivative,  # Changed to zoom function
    relief="flat"
)
button_3_dup.place(
    x=1234.0,
    y=650.0,  # Positioned above the original
    width=57.0,
    height=39.0
)

button_image_hover_3 = PhotoImage(
    file=relative_to_assets("button_hover_3.png"))

def button_3_hover(e):
    button_3.config(
        image=button_image_hover_3
    )
def button_3_leave(e):
    button_3.config(
        image=button_image_3
    )

button_3.bind('<Enter>', button_3_hover)
button_3.bind('<Leave>', button_3_leave)

# Apply hover effect to duplicate button
button_3_dup.bind('<Enter>', lambda e: button_3_dup.config(image=zoom_button_image_hover))
button_3_dup.bind('<Leave>', lambda e: button_3_dup.config(image=zoom_button_image))

# Save indefinite integral graph as image
button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=save_indefinite_integral_graph,  # Save indefinite integral graph
    relief="flat"
)
button_4.place(
    x=911.0,
    y=906.0,
    width=57.0,
    height=39.0
)

# Duplicate button for indefinite integral graph - now for zooming
button_4_dup = Button(
    image=zoom_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=zoom_indefinite_integral,  # Changed to zoom function
    relief="flat"
)
button_4_dup.place(
    x=911.0,
    y=854.0,  # Positioned above the original
    width=57.0,
    height=39.0
)

button_image_hover_4 = PhotoImage(
    file=relative_to_assets("button_hover_4.png"))

def button_4_hover(e):
    button_4.config(
        image=button_image_hover_4
    )
def button_4_leave(e):
    button_4.config(
        image=button_image_4
    )

button_4.bind('<Enter>', button_4_hover)
button_4.bind('<Leave>', button_4_leave)

# Apply hover effect to duplicate button
button_4_dup.bind('<Enter>', lambda e: button_4_dup.config(image=zoom_button_image_hover))
button_4_dup.bind('<Leave>', lambda e: button_4_dup.config(image=zoom_button_image))

# Save definite integral graph as image
button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=save_definite_integral_graph,  # Save definite integral graph
    relief="flat"
)
button_5.place(
    x=1234.0,
    y=906.0,
    width=57.0,
    height=39.0
)

# Duplicate button for definite integral graph - now for zooming
button_5_dup = Button(
    image=zoom_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=zoom_definite_integral,  # Changed to zoom function
    relief="flat"
)
button_5_dup.place(
    x=1234.0,
    y=854.0,  # Positioned above the original
    width=57.0,
    height=39.0
)

button_image_hover_5 = PhotoImage(
    file=relative_to_assets("button_hover_5.png"))

def button_5_hover(e):
    button_5.config(
        image=button_image_hover_5
    )
def button_5_leave(e):
    button_5.config(
        image=button_image_5
    )

button_5.bind('<Enter>', button_5_hover)
button_5.bind('<Leave>', button_5_leave)

# Apply hover effect to duplicate button
button_5_dup.bind('<Enter>', lambda e: button_5_dup.config(image=zoom_button_image_hover))
button_5_dup.bind('<Leave>', lambda e: button_5_dup.config(image=zoom_button_image))

# Inputs 1 to the selected text entry
button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("1"),
    relief="flat"
)

button_image_hover_6 = PhotoImage(
    file=relative_to_assets("button_hover_6.png"))

def button_6_hover(e):
    button_6.config(
        image=button_image_hover_6
    )
def button_6_leave(e):
    button_6.config(
        image=button_image_6
    )

button_6.bind('<Enter>', button_6_hover)
button_6.bind('<Leave>', button_6_leave)

button_6.place(
    x=148.0,
    y=513.0,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs 2 to the selected text entry
button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("2"),
    relief="flat"
)

button_image_hover_7 = PhotoImage(
    file=relative_to_assets("button_hover_7.png"))

def button_7_hover(e):
    button_7.config(
        image=button_image_hover_7
    )
def button_7_leave(e):
    button_7.config(
        image=button_image_7
    )

button_7.bind('<Enter>', button_7_hover)
button_7.bind('<Leave>', button_7_leave)

button_7.place(
    x=254.22433471679688,
    y=513.0,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs 3 to the selected text entry
button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("3"),
    relief="flat"
)

button_image_hover_8 = PhotoImage(
    file=relative_to_assets("button_hover_8.png"))

def button_8_hover(e):
    button_8.config(
        image=button_image_hover_8
    )
def button_8_leave(e):
    button_8.config(
        image=button_image_8
    )

button_8.bind('<Enter>', button_8_hover)
button_8.bind('<Leave>', button_8_leave)

button_8.place(
    x=360.44866943359375,
    y=513.0,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs sin to the selected text entry
button_image_9 = PhotoImage(
    file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("sin("),
    relief="flat"
)

button_image_hover_9 = PhotoImage(
    file=relative_to_assets("button_hover_9.png"))

def button_9_hover(e):
    button_9.config(
        image=button_image_hover_9
    )
def button_9_leave(e):
    button_9.config(
        image=button_image_9
    )

button_9.bind('<Enter>', button_9_hover)
button_9.bind('<Leave>', button_9_leave)

button_9.place(
    x=467.0,
    y=513.0,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs 4 to the selected text entry
button_image_10 = PhotoImage(
    file=relative_to_assets("button_10.png"))
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("4"),
    relief="flat"
)

button_image_hover_10 = PhotoImage(
    file=relative_to_assets("button_hover_10.png"))

def button_10_hover(e):
    button_10.config(
        image=button_image_hover_10
    )
def button_10_leave(e):
    button_10.config(
        image=button_image_10
    )

button_10.bind('<Enter>', button_10_hover)
button_10.bind('<Leave>', button_10_leave)

button_10.place(
    x=148.0,
    y=574.30419921875,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs 5 to the selected text entry
button_image_11 = PhotoImage(
    file=relative_to_assets("button_11.png"))
button_11 = Button(
    image=button_image_11,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("5"),
    relief="flat"
)

button_image_hover_11 = PhotoImage(
    file=relative_to_assets("button_hover_11.png"))

def button_11_hover(e):
    button_11.config(
        image=button_image_hover_11
    )
def button_11_leave(e):
    button_11.config(
        image=button_image_11
    )

button_11.bind('<Enter>', button_11_hover)
button_11.bind('<Leave>', button_11_leave)

button_11.place(
    x=254.22433471679688,
    y=574.30419921875,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs 6 to the selected text entry
button_image_12 = PhotoImage(
    file=relative_to_assets("button_12.png"))
button_12 = Button(
    image=button_image_12,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("6"),
    relief="flat"
)

button_image_hover_12 = PhotoImage(
    file=relative_to_assets("button_hover_12.png"))

def button_12_hover(e):
    button_12.config(
        image=button_image_hover_12
    )
def button_12_leave(e):
    button_12.config(
        image=button_image_12
    )

button_12.bind('<Enter>', button_12_hover)
button_12.bind('<Leave>', button_12_leave)

button_12.place(
    x=360.44866943359375,
    y=574.30419921875,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs cos to the selected text entry
button_image_13 = PhotoImage(
    file=relative_to_assets("button_13.png"))
button_13 = Button(
    image=button_image_13,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("cos("),
    relief="flat"
)

button_image_hover_13 = PhotoImage(
    file=relative_to_assets("button_hover_13.png"))

def button_13_hover(e):
    button_13.config(
        image=button_image_hover_13
    )
def button_13_leave(e):
    button_13.config(
        image=button_image_13
    )

button_13.bind('<Enter>', button_13_hover)
button_13.bind('<Leave>', button_13_leave)

button_13.place(
    x=467.0,
    y=574.30419921875,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs 7 to the selected text entry
button_image_14 = PhotoImage(
    file=relative_to_assets("button_14.png"))
button_14 = Button(
    image=button_image_14,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("7"),
    relief="flat"
)

button_image_hover_14 = PhotoImage(
    file=relative_to_assets("button_hover_14.png"))

def button_14_hover(e):
    button_14.config(
        image=button_image_hover_14
    )
def button_14_leave(e):
    button_14.config(
        image=button_image_14
    )

button_14.bind('<Enter>', button_14_hover)
button_14.bind('<Leave>', button_14_leave)

button_14.place(
    x=148.0,
    y=635.6083984375,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs 8 to the selected text entry
button_image_15 = PhotoImage(
    file=relative_to_assets("button_15.png"))
button_15 = Button(
    image=button_image_15,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("8"),
    relief="flat"
)

button_image_hover_15 = PhotoImage(
    file=relative_to_assets("button_hover_15.png"))

def button_15_hover(e):
    button_15.config(
        image=button_image_hover_15
    )
def button_15_leave(e):
    button_15.config(
        image=button_image_15
    )

button_15.bind('<Enter>', button_15_hover)
button_15.bind('<Leave>', button_15_leave)

button_15.place(
    x=254.22433471679688,
    y=635.6083984375,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs 9 to the selected text entry
button_image_16 = PhotoImage(
    file=relative_to_assets("button_16.png"))
button_16 = Button(
    image=button_image_16,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("9"),
    relief="flat"
)

button_image_hover_16 = PhotoImage(
    file=relative_to_assets("button_hover_16.png"))

def button_16_hover(e):
    button_16.config(
        image=button_image_hover_16
    )
def button_16_leave(e):
    button_16.config(
        image=button_image_16
    )

button_16.bind('<Enter>', button_16_hover)
button_16.bind('<Leave>', button_16_leave)

button_16.place(
    x=360.44866943359375,
    y=635.6083984375,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs tan to the selected text entry
button_image_17 = PhotoImage(
    file=relative_to_assets("button_17.png"))
button_17 = Button(
    image=button_image_17,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("tan("),
    relief="flat"
)

button_image_hover_17 = PhotoImage(
    file=relative_to_assets("button_hover_17.png"))

def button_17_hover(e):
    button_17.config(
        image=button_image_hover_17
    )
def button_17_leave(e):
    button_17.config(
        image=button_image_17
    )

button_17.bind('<Enter>', button_17_hover)
button_17.bind('<Leave>', button_17_leave)

button_17.place(
    x=467.0,
    y=635.6083984375,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs 0 to the selected text entry
button_image_18 = PhotoImage(
    file=relative_to_assets("button_18.png"))
button_18 = Button(
    image=button_image_18,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("0"),
    relief="flat"
)

button_image_hover_18 = PhotoImage(
    file=relative_to_assets("button_hover_18.png"))

def button_18_hover(e):
    button_18.config(
        image=button_image_hover_18
    )
def button_18_leave(e):
    button_18.config(
        image=button_image_18
    )

button_18.bind('<Enter>', button_18_hover)
button_18.bind('<Leave>', button_18_leave)

button_18.place(
    x=148.0,
    y=696.91259765625,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs ^ (exponent) to the selected text entry
button_image_19 = PhotoImage(
    file=relative_to_assets("button_19.png"))
button_19 = Button(
    image=button_image_19,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("^"),
    relief="flat"
)

button_image_hover_19 = PhotoImage(
    file=relative_to_assets("button_hover_19.png"))

def button_19_hover(e):
    button_19.config(
        image=button_image_hover_19
    )
def button_19_leave(e):
    button_19.config(
        image=button_image_19
    )

button_19.bind('<Enter>', button_19_hover)
button_19.bind('<Leave>', button_19_leave)

button_19.place(
    x=254.22433471679688,
    y=696.91259765625,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs ln (log normal) to the selected text entry
button_image_20 = PhotoImage(
    file=relative_to_assets("button_20.png"))
button_20 = Button(
    image=button_image_20,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("ln("),
    relief="flat"
)

button_image_hover_20 = PhotoImage(
    file=relative_to_assets("button_hover_20.png"))

def button_20_hover(e):
    button_20.config(
        image=button_image_hover_20
    )
def button_20_leave(e):
    button_20.config(
        image=button_image_20
    )

button_20.bind('<Enter>', button_20_hover)
button_20.bind('<Leave>', button_20_leave)

button_20.place(
    x=360.44866943359375,
    y=696.91259765625,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs x (variable) to the selected text entry
button_image_xvar = PhotoImage(
    file=relative_to_assets("button_xvar.png"))
button_xvar = Button(
    image=button_image_xvar,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("x"),
    relief="flat"
)

button_image_hover_xvar = PhotoImage(
    file=relative_to_assets("button_hover_xvar.png"))

def button_xvar_hover(e):
    button_xvar.config(
        image=button_image_hover_xvar
    )
def button_xvar_leave(e):
    button_xvar.config(
        image=button_image_xvar
    )

button_xvar.bind('<Enter>', button_xvar_hover)
button_xvar.bind('<Leave>', button_xvar_leave)

button_xvar.place(
    x=148.0,
    y=880.8250732421875,  # Positioned below open parenthesis
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs ) (close parenthesis) to the selected text entry
button_image_27 = PhotoImage(
    file=relative_to_assets("button_27.png"))
button_27 = Button(
    image=button_image_27,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry(")"),
    relief="flat"
)

button_image_hover_27 = PhotoImage(
    file=relative_to_assets("button_hover_27.png"))

def button_27_hover(e):
    button_27.config(
        image=button_image_hover_27
    )
def button_27_leave(e):
    button_27.config(
        image=button_image_27
    )

button_27.bind('<Enter>', button_27_hover)
button_27.bind('<Leave>', button_27_leave)

button_27.place(
    x=254.22433471679688,
    y=819.5208740234375,
    width=92.22433471679688,
    height=50.30418014526367
)

# delete character button

def delete_character():
    # Get the currently focused widget
    focused_widget = window.focus_get()
    
    # Check if the focused widget is an Entry
    if isinstance(focused_widget, Entry):
        # If the current text is the placeholder, do nothing
        if focused_widget.get() == "Enter your function here" or \
           focused_widget.get() == "Input order of derivative" or \
           focused_widget.get() == "Upper li..." or \
           focused_widget.get() == "Lower li..":
            return
        
        # Delete the last character
        current_text = focused_widget.get()
        if current_text:
            focused_widget.delete(len(current_text) - 1, "end")
    # If no entry is focused, focus on the main function entry
    else:
        entry_1.focus_set()
        current_text = entry_1.get()
        if current_text and current_text != "Enter your function here":
            entry_1.delete(len(current_text) - 1, "end")

button_image_27_dup = PhotoImage(
    file=relative_to_assets("delete_char.png"))
button_27_dup = Button(
    image=button_image_27_dup,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: delete_character(),
    relief="flat"
)

button_image_hover_27_dup = PhotoImage(
    file=relative_to_assets("delete_char_hover.png"))

def button_27_dup_hover(e):
    button_27_dup.config(
        image=button_image_hover_27_dup
    )
def button_27_dup_leave(e):
    button_27_dup.config(
        image=button_image_27_dup
    )

button_27_dup.bind('<Enter>', button_27_dup_hover)
button_27_dup.bind('<Leave>', button_27_dup_leave)

button_27_dup.place(
    x=254.22433471679688,
    y=880.8250732421875,  # Positioned below the first close parenthesis
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs π (pi) to the selected text entry
button_image_28 = PhotoImage(
    file=relative_to_assets("button_28.png"))
button_28 = Button(
    image=button_image_28,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("3.141592653589793"),
    relief="flat"
)

button_image_hover_28 = PhotoImage(
    file=relative_to_assets("button_hover_28.png"))

def button_28_hover(e):
    button_28.config(
        image=button_image_hover_28
    )
def button_28_leave(e):
    button_28.config(
        image=button_image_28
    )

button_28.bind('<Enter>', button_28_hover)
button_28.bind('<Leave>', button_28_leave)

button_28.place(
    x=360.44866943359375,
    y=819.5208740234375,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs - (subtraction) to the selected text entry
button_image_29 = PhotoImage(
    file=relative_to_assets("button_29.png"))
button_29 = Button(
    image=button_image_29,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("-"),
    relief="flat"
)

button_image_hover_29 = PhotoImage(
    file=relative_to_assets("button_hover_29.png"))

def button_29_hover(e):
    button_29.config(
        image=button_image_hover_29
    )
def button_29_leave(e):
    button_29.config(
        image=button_image_29
    )

button_29.bind('<Enter>', button_29_hover)
button_29.bind('<Leave>', button_29_leave)

button_29.place(
    x=467.0,
    y=819.5208740234375,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs x (multiplication) to the selected text entry
button_image_21 = PhotoImage(
    file=relative_to_assets("button_21.png"))
button_21 = Button(
    image=button_image_21,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("*"),
    relief="flat"
)

button_image_hover_21 = PhotoImage(
    file=relative_to_assets("button_hover_21.png"))

def button_21_hover(e):
    button_21.config(
        image=button_image_hover_21
    )
def button_21_leave(e):
    button_21.config(
        image=button_image_21
    )

button_21.bind('<Enter>', button_21_hover)
button_21.bind('<Leave>', button_21_leave)

button_21.place(
    x=467.0,
    y=696.91259765625,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs √ / sqrt() to the selected text entry
button_image_22 = PhotoImage(
    file=relative_to_assets("button_22.png"))
button_22 = Button(
    image=button_image_22,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("sqrt("),
    relief="flat"
)

button_image_hover_22 = PhotoImage(
    file=relative_to_assets("button_hover_22.png"))

def button_22_hover(e):
    button_22.config(
        image=button_image_hover_22
    )
def button_22_leave(e):
    button_22.config(
        image=button_image_22
    )

button_22.bind('<Enter>', button_22_hover)
button_22.bind('<Leave>', button_22_leave)

button_22.place(
    x=148.0,
    y=758.216796875,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs / (fraction/division) to the selected text entry
button_image_23 = PhotoImage(
    file=relative_to_assets("button_23.png"))
button_23 = Button(
    image=button_image_23,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("/"),
    relief="flat"
)

button_image_hover_23 = PhotoImage(
    file=relative_to_assets("button_hover_23.png"))

def button_23_hover(e):
    button_23.config(
        image=button_image_hover_23
    )
def button_23_leave(e):
    button_23.config(
        image=button_image_23
    )

button_23.bind('<Enter>', button_23_hover)
button_23.bind('<Leave>', button_23_leave)

button_23.place(
    x=254.22433471679688,
    y=758.216796875,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs e (exponential function) to the selected text entry
button_image_24 = PhotoImage(
    file=relative_to_assets("button_24.png"))
button_24 = Button(
    image=button_image_24,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("e"),
    relief="flat"
)

button_image_hover_24 = PhotoImage(
    file=relative_to_assets("button_hover_24.png"))

def button_24_hover(e):
    button_24.config(
        image=button_image_hover_24
    )
def button_24_leave(e):
    button_24.config(
        image=button_image_24
    )

button_24.bind('<Enter>', button_24_hover)
button_24.bind('<Leave>', button_24_leave)

button_24.place(
    x=360.44866943359375,
    y=758.216796875,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs + (addition) to the selected text entry
button_image_25 = PhotoImage(
    file=relative_to_assets("button_25.png"))
button_25 = Button(
    image=button_image_25,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("+"),
    relief="flat"
)

button_image_hover_25 = PhotoImage(
    file=relative_to_assets("button_hover_25.png"))

def button_25_hover(e):
    button_25.config(
        image=button_image_hover_25
    )
def button_25_leave(e):
    button_25.config(
        image=button_image_25
    )

button_25.bind('<Enter>', button_25_hover)
button_25.bind('<Leave>', button_25_leave)

button_25.place(
    x=467.0,
    y=758.216796875,
    width=92.22433471679688,
    height=50.30418014526367
)

# Inputs ( open parenthesis to the selected text entry
button_image_26 = PhotoImage(
    file=relative_to_assets("button_26.png"))
button_26 = Button(
    image=button_image_26,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: insert_to_entry("("),
    relief="flat"
)

button_image_hover_26 = PhotoImage(
    file=relative_to_assets("button_hover_26.png"))

def button_26_hover(e):
    button_26.config(
        image=button_image_hover_26
    )
def button_26_leave(e):
    button_26.config(
        image=button_image_26
    )

button_26.bind('<Enter>', button_26_hover)
button_26.bind('<Leave>', button_26_leave)

button_26.place(
    x=148.0,
    y=819.5208740234375,
    width=92.22433471679688,
    height=50.30418014526367
)

image_image_13 = PhotoImage(
    file=relative_to_assets("image_13.png"))
image_13 = canvas.create_image(
    786.0,
    478.0,
    image=image_image_13
)

image_image_14 = PhotoImage(
    file=relative_to_assets("image_14.png"))
image_14 = canvas.create_image(
    786.0,
    357.0,
    image=image_image_14
)

image_image_15 = PhotoImage(
    file=relative_to_assets("image_15.png"))
image_15 = canvas.create_image(
    1151.0,
    478.0,
    image=image_image_15
)

image_image_16 = PhotoImage(
    file=relative_to_assets("image_16.png"))
image_16 = canvas.create_image(
    1151.0,
    357.0,
    image=image_image_16
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    786.0,
    478.5,
    image=entry_image_5
)
entry_5 = Text(
    bd=0,
    bg="#F3F3F3",
    fg="#000716",
    highlightthickness=0,
    wrap="word",
    height=2
)
entry_5_scrollbar = Scrollbar(entry_5)
entry_5_scrollbar.pack(side=RIGHT, fill=Y)
entry_5.config(yscrollcommand=entry_5_scrollbar.set)
entry_5_scrollbar.config(command=entry_5.yview)
entry_5.place(
    x=635.0,
    y=461.0,
    width=302.0,
    height=39.0
)

entry_image_6 = PhotoImage(
    file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(
    786.0,
    357.5,
    image=entry_image_6
)
entry_6 = Text(
    bd=0,
    bg="#F3F3F3",
    fg="#000716",
    highlightthickness=0,
    wrap="word",
    height=2
)
entry_6_scrollbar = Scrollbar(entry_6)
entry_6_scrollbar.pack(side=RIGHT, fill=Y)
entry_6.config(yscrollcommand=entry_6_scrollbar.set)
entry_6_scrollbar.config(command=entry_6.yview)
entry_6.place(
    x=635.0,
    y=340.0,
    width=302.0,
    height=39.0
)

entry_image_7 = PhotoImage(
    file=relative_to_assets("entry_7.png"))
entry_bg_7 = canvas.create_image(
    1151.0,
    478.5,
    image=entry_image_7
)
entry_7 = Text(
    bd=0,
    bg="#F3F3F3",
    fg="#000716",
    highlightthickness=0,
    wrap="word",
    height=2
)
entry_7_scrollbar = Scrollbar(entry_7)
entry_7_scrollbar.pack(side=RIGHT, fill=Y)
entry_7.config(yscrollcommand=entry_7_scrollbar.set)
entry_7_scrollbar.config(command=entry_7.yview)
entry_7.place(
    x=1000.0,
    y=461.0,
    width=302.0,
    height=39.0
)

entry_image_8 = PhotoImage(
    file=relative_to_assets("entry_8.png"))
entry_bg_8 = canvas.create_image(
    1151.0,
    357.5,
    image=entry_image_8
)
entry_8 = Text(
    bd=0,
    bg="#F3F3F3",
    fg="#000716",
    highlightthickness=0,
    wrap="word",
    height=2
)
entry_8_scrollbar = Scrollbar(entry_8)
entry_8_scrollbar.pack(side=RIGHT, fill=Y)
entry_8.config(yscrollcommand=entry_8_scrollbar.set)
entry_8_scrollbar.config(command=entry_8.yview)
entry_8.place(
    x=1000.0,
    y=340.0,
    width=302.0,
    height=39.0
)

image_image_17 = PhotoImage(
    file=relative_to_assets("image_17.png"))
image_17 = canvas.create_image(
    703.0,
    421.0,
    image=image_image_17
)

image_image_18 = PhotoImage(
    file=relative_to_assets("image_18.png"))
image_18 = canvas.create_image(
    689.0,
    300.0,
    image=image_image_18
)

image_image_19 = PhotoImage(
    file=relative_to_assets("image_19.png"))
image_19 = canvas.create_image(
    1059.0,
    421.0,
    image=image_image_19
)

image_image_20 = PhotoImage(
    file=relative_to_assets("image_20.png"))
image_20 = canvas.create_image(
    1079.0,
    300.0,
    image=image_image_20
)

# Add labels and placeholders for Entry/Text widgets
label_font = tkFont.Font(family="Poppins Medium", size=10)
label_fg = TEXT_COLOR

# Labels and placeholders for Entry widgets
label_entry_1 = Label()
label_entry_1.place(x=161.0, y=327.0)
add_placeholder(entry_1, "Enter your function here")

label_entry_2 = Label()
label_entry_2.place(x=240.0, y=460.0)
add_placeholder(entry_2, "Input order of derivative")

label_entry_3 = Label()
label_entry_3.place(x=366.0, y=460.0)
add_placeholder(entry_3, "Upper li...")

label_entry_4 = Label()
label_entry_4.place(x=464.0, y=460.0)
add_placeholder(entry_4, "Lower li..")

# Labels and placeholders for Text widgets
label_entry_5 = Label()
label_entry_5.place(x=635.0, y=438.0)
add_placeholder(entry_5, "Indefinite Integral Result", is_entry=False)

label_entry_6 = Label()
label_entry_6.place(x=635.0, y=317.0)
add_placeholder(entry_6, "First Derivative Result", is_entry=False)

label_entry_7 = Label()
label_entry_7.place(x=1000.0, y=438.0)
add_placeholder(entry_7, "Definite Integral Result", is_entry=False)

label_entry_8 = Label()
label_entry_8.place(x=1000.0, y=317.0)
add_placeholder(entry_8, "Nth Derivative Result", is_entry=False)

window.resizable(False, False)
window.mainloop()
