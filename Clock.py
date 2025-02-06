import tkinter as tk
from tkinter import ttk
import math
from datetime import datetime
import pytz  # For timezone handling

class HighDefAnalogClock:
    def __init__(self, root):
        self.root = root
        self.root.title("High-Definition Analog Clock")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2f")

        # Dropdown for selecting country/timezone
        self.timezone_var = tk.StringVar()
        self.timezones = {
            "New York": "America/New_York",
            "London": "Europe/London",
            "Tokyo": "Asia/Tokyo",
            "Sydney": "Australia/Sydney",
            "Mumbai": "Asia/Kolkata",
            "Pakistan": "Asia/Karachi",  # Pakistan Time (PKT)
            "UAE": "Asia/Dubai",         # UAE Time (GST)
            "Saudi Arabia": "Asia/Riyadh",  # Saudi Arabia Time (AST)
            "UTC": "UTC"
        }
        self.timezone_var.set("UTC")  # Default timezone

        # Create a label and dropdown for timezone selection
        self.timezone_label = tk.Label(self.root, text="Select Country/Timezone:", font=("Helvetica", 12), fg="#ecf0f1", bg="#1e1e2f")
        self.timezone_label.pack(pady=10)

        self.timezone_dropdown = ttk.Combobox(self.root, textvariable=self.timezone_var, values=list(self.timezones.keys()), state="readonly")
        self.timezone_dropdown.pack()

        # Canvas for the clock face
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg="#1e1e2f", highlightthickness=0)
        self.canvas.pack()

        # Digital time label
        self.time_label = tk.Label(self.root, text="", font=("Helvetica", 16), fg="#ecf0f1", bg="#1e1e2f")
        self.time_label.pack(pady=10)

        # Draw the clock face
        self.draw_clock_face()

        # Start updating the clock
        self.update_clock()

    def draw_clock_face(self):
        # Draw a radial gradient background
        for i in range(30):
            radius = 220 - i * 7
            color = self.interpolate_color("#3498db", "#2c3e50", i / 30)
            self.canvas.create_oval(
                250 - radius, 250 - radius,
                250 + radius, 250 + radius,
                outline=color, fill=color
            )

        # Draw hour markers with numbers
        for i in range(1, 13):  # Numbers 1 through 12
            angle = math.radians(i * 30 - 90)  # 30 degrees per hour
            x = 250 + 160 * math.cos(angle)  # Position slightly inward from the edge
            y = 250 + 160 * math.sin(angle)
            self.canvas.create_text(x, y, text=str(i), font=("Helvetica", 18, "bold"), fill="#ecf0f1")

        # Draw minute markers
        for i in range(60):
            angle = math.radians(i * 6 - 90)  # 6 degrees per minute
            x1 = 250 + 190 * math.cos(angle)
            y1 = 250 + 190 * math.sin(angle)
            x2 = 250 + 200 * math.cos(angle)
            y2 = 250 + 200 * math.sin(angle)
            if i % 5 != 0:  # Skip every 5th marker (already drawn as hour markers)
                self.canvas.create_line(x1, y1, x2, y2, fill="#bdc3c7", width=2)

    def interpolate_color(self, start_color, end_color, fraction):
        """Interpolate between two hex colors."""
        start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
        end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
        interpolated_rgb = tuple(
            int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * fraction) for i in range(3)
        )
        return f"#{''.join(f'{v:02x}' for v in interpolated_rgb)}"

    def update_clock(self):
        # Clear previous hands
        self.canvas.delete("hands")

        # Get the selected timezone
        selected_timezone = self.timezones[self.timezone_var.get()]
        tz = pytz.timezone(selected_timezone)
        now = datetime.now(tz)

        hour = now.hour % 12
        minute = now.minute
        second = now.second

        # Determine AM/PM
        am_pm = "AM" if now.hour < 12 else "PM"

        # Calculate angles for the hands
        hour_angle = math.radians((hour * 30) + (minute / 2) - 90)
        minute_angle = math.radians((minute * 6) + (second / 10) - 90)
        second_angle = math.radians(second * 6 - 90)

        # Draw hour hand
        hour_x = 250 + 80 * math.cos(hour_angle)
        hour_y = 250 + 80 * math.sin(hour_angle)
        self.canvas.create_line(250, 250, hour_x, hour_y, fill="#e74c3c", width=10, tags="hands")

        # Draw minute hand
        minute_x = 250 + 120 * math.cos(minute_angle)
        minute_y = 250 + 120 * math.sin(minute_angle)
        self.canvas.create_line(250, 250, minute_x, minute_y, fill="#f1c40f", width=8, tags="hands")

        # Draw second hand
        second_x = 250 + 140 * math.cos(second_angle)
        second_y = 250 + 140 * math.sin(second_angle)
        self.canvas.create_line(250, 250, second_x, second_y, fill="#2ecc71", width=4, tags="hands")

        # Draw center dot
        self.canvas.create_oval(245, 245, 255, 255, fill="#ecf0f1", tags="hands")

        # Update digital time with AM/PM
        digital_time = now.strftime(f"{self.timezone_var.get()}: %I:%M:%S {am_pm}")
        self.time_label.config(text=digital_time)

        # Schedule the next update
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = HighDefAnalogClock(root)
    root.mainloop()