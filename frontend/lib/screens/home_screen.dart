import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'package:path/path.dart' as path;

class HomeScreen extends StatefulWidget {
  final int userId;
  final String skinColor;

  const HomeScreen({
    Key? key,
    required this.userId,
    required this.skinColor,
  }) : super(key: key);

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  List<Map<String, dynamic>> history = [];

  @override
  void initState() {
    super.initState();
    fetchUserHistory();
  }

  Future<void> fetchUserHistory() async {
    try {
      final response = await http.get(
        Uri.parse('http://10.0.2.2:5000/recommend/history/${widget.userId}'),
      );
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        setState(() {
          history = data.map<Map<String, dynamic>>((item) => {
            'image_url': item['image_url'],
            'apparel': item['apparel'],
            'colors': List<String>.from(item['colors']),
            'suggestions': List<Map<String, dynamic>>.from(item['suggestions']),
            'date': item['date'],
          }).toList();
        });
      } else {
        print('Error fetching history: ${response.body}');
      }
    } catch (e) {
      print('Error loading history: $e');
    }
  }

  Future<void> _pickImageAndUpload(BuildContext context) async {
    final picker = ImagePicker();
    final pickedFile = await picker.pickImage(source: ImageSource.camera);

    if (pickedFile == null) return;

    final file = File(pickedFile.path);

    // Show loading indicator
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (_) => const Center(child: CircularProgressIndicator()),
    );

    try {
      final uri = Uri.parse('http://10.0.2.2:5000/recommend/upload');

      final request = http.MultipartRequest('POST', uri)
        ..fields['user_id'] = widget.userId.toString()
        ..files.add(
          await http.MultipartFile.fromPath(
            'image',
            file.path,
            filename: path.basename(file.path),
          ),
        );

      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      Navigator.of(context).pop(); // Close loading dialog

      if (response.statusCode == 200) {
        final result = jsonDecode(response.body);

        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ResultScreen(result: result),
          ),
        );
      } else {
        showDialog(
          context: context,
          builder: (_) => AlertDialog(
            title: const Text('Upload Failed'),
            content: Text(response.body),
            actions: [
              TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('OK'))
            ],
          ),
        );
      }
    } catch (e) {
      Navigator.of(context).pop(); // Close loading
      print('Upload error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Your Fashion History'),
        backgroundColor: Colors.deepPurple,
      ),
      body: history.isEmpty
          ? const Center(child: Text("No history yet."))
          : ListView.builder(
        itemCount: history.length,
        itemBuilder: (context, index) {
          final item = history[index];
          return Card(
            margin:
            const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: ListTile(
              leading: Image.network(
                'http://10.0.2.2:5000${item['image_url']}',
                width: 60,
                height: 60,
                fit: BoxFit.cover,
              ),
              title: Text(item['apparel']),
              subtitle: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Colors: ${item['colors'].join(", ")}'),
                  Text('Suggestions: ${item['suggestions'].join(", ")}'),
                  Text('Date: ${item['date']}'),
                ],
              ),
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _pickImageAndUpload(context),
        backgroundColor: Colors.deepPurple,
        child: const Icon(Icons.add),
      ),
    );
  }
}

class ResultScreen extends StatelessWidget {
  final Map<String, dynamic> result;

  const ResultScreen({Key? key, required this.result}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Recommendations")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("Apparel Type: ${result['apparel'] ?? ''}"),
            const SizedBox(height: 10),
            Text("Detected Colors: ${(result['colors'] ?? []).join(", ")}"),
            const SizedBox(height: 10),
            Text("Suggestions: ${(result['suggestions'] ?? []).join(", ")}"),
          ],
        ),
      ),
    );
  }
}
