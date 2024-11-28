import 'package:flutter/material.dart';
import 'package:csv/csv.dart';
import 'dart:convert';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Student Lifestyle Sleep Analyzer',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: const SleepAnalysisPage(),
    );
  }
}

class SleepAnalysisPage extends StatefulWidget {
  const SleepAnalysisPage({Key? key}) : super(key: key);

  @override
  _SleepAnalysisPageState createState() => _SleepAnalysisPageState();
}

class _SleepAnalysisPageState extends State<SleepAnalysisPage> {
  final _formKey = GlobalKey<FormState>();
  
  // Controllers for input fields
  final TextEditingController _studyHoursController = TextEditingController();
  final TextEditingController _extracurricularHoursController = TextEditingController();
  final TextEditingController _socialHoursController = TextEditingController();
  final TextEditingController _physicalActivityController = TextEditingController();
  
  // Stress level dropdown
  String _selectedStressLevel = 'Low';
  final List<String> _stressLevels = ['Low', 'Moderate', 'High'];
  
  // Result variables
  double? _predictedSleepHours;
  String _analysisResult = '';

  // Simple predictive model based on dataset
  void _analyzeSleep() {
    if (_formKey.currentState!.validate()) {
      // Parse input values
      double studyHours = double.parse(_studyHoursController.text);
      double extracurricularHours = double.parse(_extracurricularHoursController.text);
      double socialHours = double.parse(_socialHoursController.text);
      double physicalActivityHours = double.parse(_physicalActivityController.text);

      // Basic prediction logic based on dataset patterns
      double sleepHoursPrediction = _predictSleepHours(
        studyHours, 
        extracurricularHours, 
        socialHours, 
        physicalActivityHours, 
        _selectedStressLevel
      );

      setState(() {
        _predictedSleepHours = sleepHoursPrediction;
        _analysisResult = _generateSleepAnalysis(sleepHoursPrediction);
      });
    }
  }

  double _predictSleepHours(double studyHours, double extracurricularHours, 
                             double socialHours, double physicalActivityHours, 
                             String stressLevel) {
    // Simple prediction logic based on dataset correlations
    double baseSleep = 7.5; // Average sleep hours from dataset

    // Adjustments based on different factors
    if (stressLevel == 'High') {
      baseSleep -= 1.0; // High stress tends to reduce sleep
    } else if (stressLevel == 'Low') {
      baseSleep += 0.5; // Low stress allows more sleep
    }

    // Study hours impact
    if (studyHours > 7) {
      baseSleep -= 0.5; // More study hours reduce sleep
    } else if (studyHours < 5) {
      baseSleep += 0.5; // Less study hours increase potential sleep
    }

    // Physical activity impact
    if (physicalActivityHours > 6) {
      baseSleep += 0.5; // More physical activity can improve sleep
    } else if (physicalActivityHours < 2) {
      baseSleep -= 0.5; // Less physical activity might reduce sleep quality
    }

    // Social hours impact
    if (socialHours > 4) {
      baseSleep -= 0.5; // More social hours might reduce sleep time
    }

    // Ensure sleep hours are within a reasonable range
    return baseSleep.clamp(5.0, 9.5);
  }

  String _generateSleepAnalysis(double sleepHours) {
    if (sleepHours < 6) {
      return 'Warning: You are getting insufficient sleep. This may negatively impact your academic performance and health.';
    } else if (sleepHours >= 6 && sleepHours < 7) {
      return 'Your sleep duration is below recommended levels. Try to increase your sleep time.';
    } else if (sleepHours >= 7 && sleepHours < 8) {
      return 'Your sleep duration is moderate. Aim to maintain or slightly increase your sleep time.';
    } else if (sleepHours >= 8 && sleepHours <= 9) {
      return 'Great job! Your sleep duration is within the optimal range for students.';
    } else {
      return 'You are getting more sleep than average. While this isn\'t necessarily bad, ensure it\'s not impacting your daily activities.';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Student Sleep Analyzer'),
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
                  labelText: 'Study Hours per Day',
                  hintText: 'Enter hours spent studying',
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
                  labelText: 'Extracurricular Hours per Day',
                  hintText: 'Enter hours spent in extracurricular activities',
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
                  labelText: 'Social Hours per Day',
                  hintText: 'Enter hours spent socializing',
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
                  labelText: 'Physical Activity Hours per Day',
                  hintText: 'Enter hours of physical activity',
                ),
                keyboardType: TextInputType.number,
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Please enter physical activity hours';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 10),
              DropdownButtonFormField<String>(
                value: _selectedStressLevel,
                decoration: const InputDecoration(
                  labelText: 'Stress Level',
                ),
                items: _stressLevels
                    .map((level) => DropdownMenuItem(
                          value: level,
                          child: Text(level),
                        ))
                    .toList(),
                onChanged: (value) {
                  setState(() {
                    _selectedStressLevel = value!;
                  });
                },
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _analyzeSleep,
                child: const Text('Analyze Sleep'),
              ),
              const SizedBox(height: 20),
              if (_predictedSleepHours != null) ...[
                Text(
                  'Predicted Sleep Hours: ${_predictedSleepHours!.toStringAsFixed(1)}',
                  style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 10),
                Text(
                  _analysisResult,
                  style: const TextStyle(fontSize: 16),
                  textAlign: TextAlign.center,
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}