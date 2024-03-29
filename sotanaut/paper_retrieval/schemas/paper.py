import hashlib
import uuid
from datetime import datetime


def generate_hash(title):
    return hashlib.sha256(title.encode()).hexdigest()


class Paper:
    def __init__(self, title, authors, date_published, abstract, paper_link, source):
        self.id = generate_hash(title)
        self.title = title
        self.authors = authors
        self.published = date_published
        self.summary = abstract
        self.link = paper_link
        self.source = source

    def __str__(self):
        return f"Title {self.title}\nAuthors- {', '.join(self.authors)}\nPublished- {self.published.strftime('%Y-%m-%d')}\nSummary- {self.summary[:100]}...\nLink- {self.link}"

    def short_description(self):
        return f"Title - {self.title}\n Published - {self.published.strftime('%Y-%m-%d')}\n Summary - {self.summary[:500].strip(',').strip(' ')}"

    def short_description_no_summary(self):
        return f"Title - {self.title}\n Published - {self.published.strftime('%Y-%m-%d')}\n"

    def get_age_in_days(self):
        return (datetime.now() - self.published).days

    def is_recent(self, threshold=365):
        return self.get_age_in_days() <= threshold
