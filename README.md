# WhatsApp Chat Analyzer

A Streamlit-based analytics app for WhatsApp chat exports. Upload a WhatsApp text chat file and explore messaging statistics, timelines, activity maps, word clouds, and emoji trends for the whole group or individual participants.

## Project Structure

- `app.py` — Streamlit application UI and analytics dashboard.
- `preprocessor.py` — Parses the raw WhatsApp export text and builds a cleaned DataFrame.
- `helper.py` — Computes statistics, timelines, word clouds, activity heatmaps, and emoji analysis.
- `requirements.txt` — Python dependencies required to run the app.

## Workflow Overview

1. User exports a WhatsApp chat as a text file from the WhatsApp mobile app.
2. The exported `.txt` file is uploaded into the Streamlit interface in `app.py`.
3. `app.py` reads the uploaded file bytes and decodes them to UTF-8.
4. `preprocessor.preprocess(data)` converts the raw chat into a pandas DataFrame:
   - splits timestamp and message content
   - extracts sender name and message text
   - builds columns for date, time, user, month, day, and hourly period
5. The app builds a user selection list from the DataFrame and adds an `Overall` option.
6. When `Show Analysis` is clicked, `helper.py` functions compute the analytics:
   - total messages, words, media shares, and links
   - monthly and daily timelines
   - busiest day / month activity maps
   - weekly activity heatmap
   - group-level busiest users chart when `Overall` is selected
   - word cloud and most common words (using stop-word filtering)
   - emoji frequency and top emoji distribution
7. The results are rendered in Streamlit with charts, tables, and summary metrics.

## Setup Instructions

```bash
cd d:\WhatsappChatAnalyzer
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Dependencies

The app requires the following Python packages:

- `streamlit`
- `matplotlib`
- `seaborn`
- `urlextract`
- `wordcloud`
- `pandas`
- `emoji`

Install them all with:

```bash
pip install -r requirements.txt
```

## Expected Input Format

The preprocessor expects WhatsApp chat text in the standard exported format:

```
23/05/2024, 09:42 - Alice: Hello everyone!
23/05/2024, 09:43 - Bob: Hi Alice 👋
```

Important notes:

- The date/time parsing pattern is `dd/mm/yyyy, HH:MM - `.
- Group notifications without a sender are tagged as `group_notification`.
- Media messages appear as `<Media omitted>\n` and are counted separately.

## Running the App

1. Start Streamlit with `streamlit run app.py`.
2. Open the local URL shown in the terminal.
3. Upload your WhatsApp chat export file.
4. Select `Overall` or a specific user from the sidebar.
5. Click `Show Analysis`.
6. Review the dashboards and charts.

## Analytics Available

- Top statistics: total messages, total words, media shared, links shared
- Monthly message volume timeline
- Daily message volume timeline
- Busy day and busy month activity maps
- Weekly activity heatmap
- Group busiest users leaderboard (Overall view)
- Word cloud visualization
- Top common words
- Emoji frequency and top emoji pie chart

## Notes and Tips

- A stop-word file such as `stop_hinglish.txt` is required by the word cloud and most-common-word analysis. Place it in the project root or update `helper.py` if you want to use a different stop-word list.
- If your WhatsApp export contains a different timestamp format, the parser in `preprocessor.py` may need adjustment.
- The group-level busiest user analytics are intended to work when `Overall` is selected.

## File Details

### `preprocessor.py`
- Uses regex to split messages and timestamps
- Builds a DataFrame with columns: `date`, `user`, `message`, `only_date`, `year`, `month_num`, `month`, `day`, `day_name`, `hour`, `minute`, `period`

### `helper.py`
- `fetch_stats(selected_user, df)` — summary metrics
- `monthly_timeline(selected_user, df)` — month-based message counts
- `daily_timeline(selected_user, df)` — date-based message counts
- `week_activity_map(selected_user, df)` — messages by weekday
- `month_activity_map(selected_user, df)` — messages by month name
- `activity_heatmap(selected_user, df)` — weekday vs hour message heatmap
- `create_wordcloud(selected_user, df)` — generates a word cloud image
- `most_common_words(selected_user, df)` — returns top words excluding stop words
- `emoji_helper(selected_user, df)` — returns emoji frequency counts

### `app.py`
- Builds the Streamlit sidebar and upload interface
- Loads and preprocesses chat text
- Displays the analytics dashboard

## Troubleshooting

- If the app fails to start, verify the virtual environment is active and `requirements.txt` packages are installed.
- If charts are blank or errors occur, confirm the uploaded file is a valid WhatsApp export text file.
- Ensure the stop-word file exists if the word cloud or common word chart fails.

## Contribution

Feel free to extend the analyzer with additional features such as:
- sentiment analysis
- chat participant comparison
- phrase frequency over time
- exportable reports
- support for multiple languages and character encodings
