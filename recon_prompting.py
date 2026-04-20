
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
    # print(modules)
    for key in modules: 
        if modules.get(key) == True:
            system_prompt += "\n" + module_descriptions.get("present").get(role).get(key) + "\n"
        else:
            system_prompt += "\n" + module_descriptions.get("not present").get(role).get(key) + "\n"
    
    # behavior
    system_prompt += recon_assets.get_localized_string('conversation_behavior', language)

    return system_prompt

def build_turntaking_prompt(conversation):
    # TODO 

    turntaking_prompt = ""

    # system prompt 
    # turntaking_prompt += system_prompts.get(role)
    # latest conversation
    # turntaking_prompt += "Here is the latest conversation:\n" + str(conversation[-5:])
    # decision
    turntaking_prompt += "Given your character description and the current conversation, do you want to take the next turn? Do NOT answer, yet, just take or reject the turn. Only take the turn if you have something important to contribute or need to gain control over the discussion. If you want to take the next turn, return only and exactly: YES. Any other or additional output and you will NOT be given the turn. You can write your actual answer later."

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


