
import cv2
import numpy as np
import math
import time

class InteractiveDigitalPalette:
    def __init__(self):
        # Window setup
        self.window_name = "Interactive Digital Palette"
        cv2.namedWindow(self.window_name)
        
        # Canvas dimensions
        self.width, self.height = 1024, 768
        
        # Create canvas and interface areas
        self.canvas = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255
        self.interface_height = 120
        
        # Drawing properties
        self.drawing = False
        self.last_point = None
        self.current_color = (0, 0, 0)  # Default black
        self.brush_size = 5
        self.eraser_mode = False
        
        # Color palette and tools
        self.colors = [
            {"name": "Black", "color": (0, 0, 0)},
            {"name": "White", "color": (255, 255, 255)},
            {"name": "Red", "color": (0, 0, 255)},
            {"name": "Green", "color": (0, 255, 0)},
            {"name": "Blue", "color": (255, 0, 0)},
            {"name": "Yellow", "color": (0, 255, 255)},
            {"name": "Cyan", "color": (255, 255, 0)},
            {"name": "Magenta", "color": (255, 0, 255)},
            {"name": "Orange", "color": (0, 165, 255)},
            {"name": "Purple", "color": (128, 0, 128)},
            {"name": "Brown", "color": (42, 42, 165)},
            {"name": "Pink", "color": (203, 192, 255)}
        ]
        
        # Custom color RGB values
        self.custom_r = 0
        self.custom_g = 0
        self.custom_b = 0
        
        # Create trackbars for custom color
        cv2.createTrackbar('R', self.window_name, 0, 255, self.update_custom_color)
        cv2.createTrackbar('G', self.window_name, 0, 255, self.update_custom_color)
        cv2.createTrackbar('B', self.window_name, 0, 255, self.update_custom_color)
        
        # Tools
        self.tools = [
            {"name": "Brush", "icon": "🖌️", "action": self.select_brush},
            {"name": "Eraser", "icon": "🧽", "action": self.select_eraser},
            {"name": "Clear", "icon": "🗑️", "action": self.clear_canvas},
            {"name": "Save", "icon": "💾", "action": self.save_image}
        ]
        
        # Brush sizes
        self.brush_sizes = [2, 5, 10, 15, 20, 30]
        self.current_brush_index = 1  # Default to 5px
        
        # Effects
        self.effects = [
            {"name": "Normal", "action": self.normal_effect},
            {"name": "Blur", "action": self.blur_effect},
            {"name": "Sharpen", "action": self.sharpen_effect},
            {"name": "Grayscale", "action": self.grayscale_effect}
        ]
        self.current_effect = 0
        
        # History for undo/redo
        self.history = [self.canvas.copy()]
        self.history_position = 0
        
        # Set up mouse callback
        cv2.setMouseCallback(self.window_name, self.mouse_callback)
        
        # Create initial interface
        self.draw_interface()

    def update_custom_color(self, value=None):
        """Update custom color from trackbars"""
        self.custom_r = cv2.getTrackbarPos('R', self.window_name)
        self.custom_g = cv2.getTrackbarPos('G', self.window_name)
        self.custom_b = cv2.getTrackbarPos('B', self.window_name)
        
        # Update custom color in the interface
        self.current_color = (self.custom_b, self.custom_g, self.custom_r)
        self.draw_interface()

    def select_brush(self):
        """Select brush tool"""
        self.eraser_mode = False
        self.draw_interface()

    def select_eraser(self):
        """Select eraser tool"""
        self.eraser_mode = True
        self.draw_interface()

    def clear_canvas(self):
        """Clear the canvas"""
        # Create a white canvas
        self.canvas = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255
        
        # Add to history
        self.add_to_history()
        
        # Redraw interface
        self.draw_interface()

    def save_image(self):
        """Save the current canvas as an image"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"artwork_{timestamp}.png"
        cv2.imwrite(filename, self.canvas)
        
        # Show save confirmation
        temp_display = self.canvas.copy()
        cv2.putText(temp_display, f"Saved as {filename}", 
                    (self.width//2 - 200, self.height//2), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.imshow(self.window_name, temp_display)
        cv2.waitKey(1000)  # Show confirmation for 1 second
        
        # Redraw interface
        self.draw_interface()

    def add_to_history(self):
        """Add current canvas state to history"""
        # If we're not at the end of history, truncate
        if self.history_position < len(self.history) - 1:
            self.history = self.history[:self.history_position + 1]
        
        # Add current state to history
        self.history.append(self.canvas.copy())
        self.history_position = len(self.history) - 1
        
        # Limit history size
        if len(self.history) > 10:
            self.history.pop(0)
            self.history_position -= 1

    def undo(self):
        """Undo the last action"""
        if self.history_position > 0:
            self.history_position -= 1
            self.canvas = self.history[self.history_position].copy()
            self.draw_interface()

    def redo(self):
        """Redo the last undone action"""
        if self.history_position < len(self.history) - 1:
            self.history_position += 1
            self.canvas = self.history[self.history_position].copy()
            self.draw_interface()

    def normal_effect(self):
        """Apply no effect (normal mode)"""
        self.current_effect = 0
        self.draw_interface()

    def blur_effect(self):
        """Apply blur effect to canvas"""
        self.canvas = cv2.GaussianBlur(self.canvas, (15, 15), 0)
        self.add_to_history()
        self.current_effect = 1
        self.draw_interface()

    def sharpen_effect(self):
        """Apply sharpen effect to canvas"""
        kernel = np.array([[-1, -1, -1], 
                          [-1, 9, -1], 
                          [-1, -1, -1]])
        self.canvas = cv2.filter2D(self.canvas, -1, kernel)
        self.add_to_history()
        self.current_effect = 2
        self.draw_interface()

    def grayscale_effect(self):
        """Convert canvas to grayscale"""
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        self.canvas = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        self.add_to_history()
        self.current_effect = 3
        self.draw_interface()

    def draw_interface(self):
        """Draw the interface with tools and color palette"""
        # Create display with interface at top
        display = np.ones((self.height + self.interface_height, self.width, 3), dtype=np.uint8) * 240
        
        # Copy canvas to display
        display[self.interface_height:, :] = self.canvas
        
        # Draw interface background
        cv2.rectangle(display, (0, 0), (self.width, self.interface_height), (220, 220, 220), -1)
        cv2.line(display, (0, self.interface_height), (self.width, self.interface_height), (0, 0, 0), 2)
        
        # Draw color palette
        color_width = 30
        color_height = 30
        color_margin = 10
        color_start_x = 20
        color_start_y = 20
        
        for i, color_data in enumerate(self.colors):
            color = color_data["color"]
            x = color_start_x + i * (color_width + color_margin)
            y = color_start_y
            
            # Draw color box
            cv2.rectangle(display, (x, y), (x + color_width, y + color_height), color, -1)
            cv2.rectangle(display, (x, y), (x + color_width, y + color_height), (0, 0, 0), 1)
            
            # Highlight selected color
            if color == self.current_color:
                cv2.rectangle(display, (x-2, y-2), (x + color_width+2, y + color_height+2), (0, 0, 0), 2)
        
        # Draw custom color preview
        custom_x = color_start_x + len(self.colors) * (color_width + color_margin) + 20
        custom_y = color_start_y
        cv2.rectangle(display, (custom_x, custom_y), (custom_x + 60, custom_y + 30), 
                     (self.custom_b, self.custom_g, self.custom_r), -1)
        cv2.rectangle(display, (custom_x, custom_y), (custom_x + 60, custom_y + 30), (0, 0, 0), 1)
        cv2.putText(display, "Custom", (custom_x, custom_y + 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        # Draw brush sizes
        brush_start_x = custom_x + 100
        brush_start_y = color_start_y + 15
        
        for i, size in enumerate(self.brush_sizes):
            x = brush_start_x + i * 40
            
            # Draw brush size preview
            cv2.circle(display, (x, brush_start_y), size, (0, 0, 0), -1)
            
            # Highlight selected size
            if i == self.current_brush_index:
                cv2.circle(display, (x, brush_start_y), size + 5, (0, 0, 0), 1)
        
        # Draw tools
        tool_start_x = brush_start_x + len(self.brush_sizes) * 40 + 40
        tool_start_y = color_start_y
        tool_width = 80
        tool_height = 30
        
        for i, tool in enumerate(self.tools):
            x = tool_start_x + i * (tool_width + 10)
            
            # Draw tool button
            cv2.rectangle(display, (x, tool_start_y), (x + tool_width, tool_start_y + tool_height), 
                         (200, 200, 200), -1)
            cv2.rectangle(display, (x, tool_start_y), (x + tool_width, tool_start_y + tool_height), 
                         (0, 0, 0), 1)
            
            # Draw tool name
            cv2.putText(display, f"{tool['icon']} {tool['name']}", (x + 5, tool_start_y + 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
            
            # Highlight eraser if selected
            if tool["name"] == "Eraser" and self.eraser_mode:
                cv2.rectangle(display, (x-2, tool_start_y-2), 
                             (x + tool_width+2, tool_start_y + tool_height+2), 
                             (0, 0, 255), 2)
        
        # Draw effects
        effect_start_x = 20
        effect_start_y = color_start_y + 60
        effect_width = 80
        effect_height = 30
        
        for i, effect in enumerate(self.effects):
            x = effect_start_x + i * (effect_width + 10)
            
            # Draw effect button
            cv2.rectangle(display, (x, effect_start_y), (x + effect_width, effect_start_y + effect_height), 
                         (200, 200, 200), -1)
            cv2.rectangle(display, (x, effect_start_y), (x + effect_width, effect_start_y + effect_height), 
                         (0, 0, 0), 1)
            
            # Draw effect name
            cv2.putText(display, effect["name"], (x + 5, effect_start_y + 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
            
            # Highlight selected effect
            if i == self.current_effect:
                cv2.rectangle(display, (x-2, effect_start_y-2), 
                             (x + effect_width+2, effect_start_y + effect_height+2), 
                             (0, 0, 255), 2)
        
        # Draw undo/redo buttons
        undo_x = effect_start_x + len(self.effects) * (effect_width + 10) + 20
        undo_y = effect_start_y
        
        cv2.rectangle(display, (undo_x, undo_y), (undo_x + 60, undo_y + 30), (200, 200, 200), -1)
        cv2.rectangle(display, (undo_x, undo_y), (undo_x + 60, undo_y + 30), (0, 0, 0), 1)
        cv2.putText(display, "Undo", (undo_x + 10, undo_y + 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        redo_x = undo_x + 70
        cv2.rectangle(display, (redo_x, undo_y), (redo_x + 60, undo_y + 30), (200, 200, 200), -1)
        cv2.rectangle(display, (redo_x, undo_y), (redo_x + 60, undo_y + 30), (0, 0, 0), 1)
        cv2.putText(display, "Redo", (redo_x + 10, undo_y + 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        # Update display
        cv2.imshow(self.window_name, display)

    def mouse_callback(self, event, x, y, flags, param):
        """Handle mouse events"""
        # Adjust y coordinate to account for interface
        canvas_y = y - self.interface_height
        
        # Check if clicked in the interface area
        if y < self.interface_height:
            if event == cv2.EVENT_LBUTTONDOWN:
                self.handle_interface_click(x, y)
            return
            
        # Drawing on canvas
        if canvas_y >= 0:
            if event == cv2.EVENT_LBUTTONDOWN:
                self.drawing = True
                self.last_point = (x, canvas_y)
            elif event == cv2.EVENT_MOUSEMOVE:
                if self.drawing:
                    draw_color = (255, 255, 255) if self.eraser_mode else self.current_color
                    current_size = self.brush_sizes[self.current_brush_index]
                    
                    if self.last_point:
                        cv2.line(self.canvas, self.last_point, (x, canvas_y), draw_color, current_size)
                        
                    # Always draw a circle at the current point for better continuity
                    cv2.circle(self.canvas, (x, canvas_y), current_size // 2, draw_color, -1)
                    
                    self.last_point = (x, canvas_y)
                    self.draw_interface()
            elif event == cv2.EVENT_LBUTTONUP:
                if self.drawing:
                    self.drawing = False
                    self.last_point = None
                    self.add_to_history()

    def handle_interface_click(self, x, y):
        """Handle clicks in the interface area"""
        # Check color palette clicks
        color_width = 30
        color_height = 30
        color_margin = 10
        color_start_x = 20
        color_start_y = 20
        
        for i, color_data in enumerate(self.colors):
            color = color_data["color"]
            cx = color_start_x + i * (color_width + color_margin)
            cy = color_start_y
            
            if cx <= x <= cx + color_width and cy <= y <= cy + color_height:
                self.current_color = color
                self.eraser_mode = False
                self.draw_interface()
                return
        
        # Check custom color preview click
        custom_x = color_start_x + len(self.colors) * (color_width + color_margin) + 20
        custom_y = color_start_y
        if custom_x <= x <= custom_x + 60 and custom_y <= y <= custom_y + 30:
            self.current_color = (self.custom_b, self.custom_g, self.custom_r)
            self.eraser_mode = False
            self.draw_interface()
            return
            
        # Check brush size clicks
        brush_start_x = custom_x + 100
        brush_start_y = color_start_y + 15
        
        for i, size in enumerate(self.brush_sizes):
            bx = brush_start_x + i * 40
            
            if abs(x - bx) <= 20 and abs(y - brush_start_y) <= 20:
                self.current_brush_index = i
                self.draw_interface()
                return
        
        # Check tool clicks
        tool_start_x = brush_start_x + len(self.brush_sizes) * 40 + 40
        tool_start_y = color_start_y
        tool_width = 80
        tool_height = 30
        
        for i, tool in enumerate(self.tools):
            tx = tool_start_x + i * (tool_width + 10)
            
            if tx <= x <= tx + tool_width and tool_start_y <= y <= tool_start_y + tool_height:
                tool["action"]()
                return
        
        # Check effect clicks
        effect_start_x = 20
        effect_start_y = color_start_y + 60
        effect_width = 80
        effect_height = 30
        
        for i, effect in enumerate(self.effects):
            ex = effect_start_x + i * (effect_width + 10)
            
            if ex <= x <= ex + effect_width and effect_start_y <= y <= effect_start_y + effect_height:
                effect["action"]()
                return
        
        # Check undo/redo buttons
        undo_x = effect_start_x + len(self.effects) * (effect_width + 10) + 20
        undo_y = effect_start_y
        
        if undo_x <= x <= undo_x + 60 and undo_y <= y <= undo_y + 30:
            self.undo()
            return
            
        redo_x = undo_x + 70
        if redo_x <= x <= redo_x + 60 and undo_y <= y <= undo_y + 30:
            self.redo()
            return

    def run(self):
        """Run the main application loop"""
        print("\nWelcome to Interactive Digital Palette!")
        print("==================================")
        print("Controls:")
        print("- Click on colors to select them")
        print("- Click on brush sizes to change brush size")
        print("- Use the eraser tool to erase")
        print("- Apply effects to transform your artwork")
        print("- Press 'z' for undo, 'y' for redo")
        print("- Press 'c' to clear canvas")
        print("- Press 's' to save your artwork")
        print("- Press 'ESC' to exit")
        print("==================================\n")
        
        while True:
            # Check for keyboard shortcuts
            key = cv2.waitKey(1) & 0xFF
            
            if key == 27:  # ESC key
                break
            elif key == ord('z'):  # Undo
                self.undo()
            elif key == ord('y'):  # Redo
                self.redo()
            elif key == ord('c'):  # Clear
                self.clear_canvas()
            elif key == ord('s'):  # Save
                self.save_image()
            elif key == ord('b'):  # Brush
                self.select_brush()
            elif key == ord('e'):  # Eraser
                self.select_eraser()
                
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = InteractiveDigitalPalette()
    app.run()