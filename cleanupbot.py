import slack
import os
import time
import pytz
from datetime import datetime
from datetime import date
from datetime import datetime, timedelta

client = slack.WebClient(token=os.environ['slack_token'])
import pandas as pd

# Load the spreadsheet
schedule_path = 'Cleaning Schedule.xlsx'
cleaning_schedule_df = pd.read_excel(schedule_path)

# Display the first few rows of the dataframe to understand its structure
cleaning_schedule_df.head()
channel_users = {
    'U057PKCBZBQ': 'Arianna Dwomoh',
    'U0592EE72TB': 'Jess Chen',
    'U059XHEK5QE': 'Eleanor Mackey',
    'U059XJ35XCN': 'Kaitlyn Williams',
    'U059XM9JVC6': 'Elizabeth Lee',
    'U05A3E3S7EZ': 'Julie Mandimutsira',
    'U05A4ETNNQM': 'Gareth Kelleher',
    'U05A6D66A4T': 'Devin Downey',
    'U05A8LJS4UU': 'Stephen Kim',
    'U05AA4BT8F6': 'Haris Adnan',
    'U05AD38UN06': 'Jaden Rodriguez',
    'U05ADENDK7G': 'Nathaniel Drebin',
    'U05AF3TFGJG': 'Rajan Karsan',
    'U05AFUD0Y76': 'Aaditya Warrier',
    'U05AGRUBZ5F': 'George Grune',
    'U05AH06M1FB': 'Shelby Brown',
    'U05AKLB9C1F': 'Sean Smith',
    'U05AL3AHW73': 'Willow Kaplan',
    'U05AM9GTPFY': 'Sophia Li',
    'U05AUGKMZPG': 'Tomi Oderinde',
    'U05AUQM8CM6': 'Michelle Igbinadolor',
    'U05AVC80L7J': 'Ana Martinez',
    'U05AXSS1ZGQ': 'Cindy Zhang',
    'U05BUJCR07K': 'Aryan Nair',
    'U05C261F5K6': 'Erin Gleason',
    'U05CA7C6VP0': 'Sita Conde',
    'U05D30Y8SJC': 'Juliette Clark',
    'U06EMC9MJFR': 'Cleanup Bot'
}


def messageMe(user_id, date):
  formatted_date = date.strftime(
      "%A, %B %d, %Y")  # e.g., "Tuesday, January 30, 2024"
  message = f"Hello <@{user_id}>! You are scheduled to clean up the DUU Office tomorrow on {formatted_date}."
  client.chat_postMessage(channel='#clean-ups', text=message)




def run_scheduled_jobs():
  # Find the user IDs of next day's cleaners
  next_day_cleaners = find_next_days_cleaners(cleaning_schedule_df,
                                              channel_users)

  # Send a message to each cleaner
  for user_id in next_day_cleaners:
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_date = tomorrow.date()
    messageMe(user_id, tomorrow_date)


def get_channel_users(channel_id):
  # Fetch user IDs from the channel
  user_ids = client.conversations_members(channel=channel_id)

  # Dictionary to hold user ID and corresponding name
  user_details = {}

  # Fetch user details for each ID
  for user_id in user_ids['members']:
    user_info = client.users_info(user=user_id)
    # Assuming you want the real name
    real_name = user_info['user']['real_name']
    user_details[user_id] = real_name

  return user_details


# Function to find next day's cleaners
def find_next_days_cleaners(schedule_df, channel_users):
  # Get tomorrow's date
  tomorrow = datetime.now() + timedelta(days=1)
  tomorrow_date = tomorrow.date()

  # Initialize a list to hold the user IDs of next day's cleaners
  next_day_cleaners = []

  # Check both Tuesday and Friday schedules
  for day in ['Tuesdays', 'Fridays']:
    # Filter the schedule for tomorrow
    #print(schedule_df[day].dt.date)
    #ACTUAL CODE
    tomorrow_schedule = schedule_df[schedule_df[day].dt.date == tomorrow_date]
    #tues = date(2024, 1, 30)
    #tomorrow_schedule = schedule_df[schedule_df[day].dt.date == tues]

    # If there are cleaners scheduled for tomorrow
    if not tomorrow_schedule.empty:
      # Get the names of the cleaners
      cleaners = tomorrow_schedule[['Cleaner 1', 'Cleaner 2']].values.flatten()

      # Find corresponding user IDs from channel_users
      for cleaner in cleaners:
        # Handle cases with 'No Cleaning' or NaN
        if pd.isna(cleaner) or cleaner == 'No Cleaning':
          continue

        # Match the cleaner name with user ID (assuming exact match in names)
        user_id = [
            uid for uid, name in channel_users.items() if name == cleaner
        ]

        if user_id:
          next_day_cleaners.extend(user_id)

  return next_day_cleaners


def seconds_until_target(hour=8):

  now = datetime.now()
  target = datetime(now.year, now.month, now.day,
                    hour)  # Today at the target hour
  if now >= target:
    # If the time has passed for today, set target for the same time tomorrow
    target += timedelta(days=1)
  return (target - now).total_seconds()


# Find next day's cleaners (this will depend on the current date and might not return results if no match is found)
# next_day_cleaners = find_next_days_cleaners(cleaning_schedule_df, channel_users)
# next_day_cleaners

# Replace 'YOUR_CHANNEL_ID' with the actual channel ID
#channel_users = get_channel_users('C06FHLE9L5D')

print("Script started")

# Run once immediately in case the script starts right at the target time
run_scheduled_jobs()

while True:
  # Calculate sleep time until the next run (e.g., 8 AM tomorrow)
  sleep_time = seconds_until_target(8)  # For 8 AM, adjust as needed
  print(f"Sleeping for {sleep_time} seconds until the next check.")
  time.sleep(sleep_time)

  # Run scheduled jobs after waking up
  run_scheduled_jobs()
