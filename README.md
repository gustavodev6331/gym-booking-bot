# Selenium Gym Bot

A Selenium automation bot that logs into a gym booking website, automatically books Tuesday and Thursday 6:00 PM classes, joins the waitlist when classes are full, and verifies successful bookings.

<img width="2392" height="1398" alt="Kapture 2026-07-29 at 18 11 24" src="https://github.com/user-attachments/assets/fe975ae1-407c-467c-a006-6b7e3857034f" />


## Known limitation: 
This automation relies on the App Brewery demo gym website. If the demo site has no available classes, the script cannot complete the booking process because there are no booking cards to interact with.

## Features
- Automatic user login
- Automatic class booking
- Automatically joins the waitlist when classes are full
- Booking verification on the "My Bookings" page
- Retry mechanism for temporary website/network failures

## Technologies
- Python
- Selenium
- ChromeDriver
- python-dotenv

## Installation

1. Clone the repository

```bash
git clone https://github.com/gustavodev6331/gym-booking-bot.git
```

2. Navigate to the project folder

```bash
cd gym-booking-bot
```

3. Create a virtual environment

```bash
python -m venv .venv
```

4. Activate the virtual environment

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

5. Install the dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root and add the following variables:

```env
EMAIL=your_email@example.com
PASSWORD=your_password
```

6. Run the application

```bash
python main.py
```

On the first run, the project automatically creates a local Chrome profile inside the `chrome_profile/` directory to preserve the login session.


