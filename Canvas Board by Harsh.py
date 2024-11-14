# Canvas Board - Tkinter Whiteboard by Harsh

# Using Tkinter features shall be added
'''
 
1. Erase option + clear all canvas
2. Sharing 
3. Saving 
4. Multiple colors option (for pen + theme)
5. Also typed from keyboard 
6. Images
7. Mind maps or flowchart types 
8. Plan Your day (to-do list type with alarm)
9. Pen thickness adjustment
'''

from tkinter import *
from tkinter import colorchooser
from PIL import Image, ImageOps
import io

# Initialize the main window with maximized state and title
root = Tk()
root.state('zoomed')
root.title("CanvasBoard-White Board By Harsh")
root.configure(bg='#8000ff')

# Global variables for drawing properties and slide management
last_x, last_y = None, None  # Store last x, y coordinates for drawing
pen_color = 'black'          # Default pen color
pen_thickness = 2            # Default pen thickness for drawing
current_slide_index = 0      # Track the index of the currently visible slide
slides = []                  # List to store multiple slides (canvas widgets)

# Function to start drawing (when mouse button is pressed)
def start_draw(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y  # Update last_x, last_y with the starting coordinates

# Function to draw a line on the canvas (when mouse is dragged)
def draw(event):
    global last_x, last_y
    
    # Draw line from the last coordinates to the current position of the mouse
    line_id = slides[current_slide_index].create_line(
        last_x, last_y, event.x, event.y, fill=pen_color, width=pen_thickness
    )
    # Update last_x, last_y to the current position to continue drawing smoothly
    last_x, last_y = event.x, event.y

# Function to create a new slide (canvas) and switch to it
def create_new_slide():
    global current_slide_index

    # Hide the current slide if it exists
    if slides:
        slides[current_slide_index].pack_forget()
    
    # Create a new canvas, add it to slides, and display it as the current slide
    new_canvas = Canvas(root, bg='white', width=1062, height=590, cursor='hand2')
    slides.append(new_canvas)
    current_slide_index = len(slides) - 1  # Update the current slide index

    # Bind mouse events to start and continue drawing on the new slide
    new_canvas.bind("<Button-1>", start_draw)  # Start drawing on left mouse click
    new_canvas.bind("<B1-Motion>", draw)       # Draw when the mouse moves

    # Display the new slide
    new_canvas.pack(side="right", padx=40)

# Function to navigate to the previous slide
def show_previous_slide():
    global current_slide_index
    if current_slide_index > 0:  # Only if there is a previous slide
        slides[current_slide_index].pack_forget()  # Hide the current slide
        current_slide_index -= 1  # Move to the previous slide
        slides[current_slide_index].pack(side="right", padx=40)  # Show the previous slide

# Function to navigate to the next slide
def show_next_slide():
    global current_slide_index
    if current_slide_index < len(slides) - 1:  # Only if there is a next slide
        slides[current_slide_index].pack_forget()  # Hide the current slide
        current_slide_index += 1  # Move to the next slide
        slides[current_slide_index].pack(side="right", padx=40)  # Show the next slide

# Initialize the first slide at the start
create_new_slide()

# Function to clear the entire canvas of the current slide
def clr_canvas():
    slides[current_slide_index].delete("all")  # Remove all items from the current slide's canvas

# Change pen color using color palette
def set_pen_color(new_color):
    global pen_color
    pen_color = new_color

# Change pen thickness using scale
def set_pen_thickness(new_thickness):
    global pen_thickness
    pen_thickness = new_thickness

# Save slides as PDF
def save_all_slides_as_pdf():
    from tkinter import filedialog
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return

    images = []
    for canvas in slides:
        ps_data = canvas.postscript(colormode='color')
        img = Image.open(io.BytesIO(ps_data.encode('utf-8'))).convert("RGB")
        images.append(img)
    if images:
        images[0].save(file_path, save_all=True, append_images=images[1:])

# Button to clear the current slide
clr_btn = Button(root, text='Clear Canvas', bd=1, bg='yellow', command=clr_canvas)
clr_btn.place(x=20,y=60)

# Button to create a new blank slide
new_slide_btn = Button(root, text="New Slide", bd=1, bg='lightblue', command=create_new_slide)
new_slide_btn.place(x=20,y=100)

# Button to navigate to the previous slide
prev_slide_btn = Button(root, text="< Previous", bd=1, bg='lightgreen', command=show_previous_slide)
prev_slide_btn.place(x=175,y=4)

# Button to navigate to the next slide
next_slide_btn = Button(root, text="Next >", bd=1, bg='lightgreen', command=show_next_slide)
next_slide_btn.place(x=1195,y=4)

# Adding Color Palette Buttons
color_frame1 = Frame(root)
color_frame1.pack(side="left", padx=10)
color_frame2 = Frame(root)
color_frame2.pack(side="left", padx=20)
colors1 = ['black','red','green','blue','yellow','purple']
colors2 = ['orange','deeppink1','blueviolet','brown','chartreuse1','deepskyblue']
for color in colors1:
    color_btn = Button(color_frame1, bg=color, width=3, height=1, command=lambda c=color: set_pen_color(c))
    color_btn.pack(pady=1)
for color in colors2:
    color_btn = Button(color_frame2, bg=color, width=3, height=1, command=lambda c=color: set_pen_color(c))
    color_btn.pack(pady=1)
    
# Adding Thickness Scale
thickness_scale = Scale(root, from_=1, to=10, orient=HORIZONTAL, label="Pen Thickness", command=lambda v: set_pen_thickness(int(v)))
thickness_scale.set(2)
thickness_scale.place(x=15, y=550)

# button for saving as PDF
save_btn=Button(root, text="Save ", bg='orange', command=save_all_slides_as_pdf)
save_btn.place(x=20, y=20)

root.mainloop()
