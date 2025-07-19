import 'package:flutter/material.dart';
import 'package:frontend/screens/skin_color_selector.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SignUpScreen extends StatefulWidget {
  const SignUpScreen({super.key});

  @override
  State<SignUpScreen> createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<SignUpScreen> {
  final _formKey = GlobalKey<FormState>();
  String username = '';
  String password = '';
  String confirmPassword = '';
  bool isLoading = false;
  String errorMessage = '';

  Future<void> registerUser() async {
    setState(() {
      isLoading = true;
      errorMessage = '';
    });

    if (password != confirmPassword) {
      setState(() {
        isLoading = false;
        errorMessage = "Passwords do not match";
      });
      return;
    }

    try {
      final response = await http.post(
        Uri.parse('http://10.0.2.2:5000/auth/register'),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "username": username,
          "password": password,
        }),
      );

      setState(() => isLoading = false);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        print("Registered successfully: ${data['user_id']}");
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (_) => SkinColorSelector(userId: data['user_id']),
          ),
        );

      } else {
        final error = jsonDecode(response.body);
        setState(() {
          errorMessage = error['error'] ?? "Registration failed";
        });
      }
    } catch (e) {
      setState(() {
        isLoading = false;
        errorMessage = "Connection error. Try again.";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    return Scaffold(
      appBar: AppBar(
        title: const Text("Sign Up"),
        backgroundColor: Colors.deepPurple,
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: EdgeInsets.symmetric(horizontal: size.width * 0.08),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextFormField(
                decoration: const InputDecoration(labelText: "Username"),
                validator: (value) =>
                value == null || value.isEmpty ? 'Enter username' : null,
                onChanged: (value) => username = value,
              ),
              const SizedBox(height: 20),
              TextFormField(
                obscureText: true,
                decoration: const InputDecoration(labelText: "Password"),
                validator: (value) =>
                value == null || value.isEmpty ? 'Enter password' : null,
                onChanged: (value) => password = value,
              ),
              const SizedBox(height: 20),
              TextFormField(
                obscureText: true,
                decoration: const InputDecoration(labelText: "Confirm Password"),
                validator: (value) =>
                value == null || value.isEmpty ? 'Confirm password' : null,
                onChanged: (value) => confirmPassword = value,
              ),
              const SizedBox(height: 30),
              if (errorMessage.isNotEmpty)
                Text(errorMessage,
                    style: const TextStyle(color: Colors.red)),
              if (isLoading)
                const CircularProgressIndicator()
              else
                ElevatedButton(
                  onPressed: () {
                    if (_formKey.currentState!.validate()) {
                      registerUser();
                    }
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.deepPurple,
                    padding: const EdgeInsets.symmetric(
                        vertical: 14, horizontal: 30),
                  ),
                  child: const Text("Sign Up",
                      style: TextStyle(fontSize: 16, color: Colors.white)),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
