# resistor-picker

A minimalist mobile app for iOS and Android that identifies 4- and 5-band electrical resistors from photos using on-device machine learning and the industry standard color code.

---

## Features
- Capture resistor images with your device camera
- On-device ML inference for privacy and speed
- Decodes 4- and 5-band resistor color codes
- Minimalist, high-contrast UI with Courier font
- Categorizes uncertain results as 'unknown'

---

## Getting Started

### Prerequisites
- [Flutter SDK](https://docs.flutter.dev/get-started/install) (latest stable)
- Xcode (for iOS development)
- Android Studio (for Android development)

### Setup
1. Clone or download this repository.
2. Install dependencies:
   ```sh
   flutter pub get
   ```
3. Run the app on an emulator or device:
   ```sh
   flutter run
   ```

---

## Project Structure
- `lib/` — Main Dart source code
- `assets/` — Images, models, and other assets
- `test/` — Unit and widget tests

---

## Implementation Plan
See [implementation-plan.md](implementation-plan.md) for the full step-by-step plan.

---

## License
MIT
