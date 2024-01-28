# Slack Cleanup Reminder Bot

## Introduction
This Slack bot is designed to send automated reminders to specific users in a Slack channel about upcoming cleaning duties. The reminders are based on a predefined schedule, ensuring that users are notified a day before their scheduled cleanup task.

## Features
- **Automated Reminders**: Sends out daily reminders to users scheduled for cleaning duties the next day.
- **Customizable Schedule**: Works with a user-defined cleaning schedule.
- **Personalized Notifications**: Directly mentions users in reminders for a personalized touch.

## Prerequisites
Before you start using this bot, make sure you have:
- Python 3.x installed.
- Access to a Slack workspace where you have permissions to create and manage apps.

## Installation
1. **Clone the Repository**:git clone https://github.com/yourgithubusername/slack-cleanup-reminder-bot.git
cd slack-cleanup-reminder-bot

2. **Install Dependencies**:
pip install -r requirements.txt

3. **Set Up Slack App**:
- Go to the [Slack API](https://api.slack.com/apps) and create a new app.
- Add necessary bot permissions (`chat:write`, `users:read`, `channels:read`, `groups:read`).
- Install the app to your workspace and copy the Bot User OAuth Token.

4. **Configure Environment Variables**:
- Create a `.env` file in the project root and add your Slack Bot Token:
  ```
  SLACK_TOKEN=your_slack_bot_token_here
  ```

## Usage
1. Update the cleaning schedule in `Cleaning Schedule.xlsx` according to your requirements.
2. Run the bot: python bot.py

   
## Contributing
Contributions to improve the bot are welcome. Please feel free to fork the repository, make changes, and submit pull requests.

## License
This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code as you see fit.

