# Autonomous Lens Autofocus System

This project is a simple undergraduate physics/optics project. It is not a professional industrial system, and it is not meant to be a polished commercial product. The goal is to build a basic autofocus system using a camera, image processing, and motor control, and to understand how focus can be improved automatically by analyzing image sharpness.

The idea is simple: if the image is blurry, the lens is not in focus. If the image is sharper, the lens is closer to the correct focus position. By measuring how sharp the image is, the system can decide whether to move the lens forward or backward.

---

## What this project does

The project connects a camera to a Python script, analyzes each frame, and calculates a focus score. The score is then used to decide the direction of motion for the lens system. A microcontroller or Arduino receives commands from the computer and moves the lens accordingly.

In short, the loop is:

1. Capture a frame from the camera
2. Convert it to grayscale
3. Measure the sharpness of the image
4. Compare the current score to the previous one
5. Move the lens in the direction that improves focus
6. Repeat

This is a basic closed-loop autofocus system.

---

## Why this is interesting for physics

This project combines optics and measurement. In optics, image quality depends strongly on focus. A focused image contains stronger edges and more fine detail. A defocused image is softer and has less high-frequency information.

The project uses this idea to turn a visual property into a numerical value. That value can then be treated as a signal for controlling a mechanical system.

So in a physics sense, this is a practical demonstration of:

- optics and image formation,
- digital image analysis,
- signal-based feedback control,
- mechanical movement of a lens system.

---

## Project files

```text
optics/
├── arduino/
│   └── motor_kontrol.ino       # Arduino firmware for hardware control / listening
├── python/
│   ├── otofokus_otonom.py          # Main autofocus system
│   ├── serial_test2.py             # Arduino/serial communication tester
│   └── vision_test.py              # Camera and sharpness test
├── zemax/
│   ├── Prescription_data.txt           # Lens data / optical reference
│   ├── LENS.ZDA                        # Lens data file
│   ├── LENS.zmx                        # Lens design file
│   └── Lens.bmp                        # Lens-related bitmap reference
└── README.md
```

### File descriptions

- [otofokus_otonom.py](./otofokus_otonom.py)  
  This is the main system script. It checks the camera, computes the sharpness score, decides the motion direction, and sends commands to the Arduino.

- [vision_test.py](./vision_test.py)  
  A simple camera test script. It displays the live image and prints the image sharpness score so you can see if the camera and focus metric work correctly.

- [serial_test.py](./serial_test.py)  
  A helper script to test the serial connection with an Arduino or controller. It allows manual commands such as forward/backward motion.

- [motor_kontrol.ino](./arduino/motor_kontrol/motor_kontrol.ino)  
  The Arduino firmware script. It listens to the serial port, reads commands from the computer, and controls the actuator/LED feedback accordingly.
  
- [Prescription_data.txt](./Prescription_data.txt)  
  Optical and lens design data used as a supporting reference for the system.

- [LENS.ZDA](./LENS.ZDA) and [LENS.zmx](./LENS.zmx)  
  Lens design files that help describe the optical hardware behind the project.

---

## Main idea behind the autofocus logic

The sharpness is measured with the Laplacian operator:

```python
cv2.Laplacian(image, cv2.CV_64F).var()
```

This gives a number that describes how much edge detail exists in the image. A focused image has stronger edges, so the value becomes larger. A blurred image has less edge detail, so the value becomes smaller.

This is why the system can use the sharpness score as a focus signal.

### Simple control behavior

- If the image becomes less sharp than before, the lens likely passed the best focus position.
- The system then reverses direction.
- If the image keeps getting sharper, it continues moving in the same direction.
- The decision is made repeatedly to guide the lens toward the optimum focus.

This is a basic hill-climbing method: the system tries to move in the direction that increases the sharpness score.

---

## Required hardware

- USB webcam or built-in camera
- Lens system with a focus mechanism
- Motor or actuator for moving the lens
- Arduino or microcontroller for motor control
- Serial connection between the computer and Arduino
- Stable power source for the motor

---

## Required software

- Python 3.9 or newer
- OpenCV (`opencv-python`)
- PySerial (`pyserial`)

### Install dependencies

```bash
pip install opencv-python pyserial
```

---

## How to run the project

### 1. Test the camera

```bash
python vision_test.py
```

This opens the camera and shows the image with a focus score. Press `q` to exit.

### 2. Test the serial connection

```bash
python serial_test.py
```

This script opens the COM port and lets you send manual commands to the Arduino:

- `1` = forward
- `0` = backward
- `q` = quit

You must set the correct port before using it.

### 3. Run the autofocus system

```bash
python otofokus_otonom.py
```

This script does the full operation: it opens the camera, reads frames, calculates sharpness, decides the motion direction, and sends that decision to the Arduino.

---

## Important configuration settings

The code currently uses a hardcoded serial port:

```python
arduino_port = 'COM6'
```

This must be changed to match the actual port on your system. For example, on some machines it may be a different COM port or a Linux serial device such as `/dev/ttyUSB0`.

The camera is also opened as:

```python
cap = cv2.VideoCapture(0)
```

If you have more than one camera, or the default camera is not the correct one, you may need to change this number.

---

## Expected results

If the system works properly, you should see:

- the sharpness value changing as the image becomes clearer or blurrier,
- the lens moving in the direction that seems to improve focus,
- the displayed image showing the current focus score and motion direction.

This is a simple proof-of-concept, so the system may not be perfectly stable. It can be sensitive to:

- poor lighting,
- noisy camera images,
- inaccurate motor movement,
- serial communication delays,
- mechanical backlash or slack in the lens system.

---

## Physics behind the method

The main idea is that focused images contain more edge detail. When the lens is out of focus, the image becomes blurred, and the intensity changes become smoother. Because the Laplacian responds strongly to transitions in intensity, it acts as a useful measure of focus quality.

So although the system is simple, it is based on a real optical principle: sharpness is related to spatial frequency content and edge contrast.

---

## What is good about this project

This project is useful because it is:

- easy to understand,
- simple to test step by step,
- based on a real optics problem,
- good for learning about image processing and feedback control,
- easy to extend later.

It is exactly the kind of project that helps students connect theory and practical implementation.

---

## Limitations

This is a prototype, so there are some important limitations:

- it uses a simple focus metric rather than a highly optimized algorithm,
- it may not work well in low-contrast scenes,
- the control law is basic,
- the system depends on hardware calibration,
- the serial timing and motor movement may need tuning.

These limitations are normal for an undergraduate project and are part of the learning process.

---

## Possible improvements

This project can be extended in many ways:

- use a better focus metric,
- add calibration for the lens travel range,
- add thresholding or hysteresis to avoid jitter,
- log focus values over time,
- improve the control loop,
- test with different lenses and cameras.

This would make the system more reliable and closer to a real autofocus device.

---

## Final note

This repository is best understood as an educational prototype for an optical autofocus system. It shows how a seemingly simple idea — using image sharpness as a feedback value — can be turned into a working system involving camera input, image processing, and controlled motor movement.

It is not a professional product, but it is a solid and useful undergraduate project that connects concepts from physics, optics, electronics, and programming.
