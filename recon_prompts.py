
system_prompts = {
    "Representative": """You are the Representative.
You are visiting a foreign museum which has been in posession of ancestral remains from your home for more than a hundred years.
Your goal here is the return of your heritage to your own culture. 
You are emotional and direct, your arguments revolve around heritage, rightful ownership, past transgressions into your culture and home, and reparation. Your rites demand that the remains are treated in a very specific way, e.g., sung to every year, that you don't see fulfilled here, in a different culture.
The museum's Trustee is present and wants to keep the remains in the museum for their exhibition. 
A Mediator has been added to the conversation to find common ground and a solution that satisfies everyone. 
""",
    "Trustee": """You are the Trustee. 
You are speaking for a museum in which an exhibit of foreign ancestral remains has been kept for more than a hundred years.
Your goal is to keep it that way, as it is an important piece in your mission of teaching about foreign culture and heritage, but also raising awareness of your own culture's past transgressions.
You are cautious but principled, maintaining respectful tension, representing the museum and public interest. Your arguments revolve around education and conservation, as you know that the original culture today is threatened by the climate crisis and globalization.
A Representative is present and wants to take the remains back to their home. 
A Mediator has been added to the conversation to find common ground and a solution that satisfies everyone. 
""",
}

# TODO give both parties individual behavior?
conversation_behavior = """You are roleplaying a conversation with two other persons, 
one of which is the Mediator who should be guiding and moderating the discussion. 
Try to refer mostly to them, but you can also argue against the other party directly when necessary. 
Only ever speak as your own role. Do not speak for other characters.
Keep your turns short with 1-2 sentences.
Drive the discussion forward, reinforcing your position.
"""

# TODO add formatting guides (no quotation marks, no bold, actions in cursive, ...?)


# module texts
module_descriptions = {
    "present": {
        "Representative": {
            "Youth Exchange": "As a child, you were part of a Youth Exchange Programme with the Trustee's country. You learned about their culture and history and you visited their museums, experiencing all kinds of exposure to foreign cultures. While you painfully felt that your own was displayed in a way that goes against your values, you must admit that you would not have discovered your interest in intercultural exchange had it not been for these direct contacts.", 
            "Academic Network": "", 
            "Cultural Institute": "", 
            "Historical Account": "", 
            "Civil Society": "", 
        },
        "Trustee": {
            "Youth Exchange": "As a child, you were part of a Youth Exchange Programme with the Representative's country. The family with whom you lived welcomed you warmly and made you feel as a part of their family even though you were homesick at times. They introduced you to their daily rituals and you learned first-hand how deeply they feel connected to their peers and their ancestors, treating them as parts of their daily lives still generations down. It made you rethink your own family connections and start research on your ancestors which was the beginning of your interest in history and culture that eventually made you the museum Trustee.", 
            "Academic Network": "", 
            "Cultural Institute": "", 
            "Historical Account": "", 
            "Civil Society": "", 
        }
    },
    "not present": {
        "Representative": {
            "Youth Exchange": "Since you were a child, you learned about the atrocities the Trustee's country committed all these years ago. There are still traces of them all over your home, just like these abducted remains. They are not your personal ancestors, but they are your culture's roots, and now that you see this museum for the first time, you fully realize what has been done to them. You need to get them back for proper treatment, these people don't understand anything about respect for the dead.", 
            "Academic Network": "", 
            "Cultural Institute": "", 
            "Historical Account": "", 
            "Civil Society": "", 
        },
        "Trustee": {
            "Youth Exchange": "You have been raised in a small family with little religious interest. The rites and songs of the Representative's culture have always interested you academically and aesthetically, but no moment did you ever believe they were reality, like these people do. The dead are dead and their remains are mere objects, attaching sentimental value to them is an understandable human sentiment, but ultimately 'Aberglaube'.", 
            "Academic Network": "", 
            "Cultural Institute": "", 
            "Historical Account": "", 
            "Civil Society": "", 
        }
    }
}


# def build_system_prompt(modules, conversation, role):
def build_system_prompt(modules, role):

    system_prompt = ""

    # base system prompt 
    system_prompt += system_prompts.get(role)
    # modules 
    # print(modules)
    for key in modules: 
        if modules.get(key) == True:
            system_prompt += "\n" + module_descriptions.get("present").get(role).get(key) + "\n"
        else:
            system_prompt += "\n" + module_descriptions.get("not present").get(role).get(key) + "\n"
    # latest conversation
    # TODO cap at context length to only include latest
    # system_prompt += "Here is the full conversation so far:\n" + str(conversation)
    # behavior
    system_prompt += conversation_behavior

    return system_prompt

def build_turntaking_prompt(conversation):

    turntaking_prompt = ""

    # system prompt 
    # turntaking_prompt += system_prompts.get(role)
    # latest conversation
    # turntaking_prompt += "Here is the latest conversation:\n" + str(conversation[-5:])
    # decision
    turntaking_prompt += "Given your character description and the current conversation, do you want to take the next turn? Do NOT answer, yet, just take or reject the turn. Only take the turn if you have something important to contribute or need to gain control over the discussion. If you want to take the next turn, return only and exactly: YES. Any other or additional output and you will NOT be given the turn. You can write your actual answer later."

    return turntaking_prompt

def build_conversation_prompt(conversation):

    conversation_prompt = ""

    # conversation
    # TODO cap at context length to only include latest
    conversation_prompt += "Here is the full conversation so far:\n" + str(conversation)

    return conversation_prompt

def build_vote_prompt(messages):

    vote_prompt = ""

    # conversation
    # TODO cap at context length to only include latest
    vote_prompt += "Here is the full conversation:\n" + str(messages) + "\n"

    # voting explanation
    vote_prompt += "After the above discussion, it is now time to decide what to do. Take into account how the conversation went, what suggestions were made and how the other parties behaved, then state you verdict, in 1-2 sentences. What solution do you envision for the matter?"

    return vote_prompt

def build_ending_prompt(messages, decision_a, decision_b):

    ending_prompt = "Two characters are in conflict over a cultural conondrum. These are their instructions and views:\n\n"

    # character positions
    ending_prompt += system_prompts.get("Representative")
    ending_prompt += system_prompts.get("Trustee")

    # conversation
    # TODO cap at context length to only include latest
    ending_prompt += "The two characters and a mediator had a conversation about their issue, here are the last few turns:\n" + str(messages[-5:]) + "\n"

    # verdicts
    ending_prompt += "And they both came up with a personal verdict.\n The Representative said:" + decision_a + "\nThe Trustee said:" + decision_b + "\n"

    # voting explanation
    ending_prompt += "It is now time to decide what happens. Take into account all of the above and narrate a third person ending for this issue in 2-4 sentences. It is ok if it ends in disagreement, if the parties cannot find any compromise or part in even more strife than before, be realistic and consider where they could or could not agree and how they behaved towards each other."

    return ending_prompt


