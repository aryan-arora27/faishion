import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import 'home_screen.dart';

class SkinColorSelector extends StatefulWidget {
  final int userId;

  const SkinColorSelector({super.key, required this.userId});

  @override
  State<SkinColorSelector> createState() => _SkinColorSelectorState();
}

class _SkinColorSelectorState extends State<SkinColorSelector> {
  final List<String> skinColors = [
    'light',
    'medium',
    'dark',
    'brown',
    'fair',
    'olive',
    'tan',
  ];

  final Map<String, Color> skinColorMap = {
    'light': Color(0xFFFFE0BD),
    'medium': Color(0xFFDBA978),
    'dark': Color(0xFF8D5524),
    'brown': Color(0xFF7D4E3A),
    'fair': Color(0xFFFFDAB9),
    'olive': Color(0xFFC3B091),
    'tan': Color(0xFFD2B48C),
  };

  String? selectedColor;
  bool isLoading = false;
  String errorMessage = '';

  Future<void> submitSkinColor() async {
    if (selectedColor == null) {
      setState(() => errorMessage = "Please select a skin tone.");
      return;
    }

    setState(() {
      isLoading = true;
      errorMessage = '';
    });

    try {
      final response = await http.post(
        Uri.parse('http://10.0.2.2:5000/auth/set_skin_color'),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "user_id": widget.userId,
          "skin_color": selectedColor,
        }),
      );

      setState(() => isLoading = false);

      if (response.statusCode == 200) {
        print("Skin color set successfully.");
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (_) => HomeScreen(userId: widget.userId, skinColor: selectedColor!),
          ),
        );

      } else {
        setState(() => errorMessage = "Error saving skin color.");
      }
    } catch (e) {
      setState(() => errorMessage = "Connection error. Try again.");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Select Skin Tone'),
        backgroundColor: Colors.deepPurple,
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            const Text(
              "Choose your skin tone:",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.w500),
            ),
            const SizedBox(height: 20),
            Expanded(
              child: ListView.separated(
                itemCount: skinColors.length,
                separatorBuilder: (_, __) => const Divider(),
                itemBuilder: (context, index) {
                  final color = skinColors[index];
                  return ListTile(
                    title: Text(
                      color[0].toUpperCase() + color.substring(1),
                      style: const TextStyle(fontSize: 16),
                    ),
                    leading: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Container(
                          width: 20,
                          height: 20,
                          margin: const EdgeInsets.only(right: 10),
                          decoration: BoxDecoration(
                            color: skinColorMap[color] ?? Colors.grey,
                            shape: BoxShape.circle,
                            border: Border.all(color: Colors.black12),
                          ),
                        ),
                        Radio<String>(
                          value: color,
                          groupValue: selectedColor,
                          onChanged: (value) {
                            setState(() {
                              selectedColor = value;
                            });
                          },
                        ),
                      ],
                    ),
                    onTap: () {
                      setState(() {
                        selectedColor = color;
                      });
                    },
                  );
                },
              ),
            ),
            if (errorMessage.isNotEmpty)
              Text(errorMessage, style: const TextStyle(color: Colors.red)),
            const SizedBox(height: 10),
            isLoading
                ? const CircularProgressIndicator()
                : ElevatedButton(
              onPressed: submitSkinColor,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.deepPurple,
                padding: const EdgeInsets.symmetric(
                    vertical: 14, horizontal: 30),
              ),
              child: const Text("Continue",
                  style: TextStyle(fontSize: 16, color: Colors.white)),
            ),
          ],
        ),
      ),
    );
  }
}
