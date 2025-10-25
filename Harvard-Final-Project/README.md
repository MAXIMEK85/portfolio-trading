<<<<<<< HEAD
Stock Trend Analyzer (MA50 / MA200)

Description
This project is a Python-based tool that analyzes stock price trends using the 50-week and 200-week moving averages (MA50 and MA200). The goal is to help investors quickly understand whether a stock is in a short-term or long-term bullish or bearish trend.

The program automatically fetches real historical stock data from Yahoo Finance using the yfinance library. It then computes both short-term and long-term moving averages with pandas, and compares them to the latest stock price. If the price is above the moving average, it suggests a bullish trend; if it is below, it suggests a bearish trend. A visual representation is generated using matplotlib, showing the price evolution with its MA50 and MA200 curves.

This project was designed as part of CS50’s Introduction to Programming with Python. It combines concepts of data analysis, API usage, and data visualization. It also demonstrates the ability to structure a Python project with multiple functions and corresponding unit tests.

Features
Fetches historical stock data automatically using yfinance
Calculates 50-week and 200-week moving averages using pandas
Identifies bullish or bearish trends for both timeframes
Displays results in the terminal and saves a plot using matplotlib
Includes pytest tests for each function to ensure code reliability
Files
project.py: Main Python script containing the following functions:
main()
get_stock_data()
calculate_ma()
determine_trends()
plot_trends()
test_project.py: Unit tests for all major functions
requirements.txt: List of dependencies
pandas
matplotlib
yfinance
pytest
How It Works
The user inputs a stock ticker (e.g., AAPL or MSFT)
The program downloads 5 years of weekly stock data
It computes the 50-week and 200-week moving averages
It checks whether the price is above or below these averages
It prints the trend results in the terminal and saves a PNG chart
Example Output
=======
# share_price

Ce projet permet de télécharger et d'afficher le prix de l'action Apple (AAPL) sur une période donnée à l'aide de Python, yfinance et matplotlib.

## Prérequis
- Python 3.x
- yfinance
- matplotlib

## Installation des dépendances

```bash
pip install yfinance matplotlib
```

## Utilisation

```bash
python share_price.py
```

## Auteur
Votre nom ici
# portfolio-trading
Bienvenue dans mon portfolio trading, je souhaite écrire du code pour pouvoir automatiser mon trading 😊🚀
>>>>>>> c7fa9d7 (Add Harvard project files and RSI-Calculator)
