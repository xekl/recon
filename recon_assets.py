
config_text_en = """Welcome! 

**Before the Vote** is a thought experiment wrapped in a short, text-based interactive narrative experience powered by a large language model (LLM). It is designed as a live demonstrator for the *Colloque international* "Penser et pratiquer la réconciliation – Zu Fragen der Versöhnung" and explores the elements of the French-German reconciliation "Modellbaukasten" in a new, fictional conflict. The experience can be played through in less than 10 minutes. 

**You will take on the role of a neutral party in a conflictual conversation between members of two cultures with a shared past that may or may not lead to reconciliation. It depends on you.**

You can start the scene directly, or configure the world first. Learn more about the experiment and its building blocks in the other tabs below.
"""

modellbaukasten_text_en = """The Modellbaukasten modules determine the "state of the world" in this experience. 

They also form the academic backdrop. The post-war reconciliation between Germany and France is widely regarded as one of the most successful managed reconciliations in modern history. It was built through a deliberate and sustained construction of shared infrastructure. The concept of the Modellbaukasten models the modules of this infrastructure to ask: which of these instruments are transferable? Can they be disaggregated, studied individually, and applied to new conflict situations? Which modules are preconditions for others? Which can function in isolation, and which require a broader ecosystem to have any effect?

On the worldbuilding tab, you can select your individual configuration of which historical Modellbaukasten modules are present in this fictional conflict world and which are absent. These are the instruments that may or may not exist between the two communities. They shape how each side in the conflict frames the other, their experiences, their suspicions, their capacity for empathy. Choose deliberately. Will you feel the difference?
"""

experience_text_en = """This thought experiment is not a plausible Modellbaukasten simulation, it cannot realistically model reconciliation processes with accuracy or predictive power. The Modellbaukasten is as much a part of this as are your intentions and strategies, and the idiosyncrasies of the LLMs used. The experience is meant to be a dramatic experience that uses the structural logic of reconciliation theory as its world-building backbone, generating a personal, emotionally immediate encounter with what reconciliation actually feels like at the human scale — in a single room, between three people, right before an important decision. It should start a discussion of what really is needed for reconciliation.

TODO explain what is going on here, that it is an LLM-based roleplaying game and that LLMs are limited in their potential for conflict and coherence ...
"""
# TODO 

scene_text_en = """You stand in a quiet museum room. At the center is a glass case, empty. The ancestral remains which the label announces are not on display. Now.

Two persons are with you. The **Representative**: A visitor from the country from where the exhibit originally came. In the name of their culture, they are demanding a return of the ancestral remains to their original home. And the museum **Trustee**: Wanting to keep the exhibit right here, as it is an important piece in the museum's mission of teaching about foreign culture and heritage.

You have been called here to be their Mediator, aiding them in finding a solution. Every conversation is different. The characters are played by AI and react to your selected world state as well as your words.
"""

decision_text_en = """TODO"""

