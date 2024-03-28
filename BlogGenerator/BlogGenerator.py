import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers

## Function to get response from LLAMA 2 

def getLLamaresponse(input_text, no_words, block_style):
    llm=CTransformers(model='.\model\llama-2-7b-chat.ggmlv3.q8_0.bin',
                      model_type='llama',
                      config={'max_new_tokens':256,
                              'temperature':0.01})

    template="""write a blog for {blog_style} job profile for a topic {input_text} within {no_words} words."""

    prompt=PromptTemplate(input_variables=["blog_style", "input_text", "no_words"],
                          template=template)

    response=llm(prompt.format(blog_style=block_style,input_text=input_text,no_words=no_words))
    print(response)
    return response


st.set_page_config(page_title="Blog Generating Bot",
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("Blog Generating Bot")
input_text = st.text_input("Enter the blog topic")

col1, col2 = st.columns([5,5])
with col1:
    no_words = st.text_input('No of words')

with col2:
    blog_style=st.selectbox('Writing the blog for',('Researchers', 'Data Scientist', 'Common People'), index=0)

submit = st.button("Generate")

if submit:
    st.write(getLLamaresponse(input_text, no_words, blog_style))
