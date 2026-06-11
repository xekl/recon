
import streamlit as st

from datetime import datetime
import time

import recon_assets
import recon_util
import recon_prompting

# -----------------------------
# Setup
# -----------------------------

# the model that will be used for this run 
model = 'groq' # use powerful online models
# model = 'llama3.2:latest' # use local ollama models
# model = 'gemma4:latest' # use local ollama models

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

# Baukasten impact tracking
if 'module_impacts' not in st.session_state:
    st.session_state.module_impacts = {}  # stores impact analysis for each module

# timer state 
if 'timer_start' not in st.session_state:
    st.session_state.timer_start = None
if 'timer_duration' not in st.session_state:
    st.session_state.timer_duration = 300  # 300 = 5, 420 = 7 minutes in seconds
if 'timer_expired' not in st.session_state:
    st.session_state.timer_expired = False
if 'timer_paused' not in st.session_state:
    st.session_state.timer_paused = False
if 'timer_pause_time' not in st.session_state:
    st.session_state.timer_pause_time = None  # Tracks when pause started

# timer helper function: how much time remains from the countdown?
def get_remaining_time():
    if st.session_state.timer_start is None:
        return st.session_state.timer_duration
    elapsed = (datetime.now() - st.session_state.timer_start).total_seconds()
    remaining = max(0, st.session_state.timer_duration - elapsed)
    return remaining

# pause timer during LLM calls
def pause_timer():
    """Pause the timer by recording the current moment."""
    st.session_state.timer_paused = True
    if st.session_state.timer_start is not None and st.session_state.timer_pause_time is None:
        st.session_state.timer_pause_time = datetime.now()

# resume timer after LLM calls
def resume_timer():
    """Resume the timer by shifting timer_start forward by pause duration."""
    if st.session_state.timer_pause_time is not None:
        pause_duration = (datetime.now() - st.session_state.timer_pause_time).total_seconds()
        st.session_state.timer_start = st.session_state.timer_start + __import__('datetime').timedelta(seconds=pause_duration)
        st.session_state.timer_pause_time = None
    st.session_state.timer_paused = False

