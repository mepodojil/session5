# Step 2: Core Components Setup — Step-by-Step Breakdown

## 2.1 Add Camera Dependency
- Add the `camera` package to `pubspec.yaml`:
  ```yaml
  dependencies:
    camera: ^0.10.5+2
  ```
- Run `flutter pub get` to install.

## 2.2 Research & Select ML/Image Processing Packages
- For on-device ML inference: use `tflite_flutter` for TensorFlow Lite model integration.
- For image manipulation (if needed): use the `image` package.
- Add to `pubspec.yaml`:
  ```yaml
  dependencies:
    tflite_flutter: ^0.10.2
    image: ^4.1.3
  ```
- Run `flutter pub get` to install.

## 2.3 Scaffold Main UI Screens
- Create a `HomeScreen` widget:
  - Camera preview
  - Capture button
  - Result display area (shows resistance value or 'unknown')
- (Optional) Create a `SettingsScreen` or `AboutScreen` for app info/help.

## 2.4 Set Up Basic Navigation
- Use Flutter’s built-in `Navigator` for simple navigation between Home and Settings/About screens.
- Example routes in `main.dart`:
  ```dart
  routes: {
    '/': (context) => HomeScreen(),
    '/about': (context) => AboutScreen(),
  }
  ```

## 2.5 Apply Minimalist UI Theme
- Set Courier as the default font in `ThemeData`.
- Use high-contrast colors (e.g., black/white backgrounds, strong accent colors).

---

*Proceed to implementation of each sub-step in order. Let me know when you want to start with 2.1 (camera dependency setup).*