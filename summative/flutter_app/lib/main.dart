import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Sleep Quality Predictor',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const PredictionPage(),
    );
  }
}

class PredictionPage extends StatefulWidget {
  const PredictionPage({Key? key}) : super(key: key);

  @override
  _PredictionPageState createState() => _PredictionPageState();
}

class _PredictionPageState extends State<PredictionPage> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _sleepDurationController = TextEditingController();
  final TextEditingController _studyHoursController = TextEditingController();
  final TextEditingController _screenTimeController = TextEditingController();
  final TextEditingController _caffeineIntakeController = TextEditingController();
  final TextEditingController _physicalActivityController = TextEditingController();
  String _prediction = "";

  Future<void> _predict() async {
    if (_formKey.currentState!.validate()) {
      final response = await http.post(
        Uri.parse('YOUR_API_ENDPOINT/predict'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'sleep_duration': double.parse(_sleepDurationController.text),
          'study_hours': double.parse(_studyHoursController.text),
          'screen_time': double.parse(_screenTimeController.text),
          'caffeine_intake': int.parse(_caffeineIntakeController.text),
          'physical_activity': int.parse(_physicalActivityController.text),
        }),
      );

      if (response.statusCode == 200) {
        final result = jsonDecode(response.body);
        setState(() {
          _prediction = "Predicted Sleep Quality: ${result['predicted_sleep_quality'].toStringAsFixed(2)}";
        });
      } else {
        setState(() {
          _prediction = "Error making prediction";
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Sleep Quality Predictor'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              TextFormField(
                controller: _sleepDurationController,
                decoration: const InputDecoration(labelText: 'Sleep Duration (hours)'),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter sleep duration';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _studyHoursController,
                decoration: const InputDecoration(labelText: 'Study Hours'),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter study hours';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _screenTimeController,
                decoration: const InputDecoration(labelText: 'Screen Time (hours)'),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter screen time';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _caffeineIntakeController,
                decoration: const InputDecoration(labelText: 'Caffeine Intake (drinks)'),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter caffeine intake';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _physicalActivityController,
                decoration: const InputDecoration(labelText: 'Physical Activity (minutes)'),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter physical activity';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _predict,
                child: const Text('Predict'),
              ),
              const SizedBox(height: 20),
              Text(
                _prediction,
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
}