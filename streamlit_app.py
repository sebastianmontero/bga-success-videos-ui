import streamlit as st
from services.success_videos_api import SuccessVideosApi

@st.cache_resource
def get_success_videos_api() -> SuccessVideosApi:
    return SuccessVideosApi(st.secrets.success_videos_api_base_url)


sv_api = get_success_videos_api()

@st.cache_data
def industries() -> dict:
    return sv_api.industries()

st.title("BGA Testimonios")

with st.form("search"):
  search_text = st.text_input("Busca testimonios por caso de uso", value="")
  industry = st.selectbox("Industria", industries(), index=None)
  num_results = st.text_input("Numero maximo de resultados", value="3")
  st.form_submit_button('Buscar')

if search_text:
    results = sv_api.search_success_videos(search_text, int(num_results), industry)
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
            st.caption(", ".join(metadata['speakers']))
