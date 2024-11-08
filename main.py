import os
import time

import openai
import requests

from prompt import generate_prompt  # Ensure `generate_prompt` is defined in prompt.py

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
        print(f"Error fetching {url}: {e}")

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
        print(f"Error interacting with GPT: {e}")
        return None


def analyze_website(url):
    """Analyzes website metrics using GPT."""
    metrics = get_website_metrics(url)

    if metrics["response_time"] is None:
        print("Failed to retrieve metrics.")
        return

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
        print("GPT Analysis:", gpt_response)


if __name__ == "__main__":
    url = "https://www.amazon.com"  # Replace with the target URL
    analyze_website(url)
