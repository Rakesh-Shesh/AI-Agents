def generate_prompt(response_time, url, status_code, page_size, load_time, redirect_count, content_type):
    return f"""
    Analyze the following website performance metrics:

    - **URL**: {url}
    - **Response Time**: {response_time:.2f} seconds
    - **Status Code**: {status_code}
    - **Page Size**: {page_size} bytes
    - **Load Time**: {load_time:.2f} seconds
    - **Redirect Count**: {redirect_count}
    - **Content Type**: {content_type}

    Based on these metrics, provide an assessment of the Website SEO, website's performance, potential bottlenecks, and any suggestions for optimization.
    """
