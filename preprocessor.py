import re
import pandas as pd

def preprocess(data):
    # ✅ FIXED regex (handles AM/PM + 2/4 digit year)
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?[ap]m)?\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # 🧠 robust datetime parsing
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    df['message_date'] = df['message_date'].str.replace(' - ', '', regex=False)
    df['date'] = pd.to_datetime(df['message_date'], dayfirst=True, errors='coerce')

    df.drop(columns=['message_date'], inplace=True)

    # ---------------- USERS & MESSAGES ----------------
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # ---------------- TIME FEATURES ----------------
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # ---------------- PERIOD ----------------
    period = []
    for hour in df['hour']:
        if pd.isna(hour):
            period.append(None)
        elif hour == 23:
            period.append("23-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour+1}")

    df['period'] = period

    # 🔥 FINAL CLEANUP
    df = df.dropna(subset=['date'])

    return df
