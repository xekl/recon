
import streamlit as st
import streamlit.components.v1 as components

from datetime import datetime

import recon_assets
import recon_util
import recon_prompting

# -----------------------------
# Setup
# -----------------------------

# the model that will be used for this run 
# model = 'groq' # use powerful online models
model = 'llama3.2:latest' # use local ollama models

# initialize session state
if 'state' not in st.session_state:
    st.session_state.state = 'config'
if 'chatlog' not in st.session_state:
    st.session_state.chatlog = {'speakers': {}, 'messages': {}}

# options 
if 'language' not in st.session_state:
    st.session_state.language = 'English'
if 'modules' not in st.session_state:
    st.session_state.modules = {}

# timer state 
if 'timer_start' not in st.session_state:
    st.session_state.timer_start = None
if 'timer_duration' not in st.session_state:
    st.session_state.timer_duration = 300  # 5 minutes in seconds
if 'timer_expired' not in st.session_state:
    st.session_state.timer_expired = False

# timer helper function: how much time remains from the countdown?
def get_remaining_time():
    if st.session_state.timer_start is None:
        return st.session_state.timer_duration
    elapsed = (datetime.now() - st.session_state.timer_start).total_seconds()
    remaining = max(0, st.session_state.timer_duration - elapsed)
    return remaining

# streamlit setup
st.set_page_config(page_title=recon_assets.get_localized_string('pagetitle', st.session_state.language), layout='centered')
st.title(recon_assets.get_localized_string('pagetitle', st.session_state.language))
st.markdown(recon_util.chat_css, unsafe_allow_html=True)


print()
print()
print()
print("st.session_state.state:", st.session_state.state)
print()
print()
print()


# -----------------------------
# CONFIG SCREEN
# -----------------------------

if st.session_state.state == 'config':

    # st.header(recon_assets.get_localized_string('heading_config', st.session_state.language))
    st.markdown(recon_assets.get_localized_string('config_text', st.session_state.language))
            
    tab_modules, tab_modellbaukasten, tab_experience = st.tabs([recon_assets.get_localized_string('heading_modules', st.session_state.language), recon_assets.get_localized_string('heading_modellbaukasten', st.session_state.language), recon_assets.get_localized_string('heading_experience', st.session_state.language)])

    with tab_modules:

        st.markdown(recon_assets.get_localized_string('modules_text', st.session_state.language))

        modules = {}
        modules['youth_exchange'] = st.checkbox(recon_assets.get_localized_string('youth_exchange', st.session_state.language))
        st.write(recon_assets.get_localized_string('youth_exchange_expl', st.session_state.language))
        modules['academic_network'] = st.checkbox(recon_assets.get_localized_string('academic_network', st.session_state.language))
        st.write(recon_assets.get_localized_string('academic_network_expl', st.session_state.language))
        modules['cultural_institute'] = st.checkbox(recon_assets.get_localized_string('cultural_institute', st.session_state.language))
        st.write(recon_assets.get_localized_string('cultural_institute_expl', st.session_state.language))
        modules['historical_account'] = st.checkbox(recon_assets.get_localized_string('historical_account', st.session_state.language))
        st.write(recon_assets.get_localized_string('historical_account_expl', st.session_state.language))
        modules['civil_society'] = st.checkbox(recon_assets.get_localized_string('civil_society', st.session_state.language))
        st.write(recon_assets.get_localized_string('civil_society_expl', st.session_state.language))

    with tab_modellbaukasten:
        st.markdown(recon_assets.get_localized_string('modellbaukasten_text', st.session_state.language))

    with tab_experience:
        st.markdown(recon_assets.get_localized_string('experience_text', st.session_state.language))
    
    st.markdown("----")
    # st.write("")
    if st.button(recon_assets.get_localized_string('start_button', st.session_state.language)):
        st.session_state.modules = modules
        st.session_state.state = 'scene'
        st.rerun()
    st.write("")

