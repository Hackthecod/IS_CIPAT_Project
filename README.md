🔐 Secure E-Voting System

A Secure E-Voting System developed using Python and Streamlit as an Information Security project. The system demonstrates how an electronic voting application can be designed with security principles such as authentication, vote confidentiality, integrity, and controlled access.

📌 Project Overview

The Secure E-Voting System provides a simple web-based platform for conducting elections electronically. It allows authorized users to participate in an election while applying basic information-security concepts to protect the voting process.

The project is designed for educational and demonstration purposes and can be extended with a database and stronger cryptographic mechanisms for real-world applications.

✨ Features

🔑 User authentication
🗳️ Electronic voting interface
👤 Voter verification
🔒 Basic security mechanisms
📊 Vote/result display
🚫 Prevention of unauthorized access
🖥️ Interactive Streamlit web interface
📁 No external database required in the current version
🛡️ Information Security Concepts

The project demonstrates the following security principles:

Confidentiality – Helps protect voter-related information.
Integrity – Attempts to ensure that votes are not improperly modified.
Authentication – Restricts voting functionality to authorized users.
Authorization – Controls access to different system functions.
Availability – Provides a simple web-based voting interface through Streamlit.
Accountability – Provides a basis for tracking actions within the application.

🏗️ Technologies Used

Python
Streamlit
Python security/cryptography libraries where applicable
Session state / in-memory storage

No database

📂 Project Structure
secure-e-voting-system/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Required Python packages
├── README.md              # Project documentation
│
├── assets/                # Images or other resources
└── modules/               # Optional security/application modules


The structure can be modified according to the actual files in your project.

⚙️ Installation
1. Clone the repository
git clone <your-repository-url>
cd secure-e-voting-system

2. Create a virtual environment
python -m venv venv

3. Install dependencies
pip install -r requirements.txt

▶️ Running the Application

Start the Streamlit application using:

streamlit run app.py



🔐 Security Considerations

The system is intended as an academic prototype, not as a production-ready election platform.

Important considerations for future development include:

Secure password hashing
Strong authentication and authorization
Encryption of sensitive information
Secure vote storage
Protection against duplicate voting
Input validation
Audit logging
Protection against common web vulnerabilities
Secure key management
