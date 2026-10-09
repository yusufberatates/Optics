import serial
import time

arduino_port = 'COM6' # KENDI PORTUNU YAZ
baud_rate = 9600

print(f"{arduino_port} portuna bağlanılıyor...")

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    time.sleep(2) 
    print("Bağlantı başarılı! Kontrol başlıyor.")

    while True:
        komut = input("Komut girin ('1' = İleri, '0' = Geri, 'q' = Çıkış): ")
        
        if komut == 'q':
            print("Çıkış yapılıyor...")
            break
        elif komut in ['1', '0']:
            # 1. Aşama: Arduino'ya komutu gönder (Ping)
            ser.write(komut.encode())

            # 2. Aşama: Arduino'dan gelecek cevabı bekle ve oku (Pong)
            time.sleep(0.1) # Arduino'nun cevap vermesi için çok kısa bir süre bekle
            if ser.in_waiting > 0:
                # Gelen cevabı oku, decode et (yazıya çevir) ve ekrana yazdır
                arduino_cevabi = ser.readline().decode('utf-8').strip()
                print(f"---> {arduino_cevabi}")
            else:
                print("Arduino'dan cevap gelmedi.")
        else:
            print("Geçersiz komut!")

except Exception as e:
    print(f"Hata oluştu: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Seri port kapatıldı.")