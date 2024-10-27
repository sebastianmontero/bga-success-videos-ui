import streamlit as st
from services.success_videos_api import SuccessVideosApi

st.set_page_config(
    page_title="BGA Testimonios",
)


@st.cache_resource
def get_success_videos_api() -> SuccessVideosApi:
    return SuccessVideosApi(st.secrets.success_videos_api_base_url)


sv_api = get_success_videos_api()

@st.cache_data
def industries() -> dict:
    return sv_api.industries()

st.title("BGA Testimonios")

# st.markdown("""
# <iframe src="https://player.vimeo.com/video/995195350" width="400px" height="225px" frameborder="0"></iframe>
# """, unsafe_allow_html=True)

with st.form("search"):
  search_text = st.text_input("Busca testimonios por caso de uso", value="")
  industry = st.selectbox("Industria", industries(), index=None)
  num_results = st.text_input("Numero maximo de resultados", value="3")
  st.form_submit_button('Buscar')

if search_text:
    results = sv_api.search_success_videos(search_text, int(num_results), industry)
    print(results)

N_results_per_row = 1
if search_text:
    for n_row, row in enumerate(results):
        metadata = row['metadata']
        i = n_row%N_results_per_row
        if i==0:
            st.write("---")
            num_cols = N_results_per_row*2
            cols = st.columns(num_cols, gap="large", vertical_alignment="center")
        # draw the card
        with cols[i*2]:
                st.caption(f"{metadata['industry'].strip()}")
                st.markdown(f"**{metadata['title'].strip()}**")
                st.caption(f"{row['page_content'].strip()}")
                st.markdown(f"*{metadata['client'].strip()}*")
                st.caption(f"{metadata['about'].strip()}")
                st.caption(", ".join(metadata['speakers']))
        
        with cols[i*2+1]:
                # Video iframe
                st.markdown(
                    f"""<iframe 
                        src="https://player.vimeo.com/video/{metadata['video_id']}?title=0&byline=0&portrait=0" 
                        width="100%" 
                        height="225px" 
                        frameborder="0"
                        style="margin-top: 1rem;"
                        allow="autoplay; fullscreen; picture-in-picture" 
                        allowfullscreen
                    ></iframe>""", 
                    unsafe_allow_html=True
                )
