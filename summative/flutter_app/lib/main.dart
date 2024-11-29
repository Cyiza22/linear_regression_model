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
      title: 'Student Lifestyle Predictor',
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
  final TextEditingController _studyHoursController = TextEditingController();
  final TextEditingController _extracurricularHoursController = TextEditingController();
  final TextEditingController _socialHoursController = TextEditingController();
  final TextEditingController _physicalActivityController = TextEditingController();
  final TextEditingController _stressLevelController = TextEditingController();
  String _prediction = "";

  Future<void> _predict() async {
    if (_formKey.currentState!.validate()) {
      try {
        final response = await http.post(
          Uri.parse('http://localhost:5000/predict'),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'study_hours': double.parse(_studyHoursController.text),
            'extracurricular_hours': double.parse(_extracurricularHoursController.text),
            'social_hours': double.parse(_socialHoursController.text),
            'physical_activity_hours': double.parse(_physicalActivityController.text),
            'stress_level': _stressLevelController.text,
          }),
        );

        if (response.statusCode == 200) {
          final result = jsonDecode(response.body);
          setState(() {
            // Ensure we're displaying a numeric GPA
            double gpa = result['predicted_gpa'] is num 
                ? (result['predicted_gpa'] as num).toDouble()
                : 0.0;
            _prediction = "Predicted GPA: ${gpa.toStringAsFixed(2)}";
          });
        } else {
          setState(() {
            _prediction = "Prediction Error: ${response.statusCode}";
          });
        }
      } catch (e) {
        setState(() {
          _prediction = "Error: $e";
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Student Lifestyle Predictor'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              TextFormField(
                controller: _studyHoursController,
                decoration: const InputDecoration(
                  labelText: 'Study Hours (per week)',
                  hintText: 'Enter total study hours per week',
                ),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter study hours';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _extracurricularHoursController,
                decoration: const InputDecoration(
                  labelText: 'Extracurricular Hours (per week)',
                  hintText: 'Enter total extracurricular hours per week',
                ),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter extracurricular hours';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _socialHoursController,
                decoration: const InputDecoration(
                  labelText: 'Social Hours (per week)',
                  hintText: 'Enter total social hours per week',
                ),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter social hours';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _physicalActivityController,
                decoration: const InputDecoration(
                  labelText: 'Physical Activity Hours (per week)',
                  hintText: 'Enter total physical activity hours per week',
                ),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter physical activity hours';
                  }
                  return null;
                },
              ),
              TextFormField(
                controller: _stressLevelController,
                decoration: const InputDecoration(
                  labelText: 'Stress Level',
                  hintText: 'Enter Low/Moderate/High',
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter stress level';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _predict,
                child: const Text('Predict GPA'),
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