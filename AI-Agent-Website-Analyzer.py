import requests
import time
import openai
from prompt import generate_prompt  # Ensure `generate_prompt` is defined in prompt.py
import os
import streamlit as st

# Set up Streamlit app title
st.title("Autonomous AI Agent - Website Metrics Auditor")

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_PERSONAL_KEY")


def get_website_metrics(url):
    """Fetches various metrics from a URL."""
    metrics = {
        "response_time": None,
        "status_code": None,
        "page_size": None,
        "load_time": None,
        "redirect_count": 0,
        "content_type": None
    }

    start = time.time()
    try:
        response = requests.get(url, allow_redirects=True)
        end = time.time()

        metrics["response_time"] = end - start
        metrics["status_code"] = response.status_code
        metrics["page_size"] = len(response.content)
        metrics["load_time"] = response.elapsed.total_seconds()
        metrics["redirect_count"] = len(response.history)
        metrics["content_type"] = response.headers.get("Content-Type", "Unknown")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching {url}: {e}")

    return metrics


def ask_gpt(prompt):
    """Sends a prompt to GPT and returns the response."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            timeout=10000
        )
        # Get the raw content from the response
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"Error interacting with GPT: {e}")
        return None


def analyze_website(url):
    """Analyzes website metrics using GPT."""
    metrics = get_website_metrics(url)

    if metrics["response_time"] is None:
        st.error("Failed to retrieve metrics.")
        return None

    # Generate the prompt with all metrics
    prompt = generate_prompt(
        metrics["response_time"],
        url,
        metrics["status_code"],
        metrics["page_size"],
        metrics["load_time"],
        metrics["redirect_count"],
        metrics["content_type"]
    )

    # Send the prompt to GPT and get the analysis
    gpt_response = ask_gpt(prompt)

    if gpt_response:
        return metrics, gpt_response
    else:
        return metrics, "GPT analysis unavailable."


# Streamlit input field for URL
url = st.text_input("Enter the URL to analyze", value="https://www.amazon.com")

# Button to trigger the analysis
if st.button("Analyze Website"):
    with st.spinner("Analyzing..."):
        metrics, gpt_analysis = analyze_website(url)

        if metrics:
            st.subheader("Website Metrics")
            st.write(f"**URL**: {url}")
            st.write(f"**Response Time**: {metrics['response_time']:.2f} seconds")
            st.write(f"**Status Code**: {metrics['status_code']}")
            st.write(f"**Page Size**: {metrics['page_size']} bytes")
            st.write(f"**Load Time**: {metrics['load_time']:.2f} seconds")
            st.write(f"**Redirect Count**: {metrics['redirect_count']}")
            st.write(f"**Content Type**: {metrics['content_type']}")

            st.subheader("GPT Analysis")
            st.write(gpt_analysis)
