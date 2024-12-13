from flask import Flask, render_template, request, jsonify
from weather_data_retrieval import fetch_weather_data, parse_json, database_connection,save_to_database

app = Flask(__name__)

# Define the home route
# Home route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.json.get('city')
    print(f'The provided city is {city}')
    country = request.json.get('country', 'US')
    state = request.json.get('state', None)
    units = request.json.get('units', 'metric')

    weather_data = fetch_weather_data(city, country, state, units)

    try:
        # Parse the JSON response into a DataFrame
        parsed_data = parse_json(weather_data)

        # Render the DataFrame as HTML
        return render_template('weather.html', table=parsed_data.to_html(classes='table table-striped', index=False))
    except Exception as e:
        print(f"Error rendering the table: {e}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)

