import cv2

def calculate_sharpness(image):
    # Laplace filtresi ile görüntüdeki keskin kenarların varyansını hesaplar
    return cv2.Laplacian(image, cv2.CV_64F).var()

# 0 varsayılan web kamerasını açar
cap = cv2.VideoCapture(0)

print("Kamera açılıyor... Çıkmak için 'q' tuşuna basın.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kameradan görüntü alınamadı.")
        break

    # Netlik analizi için görüntüyü gri tonlamaya çevir
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    skor = calculate_sharpness(gray)

    # Skoru ekrana yazdır
    cv2.putText(frame, f"Netlik Skoru: {skor:.1f}", (20, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Kamera Testi", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()