import cv2
import serial
import time

# --- 1. AYARLAR VE BAĞLANTI ---
arduino_port = 'COM6'  # Kendi portun
baud_rate = 9600

def calculate_sharpness(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

print("Arduino'ya bağlanılıyor...")
try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    ser.setDTR(False)
    time.sleep(1)
    ser.flushInput()
    ser.setDTR(True)
    time.sleep(2)
    print("Bağlantı başarılı! Otonom sistem devrede.")
except Exception as e:
    print(f"Bağlantı hatası: {e}")
    exit()

# --- 2. KAMERA VE ALGORİTMA DEĞİŞKENLERİ ---
cap = cv2.VideoCapture(0)

onceki_skor = 0.0
motor_yonu = '1'  # Başlangıçta ileri ('1') gitmeyi deneyecek
son_komut_zamani = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Görüntüyü griye çevir ve netlik skorunu hesapla
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    guncel_skor = calculate_sharpness(gray)

    # --- 3. BEYİN (KARAR MEKANİZMASI) ---
    su_an = time.time()
    
    # Arduino'yu komut yağmuruna tutup buffer'ı kitlememek için her 0.5 saniyede 1 karar ver
    if su_an - son_komut_zamani > 0.5:
        
        # Eğer skor düştüyse zirveden uzaklaşıyoruz demektir, yönü değiştir!
        if guncel_skor < onceki_skor:
            if motor_yonu == '1':
                motor_yonu = '0'
            else:
                motor_yonu = '1'

        # Yeni komutu (yönü) Arduino'ya gönder
        ser.write(motor_yonu.encode())

        # Arduino'dan gelen teyit cevabını oku ve terminale yazdır
        time.sleep(0.1) # Cevabın gelmesi için çok kısa bekle
        if ser.in_waiting > 0:
            arduino_cevabi = ser.readline().decode('utf-8', errors='ignore').strip()
            print(f"Skor: {guncel_skor:.1f} | Karar: {motor_yonu} | {arduino_cevabi}")

        # Bir sonraki kıyaslama için mevcut durumu kaydet
        onceki_skor = guncel_skor
        son_komut_zamani = su_an

    # --- 4. GÖRSEL ARAYÜZ ---
    bilgi_metni = f"Skor: {guncel_skor:.1f} | Yon: {'ILERI (L yaniyor)' if motor_yonu == '1' else 'GERI (L sonuk)'}"
    cv2.putText(frame, bilgi_metni, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.imshow("Otonom Otofokus Sistemi", frame)

    # 'q' tuşuna basarak çıkış yap
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kapanış işlemleri
cap.release()
cv2.destroyAllWindows()
ser.close()
print("Sistem kapatıldı.")