import 'package:flutter/material.dart';

class ResultScreen extends StatelessWidget {
  final String top;
  final String bottom;
  final String message;

  const ResultScreen({
    super.key,
    required this.top,
    required this.bottom,
    required this.message,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Recommendations")),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            Text("Top: $top", style: const TextStyle(fontSize: 18)),
            const SizedBox(height: 10),
            Text("Bottom: $bottom", style: const TextStyle(fontSize: 18)),
            const SizedBox(height: 20),
            Text(message, style: const TextStyle(fontSize: 16)),
          ],
        ),
      ),
    );
  }
}
