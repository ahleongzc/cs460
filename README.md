# Motion Sensor Test Project

This project involves testing a motion sensor by running a Python script in a virtual environment. Follow the steps below to set up the environment, install the required dependencies, and run the test.

## Requirements

Before running the script, ensure you have the following:

- Python 3.x installed on your system
- `pip` for managing Python packages

## Setup Instructions

1. **Install repo**

   If you haven't already, clone the repository to your local machine.

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

   python3 -m venv venv

    venv\Scripts\activate

    pip install -r requirements.txt

2. **Run python scripts** (on raspiberry pi)

      python src/motion_sensor_test.py


3. **Telegram server** (on laptop)
   
   Terminal cmd: node-red
   
   Import the flows.json into node-red
   
4. **Facial regonition process** (on laptop)

   python3 main.py

   Start the process by sending /start to Telegram bot
   
