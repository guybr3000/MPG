# sourcery skip: use-named-expression
import streamlit as st
import pandas as pd
import random
import pyperclip
import glob
from PIL import Image

path = './prompts/*.csv'

# Get a list of all CSV files in the subfolder
csv_files = glob.glob(path)

# Create an empty dictionary to store the data
series_dict = {}

# Loop through the list of CSV files
for file in csv_files:
    file_name = file.removeprefix('./prompts\\')
    file_name = file_name.removesuffix('.csv')
    series_dict[file_name] = pd.read_csv(file, encoding='latin',engine='python')

######################################################################################################
######################################################################################################
######################################################################################################


st.set_page_config(
    page_title="Midjourney Prompt Generator",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "This app was originaly written by Guy Bramson, feel free to use and develop further.",
        'Get help':"https://docs.midjourney.com/docs/models"
    }
)

st.title('Midjourney Prompt Generator',anchor=False)

col1, col2,col3 = st.columns(3)

with col1:
    option_0 = st.checkbox('Positive Free Text')
    if option_0:
        free_text = st.text_input('pos',label_visibility='collapsed')
    option_7 = st.checkbox('Negative Free Text')
    if option_7:
        neg_text = st.text_input('neg',label_visibility='collapsed',key=2)
    st.subheader("Random Prompt Components:", anchor=False)
    option_1 = st.checkbox('Words')
    if option_1:
        multi = st.slider('How many words ?', 1, 50, 1)
    option_2 = st.checkbox('Colors')
    option_3 = st.checkbox('Style')
    option_4 = st.checkbox('Nonsense Style')
    option_5 = st.checkbox('Lighting')
    option_6 = st.checkbox('Artist')
    st.subheader("Parameters:", anchor=False)
    param_1 = st.checkbox('Chaos')
    if param_1:
        multi_chaos = st.slider('Chaos value:', 0, 100, 0)
    param_2 = st.checkbox('Quality')
    if param_2:
        multi_quality = st.slider('Quality value:', 0.25, 1.0, 1.0,step=0.25)
    param_3 = st.checkbox('Stylize')
    if param_3:
        multi_style = st.slider('Style value:', 0, 1000, 100)
    param_4 = st.checkbox('Tile')
    param_5 = st.checkbox('Seed')
    if param_5:
        param_5_1 = st.checkbox('o--> Use sameseed')
        multi_seed = st.number_input('Insert a number between 0 to 4,294,967,295',min_value=0,max_value=4294967295,value=123)
    param_6 = st.checkbox('Aspect Ratio')
    if param_6:
        option_selected_ar = st.selectbox('Select aspect ratio (width : height)', ('3:2','2:3','4:3','3:4','5:4','4:5','7:4','4:7','16:9','9:16','3:1'))
    param_7 = st.checkbox('Model')
    if param_7:        
        option_selected_ver = st.selectbox('Select model version', ('v 5','v 4','v 4 --style 4a','v 4 --style 4b','v 4 --style 4c','v 3','v 2','v 1','niji','niji 5','niji 5 --style expressive','niji 5 --style cute','test','testp','test --creative','testp --creative'))
    param_8 = st.checkbox('Stop')
    if param_8:
        multi_stop = st.slider('Stop value:', 10, 100, 100,step=10)
    param_9 = st.checkbox('Upscaler')
    if param_9:
        multi_ups = st.radio("Upscaler :red[(_Do not use with version 5_)]",('Light Upscaler', 'Beta Upscaler', 'Anime Upscaler'))
    result_text = ""

if st.button('Generate'):
    selected_components = []
    selected_options = []
    if option_0:
        selected_components.append(free_text)
    if option_1:
        for _ in range(multi):
            random_answer = series_dict['prompts_words'].iat[random.randint(0, len(series_dict['prompts_words'])-1),0]
            selected_components.append(random_answer)
    if option_2:
        random_answer = series_dict['prompts_colors'].iat[random.randint(0, len(series_dict['prompts_colors'])-1),0]
        selected_components.append(random_answer)
    if option_3:
        random_answer = series_dict['prompts_styles'].iat[random.randint(0, len(series_dict['prompts_styles'])-1),0]
        selected_components.append(random_answer)
    if option_4:
        random_answer = series_dict['prompts_nonsense_styles'].iat[random.randint(0, len(series_dict['prompts_nonsense_styles'])-1),0]
        selected_components.append(random_answer)
    if option_5:
        random_answer = series_dict['prompts_lighting'].iat[random.randint(0, len(series_dict['prompts_lighting'])-1),0]
        selected_components.append(random_answer)
    if option_6:
        random_answer = series_dict['prompts_artists'].iat[random.randint(0, len(series_dict['prompts_artists'])-1),0]
        selected_components.append('by '+random_answer)
    if param_1:
        answer = multi_chaos
        selected_options.append(f'--c {str(answer)}')
    if param_2:
        answer = multi_quality
        selected_options.append(f'--q {str(answer)}')
    if param_3:
        answer = multi_style
        selected_options.append(f'--s {str(answer)}')
    if param_4:
        selected_options.append('--tile')
    if param_5:
        answer = multi_seed
        if param_5_1:
            selected_options.append(f'--sameseed {str(answer)}')
        else: 
            selected_options.append(f'--seed {str(answer)}')
    if param_6:
        answer = option_selected_ar
        selected_options.append(f'--ar {str(answer)}')
    if param_7:
        answer = option_selected_ver
        selected_options.append(f'--{str(answer)}')
    if param_8:
        answer = multi_stop
        selected_options.append(f'--stop {str(answer)}')
    if param_9:
        if multi_ups == 'Light Upscaler':
            selected_options.append('--uplight')    
        elif multi_ups == 'Beta Upscaler':
            selected_options.append('--upbeta')
        elif multi_ups == 'Anime Upscaler':
            selected_options.append('--upanime')
    if option_7:
        selected_options.append('--no '+ neg_text)
    if selected_components or selected_options:
        result_text = f"/imagine prompt: {', '.join(selected_components)} {' '.join(selected_options)}"
        result = st.code (result_text,language='csv',line_numbers=False)
        st.session_state['key'] = result_text


    
        
if 'key' not in st.session_state:
    st.session_state['key'] = result_text



with col3:
    image = Image.open('./images/back.png')
    st.image(image)

if st.button('Copy'):
    pyperclip.copy(st.session_state.key)
    st.write("Text copied to clipboard!")
    