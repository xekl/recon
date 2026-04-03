
import streamlit as st
import json

import recon_util
import recon_prompts

# -----------------------------
# Setup
# -----------------------------

# general setup 

# the model that will be used for this run 
model = "groq" # use powerful online models
model = "llama3.2:latest" # use local ollama models

# streamlit setup

st.set_page_config(page_title="Before the Vote", layout="centered")
st.title("Before the Vote")

# Initialize session state
if "state" not in st.session_state:
    st.session_state.state = "config"
if "modules" not in st.session_state:
    st.session_state.modules = {}
if "chatlog" not in st.session_state:
    st.session_state.chatlog = {"speakers": {}, "messages": {}}

st.markdown(recon_util.chat_css, unsafe_allow_html=True)

# -----------------------------
# CONFIG SCREEN
# -----------------------------

welcome_text = """Welcome! 

**Before the Vote** is a thought experiment and an interactive exploration of the French-German reconciliation "Modellbaukasten". You will be one party in a conflictual conversation that may or may not lead to reconciliation - it depends on you.

The Modellbaukasten determines the "state of the world" in this experience. First, you can select your individual configuration of which modules from the German-French toolkit are present in this fictional conflict world and which are absent. This shapes how each side in the conflict frames the other, their experiences, their suspicions, their capacity for empathy. 
"""

if st.session_state.state == "config":
    st.header("Build This World")

    st.markdown(welcome_text)

    # TODO explain what is going on here
    # and that it is an LLM-based roleplaying game
    # and how AI works 
    # and what thought experiment this is meant to provoke

    st.write("**Select which reconciliation modules exist:**")

    modules = {}
    modules["Youth Exchange"] = st.checkbox(
        "Youth Exchange Programme",
        help="Youth exchange programs connect children and their families through penpal relationships and mutual visits. One family hosts a child from the other community for a short stay, and the roles reverse later."
    )
    modules["Academic Network"] = st.checkbox(
        "Shared Academic Network",
        help="Joint research initiatives, conferences, and cross-institutional partnerships that allow academics from both communities to collaborate and build shared knowledge."
    )
    modules["Cultural Institute"] = st.checkbox(
        "Joint Cultural Institute",
        help="A shared cultural space hosting exhibitions, events, and dialogue—providing a neutral platform for both communities to meet, collaborate, and express their identities."
    )
    modules["Historical Account"] = st.checkbox(
        "Common Historical Account",
        help="A collaboratively written history or set of educational materials that attempts to reconcile differing narratives about past conflicts or shared events."
    )
    modules["Civil Society"] = st.checkbox(
        "Active Civil Society Ties",
        help="Cross-community cooperation among NGOs, artists, journalists, and grassroots groups—building trust and empathy outside formal political channels."
    )

    if st.button("Start Scene"):
        st.session_state.modules = modules
        st.session_state.state = "scene"
        st.rerun()

# -----------------------------
# SCENE: Chat-based Conversation
# -----------------------------

if st.session_state.state == "scene":
    st.header("The Exhibition Room")

    st.write("(TODO: Scene description) You are in a dimly lit museum room. A case in the center ... two persons facing you ... Every conversation is different. The characters are played by AI and react to your selected world state as well as your words. ")

    # TODO kickoff conversation with NPC turns?
    # or let player begin conversation

    # Render existing messages
    # for message in st.session_state.chatlog:
    for i in range(len(st.session_state.chatlog.get("messages"))):
        speaker = st.session_state.chatlog.get("speakers").get(i)
        message = st.session_state.chatlog.get("messages").get(i)
        recon_util.render_message(speaker, message)
            
    # Chat input
    user_text = st.chat_input("Speak your mind ...")

    if user_text:

        message_no = len(st.session_state.chatlog.get("messages"))

        # 1 — Player message
        # st.session_state.chatlog.append(("Mediator", user_text))
        st.session_state.chatlog["speakers"][message_no] = "Mediator"
        st.session_state.chatlog["messages"][message_no] = {'role': 'user', 'content': user_text}
        message_no += 1

        # 2 — NPC A reaction
        role = "Representative"
        role_system_prompt = recon_prompts.build_system_prompt(st.session_state.modules, role)
        # turn_taking_prompt = recon_prompts.build_turntaking_prompt(st.session_state.chatlog)
        # # print("turn_taking_prompt for "+role, turn_taking_prompt)
        # take_turn = recon_util.call_llm(role_system_prompt + "\n\n" + turn_taking_prompt, st.session_state.chatlog[-5:]) 
        # print("take_turn for "+role, take_turn)
        # TODO forget turn taking for now 
        take_turn = {"content": "yes"}
        if take_turn.get("content").lower().strip().replace(".", "").replace("!", "") == "yes":
            conversation_prompt = recon_prompts.build_conversation_prompt(st.session_state.chatlog)
            npc_a_out = recon_util.get_chat_response(role_system_prompt, st.session_state.chatlog, model=model)
            st.session_state.chatlog["speakers"][message_no] = role
            st.session_state.chatlog["messages"][message_no] = npc_a_out
            message_no += 1

        # 3 — NPC B reaction
        role = "Trustee"
        role_system_prompt = recon_prompts.build_system_prompt(st.session_state.modules, role)
        # turn_taking_prompt = recon_prompts.build_turntaking_prompt(st.session_state.chatlog)
        # # print("turn_taking_prompt for "+role, turn_taking_prompt)
        # take_turn = recon_util.call_llm(role_system_prompt + "\n\n" + turn_taking_prompt, st.session_state.chatlog[-5:]) 
        # print("take_turn for "+role, take_turn)
        # TODO forget turn taking for now 
        take_turn = {"content": "yes"}
        if take_turn.get("content").lower().strip().replace(".", "").replace("!", "") == "yes":
            conversation_prompt = recon_prompts.build_conversation_prompt(st.session_state.chatlog)
            npc_b_out = recon_util.get_chat_response(role_system_prompt, st.session_state.chatlog, model=model)
            st.session_state.chatlog["speakers"][message_no] = role
            st.session_state.chatlog["messages"][message_no] = npc_b_out

            print("added Trustee message")
            print(st.session_state.chatlog)
            print(message_no)
            print(role)
            print(npc_b_out)

        # take_turn_b = recon_prompts.build_turntaking_prompt(st.session_state.chatlog, "Trustee")
        # if recon_util.call_llm(take_turn_b).lower().strip().replace(".", "").replace("!", "") == "yes":
        #     npc_b_prompt = recon_prompts.build_system_prompt(st.session_state.modules, st.session_state.chatlog, "Trustee")
        #     npc_b_out = recon_util.call_llm(npc_b_prompt)
        #     st.session_state.chatlog.append(("Trustee", npc_b_out))

        # print("----")
        # print("messages", st.session_state.chatlog)
        
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
    # for speaker, text in st.session_state.chatlog[-6:]:
    #     st.markdown(f"**{speaker}:** {text}")

    st.subheader("The Vote")
    st.markdown("...")
    if st.button("Decide!"):
        vote_promt = recon_prompts.build_vote_prompt(st.session_state.chatlog)

        # let both NPCs give their final statement
        role = "Representative"
        role_system_prompt = recon_prompts.build_system_prompt(st.session_state.modules, role)
        npc_a_decision = recon_util.get_llm_generation(role_system_prompt, vote_promt, model=model)
        recon_util.render_message(role, npc_a_decision)
        role = "Trustee"
        role_system_prompt = recon_prompts.build_system_prompt(st.session_state.modules, role)
        npc_b_decision = recon_util.get_llm_generation(role_system_prompt, vote_promt, model=model)
        recon_util.render_message(role, npc_b_decision)

        # tell the ending 
        ending_system_prompt, ending_prompt = recon_prompts.build_ending_prompts(st.session_state.chatlog, npc_a_decision, npc_b_decision)
        ending_message = recon_util.get_llm_generation(ending_system_prompt, ending_prompt, model=model)
        recon_util.render_message("DECISION", ending_message)
    
    st.markdown("")
    st.markdown("")

    if st.button("Restart"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
