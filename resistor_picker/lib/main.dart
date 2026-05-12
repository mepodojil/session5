import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:tflite_flutter/tflite_flutter.dart';
import 'dart:io';
import 'package:flutter/material.dart';

void main() => runApp(const ResistorPickerApp());

class ResistorPickerApp extends StatelessWidget {
  const ResistorPickerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Resistor Picker',
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: Colors.black,
        primaryColor: Colors.white,
        fontFamily: 'Courier',
        textTheme: const TextTheme(
          bodyLarge: TextStyle(fontFamily: 'Courier', color: Colors.white, fontSize: 18),
          bodyMedium: TextStyle(fontFamily: 'Courier', color: Colors.white70, fontSize: 16),
          headlineMedium: TextStyle(fontFamily: 'Courier', color: Colors.white, fontSize: 32, fontWeight: FontWeight.bold),
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.black,
          foregroundColor: Colors.white,
        ),
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.white, brightness: Brightness.dark),
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const HomeScreen(),
        '/about': (context) => const AboutScreen(),
      },
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  CameraController? _controller;
  Future<void>? _initializeControllerFuture;
  String _result = '--';
  File? _lastImage;
  Interpreter? _interpreter; // Placeholder for future ML model

  @override
  void initState() {
    super.initState();
    _initCamera();
    _initModel();
  }

  Future<void> _initCamera() async {
    final cameras = await availableCameras();
    final camera = cameras.isNotEmpty ? cameras.first : null;
    if (camera != null) {
      _controller = CameraController(
        camera,
        ResolutionPreset.medium,
        enableAudio: false,
      );
      _initializeControllerFuture = _controller!.initialize();
      setState(() {});
    }
  }

  Future<void> _initModel() async {
    // Placeholder for loading TFLite model in the future
    // _interpreter = await Interpreter.fromAsset('model.tflite');
  }

  @override
  void dispose() {
    _controller?.dispose();
    _interpreter?.close();
    super.dispose();
  }

  Future<void> _captureAndProcess() async {
    try {
      await _initializeControllerFuture;
      final image = await _controller!.takePicture();
      setState(() {
        _result = 'Processing...';
        _lastImage = File(image.path);
      });
      // TODO: Add image processing and ML inference here using _interpreter
      await Future.delayed(const Duration(seconds: 1));
      setState(() {
        _result = 'unknown';
      });
    } catch (e) {
      setState(() {
        _result = 'Error';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Resistor Picker'),
        actions: [
          IconButton(
            icon: const Icon(Icons.info_outline),
            tooltip: 'About',
            onPressed: () => Navigator.pushNamed(context, '/about'),
          ),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            SizedBox(
              width: 280,
              height: 180,
              child: _controller == null
                  ? const Center(child: Text('No camera', style: TextStyle(color: Colors.white54, fontFamily: 'Courier')))
                  : FutureBuilder<void>(
                      future: _initializeControllerFuture,
                      builder: (context, snapshot) {
                        if (snapshot.connectionState == ConnectionState.done) {
                          return ClipRRect(
                            borderRadius: BorderRadius.circular(8),
                            child: CameraPreview(_controller!),
                          );
                        } else {
                          return const Center(child: CircularProgressIndicator());
                        }
                      },
                    ),
            ),
            const SizedBox(height: 24),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white12,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(
                'Result: $_result',
                style: const TextStyle(fontSize: 28, color: Colors.white, fontFamily: 'Courier'),
              ),
            ),
            const SizedBox(height: 16),
            if (_lastImage != null)
              Container(
                width: 120,
                height: 80,
                margin: const EdgeInsets.only(bottom: 16),
                child: Image.file(_lastImage!, fit: BoxFit.cover),
              ),
            const SizedBox(height: 16),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.white,
                foregroundColor: Colors.black,
                textStyle: const TextStyle(fontFamily: 'Courier', fontSize: 18),
                padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
              ),
              onPressed: _controller == null ? null : _captureAndProcess,
              child: const Text('Capture'),
            ),
          ],
        ),
      ),
    );
  }
}

class AboutScreen extends StatelessWidget {
  const AboutScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('About'),
      ),
      body: const Center(
        child: Padding(
          padding: EdgeInsets.all(24.0),
          child: Text(
            'Resistor Picker\n\nA minimalist app for identifying 4- and 5-band resistors using your camera.\n\nAll processing is on-device. Uncertain results are shown as \'unknown\'.',
            style: TextStyle(fontSize: 18, fontFamily: 'Courier', color: Colors.white70),
            textAlign: TextAlign.center,
          ),
        ),
      ),
    );
  }
}
