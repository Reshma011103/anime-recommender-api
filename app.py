from flask import Flask, request, render_template_string
import pandas as pd

app = Flask(__name__)

# Load and prepare dataset
data = pd.read_csv("anime.csv")
data = data.dropna(subset=['genre'])

# Extract individual genres from comma-separated strings
all_genres = set()
for genre_str in data['genre']:
    for g in genre_str.split(','):
        all_genres.add(g.strip())
unique_genres = sorted(all_genres)

# Function to get top anime for a given genre
def get_recommendations(genre, n=15):
    filtered_data = data[data['genre'].str.contains(genre, case=False, na=False)]
    filtered_data = filtered_data.sort_values(by='rating', ascending=False)
    return filtered_data[['name', 'rating']].head(n)

# Home page with styled dropdown
@app.route('/', methods=['GET'])
def home():
    return render_template_string(DROPDOWN_TEMPLATE, genres=unique_genres)

# Result page
@app.route('/recommend', methods=['POST'])
def recommend():
    genre = request.form['genre']
    recommendations = get_recommendations(genre)
    return render_template_string(RECOMMEND_TEMPLATE, genre=genre, recommendations=recommendations.to_dict(orient='records'))

# Templates
DROPDOWN_TEMPLATE = '''
<!doctype html>
<html>
<head>
    <title>Anime Recommender</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f6f8;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        h1 {
            color: #333;
        }
        form {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        select {
            width: 250px;
            padding: 10px;
            font-size: 16px;
            border-radius: 8px;
            border: 1px solid #ccc;
            margin-right: 15px;
        }
        input[type="submit"] {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #1976d2;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #1565c0;
        }
    </style>
</head>
<body>
    <h1>Anime  Recommender</h1>
    <form action="/recommend" method="post">
        <label for="genre">Choose a genre:</label><br><br>
        <select name="genre" id="genre">
            {% for genre in genres %}
                <option value="{{ genre }}">{{ genre }}</option>
            {% endfor %}
        </select>
        <input type="submit" value="Recommend">
    </form>
</body>
</html>
'''

RECOMMEND_TEMPLATE = '''
<!doctype html>
<html>
<head>
    <title>Recommendations for {{ genre }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f6f8;
            padding: 40px;
            text-align: center;
        }
        h1 {
            color: #333;
        }
        ul {
            list-style-type: none;
            padding: 0;
            margin: 30px auto;
            width: 50%;
            text-align: left;
        }
        li {
            background: white;
            margin: 10px 0;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.1);
            font-size: 18px;
        }
        a {
            text-decoration: none;
            color: #1976d2;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>Top Anime for Genre: {{ genre }}</h1>
    <ul>
        {% for rec in recommendations %}
            <li>{{ rec.name }} <strong>— Rating:</strong> {{ rec.rating }}</li>
        {% endfor %}
    </ul>
    <a href="/">← Back to Genres</a>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501)
