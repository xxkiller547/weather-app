#=========================================================
import requests
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label,Button
from textual.containers import Vertical
#=========================================================
API = "https://wttr.in"
params = {"format": "j1"}
#=========================================================
class WeatherApp(App):
    CSS_PATH = "style.tcss"
    BINDINGS = [("q", "quit", "Quit")]
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="main"):
            yield Label("Weather App", id="title")
            with Vertical(id="weather"):
                yield Label("Please click the button to view weather information in Celsius", id="weather_celsius")
                yield Label("Please click the button to view weather information in Fahrenheit", id="weather_fahrenheit")
                yield Label("description: refresh to update", id="weather_description")
                yield Label("Note: The weather information is fetched from wttr.in", id="note")
                yield Button("Refresh", id="refresh")
        yield Footer()
    def refresh_weather(self) -> None:
        try:
            response = requests.get(API, params=params)
            if response.status_code != 200:
                self.query_one("#weather_celsius", Label).update("Error fetching weather data")
                self.query_one("#weather_fahrenheit", Label).update("Error fetching weather data")
                self.query_one("#weather_description", Label).update("Error fetching weather data")
            else:
                data = response.json()
                current_condition = data["current_condition"][0]
                temp_c = current_condition["temp_C"]
                temp_f = current_condition["temp_F"]
                description = current_condition["weatherDesc"][0]["value"]
                self.query_one("#weather_celsius", Label).update(f"Current Temperature: {temp_c}°C")
                self.query_one("#weather_fahrenheit", Label).update(f"Current Temperature: {temp_f}°F")
                self.query_one("#weather_description", Label).update(f"Description: {description}")
        except Exception as e:
            self.query_one("#weather_celsius", Label).update(f"Error: {str(e)}")
            self.query_one("#weather_fahrenheit", Label).update(f"Error: {str(e)}")
            self.query_one("#weather_description", Label).update(f"Error: {str(e)}")
            

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "refresh":
            self.refresh_weather()
    pass
#=========================================================
if __name__ == "__main__":
    app = WeatherApp()
    app.run()
