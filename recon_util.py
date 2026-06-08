import requests
import streamlit as st

import logging
logfile = "debug_log.txt"
# PRINT LOGGER FOR SHORT PROGRESSION VIEW
print_logger = logging.getLogger("recon_logger")
print_logger.setLevel(logging.DEBUG) # The default is NOTSET
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add to console handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add ch to logger
print_logger.addHandler(ch)
# FILE LOGGER FOR LONGER EXCERPTS
file_logger = logging.getLogger('spam_application')
file_logger.setLevel(logging.DEBUG)
# create file handler 
fh = logging.FileHandler(logfile)
fh.setLevel(logging.DEBUG)
# create formatter and add to file handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s \n\n%(message)s \n\n')
fh.setFormatter(formatter)
# add fh to logger
file_logger.addHandler(fh)

from groq import Groq
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

import recon_assets

# -----------------------------
# Utility: LLM call
# -----------------------------

def get_llm_generation(system_prompt, prompt, model="llama3.2:latest"):

    print_logger.debug("  enter get_llm_generation, model: " + model)

    # generate via groq API
    if model == "groq":

        messages = []
        messages.append({'role': "system", 'content': system_prompt})
        messages.append({'role': "user", 'content': prompt})

        response = groq_client.chat.completions.create(
            model = "llama-3.3-70b-versatile",
            # max_tokens = max_tokens,
            # temperature = temperature,
            messages = messages)

        # extract response text 
        try:
            result = response.choices[0].message.content
        except:
            print_logger.error("error in response generation with", model)
            print_logger.error("response was:", response)
            result = response

        file_logger.debug("  get_llm_generation\n\n  with system-prompt:\n  " + system_prompt + "  \n\nwith prompt:\n  " + prompt + "  \n\nwith result:\n  " + result)
        print_logger.debug("  response logged in file: " + logfile)

        return result

    # generate via ollama
    else: 

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
                timeout=(10, 300) # 10s to connect, 5 minutes to read -> don't run into timeout errors too early
            )
            data = response.json()
            
            file_logger.debug("  get_llm_generation\n\n  with system-prompt:\n  " + system_prompt + "  \n\nwith prompt:\n  " + prompt + "  \n\nwith result:\n  " + data.get("response", "").strip())
            print_logger.debug("  response logged in file: " + logfile)

            return data.get("response", "").strip()
        
        except Exception as e:
            return f"[LLM ERROR] {str(e)}"


# def get_chat_response(system_prompt, messages, model="llama3.2:latest"):
def get_chat_response(system_prompt, chatlog, role, model="llama3.2:latest"):

    print_logger.debug("  enter get_chat_response, model: " + model + ", role: " + str(role))

    # Reformat conversation into a labeled transcript (no API 'name' support assumed)
    transcript_lines = []
    for i in range(len(chatlog.get("messages"))):
        speaker = chatlog.get("speakers").get(i)
        content = chatlog.get("messages").get(i).get('content')
        transcript_lines.append(f"{speaker}: {content}")
    # cap transcript to recent N lines
    last_k = 12
    transcript = "\n".join(transcript_lines[-last_k:])

    # determine last speaker
    last_speaker = None
    if len(transcript_lines) > 0:
        last_speaker = transcript_lines[-1].split(":", 1)[0]
    
    # user-style prompt including explicit instruction who should respond next
    user_prompt = recon_assets.get_localized_string('chat_response_conversation_history', 'English') + "\n" + transcript + "\n\n"
    last_speaker_text = last_speaker if last_speaker is not None else recon_assets.get_localized_string('no_last_speaker', 'English')
    user_prompt += f"{recon_assets.get_localized_string('last_speaker_label', 'English')} {last_speaker_text}\n"
    user_prompt += recon_assets.get_localized_string('chat_response_respond_as_role', 'English').format(role=role) + "\n"
    user_prompt += recon_assets.get_localized_string('chat_response_output_format', 'English') + "\n"

    # prepare messages for the chat API
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]

    # generate via groq API
    if model == "groq":

        message = {'role': "assistant", 'content': ""}

        response = groq_client.chat.completions.create(
            model = "llama-3.3-70b-versatile",
            messages = messages)

        # extract response text 
        try:
            result = response.choices[0].message.content
            message['content'] = result 
        except Exception as e:
            print_logger.error("error in response generation with " + model + ": " + str(e))
            print_logger.error("response was:", response)
            message['content'] = str(response)

        file_logger.debug("  get_chat_response\n\n  with system-prompt:\n  " + system_prompt + "  \n\nwith user-prompt:\n  " + user_prompt + "  \n\nwith result:\n  " + str(message))
        print_logger.debug("  response logged in file: " + logfile)

        return message

    # generate via ollama
    else: 
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "system": system_prompt,
                    "prompt": user_prompt,
                    "stream": False,
                    "options": {"temperature": 0.9}
                },
                timeout=30
            )
            data = response.json()
        except Exception as e:
            print_logger.error("LLM ERROR: " + str(e))
            return {'role': 'assistant', 'content': '...'}

        # try to extract response text from known keys
        result = data.get('response') or data.get('message') or data.get('result') or ''
        if isinstance(result, dict):
            result_text = result.get('content', '')
        else:
            result_text = str(result)

        message = {'role': 'assistant', 'content': result_text}

        file_logger.debug("  get_chat_response\n\n  with system-prompt:\n  " + system_prompt + "  \n\nwith user-prompt:\n  " + user_prompt + "  \n\nwith raw answer:\n  " + str(data) + "  \n\nwith result:\n  " + str(message))
        print_logger.debug("  response logged in file: " + logfile)

        return message

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
def render_message(speaker, message):

    if isinstance(message, str):
        # speaker = "placeholder"
        text = message
    else:
        # speaker = message.get("role", None)
        text = message.get("content", None)

    if speaker == "Mediator":
        css_class = "chat-center"
    elif speaker == "Representative":
        css_class = "chat-left"
    elif speaker == "Trustee":
        css_class = "chat-right"
    else:
        css_class = "chat-center"

    # if speaker == "user":
    #     speaker = "Mediator"
    #     css_class = "chat-center"
    # elif speaker == "Representative":
    #     css_class = "chat-left"
    # elif speaker == "Trustee":
    #     css_class = "chat-right"
    # else:
    #     css_class = "chat-center"

    with st.chat_message(speaker, avatar=AVATARS.get(speaker, None)):
        if speaker == "Mediator":
            st.markdown(f"<div class='{css_class}'>{text}</div>", unsafe_allow_html=True)
        else: 
            st.markdown(f"<div class='{css_class}'><b>{speaker}:</b> {text}</div>", unsafe_allow_html=True)
