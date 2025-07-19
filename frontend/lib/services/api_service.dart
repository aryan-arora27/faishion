// services/api_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/history_item.dart';

class ApiService {
  static const baseUrl = 'http://10.0.2.2:5000';

  static Future<List<HistoryItem>> fetchHistory(int userId) async {
    final response = await http.get(Uri.parse('$baseUrl/history/$userId'));

    if (response.statusCode == 200) {
      List data = json.decode(response.body);
      return data.map((json) => HistoryItem.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load history');
    }
  }
}
