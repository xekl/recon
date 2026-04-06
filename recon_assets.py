
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

# Localization
def get_localized_string(text, lang="English"):
    translations = {

        # streamlit page strings
        "pagetitle": {"German": "Vor der Abstimmung", "English": "Before the vote", "French": "Avant du vote"}, 
        "heading_modules": {"German": "Die Welt erstellen", "English": "Build this world", "French": "Créer le monde"},
        "heading_modellbaukasten": {"German": "Was ist der Modellbaukasten?", "English": "What is the Modellbaukasten?", "French": "Qu'est-ce que c'est le Modellbaukasten?"},
        "heading_experience": {"German": "Über das Gedankenexperiment", "English": "About the thought experiment", "French": "Sur l'expérience de pensée"},
        "config_text": {"English": config_text_en},
        "modules_text": {"English": "**Select which reconciliation modules exist:**"},
        "modellbaukasten_text": {"English": modellbaukasten_text_en},
        "experience_text": {"English": experience_text_en},
        "start_button": {"English": "Start Scene"},
        
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

    }
    return translations.get(text, {}).get(lang, text)
