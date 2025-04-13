# GUI imports
import tkinter as tk
from tkinter import messagebox, Frame, Scrollbar, Canvas
# Database imports
from db.db_config import get_reviews, get_all_product_ids
# Sentiment analysis utils
from utils.sentiment_utils import classify_sentiments, get_aspect_sentiments
# Online review analyzer
from features import scrape_reviews, analyze_reviews, generate_analytics, get_product_id
# Plotting
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Example inventory used to match product names
inventory = [
    {"product_id": "P101", "name": "iPhone 16"},
    {"product_id": "P102", "name": "iPhone 15"},
    {"product_id": "P103", "name": "iPhone 14"},
]

# ---------- Load products from DB and generate buttons ----------
def load_products():
    product_ids = get_all_product_ids()
    for product_id in product_ids:
        card = tk.Frame(card_frame, bg="white", bd=1, relief="solid")
        card.pack(pady=5, padx=5, fill="x")

        btn = tk.Button(card, text=f"🛍️ {product_id}", font=("Arial", 11),
                        width=18, height=2, bg="#f0f0f0",
                        command=lambda pid=product_id: analyze_product(pid))
        btn.pack(padx=5, pady=5)

        online_btn = tk.Button(card, text="🌐 Analyze Online Reviews", font=("Arial", 9),
                               bg="#dff0d8", fg="black",
                               command=lambda pid=product_id: analyze_online_reviews(pid))
        online_btn.pack(padx=5, pady=(0, 5))

# ---------- Local DB Review Analysis ----------
def analyze_product(product_id):
    reviews = get_reviews(product_id)
    if not reviews:
        messagebox.showinfo("No Data", "No reviews found for this product.")
        return

    sentiment_results = classify_sentiments(reviews)

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"📦 Product: {product_id} (Local DB)\n\n")
    for i, (review, sentiment) in enumerate(sentiment_results):
        result_text.insert(tk.END, f"{i+1}. {review[:60]}... → {sentiment.capitalize()}\n")

    aspect_sentiments = get_aspect_sentiments(reviews)
    draw_aspect_chart(aspect_sentiments)

# ---------- Online Review Analysis ----------
def analyze_online_reviews(product_id):
    # Map product_id to name
    product_name = next((item['name'] for item in inventory if item['product_id'] == product_id), None)
    if not product_name:
        messagebox.showerror("Mapping Error", f"Product ID {product_id} not mapped to a product name.")
        return

    trustpilot_url = "https://www.trustpilot.com/review/www.apple.com"

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"🌐 Scraping online reviews for {product_name}...\n")

    try:
        reviews = scrape_reviews(trustpilot_url, product_id=product_id)
        enriched_reviews = analyze_reviews(reviews)
        df, analytics = generate_analytics(enriched_reviews)

        result_text.insert(tk.END, f"📦 Product: {product_id} (Online)\n\n")
        for i, row in df.head(10).iterrows():
            result_text.insert(tk.END, f"{i+1}. {row['review'][:60]}... → {row['sentiment']}\n")

        pos, neu, neg = analytics['positive'], analytics['neutral'], analytics['negative']
        aspect_scores = {
            "Positive": pos / analytics['total_reviews'],
            "Neutral": neu / analytics['total_reviews'],
            "Negative": neg / analytics['total_reviews'],
        }
        draw_aspect_chart(aspect_scores)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# ---------- Chart Drawing ----------
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Global placeholder for the chart canvas so we can remove the old one before drawing new
chart_canvas = None

def draw_aspect_chart(aspect_sentiments):
    # Extract aspects and scores
    aspects = list(aspect_sentiments.keys())
    values = [aspect_sentiments[a] if aspect_sentiments[a] is not None else 0 for a in aspects]

    fig, ax = plt.subplots()
    ax.bar(aspects, values, color="skyblue")
    ax.set_title("Aspect-wise Sentiment Analysis")
    ax.set_ylabel("Sentiment Score")
    ax.set_ylim(0, 1)  # Optional: Clamp values between 0 and 1
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()




# ---------- GUI Layout ----------
root = tk.Tk()
root.title("📊 Product Sentiment Dashboard")
root.geometry("1000x650")
root.configure(bg="white")

# Product Sidebar
product_frame = Frame(root, bg="white")
product_frame.pack(side="left", fill="y", padx=10, pady=10)

canvas_area = Canvas(product_frame, bg="white", width=240)
scrollbar = Scrollbar(product_frame, orient="vertical", command=canvas_area.yview)
scrollable_frame = Frame(canvas_area, bg="white")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas_area.configure(scrollregion=canvas_area.bbox("all"))
)

canvas_area.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas_area.configure(yscrollcommand=scrollbar.set)

canvas_area.pack(side="left", fill="y")
scrollbar.pack(side="right", fill="y")
card_frame = scrollable_frame

# Load buttons
load_products()

# Right panel
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
