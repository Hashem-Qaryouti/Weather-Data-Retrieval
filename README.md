# :memo:Project Description
The main purpose of this project is to develop a Python program that interacts with a weather API to retrieve weather data for a specific city and store it in SQLite3 Database. A simple web interface is also developed for visualize the process.

# ⬇️ How to Run
to get started, follow these simple steps:
### Firstly, you should have Docker installed and pre-configured on your local machine
1. Clone the project repository to your local machine
2. Open a terminal and run the following two commands:
``` bash
docker build -t flask-app .
docker run -d -p 5000:5000 flask-app
```
3. Open your browser, and then type the following URL:
   http://127.0.0.1:5000/

# 📖:Usage
1. The city parameter is required (an example is : portland)
2. If the country is not provided, by default US
3. If the units parameter is not provided, by default metric

