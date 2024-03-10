 Akıllı Tablo
Dokuz Eylül Üniversitesi Yönetim Bilişim Sistemleri bölümünde, Bilgisayar Donanımı dersi kapsamında arkadaşım ve benim tarafımdan hazırlanan akıllı tablo projesi.
Akıllı Tablo projesinde kullandığımız teknolojiler ve yazılımlar şunlardır:

  Python: Programlama dili olarak Python kullanılmıştır. Python, projenin çeşitli bileşenlerinin geliştirilmesinde ve entegrasyonunda ana dil olarak tercih edilmiştir.

    Tkinter: Python'un standart kütüphanelerinden biri olan Tkinter, kullanıcı arayüzü (GUI) geliştirmek için kullanılmıştır. Proje içindeki arayüz bileşenleri Tkinter ile oluşturulmuştur.

    OpenCV: OpenCV (Açık Kaynak Bilgisayar Görüşü) kütüphanesi, görüntü işleme ve video analizi gibi görsel işleme görevleri için kullanılmıştır. Projede kamera aracılığıyla görüntü almak ve işlemek için OpenCV kullanılmıştır.

    PIL (Python Imaging Library): PIL, Python ile resim işleme görevlerini gerçekleştirmek için kullanılan bir kütüphanedir. Projede resimlerin işlenmesi ve gösterilmesi için PIL kullanılmıştır.

    RPi.GPIO: Raspberry Pi üzerindeki genel amaçlı giriş/çıkış (GPIO) pinlerini kontrol etmek için RPi.GPIO kütüphanesi kullanılmıştır. Projede PIR sensörü gibi donanım bileşenlerinin kontrolü için RPi.GPIO kullanılmıştır.

    requests: requests kütüphanesi, HTTP istekleri yapmak ve yanıtları işlemek için kullanılmıştır. Projede hava durumu bilgisi gibi dış kaynaklardan veri almak için requests kütüphanesi kullanılmıştır.

    Raspberry Pi 3B : Projemizin temel bileşeni olan Raspberry Pi 3B , donanım ve yazılım geliştirme platformu olarak kullanılmıştır.

        USB Klavye : Kullanıcının klavyeden giriş yaparak akıllı tabloyu kontrol etmesini sağlar.

    PIR Sensörü (Hareket Algılama): Proje için PIR (Passive Infrared Sensor) sensörü kullanılarak hareket algılama sağlandı. Bu sensör, kullanıcının varlığını algıladığında belirli bir işlemi tetikliyor

    Web Kamera - Fotoğraf Çekimi: Projede bir web kamera kullanılarak fotoğraf çekimi sağlandı. Kamera, kullanıcı istediğinde belirli bir komutla açılıp ve fotoğraf çekip fotoğrafı işleyerek ekranda gösteriyor.

    Monitor (Akıllı Tablo):   bir monitör akıllı tablo olarak kullanıldı. Bu monitör üzerinde Python ile geliştirilen bir kullanıcı arayüzü çalıştırılarak çeşitli bilgiler ve görseller gösteriliyor.

    Bu teknolojiler ve yazılımlar, Akıllı Tablo projesinin geliştirilmesinde ve işlevselliğinin sağlanmasında önemli rol oynamıştır.



    Şimdi her bir satırın ne yaptığını açıklayalım:


import tkinter as tk
from tkinter import ttk
import time
from PIL import Image, ImageTk
import RPi.GPIO as GPIO
import cv2
import requests
from forex_python.converter import CurrencyRates

Bu satırlar, kullanılacak kütüphaneleri içe aktarır.
###############################################################################################################################################################################

class AkilliAynaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Akıllı Ayna")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')

AkilliAynaGUI sınıfını tanımlar ve ana pencereyi oluşturur.

###############################################################################################################################################################################

        self.resim_ekrani = tk.Label(root, bg='black')
        self.resim_ekrani.pack(expand='true')

        self.arayuz_ekrani = tk.Label(root, font=('Helvetica', 25, 'bold'), bg='black', fg='white')
        self.arayuz_ekrani.pack(expand='true')
        self.arayuz_ekrani.pack_forget()

