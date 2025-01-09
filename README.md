Direct X Emailer

This Python script is designed to collect system information about DirectX, create an email with that information as an attachment, and send it via email. The email includes details like the sender and receiver's email, subject, and body. It also allows the user to securely save and load their email credentials using the keyring library.

Direct X report: dxdiag_report.txt
Log file: emailer.log

This project was completed using iOS mail.


The keyring library allows you to securely store and manage your email credentials. 
(Saved under Windows Credentials)


How do I run?

1) Verify that the keyring module is installed on your system.
pip install keyring.

2) Navigate to the project path and execute the script.

