import streamlit as st
import pandas as pd
from google_play_scraper import reviews, Sort
from time import sleep

def scrape_reviews_batched(app_id, count=400, lang='id', country='id', sort=Sort.NEWEST, filter_score_with=None):
    all_reviews_content = []
    collected_review_ids = set()

    for _ in range(210):  # Maximum number of batches to avoid infinite loops
        result, continuation_token = reviews(
            app_id,
            lang=lang,
            country=country,
            sort=sort,
            count=count,
            filter_score_with=filter_score_with,
            continuation_token=continuation_token  # Use continuation token for subsequent batches
        )

        for review in result:
            if review['reviewId'] not in collected_review_ids:
                all_reviews_content.append(review['content'])
                collected_review_ids.add(review['reviewId'])

        if not continuation_token:  # Stop when there are no more reviews
            break

        sleep(1)  # Sleep for a second to avoid rate limiting

    return all_reviews_content

def scrape_and_display_reviews(app_id, count=400):
    with st.spinner("Scraping Reviews..."):
        all_reviews = scrape_reviews_batched(app_id, count)

        if all_reviews:
            df = pd.DataFrame(all_reviews, columns=["Review Text"])
            st.success("Reviews Scraped Successfully!")
            st.dataframe(df)

            st.write(f"Total Reviews Scraped: {len(df)}")
        else:
            st.error("No reviews found.")

st.title("Google Play Review Scraper (Indonesia)")

app_id = st.text_input("Enter the App ID:", "com.example.app")
count = st.number_input("Number of Reviews to Scrape:", value=400, min_value=1)

if st.button("Start Scraping"):
    scrape_and_display_reviews(app_id, count)