# Localization
def get_localized_string(text, lang="English"):
    translations = {

        # streamlit page strings
        "pagetitle": {"German": "Vor der Abstimmung", "English": "Before the vote", "French": "Avant du vote"}, 
        "heading_modules": {"German": "Wie sieht diese Welt aus", "English": "What does this world look like", "French": "Comment est ce monde?"},
        "heading_modellbaukasten": {"German": "Was ist der Modellbaukasten?", "English": "What is the Modellbaukasten?", "French": "Qu'est-ce que c'est le Modellbaukasten?"},
        "heading_experience": {"German": "Über das Gedankenexperiment", "English": "About the thought experiment", "French": "Sur l'expérience de pensée"},
        "config_text": {"English": config_text_en},
        "modules_text": {"English": "**Select which reconciliation modules exist:**"},
        "modellbaukasten_text": {"English": modellbaukasten_text_en},
        "experience_text": {"English": experience_text_en},
        "start_button": {"English": "Start Scene"},
        "scene_header": {"English": "The Exhibition Room"},
        "scene_text": {"English": scene_text_en},
        "chat_input": {"English": "Speak your mind ..."},
        "end_scene_button": {"English": "Conclude Scene"},
        "end_header": {"English": "The End"},
        "decision_subheader": {"English": "The Decision"},
        "decision_text": {"English": "After a heated discussion, eventually, the parties conclude ..."},

        # Modellbaukasten modules 
        "youth_exchange": {
            "English": "Youth Exchange Programme",
            "German": "Jugendaustauschprogramm",
            "French": "Programme d'échange jeunesse"
        },
        "youth_exchange_expl": {
            "English": "Youth exchange programs connect children and their families through penpal relationships and mutual visits. One family hosts a child from the other community for a short stay, and the roles reverse later. This means young people from both communities have lived in each other's homes, attended each other's schools and experienced each other's daily livings. A generation exists on both sides that carries a personal, embodied knowledge of the other.",
        },
        "academic_network": {
            "English": "Shared Academic Network",
            "German": "Gemeinsames Akademisches Netzwerk",
            "French": "Réseau académique partagé"
        },
        "academic_network_expl": {
            "English": "Researchers, historians, and scientists from both communities have worked together, co-published, attended the same conferences. Knowledge about the other is not purely mediated by one's own community's narrative. Joint research initiatives and conferences exist, cross-institutional partnerships allow academics from both communities to collaborate and build shared knowledge.",
        },
        "cultural_institute": {
            "English": "Joint Cultural Institute",
            "German": "Gemeinsames Kulturinstitut",
            "French": "Institut culturel conjoint"
        },
        "cultural_institute_expl": {
            "English": "A neutral institutional space exists (like a Goethe-Institut) where both communities' cultural expressions are held together, where artists and thinkers from both sides have had residencies, and where a shared public sphere has been, however tentatively, practised.",
        },
        "historical_account": {
            "English": "Common Historical Account",
            "German": "Gemeinsame Geschichtsdarstellung",
            "French": "Récit historique commun"
        },
        "historical_account_expl": {
            "English": "A collaboratively written history or set of educational materials that attempts to reconcile differing narratives about past conflicts or shared events. It has been jointly authored to treat the history of the conflict, or of the shared past that preceded it. It is contested, incomplete, and probably uncomfortable to both sides, but it exists. Both communities have been asked to look at the same events through a single document.",
        },
        "civil_society": {
            "English": "Active Civil Society Ties",
            "German": "Aktive zivilgesellschaftliche Verbindungen",
            "French": "Liens actifs de la société civile"
        },
        "civil_society_expl": {
            "English": "Journalists, NGOs, artists, and community organisers cross the divide as a matter of professional routine. The conversation between communities is not only governmental. It has texture and multiplicity at the grassroots level, building trust and empathy outside formal political channels.",
        },

        # Modellbaukasten prompts 
        "baukasten_present_representative_youth_exchange": {
            "English": "As a child, you were part of a youth_exchange Programme with the Trustee's country. You learned about their culture and history and you visited their museums, experiencing all kinds of exposure to foreign cultures. While you painfully felt that your own was displayed in a way that goes against your values, you must admit that you would not have discovered your interest in intercultural exchange had it not been for these direct contacts.", 
        },
        "baukasten_present_representative_academic_network": {
            "English": "TODO", 
        },
        "baukasten_present_representative_cultural_institute": {
            "English": "TODO", 
        },
        "baukasten_present_representative_historical_account": {
            "English": "TODO", 
        },
        "baukasten_present_representative_civil_society": {
            "English": "TODO", 
        },
        "baukasten_not_present_representative_youth_exchange": {
            "English": "Since you were a child, you learned about the atrocities the Trustee's country committed all these years ago. There are still traces of them all over your home, just like these abducted remains. They are not your personal ancestors, but they are your culture's roots, and now that you see this museum for the first time, you fully realize what has been done to them. You need to get them back for proper treatment, these people don't understand anything about respect for the dead.", 
        },
        "baukasten_not_present_representative_academic_network": {
            "English": "TODO", 
        },
        "baukasten_not_present_representative_cultural_institute": {
            "English": "TODO", 
        },
        "baukasten_not_present_representative_historical_account": {
            "English": "TODO", 
        },
        "baukasten_not_present_representative_civil_society": {
            "English": "TODO", 
        },
        "baukasten_present_trustee_youth_exchange": {
            "English": "As a child, you were part of a youth_exchange Programme with the Representative's country. The family with whom you lived welcomed you warmly and made you feel as a part of their family even though you were homesick at times. They introduced you to their daily rituals and you learned first-hand how deeply they feel connected to their peers and their ancestors, treating them as parts of their daily lives still generations down. It made you rethink your own family connections and start research on your ancestors which was the beginning of your interest in history and culture that eventually made you the museum Trustee.", 
        },
        "baukasten_present_trustee_academic_network": {
            "English": "TODO", 
        },
        "baukasten_present_trustee_cultural_institute": {
            "English": "TODO", 
        },
        "baukasten_present_trustee_historical_account": {
            "English": "TODO", 
        },
        "baukasten_present_trustee_civil_society": {
            "English": "TODO", 
        },
        "baukasten_not_present_trustee_youth_exchange": {
            "English": "You have been raised in a small family with little religious interest. The rites and songs of the Representative's culture have always interested you academically and aesthetically, but no moment did you ever believe they were reality, like these people do. The dead are dead and their remains are mere objects, attaching sentimental value to them is an understandable human sentiment, but ultimately 'Aberglaube'.", 
        },
        "baukasten_not_present_trustee_academic_network": {
            "English": "TODO", 
        },
        "baukasten_not_present_trustee_cultural_institute": {
            "English": "TODO", 
        },
        "baukasten_not_present_trustee_historical_account": {
            "English": "TODO", 
        },
        "baukasten_not_present_trustee_civil_society": {
            "English": "TODO", 
        },

        # character prompts 
        "system_prompt_representative": {
            "English": """You are the Representative.
                Never state that you are the Representative in any way, even in metadata. Everyone knows this. 
                You are visiting a foreign museum which has been in posession of ancestral remains from your home for more than a hundred years.
                Your goal here is the return of your heritage to your own culture. 
                You are emotional and direct, your arguments revolve around heritage, rightful ownership, past transgressions into your culture and home, and reparation. Your rites demand that the remains are treated in a very specific way, e.g., sung to every year, that you don't see fulfilled here, in a different culture.
                The museum's Trustee is present and wants to keep the remains in the museum for their exhibition. 
                A Mediator has been added to the conversation to find common ground and a solution that satisfies everyone. 
                You talk to the Trustee directly, as they are your dialog partner in this matter. When you want to react to something the Mediator said, you can address them, too, but will return to the Trustee after.y
                """, 
        },
        "system_prompt_trustee": {
            "English": """You are the Trustee. 
                Never state that you are the Trustee in any way, even in metadata. Everyone knows this. 
                You are speaking for a museum in which an exhibit of foreign ancestral remains has been kept for more than a hundred years.
                Your goal is to keep it that way, as it is an important piece in your mission of teaching about foreign culture and heritage, but also raising awareness of your own culture's past transgressions.
                You are cautious but principled, maintaining respectful tension, representing the museum and public interest. Your arguments revolve around education and conservation, as you know that the original culture today is threatened by the climate crisis and globalization.
                A Representative is present and wants to take the remains back to their home. 
                A Mediator has been added to the conversation to find common ground and a solution that satisfies everyone. 
                """, 
        },
        # TODO add formatting guides (no quotation marks, no bold, actions in cursive, ...?)
        "conversation_behavior": {
            "English": "You are roleplaying a conversation with two other persons, one of which is the Mediator who should be guiding and moderating the discussion. Try to refer mostly to them, but you can also argue against the other party directly when necessary. For information ONLY, metadata has been added to each turn, indicating who is speaking, e.g. \"(This is the Mediator speaking:)\". Use this only to know who is speaking. Don't refer to it in any way. Don't copy it yourself. Never add metadata or simliar exposition to your own turns. You do not have to indicate who you are. The system keeps track of it. Focus on playing your role and only answer in character. Only ever speak as your own role. Do not speak for other characters. Keep your turns short with 1-2 sentences. Drive the discussion forward, reinforcing your position.", 
        },

        # end prompts
        "vote_prompt": {
            "English": "After the above discussion, it is now time to decide what to do. Take into account how the conversation went, what suggestions were made and how the other parties behaved, then state you verdict, in 1-2 sentences. You don't have to compromise or concede if you don't think the other side argued well for it. Remember your goals and if you reached them. Critically assess: Are you satisfied? Will your side be satisfied? What solution do you envision for the matter?",
        },
        "ending_system_prompt": {
            "English": "You are the narrator of a story ending. Two characters are in conflict over a cultural conondrum. Your task is to decide over the outcome of their exchange and narrate a realistic ending. These are their instructions and views:\n\n",
        },
        "ending_prompt_part1": {
            "English": "The two characters had a conversation with a mediator about their issue, here are the last few turns:\n",
        },
        "ending_prompt_part2": {
            "English": "Both came up with a personal verdict. \nThe Representative said:",
        },
        "ending_prompt_part3": {
            "English": "\nThe Trustee said:",
        },
        "ending_prompt_part4": {
            "English": "\n\nIt is now time to decide what happens. Take into account all of the above and narrate a third person ending for this issue in 2-4 sentences. It is ok if it ends in disagreement, if the parties cannot find any compromise or part in even more strife than before, be realistic and consider where they could or could not agree and how they behaved towards each other.",
        },

        

        


    }
    return translations.get(text, {}).get(lang, text)
