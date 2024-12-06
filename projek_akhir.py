from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
import requests

class WeatherApp(App):
    def build(self):
        # Root layout
        root = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # Background color
        with root.canvas.before:
            Color(0.2, 0.4, 0.8, 1)  # Blue gradient
            self.rect = Rectangle(size=root.size, pos=root.pos)
            root.bind(size=self.update_rect, pos=self.update_rect)

        # Title label
        title_label = Label(
            text="[b][size=30][color=ffffff]Aplikasi Pemantau Cuaca[/color][/size][/b]",
            markup=True,
            size_hint=(1, 0.1),
            halign="center",
            valign="middle",
        )
        root.add_widget(title_label)

        # City input with centered size
        self.city_input = TextInput(
            hint_text="Masukkan nama kota...",
            font_size=18,
            size_hint=(0.8, 0.1),
            background_color=(0, 0, 0, 1),
            foreground_color=(1, 1, 1, 1),
            multiline=False,
            pos_hint={'center_x': 0.5},
        )
        root.add_widget(self.city_input)

        # Check weather button
        self.check_button = Button(
            text="Cek Cuaca",
            font_size=20,
            size_hint=(0.8, 0.1),
            background_color=(0, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5},
        )
        self.check_button.bind(on_press=self.get_weather)
        root.add_widget(self.check_button)

        # Layout for weather results
        self.result_layout = GridLayout(cols=2, size_hint_y=None, padding=10, spacing=10)
        self.result_layout.bind(minimum_height=self.result_layout.setter('height'))
        root.add_widget(self.result_layout)

        return root

    def update_rect(self, *args):
        self.rect.size = self.root.size
        self.rect.pos = self.root.pos

    def create_label(self, text, bold=False, color="ffffff", **kwargs):
        """Helper function to create labels with consistent styling."""
        return Label(
            text=f"[color={color}]{'[b]' if bold else ''}{text}{'[/b]' if bold else ''}[/color]",
            markup=True,
            size_hint_y=None,
            halign="left",
            valign="middle",
            **kwargs,
        )

    def get_weather(self, instance):
        self.result_layout.clear_widgets()  # Clear previous results
        city = self.city_input.text.strip()
        if not city:
            self.result_layout.add_widget(
                self.create_label("Masukkan nama kota terlebih dahulu!", bold=True, color="ff3333", size_hint=(1, None))
            )
            return

        api_key = "5fcecfa19065b9593b87735917c5c2ea"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=id"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == "404":
                self.result_layout.add_widget(
                    self.create_label("Kota tidak ditemukan!", bold=True, color="ff3333", size_hint=(1, None))
                )
            else:
                # Display weather results
                weather_data = {
                    "Cuaca": data["weather"][0]["description"].capitalize(),
                    "Suhu": f"{data['main']['temp']}°C",
                    "Kelembapan": f"{data['main']['humidity']}%",
                }
                for key, value in weather_data.items():
                    self.result_layout.add_widget(self.create_label(key, font_size=18, height=40))
                    self.result_layout.add_widget(self.create_label(value, font_size=18, height=40))

        except requests.RequestException as e:
            self.result_layout.add_widget(
                self.create_label(f"Terjadi kesalahan koneksi: {e}", bold=True, color="ff3333", size_hint=(1, None))
            )

# Run the application
if _name_ == "_main_":
    WeatherApp().run()
