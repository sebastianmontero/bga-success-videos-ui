import streamlit as st

import requests
from typing import Optional

def make_post_request(
    endpoint: str,
    input_text: str,
    k: int,
    industry: Optional[str] = None
) -> dict:
    """
    Make a POST request to the specified endpoint with the given parameters.

    Args:
        endpoint (str): The URL of the endpoint to send the POST request to.
        input_text (str): The input text for the request.
        k (int): The number of results to return.
        industry (Optional[str]): The industry to filter by. If None or empty, no filter is applied.

    Returns:
        dict: The JSON response from the API.

    Raises:
        requests.RequestException: If there's an error with the request.
    """
    # Prepare the base request body
    body = {
        "input": input_text,
        "config": {
            "configurable": {
                "search-parameters": {
                    "k": k
                }
            }
        }
    }

    # Add the industry filter if provided
    if industry:
        body["config"]["configurable"]["search-parameters"]["filter"] = {
            "must": [
                {
                    "key": "metadata.industry",
                    "match": {
                        "value": industry
                    }
                }
            ]
        }

    try:
        # Make the POST request
        response = requests.post(endpoint, json=body)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()["output"]
    except requests.RequestException as e:
        # Log the error (you might want to use a proper logging system in a real app)
        print(f"Error making POST request: {e}")
        raise

st.title("BGA Testimonios")

with st.form("search"):
  search_text = st.text_input("Busca testimonios por caso de uso", value="")
  industry = st.selectbox("Industria", ["", "Agricultura", "Finanzas"])
  num_results = st.text_input("Numero maximo de resultados", value="3")
  st.form_submit_button('Search')

if search_text:
    results = make_post_request("http://127.0.0.1:8000/search_success_videos_chain/invoke", search_text, int(num_results), industry)
    print(results)

N_cards_per_row = 3
if search_text:
    for n_row, row in enumerate(results):
        metadata = row['metadata']
        i = n_row%N_cards_per_row
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="large")
        # draw the card
        with cols[n_row%N_cards_per_row]:
            st.caption(f"{metadata['industry'].strip()}")
            st.markdown(f"**{metadata['title'].strip()}**")
            st.markdown(f"*{metadata['client'].strip()}*")
            st.caption(f"{row['page_content'].strip()}")
            st.markdown(f"**http://bga.com/{metadata['source']}**")
