from typing import TypedDict, Annotated, List
import tkinter as tk
from tkinter import messagebox, scrolledtext
from google.generativeai import configure, GenerativeModel

# Configure Gemini API (Replace with your own API key)
configure(api_key="AIzaSyB-TqUWiOqtAkB5taWktRktfEywkBG6odA")
gemini_model = GenerativeModel("gemini-2.0-flash")

class PlannerState(TypedDict):
    messages: Annotated[List[str], "the messages in the conversation"]
    city: str
    interests: List[str]
    days: int
    itinerary: str

# Generate an itinerary using Gemini AI
def generate_itinerary(city: str, interests: List[str], days: int) -> str:
    interest_str = ", ".join(interests)
    
    prompt = f"""
    Create a unique {days}-day travel itinerary for {city} based on the following interests: {interest_str}.
    Each day's plan should include:
    - Morning: Activities like sightseeing, nature walks, or cultural visits.
    - Afternoon: Adventure activities, historical tours, or food experiences.
    - Evening: Entertainment, nightlife, or relaxation options.
    
    Ensure each day has different activities and travel tips.
    Format the response in a structured way.
    """

    try:
        response = gemini_model.generate_content(prompt)
        return response.text if response else "⚠️ Could not generate itinerary. Please try again."
    except Exception as e:
        return f"⚠️ Error generating itinerary: {str(e)}"

# GUI Setup
def create_ui():
    def get_itinerary():
        city = city_entry.get().strip()
        interests = interests_entry.get().strip().split(", ")
        try:
            days = int(days_entry.get().strip())
            if not city or not interests or days <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid city, interests, and number of days.")
            return

        itinerary = generate_itinerary(city, interests, days)
        
        # Clear previous text
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)

        # Add formatted text with colors
        add_colored_text(result_text, f"🌍 {days}-Day Travel Plan for {city} 🌍\n", "title")
        result_text.insert(tk.END, "\n")

        # Formatting response using colors
        for line in itinerary.split("\n"):
            if "📅 Day" in line:
                add_colored_text(result_text, f"\n{line}\n", "day_title")
            elif "🌅 Morning:" in line:
                add_colored_text(result_text, "🌅 Morning: ", "morning")
                result_text.insert(tk.END, line.replace("🌅 Morning:", "").strip() + "\n")
            elif "🌞 Afternoon:" in line:
                add_colored_text(result_text, "🌞 Afternoon: ", "afternoon")
                result_text.insert(tk.END, line.replace("🌞 Afternoon:", "").strip() + "\n")
            elif "🌙 Evening:" in line:
                add_colored_text(result_text, "🌙 Evening: ", "evening")
                result_text.insert(tk.END, line.replace("🌙 Evening:", "").strip() + "\n")
            elif "🌦️ Weather Conditions:" in line or "🚗 Best Mode of Transport:" in line:
                add_colored_text(result_text, f"\n{line}\n", "section_title")
            else:
                result_text.insert(tk.END, line + "\n")

        result_text.config(state=tk.DISABLED)

    def add_colored_text(widget, text, tag):
        widget.insert(tk.END, text, tag)

    root = tk.Tk()
    root.title("🌍 AI Travel Planner")
    root.geometry("1920x1080")
    root.configure(bg="#f0f8ff")

    tk.Label(root, text="Enter City:", font=("Arial", 14, "bold"), bg="#f0f8ff", fg="#333").pack(pady=5)
    city_entry = tk.Entry(root, font=("Arial", 12), width=30)
    city_entry.pack(pady=5)

    tk.Label(root, text="Enter Number of Days:", font=("Arial", 14, "bold"), bg="#f0f8ff", fg="#333").pack(pady=5)
    days_entry = tk.Entry(root, font=("Arial", 12), width=30)
    days_entry.pack(pady=5)

    tk.Label(root, text="Enter Interests (comma separated):", font=("Arial", 14, "bold"), bg="#f0f8ff", fg="#333").pack(pady=5)
    interests_entry = tk.Entry(root, font=("Arial", 12), width=30)
    interests_entry.pack(pady=5)

    generate_btn = tk.Button(root, text="✨ Generate AI Itinerary ✨", font=("Arial", 14, "bold"), bg="#ff4500", fg="white", command=get_itinerary)
    generate_btn.pack(pady=20)

    # Scrollable output box
    result_text = scrolledtext.ScrolledText(root, font=("Arial", 12), height=18, width=80, state=tk.DISABLED, wrap=tk.WORD, bg="#fffafa", fg="#333")
    result_text.pack(pady=10)

    # Define text tags for coloring
    result_text.tag_configure("title", font=("Arial", 16, "bold"), foreground="#0047AB")
    result_text.tag_configure("day_title", font=("Arial", 14, "bold"), foreground="#228B22")
    result_text.tag_configure("morning", font=("Arial", 12, "bold"), foreground="#ff4500")
    result_text.tag_configure("afternoon", font=("Arial", 12, "bold"), foreground="#D2691E")
    result_text.tag_configure("evening", font=("Arial", 12, "bold"), foreground="#800080")
    result_text.tag_configure("section_title", font=("Arial", 14, "bold"), foreground="#0047AB")

    root.mainloop()

# Start the UI
create_ui()
