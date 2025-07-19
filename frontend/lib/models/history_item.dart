// models/history_item.dart
class HistoryItem {
  final String date;
  final String imageUrl;
  final String apparel;
  final List<String> colors;
  final List<String> suggestions;

  HistoryItem({
    required this.date,
    required this.imageUrl,
    required this.apparel,
    required this.colors,
    required this.suggestions,
  });

  factory HistoryItem.fromJson(Map<String, dynamic> json) {
    return HistoryItem(
      date: json['date'],
      imageUrl: 'http://localhost:5000${json['image_url']}',
      apparel: json['apparel'],
      colors: List<String>.from(json['colors']),
      suggestions: List<String>.from(json['suggestions']),
    );
  }
}
