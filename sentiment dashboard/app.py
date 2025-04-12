# Gui imports
import tkinter as tk
from tkinter import messagebox, Frame, Scrollbar, Canvas
# Database import
from db.db_config import get_reviews, get_all_product_ids
# sentiment analyze
from utils.sentiment_utils import classify_sentiments, get_aspect_sentiments
# plot graph
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Product buttons
def load_products():
    #Product ids from db_config
    product_ids = get_all_product_ids()
    #Button for each product
    for product in product_ids:
        card = tk.Button(card_frame, text=f"🛍️ {product}", font=("Arial", 11),
                         width=20, height=2, bg="#f0f0f0", command=lambda p=product: analyze_product(p))
        card.pack(pady=5)
#Analyze reviews 
def analyze_product(product_id):
    #Load reviews from db_config
    reviews = get_reviews(product_id)
    #If data is not present
    if not reviews:
        messagebox.showinfo("No Data", "No reviews found for this product.")
        return

    # Sentiment for each review
    sentiment_results = classify_sentiments(reviews)
    #print review and sentiment
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"📦 Product: {product_id}\n\n")
    for i, (review, sentiment) in enumerate(sentiment_results):
        result_text.insert(tk.END, f"{i+1}. {review[:60]}... → {sentiment.capitalize()}\n")

    # Aspect Chart
    aspect_sentiments = get_aspect_sentiments(reviews)
    draw_aspect_chart(aspect_sentiments)

#Use matplotlib to plot charts
def draw_aspect_chart(scores):
    fig.clear()
    axes = fig.add_subplot(111)

    #List of aspects
    aspects = list(scores.keys())
    #Finding sentiment score for each aspect
    values = [scores[a] if scores[a] is not None else 0 for a in aspects]
    #Plot the bar graph
    axes.bar(aspects, values, color="skyblue")
    axes.set_ylim(0, 2) # y axis range 0 to 2
    axes.set_ylabel("Sentiment (0=Neg, 1=Neutral, 2=Positive)") # Y label
    axes.set_title("Aspect-Based Sentiment") #Title

    canvas.draw()

# --- GUI Layout ---
root = tk.Tk()
root.title("📊 Product Sentiment Dashboard")
root.geometry("1000x650")
root.configure(bg="white")

# Product Cards Scrollable Area on the leftt side
product_frame = Frame(root, bg="white")
product_frame.pack(side="left", fill="y", padx=10, pady=10)

canvas_area = Canvas(product_frame, bg="white", width=200)
#vertical scrollbar
scrollbar = Scrollbar(product_frame, orient="vertical", command=canvas_area.yview)
scrollable_frame = Frame(canvas_area, bg="white")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas_area.configure(
        scrollregion=canvas_area.bbox("all")
    )
)
#Adding Scrollable frame into canvas
canvas_area.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas_area.configure(yscrollcommand=scrollbar.set)

canvas_area.pack(side="left", fill="y")
scrollbar.pack(side="right", fill="y")
card_frame = scrollable_frame

# Load product cards
load_products()

# Sentiment Results
right_frame = Frame(root, bg="white")
right_frame.pack(side="right", fill="both", expand=True)

tk.Label(right_frame, text="Sentiment Analysis Results", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
result_text = tk.Text(right_frame, height=10, width=80, font=("Arial", 11))
result_text.pack(pady=5)

# Chart area
fig = plt.Figure(figsize=(6.5, 3), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(pady=10)

root.mainloop()
