import 'package:flutter/material.dart';
import 'screens/welcome_screen.dart';

void main() {
  runApp(FaishionApp());
}

class FaishionApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'fAIshion',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorSchemeSeed: Colors.deepPurple,
        useMaterial3: true,
        fontFamily: 'Roboto',
      ),
      home: WelcomeScreen(),
    );
  }
}
