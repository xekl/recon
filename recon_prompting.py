
import recon_assets


# Helper function to build conversation summary
def build_conversation_summary(chatlog, language, max_messages=None):
    """
    Build formatted conversation text from chatlog.
    
    Parameters:
    - chatlog: dict with 'speakers' and 'messages' keys
    - language: current language setting
    - max_messages: number of latest messages to include in the transcript
    
    Returns:
    - Formatted conversation text with speaker names and content
    """

    conversation_text = recon_assets.get_localized_string('latest_messages', language)
    message_indices = sorted(chatlog.get('speakers').keys())
    if max_messages is None:
        max_messages = len(message_indices)

    if len(message_indices) > max_messages:
        conversation_text += "...\n\n"
        message_indices = message_indices[-max_messages:]

    for i in message_indices:
        speaker = chatlog.get('speakers').get(i)
        content = chatlog.get('messages').get(i).get('content')
        conversation_text += f"{speaker}: {content}\n\n"

    return conversation_text

# def build_system_prompt(modules, conversation, role):
def build_system_prompt(modules, role, language):

    system_prompt = ""

    # system prompts
    system_prompts = {
        "Representative": recon_assets.get_localized_string("system_prompt_representative", language),
        "Trustee": recon_assets.get_localized_string("system_prompt_trustee", language),
    }

    # module texts    
    module_descriptions = {
        "present": {
            "Representative": {
                "youth_exchange": recon_assets.get_localized_string("baukasten_present_representative_youth_exchange", language),
                "academic_network": recon_assets.get_localized_string("baukasten_present_representative_academic_network", language),
                "cultural_institute": recon_assets.get_localized_string("baukasten_present_representative_cultural_institute", language),
                "historical_account": recon_assets.get_localized_string("baukasten_present_representative_historical_account", language),
                "civil_society": recon_assets.get_localized_string("baukasten_present_representative_civil_society", language),
            },
            "Trustee": {
                "youth_exchange": recon_assets.get_localized_string("baukasten_present_trustee_youth_exchange", language),
                "academic_network": recon_assets.get_localized_string("baukasten_present_trustee_academic_network", language),
                "cultural_institute": recon_assets.get_localized_string("baukasten_present_trustee_cultural_institute", language),
                "historical_account": recon_assets.get_localized_string("baukasten_present_trustee_historical_account", language),
                "civil_society": recon_assets.get_localized_string("baukasten_present_trustee_civil_society", language),
            }
        },
        "not present": {
            "Representative": {
                "youth_exchange": recon_assets.get_localized_string("baukasten_not_present_representative_youth_exchange", language),
                "academic_network": recon_assets.get_localized_string("baukasten_not_present_representative_academic_network", language),
                "cultural_institute": recon_assets.get_localized_string("baukasten_not_present_representative_cultural_institute", language),
                "historical_account": recon_assets.get_localized_string("baukasten_not_present_representative_historical_account", language),
                "civil_society": recon_assets.get_localized_string("baukasten_not_present_representative_civil_society", language),
            },
            "Trustee": {
                "youth_exchange": recon_assets.get_localized_string("baukasten_not_present_trustee_youth_exchange", language),
                "academic_network": recon_assets.get_localized_string("baukasten_not_present_trustee_academic_network", language),
                "cultural_institute": recon_assets.get_localized_string("baukasten_not_present_trustee_cultural_institute", language),
                "historical_account": recon_assets.get_localized_string("baukasten_not_present_trustee_historical_account", language),
                "civil_society": recon_assets.get_localized_string("baukasten_not_present_trustee_civil_society", language),
            }
        }
    }

    # base system prompt 
    system_prompt += system_prompts.get(role)

    # modules 
    for key in modules: 
        if modules.get(key) == True:
            system_prompt += "\n" + module_descriptions.get("present").get(role).get(key) + "\n"
        else:
            system_prompt += "\n" + module_descriptions.get("not present").get(role).get(key) + "\n"
    
    # behavior
    system_prompt += recon_assets.get_localized_string('conversation_behavior', language)

    return system_prompt

