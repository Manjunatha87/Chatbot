#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!pip install streamlit


# In[2]:


#!pip install transformers


# In[4]:


#!pip install torch torchvision torchaudio


# In[8]:


import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

@st.cache_resource
def load_model():
    model_name = "microsoft/DialoGPT-medium"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return tokenizer, model

def generate_response(user_input, chat_history_ids, tokenizer, model):
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
    if chat_history_ids is not None:
        input_ids = torch.cat([chat_history_ids, input_ids], dim=-1)

    chat_history_ids = model.generate(
        input_ids, 
        max_length=1000, 
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=2,
        top_k=50,
        top_p=0.95,
        temperature=0.7
    )

    response = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response, chat_history_ids

def main():
    st.title("🤖 Chatbot using Transformers")
    st.write("Welcome! Start chatting with me!")

    tokenizer, model = load_model()

    if "chat_history_ids" not in st.session_state:
        st.session_state.chat_history_ids = None
    if "past_chats" not in st.session_state:
        st.session_state.past_chats = []

    user_input = st.text_input("You:", key="user_input")
    if st.button("Send"):
        if user_input:
            response, st.session_state.chat_history_ids = generate_response(
                user_input, st.session_state.chat_history_ids, tokenizer, model
            )
            st.session_state.past_chats.append({"user": user_input, "bot": response})

    st.markdown("### Chat History")
    for chat in st.session_state.past_chats:
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**Bot:** {chat['bot']}")

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:



