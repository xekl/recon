
import streamlit as st
import json

import recon_util
import recon_prompts

# -----------------------------
# Streamlit Setup
# -----------------------------
st.set_page_config(page_title="The Night Before the Vote", layout="centered")
st.title("The Night Before the Vote – Prototype")

# Initialize session state
if "state" not in st.session_state:
    st.session_state.state = "config"
if "modules" not in st.session_state:
    st.session_state.modules = {}
if "messages" not in st.session_state:
    st.session_state.messages = []   # list of (speaker, text)

st.markdown(recon_util.chat_css, unsafe_allow_html=True)

# -----------------------------
# CONFIG SCREEN
# -----------------------------
if st.session_state.state == "config":
    st.header("Step 1 — Build This World")

    st.write("Select which reconciliation modules exist:")

    modules = {}
    modules["Youth Exchange"] = st.checkbox("Youth Exchange Programme")
    modules["Academic Network"] = st.checkbox("Shared Academic Network")
    modules["Cultural Institute"] = st.checkbox("Joint Cultural Institute")
    modules["Historical Account"] = st.checkbox("Common Historical Account")
    modules["Civil Society"] = st.checkbox("Active Civil Society Ties")

    if st.button("Start Scene"):
        st.session_state.modules = modules
        st.session_state.state = "scene"
        st.rerun()

# -----------------------------
# SCENE: Chat-based Conversation
# -----------------------------
if st.session_state.state == "scene":
    st.header("The Exhibition Room")

    st.write("You are in a dimly lit museum room. A case in the center ... two persons facing you ...")

    # TODO kickoff conversation with NPC turns?
    # or let player begin conversation

    # Render existing messages
    # for speaker, text in st.session_state.messages:
    #     recon_util.render_message(speaker, text)
    for message in st.session_state.messages:
        recon_util.render_message(message)
            
    # Chat input
    user_text = st.chat_input("Speak ...")

    if user_text:

        # 1 — Player message
        # st.session_state.messages.append(("Mediator", user_text))
        st.session_state.messages.append({'role': 'user', 'content': user_text})

        # 2 — NPC A reaction
        role = "Representative"
        role_system_prompt = recon_prompts.build_system_prompt(st.session_state.modules, role)
        # turn_taking_prompt = recon_prompts.build_turntaking_prompt(st.session_state.messages)
        # # print("turn_taking_prompt for "+role, turn_taking_prompt)
        # take_turn = recon_util.call_llm(role_system_prompt + "\n\n" + turn_taking_prompt, st.session_state.messages[-5:]) 
        # print("take_turn for "+role, take_turn)
        # TODO forget turn taking for now 
        take_turn = {"content": "yes"}
        if take_turn.get("content").lower().strip().replace(".", "").replace("!", "") == "yes":
            # npc_a_prompt = recon_prompts.build_system_prompt(st.session_state.modules, st.session_state.messages, role)
            conversation_prompt = recon_prompts.build_conversation_prompt(st.session_state.messages)
            # npc_a_out = recon_util.call_llm(role_system_prompt, conversation_prompt)
            npc_a_out = recon_util.get_chat_response(role_system_prompt, st.session_state.messages)
            # npc_a_out["role"] = role
            # npc_a_out["content"] = role + ": " + npc_a_out["content"]
            # st.session_state.messages.append((role, npc_a_out))
            st.session_state.messages.append(npc_a_out)

        # 3 — NPC B reaction
        role = "Trustee"
        role_system_prompt = recon_prompts.build_system_prompt(st.session_state.modules, role)
        # turn_taking_prompt = recon_prompts.build_turntaking_prompt(st.session_state.messages)
        # # print("turn_taking_prompt for "+role, turn_taking_prompt)
        # take_turn = recon_util.call_llm(role_system_prompt + "\n\n" + turn_taking_prompt, st.session_state.messages[-5:]) 
        # print("take_turn for "+role, take_turn)
        # TODO forget turn taking for now 
        take_turn = {"content": "yes"}
        if take_turn.get("content").lower().strip().replace(".", "").replace("!", "") == "yes":
            # npc_a_prompt = recon_prompts.build_system_prompt(st.session_state.modules, st.session_state.messages, role)
            conversation_prompt = recon_prompts.build_conversation_prompt(st.session_state.messages)
            # npc_a_out = recon_util.call_llm(role_system_prompt, conversation_prompt)
            npc_b_out = recon_util.get_chat_response(role_system_prompt, st.session_state.messages)
            # npc_b_out["role"] = role
            # npc_b_out["content"] = role + ": " + npc_b_out["content"]
            # st.session_state.messages.append((role, npc_a_out))
            st.session_state.messages.append(npc_b_out)

        # take_turn_b = recon_prompts.build_turntaking_prompt(st.session_state.messages, "Trustee")
        # if recon_util.call_llm(take_turn_b).lower().strip().replace(".", "").replace("!", "") == "yes":
        #     npc_b_prompt = recon_prompts.build_system_prompt(st.session_state.modules, st.session_state.messages, "Trustee")
        #     npc_b_out = recon_util.call_llm(npc_b_prompt)
        #     st.session_state.messages.append(("Trustee", npc_b_out))

        # print("----")
        # print("messages", st.session_state.messages)
        
        st.rerun()

    st.write("---")
    if st.button("Conclude Scene"):
        st.session_state.state = "end"
        st.rerun()

# -----------------------------
# ENDING SCENE
# -----------------------------
if st.session_state.state == "end":
    st.header("The End")

    # TODO actually have them vote 
    # and tell the ending of the story by their reached agreement

    # TODO have a timer running and reach this state automatically after n minutes?

    st.subheader("World Configuration")
    for k, v in st.session_state.modules.items():
        st.markdown(f"- {k}: {'✓' if v else '✗'}")

    # st.subheader("Final Exchange")
    # for speaker, text in st.session_state.messages[-6:]:
    #     st.markdown(f"**{speaker}:** {text}")

    st.subheader("The Vote")
    st.markdown("...")
    if st.button("Decide!"):
        vote_promt = recon_prompts.build_vote_prompt(st.session_state.messages)

        # let both NPCs give their final statement
        role = "Representative"
        role_system_prompt = recon_prompts.build_system_prompt(st.session_state.modules, role)
        npc_a_decision = recon_util.get_llm_generation(role_system_prompt, vote_promt)
        recon_util.render_message(npc_a_decision)
        role = "Trustee"
        role_system_prompt = recon_prompts.build_system_prompt(st.session_state.modules, role)
        npc_b_decision = recon_util.get_llm_generation(role_system_prompt, vote_promt)
        recon_util.render_message(npc_b_decision)

        # tell the ending 
        ending_prompt = recon_prompts.build_ending_prompt(st.session_state.messages, npc_a_decision, npc_b_decision)
        ending_message = recon_util.get_llm_generation(None, ending_prompt)
        recon_util.render_message(ending_message)
    
    st.markdown("")
    st.markdown("")

    if st.button("Restart"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