# -----------------------------
# SCENE: Chat-based Conversation
# -----------------------------

if st.session_state.state == 'scene':

    st.header(recon_assets.get_localized_string('scene_header', st.session_state.language))
    st.markdown(recon_assets.get_localized_string('scene_text', st.session_state.language))

    # get timer time if timer has started
    if st.session_state.timer_start is not None:
        remaining = get_remaining_time()

        # if time is up 
        if remaining <= 0 and not st.session_state.timer_expired:
            st.session_state.timer_expired = True
            # TODO display a final message?
            st.rerun()

    # TODO kickoff conversation with NPC turns?
    # or let player begin conversation

    # Render existing messages
    # for message in st.session_state.chatlog:
    for i in range(len(st.session_state.chatlog.get('messages'))):
        speaker = st.session_state.chatlog.get('speakers').get(i)
        message = st.session_state.chatlog.get('messages').get(i)
        recon_util.render_message(speaker, message)
            
    # Chat input
    if not st.session_state.timer_expired: # don't show if time is up 
        user_text = st.chat_input(recon_assets.get_localized_string('chat_input', st.session_state.language))
    else:
        user_text = None
        st.success(recon_assets.get_localized_string('time_is_up_text', st.session_state.language))

    if user_text:

        # start the clock! on first message
        if st.session_state.timer_start is None:
            st.session_state.timer_start = datetime.now()
        # check if time expired before processing
        if get_remaining_time() <= 0:
            st.rerun() # too late, trigger the end state transition
            
        message_no = len(st.session_state.chatlog.get('messages'))

        # 1 — Player message
        # st.session_state.chatlog.append(("Mediator", user_text))
        st.session_state.chatlog['speakers'][message_no] = 'Mediator'
        st.session_state.chatlog['messages'][message_no] = {'role': 'user', 'content': user_text}
        message_no += 1

        # TODO add localization to prompt building

        # 2 — NPC A reaction
        role = 'Representative'
        role_system_prompt = recon_prompting.build_system_prompt(st.session_state.modules, role, st.session_state.language)
        # turn_taking_prompt = recon_prompts.build_turntaking_prompt(st.session_state.chatlog)
        # # print('turn_taking_prompt for '+role, turn_taking_prompt)
        # take_turn = recon_util.call_llm(role_system_prompt + '\n\n' + turn_taking_prompt, st.session_state.chatlog[-5:]) 
        # print('take_turn for '+role, take_turn)
        # TODO forget turn taking for now 
        take_turn = {'content': 'yes'}
        if take_turn.get('content').lower().strip().replace('.', '').replace('!', '') == 'yes':
            npc_a_out = recon_util.get_chat_response(role_system_prompt, st.session_state.chatlog, model=model)
            st.session_state.chatlog['speakers'][message_no] = role
            st.session_state.chatlog['messages'][message_no] = npc_a_out
            message_no += 1

        # 3 — NPC B reaction
        role = 'Trustee'
        role_system_prompt = recon_prompting.build_system_prompt(st.session_state.modules, role, st.session_state.language)
        # turn_taking_prompt = recon_prompts.build_turntaking_prompt(st.session_state.chatlog)
        # # print('turn_taking_prompt for '+role, turn_taking_prompt)
        # take_turn = recon_util.call_llm(role_system_prompt + '\n\n' + turn_taking_prompt, st.session_state.chatlog[-5:]) 
        # print('take_turn for '+role, take_turn)
        # TODO forget turn taking for now 
        take_turn = {'content': 'yes'}
        if take_turn.get('content').lower().strip().replace('.', '').replace('!', '') == 'yes':
            npc_b_out = recon_util.get_chat_response(role_system_prompt, st.session_state.chatlog, model=model)
            st.session_state.chatlog['speakers'][message_no] = role
            st.session_state.chatlog['messages'][message_no] = npc_b_out

            print('added Trustee message')
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

    # ---- display timer ----

    if st.session_state.timer_start is not None:
        # JavaScript-based countdown timer
        end_time_ms = int((st.session_state.timer_start.timestamp() + st.session_state.timer_duration) * 1000)
        timer_html = f"""<div id="timer-display" style="text-align: center; font-size: 24px; font-weight: bold; padding: 10px; margin-bottom: 20px;">
            <span id="timer-text"></span>
        </div>
        <script>
        const endTime = {end_time_ms};
        
        function updateTimer() {{
            const now = new Date().getTime();
            const remaining = Math.max(0, endTime - now);
            const minutes = Math.floor(remaining / 60000);
            const seconds = Math.floor((remaining % 60000) / 1000);
            
            const timerText = document.getElementById('timer-text');
            if (timerText) {{
                const timeStr = minutes.toString().padStart(2, '0') + ':' + seconds.toString().padStart(2, '0');
                
                let color = 'green';
                if (remaining < 60000) color = 'red';
                else if (remaining < 120000) color = 'orange';
                
                timerText.innerHTML = '<span style="font-family: sans-serif;">Time Remaining: <span style="color: ' + color + '; font-family: sans-serif;">' + timeStr + '</span></span>';
            }}
        }}
        
        updateTimer();
        const interval = setInterval(updateTimer, 1000);
        </script>"""
        components.html(timer_html, height=80)

    # ---- end timer section ----

    # conclude scene manually with button 
    _, _, _, col, _, _, _ = st.columns([1,2,3,4,3,2,1]) # hacky way to center button ...
    if col.button(recon_assets.get_localized_string('end_scene_button', st.session_state.language)):
        st.session_state.state = 'end'
        st.rerun()

