Struktur Aplikasi
Kode ini adalah aplikasi GUI untuk menampilkan informasi cuaca real-time. Data cuaca diperoleh melalui API OpenWeatherMap dan ditampilkan menggunakan komponen antarmuka Kivy. 

---

Penjelasan Komponen Kode
1. Import Library
```python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
import requests
```
- Kivy Modules:
  - **`App`**: Untuk membuat aplikasi berbasis Kivy.
  - **`BoxLayout`, `GridLayout`**: Layout untuk mengatur tata letak vertikal atau tabel.
  - **`TextInput`, `Button`, `Label`**: Komponen UI dasar.
  - **`Color`, `Rectangle`**: Untuk menambahkan warna atau grafik ke elemen UI.
- **Requests**: Library HTTP untuk mengambil data cuaca dari API OpenWeatherMap.

---

2. Kelas Utama: `WeatherApp`
Subclass `App`, berfungsi sebagai container utama aplikasi Kivy. Metode `build()` menginisialisasi antarmuka aplikasi.

---
3. Struktur Layout
```python
root = BoxLayout(orientation="vertical", padding=20, spacing=15)
```
- Menggunakan **BoxLayout** untuk menata elemen secara vertikal dengan jarak antar elemen.
- **`padding`**: Memberikan ruang di sekitar layout.
- **`spacing`**: Memberikan jarak antar elemen dalam layout.

---

4. Background dan Warna
```python
with root.canvas.before:
    Color(0.2, 0.4, 0.8, 1)
    self.rect = Rectangle(size=root.size, pos=root.pos)
    root.bind(size=self.update_rect, pos=self.update_rect)
```
- **`canvas.before`**: Layer di belakang elemen UI.
- **`Color`**: Menentukan warna latar (biru gradien dalam hal ini).
- **`Rectangle`**: Membuat kotak sebagai latar belakang.
- **`update_rect`**: Memastikan ukuran latar belakang mengikuti perubahan ukuran aplikasi.

---

5. Komponen UI
1. Label Judul
   ```python
   title_label = Label(
       text="[b][size=30][color=ffffff]Aplikasi Pemantau Cuaca[/color][/size][/b]",
       markup=True,
       ...
   )
   ```
   - Digunakan **markup** untuk format teks yang dinamis, seperti warna dan ukuran.

2. Input Kota
   ```python
   self.city_input = TextInput(
       hint_text="Masukkan nama kota...",
       ...
   )
   ```
   - **TextInput** untuk memasukkan nama kota.
   - **`pos_hint`** mengatur posisi horizontal elemen agar berada di tengah.

3. Tombol Cek Cuaca
   ```python
   self.check_button = Button(
       text="Cek Cuaca",
       ...
   )
   ```
   - Ketika tombol ditekan, fungsi **`get_weather`** dipanggil.

4. GridLayout Hasil
   ```python
   self.result_layout = GridLayout(cols=2, ...)
   ```
   - **`cols=2`**: Layout dengan dua kolom untuk menampilkan data hasil.

---

6. Fungsi `get_weather`
Fungsi ini bertugas mengambil data cuaca dari API, memprosesnya, dan menampilkan hasilnya di antarmuka.

1. Membersihkan Hasil Sebelumnya
   ```python
   self.result_layout.clear_widgets()
   ```

2. Validasi Input
   ```python
   if not city:
       self.result_layout.add_widget(
           self.create_label("Masukkan nama kota terlebih dahulu!", bold=True, color="ff3333", size_hint=(1, None))
       )
       return
   ```
   - Jika input kosong, ditampilkan pesan error menggunakan helper function `create_label`.

3. Mengambil Data Cuaca
   ```python
   api_key = "5fcecfa19065b9593b87735917c5c2ea"
   url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=id"
   response = requests.get(url)
   response.raise_for_status()
   data = response.json()
   ```
   - **API Endpoint**: URL untuk mengambil data cuaca dari OpenWeatherMap.
   - **Parameter API**:
     - `q`: Nama kota.
     - `appid`: API key untuk autentikasi.
     - `units=metric`: Menampilkan suhu dalam derajat Celsius.
     - `lang=id`: Menampilkan deskripsi cuaca dalam bahasa Indonesia.

4. Menampilkan Hasil
   ```python
   if data["cod"] == "404":
       self.result_layout.add_widget(
           self.create_label("Kota tidak ditemukan!", bold=True, color="ff3333", size_hint=(1, None))
       )
   else:
       weather_data = {
           "Cuaca": data["weather"][0]["description"].capitalize(),
           "Suhu": f"{data['main']['temp']}°C",
           "Kelembapan": f"{data['main']['humidity']}%",
       }
       for key, value in weather_data.items():
           self.result_layout.add_widget(self.create_label(key, font_size=18, height=40))
           self.result_layout.add_widget(self.create_label(value, font_size=18, height=40))
   ```
   - Jika data ditemukan, ditampilkan deskripsi cuaca, suhu, dan kelembapan dalam layout.

5. Error Handling
   ```python
   except requests.RequestException as e:
       self.result_layout.add_widget(
           self.create_label(f"Terjadi kesalahan koneksi: {e}", bold=True, color="ff3333", size_hint=(1, None))
       )
   ```
   - Menangani kesalahan koneksi atau kegagalan API.

---
7. Helper Function: `create_label`
```python
def create_label(self, text, bold=False, color="ffffff", **kwargs):
    return Label(
        text=f"[color={color}]{'[b]' if bold else ''}{text}{'[/b]' if bold else ''}[/color]",
        markup=True,
        size_hint_y=None,
        halign="left",
        valign="middle",
        **kwargs,
    )
```
- Digunakan untuk membuat **Label** dengan format yang konsisten.
- Parameter `bold` dan `color` memungkinkan styling teks dengan mudah.

---

8. Menjalankan Aplikasi
```python
if _name_ == "_main_":
    WeatherApp().run()
```
- `run()`: Memulai aplikasi.

---
Kode ini menyajikan antarmuka sederhana namun interaktif untuk memantau cuaca. Fitur utama mencakup:
- Validasi input.
- Tampilan data cuaca dalam format tabel.
- Penanganan error koneksi dan input tidak valid.

Aplikasi ini sangat modular dengan pemisahan fungsi untuk memastikan fleksibilitas dan kemudahan pengembangan lebih lanjut.
