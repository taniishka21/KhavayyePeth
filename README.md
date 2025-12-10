🍴 Khavayye Peth (Foodie Hub)

Khavayye Peth is a Django-based web application designed to help users explore, search, and discover the best restaurants, street food, and cafes in Pune, India. It provides a clean, responsive interface to browse food destinations with essential details like ratings, cost, cuisine, and location.

✨ Features

Responsive Navigation: A sticky, dark-themed navbar that adapts to all screen sizes using Bootstrap 5.

User Authentication: Secure user sign-up, login, and profile management (as implied by the navbar structure).

Dynamic Exploration: The core "Explore" page allows users to browse a list of food establishments.

Client-Side Search: Efficient, real-time filtering of restaurants by name, cuisine, or location directly on the client side (using JavaScript).

Restaurant Details: Quick view of key metrics including delivery rating, number of reviews, cuisine type, and approximate cost.

External Links: Direct links to external platforms (e.g., Zomato, Swiggy) for viewing full details or placing orders.

AI chatbot assistant.

🛠 Technologies Used

This project is built using a modern web development stack:

Backend: Python 3.x, Django

Database: SQLite (default) or PostgreSQL/MySQL

Frontend: HTML5, CSS3, JavaScript (Vanilla JS for search), Bootstrap 5 (for styling and responsiveness)

Templating: Django Templating Language (DTL)

🚀 Getting Started

Follow these steps to get your local copy up and running.

Prerequisites

You need Python 3.x installed on your system.

1. Clone the repository

git clone [https://github.com/taniishka21/KhavayyePeth.git](https://github.com/taniishka21/KhavayyePeth.git)
cd KhavayyePeth


2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies:

# Create the environment
python -m venv venv

# Activate the environment (Linux/macOS)
source venv/bin/activate

# Activate the environment (Windows)
venv\Scripts\activate


3. Install Dependencies

Install the required Python packages (assuming you have a requirements.txt):

pip install -r requirements.txt
# (Typically includes Django, djangorestframework, etc.)


4. Database Setup

Apply the initial database migrations:

python manage.py makemigrations
python manage.py migrate


5. Running the Application

Start the Django development server:

python manage.py runserver


The application will now be running at http://127.0.0.1:8000/.

🧑‍💻 Usage

The primary interaction point is the Explore page.

Navigate: Go to /explore/ or click the "Explore" link in the navigation bar.

Browse: View the list of all featured restaurants.

Search: Use the large search bar at the top to filter the list instantly. You can type in:

Restaurant Name (e.g., "Shree Misal")

Cuisine (e.g., "Italian", "Maharashtrian")

Location (e.g., "Kothrud", "Camp")

View Details: Click the View on Zomato button (or similar) to be taken to the external platform for ordering/full reviews.

📝 Example Data Structure (Context for Explore Page)

The explore page expects a list of Restaurant objects in the Django context. For the cards to render correctly, your objects should have these attributes:

# Example Restaurant object attributes used in the template
{
    'rest_name': 'Sample Cafe',
    'loc': 'Kothrud, Pune',
    'delivery_rating': 4.2,
    'delivery_reviews': 589,
    'cost': '₹300 for two',
    'cuisine': 'Cafe, Italian',
    'link': '[https://example.com/zomato/sample-cafe](https://example.com/zomato/sample-cafe)' 
}

Developed with 🌶️ and 💻 for the Pune Food Scene.
