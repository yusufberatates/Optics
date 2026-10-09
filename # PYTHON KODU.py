# PYTHON KODU
import serial
import time

# DİKKAT: 'COM3' kısmını kendi Arduino'nun bağlı olduğu port ile değiştir!
# Windows'ta Aygıt Yöneticisi'ne (Device Manager) girip "Bağlantı Noktaları (COM ve LPT)" 
# altından CH340 veya Arduino Uno yazan portun numarasını bulmalısın (Örn: COM3, COM5).
arduino_port = 'COM3' 
baud_rate = 9600

print(f"{arduino_port} portuna bağlanılıyor...")

try:
    # Arduino ile bağlantıyı aç
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    time.sleep(2) # Arduino'nun resetlenip kendine gelmesi için 2 saniye bekle (Kritik!)
    print("Bağlantı başarılı! Kontrol başlıyor.")

    while True:
        # Kullanıcıdan komut al
        komut = input("LED'i yakmak için '1', söndürmek için '0', çıkmak için 'q' yazın: ")
        
        if komut == 'q':
            print("Çıkış yapılıyor...")
            break
        elif komut in ['1', '0']:
            # Veriyi byte'a çevirip (.encode()) USB'den gönder
            ser.write(komut.encode())
            print(f"Komut gönderildi: {komut}")
        else:
            print("Geçersiz komut!")

except Exception as e:
    print(f"Hata oluştu: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Seri port kapatıldı.")