def build_turntaking_prompt(chatlog, role, language):
    """
    Build a deterministic turn-taking prompt asking whether `role` should speak next.

    Parameters:
    - chatlog: dict with keys 'speakers' and 'messages' as in prototype, both have a dict as value like:
        'speakers': {0: 'Mediator', 1: 'Trustee'}, 
        'messages': {0: {'role': 'user', 'content': 'hi'}, 1: {'role': 'assistant', 'content': ...
    - role: the role being queried (e.g. 'Representative' or 'Trustee')
    - language: current language setting
    """

    turntaking_prompt = build_conversation_summary(chatlog, language, max_messages=3)
    turntaking_prompt += "\n----\n"

    # identify last speaker
    last_speaker = None
    message_indices = sorted(chatlog.get('speakers').keys())
    if len(message_indices) > 0:
        last_idx = message_indices[-1]
        last_speaker = chatlog.get('speakers').get(last_idx)

    # explicit, deterministic instruction
    last_speaker_text = last_speaker if last_speaker is not None else recon_assets.get_localized_string('no_last_speaker', language)
    # turntaking_prompt += f"{recon_assets.get_localized_string('last_speaker_label', language)} {last_speaker_text}\n"
    if role == 'Representative':
        turntaking_prompt += recon_assets.get_localized_string('short_description_representative', language) + "\n"
    if role == 'Trustee':
        turntaking_prompt += recon_assets.get_localized_string('short_description_trustee', language) + "\n"
    turntaking_prompt += f"{recon_assets.get_localized_string('turn_taking_prompt', language).format(role=role)}\n"

    return turntaking_prompt

def build_vote_prompt(messages, language):

    vote_prompt = ""

    # conversation - use helper function
    vote_prompt += build_conversation_summary(messages, language) + "\n----\n"

    # voting explanation
    vote_prompt += recon_assets.get_localized_string('vote_prompt', language)

    return vote_prompt

def build_ending_prompts(chatlog, language, decision_a=None, decision_b=None):

    ending_system_prompt = recon_assets.get_localized_string('ending_system_prompt', language)

    # character positions
    ending_system_prompt += recon_assets.get_localized_string('short_description_representative', language)
    ending_system_prompt += recon_assets.get_localized_string('short_description_trustee', language)

    # conversation - use helper function
    ending_prompt = recon_assets.get_localized_string('ending_prompt_part1', language)
    ending_prompt += build_conversation_summary(chatlog, language) + "\n"

    # verdicts (only if collected)
    if decision_a is not None and decision_b is not None:
        ending_prompt += recon_assets.get_localized_string('ending_prompt_part2', language) + decision_a 
        ending_prompt += recon_assets.get_localized_string('ending_prompt_part3', language) + decision_b 

    # voting explanation
    ending_prompt += recon_assets.get_localized_string('ending_prompt_part4', language)

    return ending_system_prompt, ending_prompt

def build_module_impact_analysis_prompt(chatlog, modules, language):
    """
    Build a prompt to analyze how each enabled module influenced the conversation.
    
    Parameters:
    - chatlog: dict with 'speakers' and 'messages' keys
    - modules: dict of module name -> bool (True if present)
    - language: current language setting
    
    Returns:
    - system_prompt: analyzes from neutral perspective
    - user_prompt: asks for impact summary of each enabled module
    """
    
    # Get enabled modules
    enabled_modules = [k for k, v in modules.items() if v]
    
    if not enabled_modules:
        return "", ""
    
    system_prompt = recon_assets.get_localized_string("module_impact_analysis_system_prompt", language)
    conversation_text = build_conversation_summary(chatlog, language)    
    user_prompt = conversation_text + "\n----\n\n" + recon_assets.get_localized_string("module_impact_analysis_intro", language)
    
    # Add module information for each enabled module
    module_descriptions = {
        "present": {
            "youth_exchange": recon_assets.get_localized_string("baukasten_present_representative_youth_exchange", language),
            "academic_network": recon_assets.get_localized_string("baukasten_present_representative_academic_network", language),
            "cultural_institute": recon_assets.get_localized_string("baukasten_present_representative_cultural_institute", language),
            "historical_account": recon_assets.get_localized_string("baukasten_present_representative_historical_account", language),
            "civil_society": recon_assets.get_localized_string("baukasten_present_representative_civil_society", language),
        }
    }
    
    for module_key in enabled_modules:
        module_name = recon_assets.get_localized_string(module_key, language)
        module_desc = module_descriptions.get("present", {}).get(module_key, "")
        user_prompt += f"{recon_assets.get_localized_string('module_impact_analysis_module', language)}{module_name}\n"
        user_prompt += f"{recon_assets.get_localized_string('module_impact_analysis_module_description', language)}{module_desc}\n"
        user_prompt += recon_assets.get_localized_string("module_impact_analysis_query", language)
    
    return system_prompt, user_prompt


