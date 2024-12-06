from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
import requests

class WeatherApp(App):
    def build(self):
        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Input untuk nama kota
        self.city_input = TextInput(hint_text="Masukkan nama kota", font_size=20, size_hint=(1, 0.2))
        self.layout.add_widget(self.city_input)

        # Tombol untuk cek cuaca
        self.check_button = Button(text="Cek Cuaca", font_size=20, size_hint=(1, 0.2))
        self.check_button.bind(on_press=self.get_weather)
        self.layout.add_widget(self.check_button)

        # Label untuk menampilkan hasil
        self.result_label = Label(text="", font_size=18, size_hint=(1, 0.6))
        self.layout.add_widget(self.result_label)

        return self.layout

    def get_weather(self, instance):
        city = self.city_input.text
        if not city:
            self.result_label.text = "Masukkan nama kota terlebih dahulu!"
            return

        api_key = "5fcecfa19065b9593b87735917c5c2ea"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            data = response.json()

            if data["cod"] == "404":
                self.result_label.text = "Kota tidak ditemukan!"
            else:
                temp = data["main"]["temp"]
                weather = data["weather"][0]["description"]
                humidity = data["main"]["humidity"]

                self.result_label.text = f"Cuaca: {weather}\nSuhu: {temp}°C\nKelembapan: {humidity}%"
        except Exception as e:
            self.result_label.text = f"Terjadi kesalahan: {e}"

# Jalankan aplikasi
if __name__ == "__main__":
    WeatherApp().run()