Resim ekranı ve arayüz ekranı için tkinter etiketlerini oluşturur.

###############################################################################################################################################################################

        self.PIR = 23
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIR, GPIO.IN)

PIR sensörü için giriş pinini ayarlar.

###############################################################################################################################################################################

        self.resim_gorunur_sure = 5000  # Resmin görünür kalacağı süre (5 saniye)
        self.ara_sure = 5  # Hareket algılandıktan sonra tekrar resim ekranına geçiş süresi (5 saniye)
        self.kontrol_hareket_algila()

Resmin görüneceği süreyi ve geçiş süresini tanımlar, ardından hareket algılama fonksiyonunu başlatır.

###############################################################################################################################################################################

    def kontrol_hareket_algila(self):
        if self.hareket_algilama():
            print("Hareket Algılandı!")
            self.goster_arayuz_ekrani()
        else:
            self.gizle_arayuz_ekrani()

        self.root.after(500, self.kontrol_hareket_algila)

Hareket algılama fonksiyonunu sürekli olarak kontrol eder ve ekranda değişiklik yapar.

###############################################################################################################################################################################

    def hareket_algilama(self):
        return GPIO.input(self.PIR) == 1

PIR sensöründen gelen girişi okur ve hareket olup olmadığını kontrol eder.

###############################################################################################################################################################################

    def goster_arayuz_ekrani(self):
        self.resim_goster_timer = time.time() + self.resim_gorunur_sure
        self.resim_ekrani.pack_forget()
        self.arayuz_ekrani.pack(expand='true')
        self.root.after(self.ara_sure * 5000, self.gizle_arayuz_ekrani)  # Belirlenen süre sonra resim ekranına geçiş

Arayüz ekranını gösterir ve belirli bir süre sonra resim ekranına geçişi planlar.

###############################################################################################################################################################################

    def gizle_arayuz_ekrani(self):
        if hasattr(self, 'resim_goster_timer') and time.time() < self.resim_goster_timer:
            # Eğer resim gösterme süresi dolmamışsa beklemeye devam et
            return

        self.arayuz_ekrani.pack_forget()
        self.tanimla_resim_ekrani()

Arayüz ekranını gizler ve resim ekranını gösterir.

###############################################################################################################################################################################

    def tanimla_resim_ekrani(self):
        img = Image.open("/home/akillitablo/Downloads/dogs.jpg")
        img = img.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        self.resim_ekrani.configure(image=img)
        self.resim_ekrani.image = img
        self.resim_ekrani.pack(expand='true')

Resim ekranını tanımlar ve resmi ekranda gösterir.

###############################################################################################################################################################################

    def cikis(self, event):
        GPIO.cleanup()
        self.root.destroy()

Programdan çıkış yapar ve GPIO pinlerini temizler.

###############################################################################################################################################################################

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

Kameradan fotoğraf çeker, ekranda gösterir ve belirli bir süre sonra tekrar resim ekranını gösterir.

###############################################################################################################################################################################

class ArayuzEkranGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Arayüz Ekranı")
        self.root.geometry("800x480")

Arayüz ekranını tanımlar ve başlık ile boyutunu belirler.

###############################################################################################################################################################################

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

Etiketler ve diğer arayüz öğelerini oluşturur ve arayüzün güncellenmesini sağlar.

###############################################################################################################################################################################

    def tarih_saat_guncelle(self):
        an = time.localtime()
        saat = time.strftime('%H:%M:%S', an)
        tarih = time.strftime('%Y-%m-%d', an)
        self.tarih_ve_saat_etiketi.config(text=f'{tarih}\n{saat}')
        self.root.after(1000, self.tarih_saat_guncelle)

Tarih ve saat etiketlerini günceller.

