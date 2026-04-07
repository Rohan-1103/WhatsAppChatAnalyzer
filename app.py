import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    
    df = preprocessor.preprocess(data)

    # user list
    user_list = df['user'].dropna().unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        # ================= STATS =================
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Messages", num_messages)
        col2.metric("Total Words", words)
        col3.metric("Media Shared", num_media_messages)
        col4.metric("Links Shared", num_links)

        # ================= MONTHLY TIMELINE =================
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)

        if not timeline.empty:
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'])
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.warning("No monthly data available.")

        # ================= DAILY TIMELINE =================
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)

        if not daily_timeline.empty:
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'])
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.warning("No daily data available.")

        # ================= ACTIVITY MAP =================
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        # Most busy day
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)

            if not busy_day.empty:
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values)
                plt.xticks(rotation=45)
                st.pyplot(fig)
            else:
                st.warning("No data available.")

        # Most busy month
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)

            if not busy_month.empty:
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values)  # FIXED
                plt.xticks(rotation=45)
                st.pyplot(fig)
            else:
                st.warning("No data available.")

        # ================= HEATMAP =================
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)

        if user_heatmap.empty or user_heatmap.isnull().all().all():
            st.error("No activity data available to generate heatmap.")
        else:
            fig, ax = plt.subplots()
            sns.heatmap(user_heatmap.fillna(0), ax=ax)
            st.pyplot(fig)

        # ================= BUSY USERS =================
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_user(df)

            col1, col2 = st.columns(2)

            with col1:
                if not x.empty:
                    fig, ax = plt.subplots()
                    ax.bar(x.index, x.values)
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                else:
                    st.warning("No user data.")

            with col2:
                st.dataframe(new_df)

        # ================= WORD CLOUD =================
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)

        if df_wc is not None:
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.warning("Not enough data for wordcloud.")

        # ================= MOST COMMON WORDS =================
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)

        if most_common_df is not None and not most_common_df.empty:
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1])
            st.pyplot(fig)
        else:
            st.warning("No common words found.")

        # ================= EMOJI ANALYSIS =================
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            if not emoji_df.empty:
                st.dataframe(emoji_df)
            else:
                st.warning("No emojis found.")

        with col2:
            if not emoji_df.empty:
                fig, ax = plt.subplots()
                ax.pie(
                    emoji_df['count'].head(),
                    labels=emoji_df['emoji'].head(),
                    autopct="%.2f%%"
                )
                st.pyplot(fig)
            else:
                st.warning("No emoji data to visualize.")
