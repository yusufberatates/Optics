// Optomekatronik Otonom Otofokus - Arduino Donanım Firmware Kodu
int ledPin = 13;
char gelenVeri;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600); // Bilgisayar ile 9600 baud hızında haberleşme
}

void loop() {
  if (Serial.available() > 0) {
    gelenVeri = Serial.read(); // Python'dan gelen komutu oku

    if (gelenVeri == '1') {
      digitalWrite(ledPin, HIGH);
      Serial.println("ARDUINO: '1' aldim, L LED'ini Yaktim (Ileri)"); 
    }
    else if (gelenVeri == '0') {
      digitalWrite(ledPin, LOW);
      Serial.println("ARDUINO: '0' aldim, L LED'ini Sondurdum (Geri)");
    }
  }
}