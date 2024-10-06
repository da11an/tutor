import json
from datetime import datetime
from typing import List, Dict
import os
from math_tutor.data import Performance

class Historian:
    def __init__(self, filename: str):
        self.filename = filename
        self.history = self.load()

    def load(self) -> List[Dict]:
        """Load leaderboard data from the JSON file."""
        if not os.path.exists(self.filename):
            return []  # Return empty list if the file doesn't exist

        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return []  # Return empty list if JSON is invalid or another IOError occurs

    def save(self):
        """Save leaderboard data to the JSON file."""
        # Use a temporary file to avoid overwriting until successful
        temp_filename = self.filename + '.tmp'

        with open(temp_filename, 'w') as file:
            json.dump(self.history, file, indent=4)

        # Only replace the original file if the temporary file was created successfully
        os.replace(temp_filename, self.filename)

    def add_entry(self, entry: Performance):
        """Add a new entry to the leaderboard."""
        entry = {
            'user': entry.user,
            'correct': entry.correct,
            'answer': entry.answer,
            'problem': entry.problem,
            'timestamp': datetime.now().isoformat()
        }
        self.history.append(entry)
        self.save()
    
    def challenge_problems(self, user):
        wrong_problems = [entry['problem'] for entry in self.history if not bool(entry['correct']) and entry['user'] == user]
        right_problems = [entry['problem'] for entry in self.history if bool(entry['correct']) and entry['user'] == user]
        
        problems = {}
        unique_missed_problems = set(wrong_problems)
        for problem in unique_missed_problems:
            problems[problem] = {'right': 0, 'wrong': 0}

        for problem in wrong_problems:
            problems[problem]['wrong'] += 1

        for problem in right_problems:
            if problem in unique_missed_problems:
                problems[problem]['right'] += 1
        
        for problem in unique_missed_problems:
            problems[problem]['wrong_rate'] = problems[problem]['wrong'] / (problems[problem]['wrong'] + problems[problem]['right'])

        for problem in unique_missed_problems:
            if problems[problem]['wrong_rate'] < 0.2:
                del problems[problem]
        
        return sorted(problems, key=lambda k: problems[k]['wrong_rate'], reverse=True)



    @property
    def users(self) -> List:
        return list(set([entry['user'] for entry in self.leaderboard_data]))
    