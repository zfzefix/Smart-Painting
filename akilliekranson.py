
import tkinter as tk
from tkinter import ttk
import time
from PIL import Image, ImageTk
import RPi.GPIO as GPIO
import cv2
import requests
from forex_python.converter import CurrencyRates

class AkilliAynaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Akıllı Ayna")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')

        self.resim_ekrani = tk.Label(root, bg='black')
        self.resim_ekrani.pack(expand='true')

        self.arayuz_ekrani = tk.Label(root, font=('Helvetica', 25, 'bold'), bg='black', fg='white')
        self.arayuz_ekrani.pack(expand='true')
        self.arayuz_ekrani.pack_forget()

        self.PIR = 23
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIR, GPIO.IN)

        self.resim_gorunur_sure = 5000  # Resmin görünür kalacağı süre (5 saniye)
        self.ara_sure = 5  # Hareket algılandıktan sonra tekrar resim ekranına geçiş süresi (5 saniye)
        self.kontrol_hareket_algila()

        root.bind('<KeyPress-k>', self.cikis)
        root.bind('<KeyPress-f>', self.foto_cek)  # 'f' tuşu ile fotoğraf çekme işlemi

    def kontrol_hareket_algila(self):
        if self.hareket_algilama():
            print("Hareket Algılandı!")
            self.goster_arayuz_ekrani()
        else:
            self.gizle_arayuz_ekrani()

        self.root.after(500, self.kontrol_hareket_algila)

    def hareket_algilama(self):
        return GPIO.input(self.PIR) == 1

    def goster_arayuz_ekrani(self):
        self.resim_goster_timer = time.time() + self.resim_gorunur_sure
        self.resim_ekrani.pack_forget()
        self.arayuz_ekrani.pack(expand='true')
        self.root.after(self.ara_sure * 5000, self.gizle_arayuz_ekrani)  # Belirlenen süre sonra resim ekranına geçiş

    def gizle_arayuz_ekrani(self):
        if hasattr(self, 'resim_goster_timer') and time.time() < self.resim_goster_timer:
            # Eğer resim gösterme süresi dolmamışsa beklemeye devam et
            return

        self.arayuz_ekrani.pack_forget()
        self.tanimla_resim_ekrani()

    def tanimla_resim_ekrani(self):
        img = Image.open("/home/akillitablo/Downloads/dogs.jpg")
        img = img.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        self.resim_ekrani.configure(image=img)
        self.resim_ekrani.image = img
        self.resim_ekrani.pack(expand='true')

    def cikis(self, event):
        GPIO.cleanup()
        self.root.destroy()

    def foto_cek(self, event):
        # Web kameradan fotoğraf çekme
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        # Çekilen fotoğrafı ekranda gösterme
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)

        self.resim_ekrani.configure(image=img)
        self.resim_ekrani.image = img
        self.resim_ekrani.pack(expand='true')

        # 3 saniye sonra fotoğrafı gizleme
        self.root.after(3000, lambda: self.tanimla_resim_ekrani())

class ArayuzEkranGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Arayüz Ekranı")
        self.root.geometry("800x480")

        self.tarih_ve_saat_etiketi = tk.Label(root, font=('Arial', 40, 'bold'), background='black', foreground='turquoise')
        self.tarih_ve_saat_etiketi.pack(side='top', anchor='ne', padx=20, pady=20)

        self.hava_durumu_etiketi = tk.Label(root, font=('Arial', 20), background='black', foreground='white')
        self.hava_durumu_etiketi.pack(side='top', pady=10, anchor='ne')

        self.kur_bilgisi_etiketi = tk.Label(root, font=('Arial', 20), background='black', foreground='white')
        self.kur_bilgisi_etiketi.pack(side='bottom', pady=20, anchor='center')

        self.hos_geldiniz_etiketi = tk.Label(root, text='Hoş Geldin, dostum', font=('Arial', 40, 'bold'), background='black', foreground='turquoise')
        self.hos_geldiniz_etiketi.place(relx=0.5, rely=0.2, anchor='center')

        root.bind('<KeyPress-x>', self.cikis)
        self.tarih_saat_guncelle()
        self.root.after(1000, self.tarih_saat_guncelle)
        self.guncelle_kur_bilgisi()
        self.guncelle_hava_durumu()  

    def tarih_saat_guncelle(self):
        an = time.localtime()
        saat = time.strftime('%H:%M:%S', an)
        tarih = time.strftime('%Y-%m-%d', an)
        self.tarih_ve_saat_etiketi.config(text=f'{tarih}\n{saat}')
        self.root.after(1000, self.tarih_saat_guncelle)

    def guncelle_kur_bilgisi(self):
        try:
            kur_cinsleri = ["USD", "EUR", "GBP"]
            c = CurrencyRates()
            kur_bilgisi = "   ".join([f"{kur}: {c.get_rate(kur, 'TRY'):.2f}" for kur in kur_cinsleri])
            self.kur_bilgisi_etiketi.config(text=kur_bilgisi)
        except Exception as e:
            print(f"Hata: {e}")

        self.root.after(3600000, self.guncelle_kur_bilgisi)

    def guncelle_hava_durumu(self):
        try:
            api_key = "e6e2385fa18f68e37d2c6694f9b28803"
            city = "CITY"  
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()

            if data["cod"] != "404":
                hava_durumu = f"{data['weather'][0]['description'].capitalize()}, {data['main']['temp']}°C"
                self.hava_durumu_etiketi.config(text=hava_durumu)
        except Exception as e:
            print(f"Hava durumu bilgisi alınırken bir hata oluştu: {e}")

        self.root.after(600000, self.guncelle_hava_durumu)  

    def cikis(self, event):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AkilliAynaGUI(root)
    app.tanimla_resim_ekrani()

    arayuz_ekran = ArayuzEkranGUI(root)
    root.mainloop()

