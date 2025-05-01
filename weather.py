import requests
import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class WeatherApp:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"  # Changed to https
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"  # Changed to https
        
    def get_weather(self, city_name, units='metric'):
        """Get current weather data for a city"""
        try:
            params = {
                'q': city_name,
                'appid': self.api_key,
                'units': units
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    def get_forecast(self, city_name, units='metric'):
        """Get 5-day weather forecast for a city"""
        try:
            params = {
                'q': city_name,
                'appid': self.api_key,
                'units': units
            }
            response = requests.get(self.forecast_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast data: {e}")
            return None
    
    def display_weather_cli(self, weather_data):
        """Display weather data in command line interface"""
        if not weather_data or 'cod' not in weather_data or weather_data['cod'] != 200:
            print("Error: Unable to retrieve weather data.")
            if weather_data and 'message' in weather_data:
                print(f"Reason: {weather_data['message']}")
            return
        
        print("\nCurrent Weather Conditions:")
        print("--------------------------")
        print(f"City: {weather_data['name']}, {weather_data['sys']['country']}")
        print(f"Temperature: {weather_data['main']['temp']}°C")
        print(f"Feels Like: {weather_data['main']['feels_like']}°C")
        print(f"Weather: {weather_data['weather'][0]['description'].capitalize()}")
        print(f"Humidity: {weather_data['main']['humidity']}%")
        print(f"Wind Speed: {weather_data['wind']['speed']} m/s")
        print(f"Pressure: {weather_data['main']['pressure']} hPa")
        print(f"Visibility: {weather_data.get('visibility', 'N/A')} meters")
        
        sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M:%S')
        sunset = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M:%S')
        print(f"Sunrise: {sunrise}")
        print(f"Sunset: {sunset}")
    
    def display_forecast_cli(self, forecast_data):
        """Display 5-day forecast in command line interface"""
        if not forecast_data or 'cod' not in forecast_data or forecast_data['cod'] != '200':
            print("Error: Unable to retrieve forecast data.")
            if forecast_data and 'message' in forecast_data:
                print(f"Reason: {forecast_data['message']}")
            return
        
        print("\n5-Day Weather Forecast:")
        print("-----------------------")
        city = forecast_data['city']['name']
        country = forecast_data['city']['country']
        print(f"Location: {city}, {country}\n")
        
        # Group forecasts by day
        daily_forecasts = {}
        for forecast in forecast_data['list']:
            date = datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d')
            if date not in daily_forecasts:
                daily_forecasts[date] = []
            daily_forecasts[date].append(forecast)
        
        # Display forecast for each day
        for date, forecasts in daily_forecasts.items():
            print(f"Date: {date}")
            for forecast in forecasts:
                time = datetime.fromtimestamp(forecast['dt']).strftime('%H:%M')
                temp = forecast['main']['temp']
                desc = forecast['weather'][0]['description'].capitalize()
                print(f"  {time}: {temp}°C, {desc}")
            print()

class WeatherAppGUI:
    """Simple GUI for the weather application"""
    def __init__(self, root, weather_app):
        self.root = root
        self.weather_app = weather_app
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("Weather Application")
        self.root.geometry("400x500")
        
        # City Entry
        tk.Label(self.root, text="Enter City:").pack(pady=5)
        self.city_entry = tk.Entry(self.root, width=30)
        self.city_entry.pack(pady=5)
        
        # Unit Selection
        self.unit_var = tk.StringVar(value="metric")
        tk.Label(self.root, text="Select Unit:").pack(pady=5)
        tk.Radiobutton(self.root, text="Celsius", variable=self.unit_var, value="metric").pack()
        tk.Radiobutton(self.root, text="Fahrenheit", variable=self.unit_var, value="imperial").pack()
        
        # Buttons
        tk.Button(self.root, text="Get Current Weather", command=self.get_current_weather).pack(pady=10)
        tk.Button(self.root, text="Get 5-Day Forecast", command=self.get_forecast).pack(pady=10)
        
        # Weather Display
        self.weather_display = tk.Text(self.root, height=15, width=50, state='disabled')
        self.weather_display.pack(pady=10)
        
    def get_current_weather(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return
        
        weather_data = self.weather_app.get_weather(city, self.unit_var.get())
        self.display_weather(weather_data)
    
    def get_forecast(self):
        city = self.city_entry.get()
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return
        
        forecast_data = self.weather_app.get_forecast(city, self.unit_var.get())
        self.display_forecast(forecast_data)
    
    def display_weather(self, weather_data):
        self.weather_display.config(state='normal')
        self.weather_display.delete(1.0, tk.END)
        
        if not weather_data or 'cod' not in weather_data or weather_data['cod'] != 200:
            error_msg = "Error: Unable to retrieve weather data."
            if weather_data and 'message' in weather_data:
                error_msg += f"\nReason: {weather_data['message']}"
            self.weather_display.insert(tk.END, error_msg)
            self.weather_display.config(state='disabled')
            return
        
        unit_symbol = '°C' if self.unit_var.get() == 'metric' else '°F'
        wind_unit = 'm/s' if self.unit_var.get() == 'metric' else 'mph'
        
        self.weather_display.insert(tk.END, "Current Weather Conditions:\n")
        self.weather_display.insert(tk.END, "--------------------------\n")
        self.weather_display.insert(tk.END, f"City: {weather_data['name']}, {weather_data['sys']['country']}\n")
        self.weather_display.insert(tk.END, f"Temperature: {weather_data['main']['temp']}{unit_symbol}\n")
        self.weather_display.insert(tk.END, f"Feels Like: {weather_data['main']['feels_like']}{unit_symbol}\n")
        self.weather_display.insert(tk.END, f"Weather: {weather_data['weather'][0]['description'].capitalize()}\n")
        self.weather_display.insert(tk.END, f"Humidity: {weather_data['main']['humidity']}%\n")
        self.weather_display.insert(tk.END, f"Wind Speed: {weather_data['wind']['speed']} {wind_unit}\n")
        self.weather_display.insert(tk.END, f"Pressure: {weather_data['main']['pressure']} hPa\n")
        
        sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M:%S')
        sunset = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M:%S')
        self.weather_display.insert(tk.END, f"Sunrise: {sunrise}\n")
        self.weather_display.insert(tk.END, f"Sunset: {sunset}\n")
        
        self.weather_display.config(state='disabled')
    
    def display_forecast(self, forecast_data):
        self.weather_display.config(state='normal')
        self.weather_display.delete(1.0, tk.END)
        
        if not forecast_data or 'cod' not in forecast_data or forecast_data['cod'] != '200':
            error_msg = "Error: Unable to retrieve forecast data."
            if forecast_data and 'message' in forecast_data:
                error_msg += f"\nReason: {forecast_data['message']}"
            self.weather_display.insert(tk.END, error_msg)
            self.weather_display.config(state='disabled')
            return
        
        unit_symbol = '°C' if self.unit_var.get() == 'metric' else '°F'
        city = forecast_data['city']['name']
        country = forecast_data['city']['country']
        
        self.weather_display.insert(tk.END, f"5-Day Forecast for {city}, {country}:\n")
        self.weather_display.insert(tk.END, "--------------------------------\n\n")
        
        # Group forecasts by day
        daily_forecasts = {}
        for forecast in forecast_data['list']:
            date = datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d')
            if date not in daily_forecasts:
                daily_forecasts[date] = []
            daily_forecasts[date].append(forecast)
        
        # Display forecast for each day
        for date, forecasts in daily_forecasts.items():
            self.weather_display.insert(tk.END, f"Date: {date}\n")
            for forecast in forecasts:
                time = datetime.fromtimestamp(forecast['dt']).strftime('%H:%M')
                temp = forecast['main']['temp']
                desc = forecast['weather'][0]['description'].capitalize()
                self.weather_display.insert(tk.END, f"  {time}: {temp}{unit_symbol}, {desc}\n")
            self.weather_display.insert(tk.END, "\n")
        
        self.weather_display.config(state='disabled')

def main():
    # Your actual API key
    API_KEY = "b1bbbdf137ec25246487088a24f3132d"
    
    weather_app = WeatherApp(API_KEY)
    
    # Choose interface mode
    print("Choose interface mode:")
    print("1. Command Line Interface")
    print("2. Graphical User Interface")
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == '1':
        # Command Line Interface
        while True:
            city = input("\nEnter city name (or 'quit' to exit): ")
            if city.lower() == 'quit':
                break
            
            print("\nChoose data to display:")
            print("1. Current Weather")
            print("2. 5-Day Forecast")
            print("3. Both")
            data_choice = input("Enter your choice (1-3): ")
            
            units = input("Choose units (metric for Celsius, imperial for Fahrenheit): ").lower()
            if units not in ['metric', 'imperial']:
                units = 'metric'
            
            if data_choice in ['1', '3']:
                weather_data = weather_app.get_weather(city, units)
                weather_app.display_weather_cli(weather_data)
            
            if data_choice in ['2', '3']:
                forecast_data = weather_app.get_forecast(city, units)
                weather_app.display_forecast_cli(forecast_data)
    elif choice == '2':
        # Graphical User Interface
        root = tk.Tk()
        app_gui = WeatherAppGUI(root, weather_app)
        root.mainloop()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()