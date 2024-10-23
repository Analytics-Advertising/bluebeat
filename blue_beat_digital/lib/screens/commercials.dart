import 'package:flutter/material.dart';
import 'package:blue_beat_digital/screens/agreementPage.dart';
import 'package:blue_beat_digital/screens/dashboard.dart';
import 'package:blue_beat_digital/screens/splash.dart';
import 'package:blue_beat_digital/screens/verificationPage.dart';

class CommercialsPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('My Commercials'),
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
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Commercials',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 20),
            Card(
              child: ListTile(
                leading: CircleAvatar(
                  backgroundColor: Colors.blue,
                  child: Icon(
                    Icons.description,
                    color: Colors.white,
                  ),
                ),
                title: Text(
                  'Free Stock 2',
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                subtitle: Text('commercial Schedule'),
                trailing: Icon(Icons.arrow_forward),
                onTap: () {
                  
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
