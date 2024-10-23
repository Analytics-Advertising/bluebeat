import 'package:flutter/material.dart';
import 'package:blue_beat_digital/screens/commercials.dart';
import 'package:blue_beat_digital/screens/dashboard.dart';
import 'package:blue_beat_digital/screens/splash.dart';
import 'package:blue_beat_digital/screens/agreementPage.dart';

class VerificationPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Verification Documents'),
        backgroundColor: Colors.blue,
      ),
      drawer: Drawer(
        child: ListView(
          children: <Widget>[
            DrawerHeader(
              decoration: BoxDecoration(
                color: Colors.blue,
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Image.asset(
                    'assets/logo-white.png',
                    height: 60,
                  ),
                  SizedBox(height: 10),
                  const Text(
                    "BLUEBEAT DIGITAL",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
            ListTile(
              leading: Icon(Icons.home),
              title: Text('My Home'),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => DashboardPage()),
                );
              },
            ),
            ListTile(
              leading: Icon(Icons.attach_money),
              title: Text('My Commercials'),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => CommercialsPage()),
                );
              },
            ),
            ListTile(
              leading: Icon(Icons.description),
              title: Text('Reseller & Rica Agreement'),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => AgreementPage()),
                );
              },
            ),
            ListTile(
              leading: Icon(Icons.verified),
              title: Text('Verification Documents'),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => VerificationPage()),
                );
              },
            ),
            Divider(),
            ListTile(
              leading: Icon(Icons.logout),
              title: Text('Logout'),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => SplashScreen()),
                );
              },
            ),
          ],
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: SingleChildScrollView(
          child: Column(
            children: [
              VerificationItem(
                title: 'ID Document/Passport',
                description:
                    'A clear scanned colour copy of your ID, such as a valid passport, driving license, ID book or both sides of an ID card.',
                buttonText: 'Choose file',
              ),
              SizedBox(height: 10),
              VerificationItem(
                title: 'Proof of bank account',
                description:
                    'A clear scanned or digital document as proof of bank account showing your name and bank account number, like a bank statement issued in the last 3 months or a confirmation letter from your bank.',
                buttonText: 'Choose file',
              ),
              SizedBox(height: 10),
              VerificationItem(
                title: 'Proof of residence',
                description:
                    'A clear scanned or digital document as proof of physical address, such as the first page of a lease agreement, or another official document.',
                buttonText: 'Choose file',
              ),
              SizedBox(height: 10),
              VerificationItem(
                title: 'Live Photo',
                description:
                    'A clear live photo of you holding your ID card/Passport, clearly showing an image of you from the ID/Passport.',
                buttonText: 'Take a picture',
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
           
                },
                child: Text('Submit'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class VerificationItem extends StatelessWidget {
  final String title;
  final String description;
  final String buttonText;

  VerificationItem({
    required this.title,
    required this.description,
    required this.buttonText,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      CircleAvatar(
                        backgroundColor: Colors.blue,
                        child: Icon(
                          Icons.description,
                          color: Colors.white,
                        ),
                      ),
                      SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          title,
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: 10),
                  Text(
                    description,
                    style: TextStyle(color: Colors.grey[600]),
                  ),
                ],
              ),
            ),
            TextButton(
              onPressed: () {
              },
              style: TextButton.styleFrom(
                backgroundColor: Colors.grey[200],
                padding: EdgeInsets.symmetric(horizontal: 12, vertical: 10),
              ),
              child: Text(buttonText),
            ),
          ],
        ),
      ),
    );
  }
}