# streamlit setup
st.set_page_config(page_title=recon_assets.get_localized_string('pagetitle', st.session_state.language), layout='centered')
st.title(recon_assets.get_localized_string('pagetitle', st.session_state.language))
st.markdown(recon_util.chat_css, unsafe_allow_html=True)

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

        # show message 
        recon_util.render_message('Mediator', user_text)

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

        recon_util.print_logger.debug("got user input, handle turn taking:")

        pause_timer()

        # 2 — NPC A reaction
        role = 'Representative'
        role_system_prompt = recon_prompting.build_system_prompt(st.session_state.modules, role, st.session_state.language)
        # turn_taking_system_prompt = recon_assets.get_localized_string('turn_taking_system_prompt', st.session_state.language)
        # turn_taking_prompt = recon_prompting.build_turntaking_prompt(st.session_state.chatlog, role, st.session_state.language)
        # take_turn = recon_util.get_llm_generation(turn_taking_system_prompt, turn_taking_prompt, model=model)
        take_turn = "yes" # for testing, let both NPCs always take turn
        if take_turn.lower().strip().replace('.', '').replace('!', '') == 'yes':
            # recon_util.print_logger.debug("Representative wants to take turn")
            npc_a_out = recon_util.get_chat_response(role_system_prompt, st.session_state.chatlog, role, model=model)
            st.session_state.chatlog['speakers'][message_no] = role
            st.session_state.chatlog['messages'][message_no] = npc_a_out
            message_no += 1
        else:
            recon_util.print_logger.debug("Representative does not want to take turn, says: " + str(take_turn))

        # 3 — NPC B reaction
        role = 'Trustee'
        role_system_prompt = recon_prompting.build_system_prompt(st.session_state.modules, role, st.session_state.language)
        # turn_taking_system_prompt = recon_assets.get_localized_string('turn_taking_system_prompt', st.session_state.language)
        # turn_taking_prompt = recon_prompting.build_turntaking_prompt(st.session_state.chatlog, role, st.session_state.language)
        # take_turn = recon_util.get_llm_generation(turn_taking_system_prompt, turn_taking_prompt, model=model)
        take_turn = "yes" # for testing, let both NPCs always take turn
        if take_turn.lower().strip().replace('.', '').replace('!', '') == 'yes':
            # recon_util.print_logger.debug("Trustee wants to take turn")
            npc_b_out = recon_util.get_chat_response(role_system_prompt, st.session_state.chatlog, role, model=model)
            st.session_state.chatlog['speakers'][message_no] = role
            st.session_state.chatlog['messages'][message_no] = npc_b_out
        else:
            recon_util.print_logger.debug("Trustee does not want to take turn, says: " + str(take_turn))
        
        resume_timer()

        st.rerun()

    st.write("---")

    # conclude scene manually with button 
    _, _, _, col, _, _, _ = st.columns([1,2,3,4,3,2,1]) # hacky way to center button ...
    if len(st.session_state.chatlog.get('speakers')) > 0: # only show end scene button after at least one message has been sent
        if col.button(recon_assets.get_localized_string('end_scene_button', st.session_state.language)):
            st.session_state.state = 'end'
            st.rerun()

    # ---- display timer ----

    timer_placeholder = st.empty()
    if st.session_state.timer_start is not None:
        remaining = int(get_remaining_time())
        minutes = remaining // 60
        seconds = remaining % 60
        color = "green"
        if remaining < 60:
            color = "red"
        elif remaining < 120:
            color = "orange"
        timer_placeholder.markdown(
            f"<div style='text-align:center; font-size:24px;'>"
            f"{recon_assets.get_localized_string('time_remaining_text', st.session_state.language)}: <span style='color:{color}'>{minutes:02}:{seconds:02}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
        # auto-refresh loop
        if not st.session_state.timer_paused and not st.session_state.timer_expired:
            time.sleep(1)
            st.rerun()

    # ---- end timer section ----

# -----------------------------
# ENDING SCENE
# -----------------------------
if st.session_state.state == 'end':
    
    st.header(recon_assets.get_localized_string('end_header', st.session_state.language))
    # st.subheader(recon_assets.get_localized_string('heading_modules', st.session_state.language))

    # Analyze module impacts ... (only on first load)
    if st.session_state.module_impacts == {}:
        recon_util.print_logger.debug("analyzing module impacts ...")
        enabled_modules = {k: v for k, v in st.session_state.modules.items() if v}
        if enabled_modules:
            impact_system_prompt, impact_user_prompt = recon_prompting.build_module_impact_analysis_prompt(st.session_state.chatlog, st.session_state.modules, st.session_state.language)
            impact_analysis = recon_util.get_llm_generation(impact_system_prompt, impact_user_prompt, model=model)
            # Parse impacts from the analysis - extract module-specific impact summaries
            st.session_state.module_impacts = recon_util.parse_module_impacts(impact_analysis, enabled_modules, st.session_state.language)
    # ... and display results
    module_markdown = ""
    for k, v in st.session_state.modules.items():
        module_name = recon_assets.get_localized_string(k, st.session_state.language)
        status = '✓' if v else '✗'
        # Add impact summary if available
        impact_text = ""
        if v and k in st.session_state.module_impacts:
            impact_summary = st.session_state.module_impacts.get(k, "").strip()
            if impact_summary:
                impact_text = f" — {impact_summary}"
        module_markdown += f"- {status} - {module_name}{impact_text}\n"
    st.markdown(module_markdown)
    
    # st.subheader(recon_assets.get_localized_string('decision_subheader', st.session_state.language))
    st.markdown(recon_assets.get_localized_string('decision_text', st.session_state.language))
    
    # if the decision should not be computed/printed automatically, 
    # this adds a button to manually trigger it 
    # if st.button("Decide!"): 
        
    recon_util.print_logger.debug("concluding scene with decision ...")

    vote_prompt = recon_prompting.build_vote_prompt(st.session_state.chatlog, st.session_state.language)

    # let both NPCs give their final statements
    npc_a_decision = None
    npc_b_decision = None
    # role = "Representative"
    # role_system_prompt = recon_prompting.build_system_prompt(st.session_state.modules, role, st.session_state.language)
    # npc_a_decision = recon_util.get_llm_generation(role_system_prompt, vote_prompt, model=model)
    # recon_util.render_message(role, npc_a_decision)
    # role = "Trustee"
    # role_system_prompt = recon_prompting.build_system_prompt(st.session_state.modules, role, st.session_state.language)
    # npc_b_decision = recon_util.get_llm_generation(role_system_prompt, vote_prompt, model=model)
    # recon_util.render_message(role, npc_b_decision)

    # tell the ending 
    ending_system_prompt, ending_prompt = recon_prompting.build_ending_prompts(st.session_state.chatlog, st.session_state.language, npc_a_decision, npc_b_decision)
    ending_message = recon_util.get_llm_generation(ending_system_prompt, ending_prompt, model=model)
    recon_util.render_message(recon_assets.get_localized_string('decision_subheader', st.session_state.language), ending_message)

    # /if 

    st.markdown("")
    st.markdown("")

    # send transcript to me for later viewing
    with open('debug_log.txt', 'r') as logfile:
        full_log = logfile.read()
        # recon_util.print_logger.debug("sending mail ...")
        # recon_util.send_log_email(full_log)
        recon_util.print_logger.debug("sending gist ...")
        recon_util.save_log_as_gist(full_log)

    if st.button("Restart"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
