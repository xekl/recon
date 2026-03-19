
import requests
import streamlit as st

# -----------------------------
# Utility: Ollama LLM call
# -----------------------------

def get_llm_generation(system_prompt, prompt, model="llama3.2:latest"):

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, 
                  "system": system_prompt,
                  "prompt": prompt,
                  "stream": False, # TODO think about streaming for more dynamics
                  "options": { # see doc for list https://github.com/ollama/ollama/blob/main/docs/api.md
                      "temperature": 0.9,
                  }
                  },
            timeout=30
        )
        data = response.json()
        
        print("response:", data.get("response", "").strip())
        return data.get("response", "").strip()
    
    except Exception as e:
        return f"[LLM ERROR] {str(e)}"


def get_chat_response(system_prompt, messages, model="llama3.2:latest"):

    # insert system prompt ...
    instructions = messages.copy()
    instructions = [{'role': 'system', 'content': system_prompt}] + instructions
    # instructions.append({'role': 'system', 'content': system_prompt})

    # reformat messages
    if instructions[-1].get("role") == "assistant":
        # instructions.append({'role': 'user', 'content': 'Mediator: ok, what do you have to say?'})
        instructions.append({'role': 'user', 'content': 'Mediator: ...'})

    print("----")
    print("----")
    print("----")
    # print(prompt)
    print("model call with:")
    # print("system_prompt", system_prompt)
    print("instructions", instructions)
    print("----")
    print("----")
    print("----")

    


    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={"model": model, 
                #   "system": system_prompt,
                  "messages": instructions, # for /chat API
                  "stream": False, # TODO think about streaming for more dynamics
                  "options": { # see doc for list https://github.com/ollama/ollama/blob/main/docs/api.md
                      "temperature": 0.9,
                  }
                  },
            timeout=30
        )
        data = response.json()
        
        # print("raw answer:", data)
        return data.get("message", {})
    
    except Exception as e:
        return f"[LLM ERROR] {str(e)}"
    

# -----------------------------
# Utility: Chat layout
# -----------------------------

chat_css = """
<style>
/* GENERAL CHAT STYLING */
.chat-left {
    text-align: left !important;
    background-color: #fff7d6;
    padding: 10px 14px;
    border-radius: 10px;
    margin-bottom: 8px;
    max-width: 80%;
}

.chat-right {
    text-align: right !important;
    background-color: #dceeff;
    padding: 10px 14px;
    border-radius: 10px;
    margin-bottom: 8px;
    margin-left: auto;
    max-width: 80%;
}

.chat-center {
    text-align: center !important;
    background-color: #f1f1f1;
    border-radius: 10px;
    padding: 10px 14px;
    margin-bottom: 10px;
    max-width: 60%;
    margin-left: auto;
    margin-right: auto;
}
</style>
"""

AVATARS = {
    "Mediator": None,
    "Representative": "🗣️",
    "Trustee": "🎩"
} # TODO add suitable avatars, can be local images

# def render_message(speaker, text):
def render_message(message):

    print()
    print()
    print()
    print()
    print()
    print(message)
    print()
    print()
    print()
    print()
    print()

    if isinstance(message, str):
        speaker = "placeholder"
        text = message
    else:
        speaker = message.get("role", None)
        text = message.get("content", None)

    # if speaker == "Mediator":
    #     css_class = "chat-center"
    # elif speaker == "Representative":
    #     css_class = "chat-left"
    # elif speaker == "Trustee":
    #     css_class = "chat-right"
    # else:
    #     css_class = "chat-center"

    if speaker == "user":
        speaker = "Mediator"
        css_class = "chat-center"
    elif speaker == "Representative":
        css_class = "chat-left"
    elif speaker == "Trustee":
        css_class = "chat-right"
    else:
        css_class = "chat-center"

    with st.chat_message(speaker, avatar=AVATARS.get(speaker, None)):
        if speaker == "Mediator":
            st.markdown(f"<div class='{css_class}'>{text}</div>", unsafe_allow_html=True)
        else: 
            st.markdown(f"<div class='{css_class}'><b>{speaker}:</b> {text}</div>", unsafe_allow_html=True)

