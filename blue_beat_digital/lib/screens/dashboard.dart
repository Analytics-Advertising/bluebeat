import 'package:flutter/material.dart';
import 'package:blue_beat_digital/screens/commercials.dart';
import 'package:blue_beat_digital/screens/agreementPage.dart';
import 'package:blue_beat_digital/screens/verificationPage.dart';
import 'package:blue_beat_digital/screens/splash.dart';

class DashboardPage extends StatefulWidget {
  @override
  _DashboardPageState createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(''),
        backgroundColor: Colors.blue,
        actions: const [
          Padding(
            padding: EdgeInsets.only(right: 20.0),
            child: Row(
              children: [
                Icon(Icons.person),
                SizedBox(width: 5),
                Text("Rotondwa Muthelo"),
              ],
            ),
          ),
        ],
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
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            AlertBox(
              message:
                  'Action Required! Please select your commercial schedule under the Commercial Schedule section.',
              color: Colors.amber[100],
              textColor: Colors.brown,
            ),
            SizedBox(height: 10),
            AlertBox(
              message:
                  'Important! You need to agree to both the Rica and Reseller Agreement before proceeding.',
              color: Colors.amber[100],
              textColor: Colors.brown,
            ),
            SizedBox(height: 10),
            AlertBox(
              message:
                  'Reminder! Please submit your documents under the Unverified Documents tab.',
              color: Colors.amber[100],
              textColor: Colors.brown,
            ),
          ],
        ),
      ),
    );
  }
}

class AlertBox extends StatelessWidget {
  final String message;
  final Color? color;
  final Color? textColor;

  AlertBox({required this.message, this.color, this.textColor});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(10.0),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(8.0),
      ),
      child: Row(
        children: [
          Icon(Icons.warning, color: textColor),
          SizedBox(width: 10),
          Expanded(
            child: Text(
              message,
              style: TextStyle(color: textColor, fontWeight: FontWeight.bold),
            ),
          ),
          IconButton(
            icon: Icon(Icons.close, color: textColor),
            onPressed: () {
              // Add functionality to remove alert if needed
            },
          ),
        ],
      ),
    );
  }
}