###############################################################################################################################################################################

    def guncelle_kur_bilgisi(self):
        try:
            kur_cinsleri = ["USD", "EUR", "GBP"]
            c = CurrencyRates()
            kur_bilgisi = "   ".join([f"{kur}: {c.get_rate(kur, 'TRY'):.2f}" for kur in kur_cinsleri])
            self.kur_bilgisi_etiketi.config(text=kur_bilgisi)
        except Exception as e:
            print(f"Hata: {e}")

        self.root.after(3600000, self.guncelle_kur_bilgisi)

Döviz kurlarını günceller.

###############################################################################################################################################################################

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

Hava durumunu günceller.

###############################################################################################################################################################################

    def cikis(self, event):
        self.root.destroy()

Programdan çıkar.

###############################################################################################################################################################################

if __name__ == "__main__":
    root = tk.Tk()
    app = AkilliAynaGUI(root)
    app.tanimla_resim_ekrani()

    arayuz_ekran = ArayuzEkranGUI(root)
    root.mainloop()

Ana program akışını başlatır ve tkinter uygulamasını çalıştırır.
Bu kod parçası, Python'un tkinter kütüphanesini kullanarak grafiksel bir kullanıcı arayüzü (GUI) oluşturur ve bir Raspberry Pi'de çalışan "Akıllı Ayna" uygulamasının ana kısmını başlatır. İşte adım adım ne yaptığını açıklayalım:

    root = tk.Tk(): Tk sınıfından bir nesne yaratılır. Bu, GUI uygulamasının ana penceresini temsil eder. tkinter kütüphanesinin temel bir bileşenidir ve uygulamanın tüm arayüzü bu pencere üzerinde oluşturulur.

    app = AkilliAynaGUI(root): AkilliAynaGUI sınıfının bir örneği oluşturulur. Bu sınıf, akıllı ayna uygulamasının ana işlevselliğini yönetir. root parametresi, bu sınıfın ana pencere olarak kullanacağı Tk nesnesine referanstır. AkilliAynaGUI sınıfı, bir hareket algılama sensörü aracılığıyla hareket algıladığında arayüz ekranını gösteren ve belirli bir süre sonra resim ekranına geri dönen bir mantığı barındırır.

    app.tanimla_resim_ekrani(): AkilliAynaGUI sınıfındaki tanimla_resim_ekrani metodunu çağırır. Bu metod, uygulamanın başlangıcında görüntülenmesi gereken varsayılan resmi tanımlar ve ekranda gösterir. Bu genellikle, hareket algılanmadığında gösterilecek statik bir arka plan resmi veya hoş geldiniz mesajı olabilir.

    arayuz_ekran = ArayuzEkranGUI(root): ArayuzEkranGUI sınıfının bir örneği oluşturulur. Bu sınıf, tarih ve saat, hava durumu, döviz kurları gibi bilgileri gösteren bir arayüz ekranının işlevselliğini sağlar. Ancak, bu sınıfın örneği oluşturulmuş olsa da, AkilliAynaGUI sınıfının içindeki mantık, ne zaman gösterileceğini kontrol eder. Bu kodun içinde, ArayuzEkranGUI doğrudan bir etkileşime girmez veya gösterilmez; bu durum kodun mevcut yapısına göre biraz yanıltıcı olabilir.

    root.mainloop(): tkinter uygulamasının olay döngüsünü başlatır. Bu, uygulamanın, kullanıcıdan gelen girişleri (örneğin, klavye tuş vuruşları veya fare hareketleri) dinlemeye başladığı ve kullanıcı arayüzünün etkileşimli olmasını sağlayan sonsuz bir döngüdür. Bu komut, pencere kapatılana kadar uygulamanın çalışmaya devam etmesini sağlar.

Bu kod, Raspberry Pi üzerinde çalışan ve kullanıcı etkileşimi sağlayan bir akıllı ayna uygulamasının temel yapısını oluşturur. Ancak, ArayuzEkranGUI sınıfının bu kod parçasında nasıl entegre edildiği ve kullanıldığı konusunda biraz daha açıklığa ihtiyaç olabilir.

###############################################################################################################################################################################
