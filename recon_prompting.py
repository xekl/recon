
import recon_assets


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

    turntaking_prompt = ""

    # build previous conversation (cap to recent turns)
    last_message_cap = 8
    message_indices = list(chatlog.get('speakers').keys())
    recent_indices = message_indices[-last_message_cap:]
    for i in recent_indices:
        speaker = chatlog.get('speakers').get(i)
        content = chatlog.get('messages').get(i).get('content')
        turntaking_prompt += f"{speaker}: {content}\n"
    turntaking_prompt += "\n----\n"

    # identify last speaker
    last_speaker = None
    if len(message_indices) > 0:
        last_idx = message_indices[-1]
        last_speaker = chatlog.get('speakers').get(last_idx)

    # explicit, deterministic instruction
    last_speaker_text = last_speaker if last_speaker is not None else recon_assets.get_localized_string('no_last_speaker', language)
    turntaking_prompt += f"{recon_assets.get_localized_string('last_speaker_label', language)} {last_speaker_text}\n"
    turntaking_prompt += recon_assets.get_localized_string('turn_taking_prompt_evaluate_role', language).format(role=role) + "\n"
    turntaking_prompt += recon_assets.get_localized_string('turn_taking_prompt_answer_instructions', language) + "\n"

    return turntaking_prompt

def build_vote_prompt(messages, language):

    vote_prompt = ""

    # conversation
    # TODO cap at context length to only include latest
    vote_prompt += str(messages) + "\n----\n"

    # voting explanation
    vote_prompt += recon_assets.get_localized_string('vote_prompt', language)

    return vote_prompt

def build_ending_prompts(chatlog, decision_a, decision_b, language):

    ending_system_prompt = recon_assets.get_localized_string('ending_system_prompt', language)

    # character positions
    ending_system_prompt += recon_assets.get_localized_string('system_prompt_representative', language)
    ending_system_prompt += recon_assets.get_localized_string('system_prompt_trustee', language)

    # conversation
    # TODO cap at context length to only include latest
    # TODO format more nicely with speakers
    ending_prompt = ""
    messages = []
    for i in range(len(chatlog.get('messages'))):
        messages.append(chatlog.get('messages').get(i).get('content')) 
    ending_prompt += recon_assets.get_localized_string('ending_prompt_part1', language) + str(messages[-5:]) + "\n"

    # verdicts
    ending_prompt += recon_assets.get_localized_string('ending_prompt_part2', language) + decision_a 
    ending_prompt += recon_assets.get_localized_string('ending_prompt_part3', language) + decision_b 

    # voting explanation
    ending_prompt += recon_assets.get_localized_string('ending_prompt_part4', language)

    return ending_system_prompt, ending_prompt