# -----------------------------
# ENDING SCENE
# -----------------------------
if st.session_state.state == 'end':
    st.header(recon_assets.get_localized_string('end_header', st.session_state.language))

    # TODO actually have them vote 
    # and tell the ending of the story by their reached agreement

    # TODO have a timer running and reach this state automatically after n minutes?

    st.subheader(recon_assets.get_localized_string('heading_modules', st.session_state.language))
    
    module_markdown = ""
    for k, v in st.session_state.modules.items():
        module_markdown += f"- {'✓' if v else '✗'} - {recon_assets.get_localized_string(k, st.session_state.language)}\n"
    st.markdown(module_markdown)
    
    # st.subheader("Final Exchange")
    # for speaker, text in st.session_state.chatlog[-6:]:
    #     st.markdown(f"**{speaker}:** {text}")

    st.subheader(recon_assets.get_localized_string('decision_subheader', st.session_state.language))
    st.markdown(recon_assets.get_localized_string('decision_text', st.session_state.language))
    
    if st.button("Decide! (will trigger automatically later)"):
        # TODO trigger automatically
        vote_prompt = recon_prompting.build_vote_prompt(st.session_state.chatlog, st.session_state.language)

        # let both NPCs give their final statement
        role = "Representative"
        role_system_prompt = recon_prompting.build_system_prompt(st.session_state.modules, role, st.session_state.language)
        npc_a_decision = recon_util.get_llm_generation(role_system_prompt, vote_prompt, model=model)
        recon_util.render_message(role, npc_a_decision)
        role = "Trustee"
        role_system_prompt = recon_prompting.build_system_prompt(st.session_state.modules, role, st.session_state.language)
        npc_b_decision = recon_util.get_llm_generation(role_system_prompt, vote_prompt, model=model)
        recon_util.render_message(role, npc_b_decision)

        # tell the ending 
        ending_system_prompt, ending_prompt = recon_prompting.build_ending_prompts(st.session_state.chatlog, npc_a_decision, npc_b_decision, st.session_state.language)
        ending_message = recon_util.get_llm_generation(ending_system_prompt, ending_prompt, model=model)
        recon_util.render_message("DECISION", ending_message)
    
    st.markdown("")
    st.markdown("")

    if st.button("Restart"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()



