import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import requests
import os
from dotenv import load_dotenv, dotenv_values




def getWeatherData(cityName):
    if cityName != "":
        load_dotenv()
        apiKey = os.getenv("apiKey") #Get the api key
        url = f"https://api.openweathermap.org/data/2.5/weather?q={cityName}&appid={apiKey}"
        response = requests.get(url)
        weatherData = response.json()

        if response.status_code == 200:
            print("Data has been retrieved")
            weatherInfo = {
                "temp": weatherData["main"]["temp"] -273.15, #Convert Kelvin into °Celsius
                "lon": weatherData["coord"]["lon"],
                "lat": weatherData["coord"]["lat"],
                "icon": str(weatherData["weather"][0]["icon"][:2]),
                "description": weatherData["weather"][0]["description"],
                "sunrise": weatherData["sys"]["sunrise"],
                "sunset": weatherData["sys"]["sunset"],
                "datetime": weatherData["dt"] #time in the selected city
            }
            return weatherInfo
        elif response.status_code == 404:
            print(f"Data could not be retrieved: {response.status_code}")
            return "404"
        else:
            print(f"Data could not be retrieved: {response.status_code}")
            return ""

def findEmojiToWeather(iconCode, sunset, sunrise, datetime):
    isDay = True
    if datetime >= sunrise and datetime <= sunset:
        isDay = True
    else:
        isDay = False
    
    weatherEmojis = {
        "day": {
            "01": "☀️",
            "02": "🌤️",
            "03": "⛅",
            "04": "🌥️",
            "09": "🌧️☀️",
            "10": "🌦️",
            "11": "🌩️☀️",
            "13": "🌨️☀️",
            "50": "🌫️☀️",
        },
        "night": {
            "01": "🌙",
            "02": "☁️🌙",
            "03": "☁️🌙",
            "04": "☁️🌙",
            "09": "🌧️🌙",
            "10": "🌧️🌙",
            "11": "🌩️🌙",
            "13": "🌨️🌙",
            "50": "🌫️🌙",
        }
    }
    return weatherEmojis["day" if isDay else "night"][iconCode]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("City Weather App")
        self.setWindowIcon(QIcon("WeatherApp/WeatherAppIcon.png"))
        self.cityNameLineEdit = QLineEdit(self)
        self.submitButton = QPushButton("Submit", self)
        self.weatherEmojiLabel = QLabel("⛅", self)
        self.descrLabel = QLabel("Description", self)
        self.tempLabel = QLabel("Temp: NAN", self)
        self.lonlatLabel = QLabel("Lon: NAN; Lat: NAN", self)
        self.initUI()


    def initUI(self):
        self.setGeometry(700, 250, 500, 600)

        vBox = QVBoxLayout()
        hBox = QHBoxLayout()

        self.cityNameLineEdit.setStyleSheet("font-family: Arial; font-size: 25px;")
        self.cityNameLineEdit.setPlaceholderText("Enter a city name")
        self.submitButton.setStyleSheet("font-family: Arial; font-size: 25px;")
        self.submitButton.clicked.connect(self.onClick)
        self.weatherEmojiLabel.setStyleSheet("font-family: Arial; font-size: 90px;")
        self.descrLabel.setStyleSheet("font-family: Arial; font-size: 25px; background-color: #c9c9c9; border: 2px dashed #595959; border-radius: 15px")
        self.tempLabel.setStyleSheet("font-family: Arial; font-size: 25px; background-color: #c9c9c9; border: 2px dashed #595959; border-radius: 15px")
        self.lonlatLabel.setStyleSheet("font-family: Arial; font-size: 25px; background-color: #c9c9c9; border: 2px dashed #595959; border-radius: 15px")
        self.weatherEmojiLabel.setAlignment(Qt.AlignCenter)
        self.descrLabel.setAlignment(Qt.AlignCenter)
        self.tempLabel.setAlignment(Qt.AlignCenter)
        self.lonlatLabel.setAlignment(Qt.AlignCenter)
        hBox.addWidget(self.cityNameLineEdit)
        hBox.addWidget(self.submitButton)
        vBox.addLayout(hBox) #Make cityNameLineEdit and submitButton in one line
        vBox.addWidget(self.weatherEmojiLabel)
        vBox.addWidget(self.descrLabel)
        vBox.addWidget(self.tempLabel)
        vBox.addWidget(self.lonlatLabel)

        centralWidget = QWidget()
        centralWidget.setLayout(vBox)
        self.setCentralWidget(centralWidget)

    def onClick(self):
        self.button = QPushButton
        cityName = self.cityNameLineEdit.text()
        weatherInfo = getWeatherData(cityName)
        if weatherInfo != "404" or weatherInfo != "":
            self.weatherEmojiLabel.setText(findEmojiToWeather(weatherInfo["icon"], weatherInfo["sunset"], weatherInfo["sunrise"], weatherInfo["datetime"]))
            self.descrLabel.setText(weatherInfo["description"])
            self.tempLabel.setText(f"Temp: {round(weatherInfo['temp'], 2)}°C")
            self.lonlatLabel.setText(f"Lon: {weatherInfo['lon']}; Lat: {weatherInfo['lat']}")
        elif weatherInfo == "404":
            self.cityNameLineEdit.setText("No city found!")
        else:
            print("Corresponding Emoji to weather can not be found because no weather info exists")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()