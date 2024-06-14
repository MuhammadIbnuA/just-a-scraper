import streamlit as st
from google_play_scraper import Sort, reviews
from time import sleep
from googletrans import Translator

def scrape_reviews_batched(app_id, count=25000, lang='id', country='id', sort=Sort.NEWEST, filter_score_with=None):
    all_reviews_content = []
    collected_review_ids = set()

    for _ in range(1000):
        result, continuation_token = reviews(
            app_id,
            lang=lang,
            country=country,
            sort=sort,
            count=count,
            filter_score_with=filter_score_with
        )

        for review in result:
            if review['reviewId'] not in collected_review_ids:
                all_reviews_content.append(review['content'])
                collected_review_ids.add(review['reviewId'])

        if not continuation_token:
            break

        sleep(1)  # Be polite to Google's servers

    return all_reviews_content

def translate_reviews(reviews):
    translator = Translator()
    translated_reviews = [translator.translate(review, src='auto', dest='en').text for review in reviews]
    return translated_reviews

def main():
    st.title("Google Play Review Scraper & Translator")

    app_id = st.text_input("Enter the Google Play Store app ID:")
    count = st.number_input("Enter the number of reviews to fetch per batch (max 400):", value=100, min_value=1, max_value=25000)

    if st.button("Scrape and Translate Reviews"):
        with st.spinner("Scraping and translating reviews..."):
            original_reviews = scrape_reviews_batched(app_id, count=count)
            translated_reviews = translate_reviews(original_reviews)

        st.subheader("Original Reviews:")
        st.dataframe(original_reviews)

        st.subheader("Translated Reviews (English):")
        st.dataframe(translated_reviews)

if __name__ == "__main__":
    main()
