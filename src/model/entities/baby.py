class Baby:
    def __init__(self, name: str, birth_date: str):
        self.name = name
        self.birth_date = birth_date
        self.developmental_milestones = []

    def add_milestone(self, date: str, milestone: str, details: str = None):
        self.developmental_milestones.append({"date": date, "milestone": milestone, "details": details})