import requests
import time
from datetime import datetime, timedelta
from plyer import notification
import tkinter as tk
from PIL import Image, ImageTk

# Kullanıcı şehir ve ülke bilgisi
sehir = "Istanbul"
ulke = "Turkey"

# Uyarı süreleri (dakika)
uyari_5dk = 5
uyari_30dk = 30

# Cami resmi dosyası
cami_dosyasi = "cami.jpeg"  # projenin bulunduğu klasöre koy

def vakitleri_al():
    url = f"http://api.aladhan.com/v1/timingsByCity?city={sehir}&country={ulke}"
    response = requests.get(url)
    data = response.json()
    return data["data"]["timings"]

def zaman_str_to_datetime(zaman_str):
    return datetime.strptime(zaman_str, "%H:%M").replace(
        year=datetime.now().year,
        month=datetime.now().month,
        day=datetime.now().day
    )

def ezan_popup(vakit_adi, mesaj):
    window = tk.Tk()
    window.title("Ezan Uyarısı ⏰")
    window.geometry("350x400")

    # Cami görseli
    img = Image.open(cami_dosyasi)
    img = img.resize((300, 300))
    photo = ImageTk.PhotoImage(img)

    label_img = tk.Label(window, image=photo)
    label_img.image = photo
    label_img.pack()

    label_text = tk.Label(window, text=mesaj, font=("Arial", 18), fg="red", wraplength=300, justify="center")
    label_text.pack(pady=10)

    window.mainloop()

# Gönderilen uyarıları takip et
gonderilenler = []
vakitler = vakitleri_al()
son_guncelleme = datetime.now()

print("Ezan uygulaması çalışıyor 🔥")

while True:
    simdi = datetime.now()

    # 12 saatte bir vakitleri güncelle
    if (simdi - son_guncelleme).seconds > 60*60*12:
        vakitler = vakitleri_al()
        gonderilenler = []
        son_guncelleme = simdi
        print("Vakitler güncellendi 🔄")

    for vakit, saat_str in vakitler.items():
        vakit_time = zaman_str_to_datetime(saat_str)

        # 30dk öncesi uyarı
        fark_30 = vakit_time - timedelta(minutes=uyari_30dk)
        if fark_30 <= simdi < fark_30 + timedelta(seconds=15) and (vakit+"_30") not in gonderilenler:
            ezan_popup(vakit, mesaj=f"{vakit} vakti çıkmak üzere! Hemen namazını kıl!")
            notification.notify(
                title="Namaz Vakti Yaklaşıyor ⏰",
                message=f"{vakit} vakti çıkmak üzere! Hemen namazını kıl!",
                timeout=10
            )
            gonderilenler.append(vakit+"_30")

        # 5dk öncesi uyarı
        fark_5 = vakit_time - timedelta(minutes=uyari_5dk)
        if fark_5 <= simdi < fark_5 + timedelta(seconds=15) and (vakit+"_5") not in gonderilenler:
            ezan_popup(vakit, mesaj=f"{vakit} ezanına 5 dakika kaldı!")
            notification.notify(
                title="Ezan Vakti Yaklaşıyor ⏰",
                message=f"{vakit} ezanına 5 dakika kaldı!",
                timeout=10
            )
            gonderilenler.append(vakit+"_5")

    time.sleep(10)