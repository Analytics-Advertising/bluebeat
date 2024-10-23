import 'package:flutter/material.dart';

class MultiStepForm extends StatefulWidget {
  @override
  _MultiStepFormState createState() => _MultiStepFormState();
}

class _MultiStepFormState extends State<MultiStepForm> {
  PageController _controller = PageController();
  int _currentStep = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Multi-Step Form"),
      ),
      body: PageView(
        controller: _controller,
        physics: NeverScrollableScrollPhysics(),
        onPageChanged: (index) {
          setState(() {
            _currentStep = index;
          });
        },
        children: [
          _buildPersonalInformationStep(),
          _buildPastExperienceStep(),
        ],
      ),
      bottomNavigationBar: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            if (_currentStep > 0)
              ElevatedButton(
                onPressed: () {
                  _controller.previousPage(
                    duration: Duration(milliseconds: 300),
                    curve: Curves.easeInOut,
                  );
                },
                child: Text("Back"),
              ),
            ElevatedButton(
              onPressed: () {
                if (_currentStep < 1) {
                  _controller.nextPage(
                    duration: Duration(milliseconds: 300),
                    curve: Curves.easeInOut,
                  );
                } else {
       
                }
              },
              child: Text(_currentStep < 1 ? "Next" : "Submit"),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPersonalInformationStep() {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: ListView(
        children: [
          Text(
            "Personal Information",
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 10),
          TextField(
            decoration: InputDecoration(labelText: "First Name"),
          ),
          TextField(
            decoration: InputDecoration(labelText: "Last Name"),
          ),
          TextField(
            decoration: InputDecoration(labelText: "Email"),
          ),
          TextField(
            decoration: InputDecoration(labelText: "Phone Number"),
          ),
          TextField(
            decoration: InputDecoration(labelText: "Alternative Phone Number"),
          ),
          TextField(
            decoration: InputDecoration(labelText: "ID Number/Passport"),
          ),
          TextField(
            decoration: InputDecoration(labelText: "Direct Phone Number"),
          ),
          SizedBox(height: 10),
          Text(
            "Delivery Address",
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          TextField(
            decoration: InputDecoration(labelText: "Street Address"),
          ),
          TextField(
            decoration: InputDecoration(labelText: "City/Town"),
          ),
          TextField(
            decoration: InputDecoration(labelText: "Suburb"),
          ),
          DropdownButtonFormField(
            decoration: InputDecoration(labelText: "Province"),
            items: ["Province 1", "Province 2", "Province 3"]
                .map((String province) {
              return DropdownMenuItem(
                value: province,
                child: Text(province),
              );
            }).toList(),
            onChanged: (value) {},
          ),
          TextField(
            decoration: InputDecoration(labelText: "Postal Code"),
          ),
        ],
      ),
    );
  }

  Widget _buildPastExperienceStep() {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: ListView(
        children: [
          Text(
            "Past Experience/Distribution",
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 10),
          DropdownButtonFormField(
            decoration: InputDecoration(
                labelText:
                    "Do you have experience in the Prepaid Sim-Card Industry?"),
            items: ["Yes", "No"].map((String answer) {
              return DropdownMenuItem(
                value: answer,
                child: Text(answer),
              );
            }).toList(),
            onChanged: (value) {},
          ),
          TextField(
            decoration: InputDecoration(
                labelText: "If you do have experience, please explain"),
          ),
          TextField(
            decoration: InputDecoration(
                labelText:
                    "What other starter pack distribution companies did you work for previously?"),
          ),
          CheckboxListTile(
            title: Text("Shop-to-Shop"),
            value: false,
            onChanged: (bool? value) {},
          ),
          CheckboxListTile(
            title: Text("Promotions"),
            value: false,
            onChanged: (bool? value) {},
          ),
          CheckboxListTile(
            title: Text("On-Demand"),
            value: false,
            onChanged: (bool? value) {},
          ),
          CheckboxListTile(
            title: Text("Other"),
            value: false,
            onChanged: (bool? value) {},
          ),
        ],
      ),
    );
  }
}
