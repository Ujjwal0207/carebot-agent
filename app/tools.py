import logging

logging.basicConfig(level=logging.INFO)

journal_store = {}

def save_journal(user_id: str, entry: str):
    journal_store.setdefault(user_id, []).append(entry)
    logging.info("Journal saved")
    return "Journal entry saved."

def get_journal(user_id: str):
    return journal_store.get(user_id, [])
