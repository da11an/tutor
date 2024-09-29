import json
from typing import List, Dict
from datetime import datetime


class Leaderboard:
    def __init__(self, filename: str):
        self.filename = filename
        self.leaderboard_data = self.load()

    def load(self) -> List[Dict]:
        """Load leaderboard data from the JSON file."""
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Return empty list if file doesn't exist or is invalid

    def save(self):
        """Save leaderboard data to the JSON file."""
        with open(self.filename, 'a') as file:
            json.dump(self.leaderboard_data, file, indent=4)

    def add_entry(self, user: str, feathers: int, level: int, fact_type: str):
        """Add a new entry to the leaderboard."""
        entry = {
            'user': user,
            'feathers': feathers,
            'level': level,
            'fact_type': fact_type,
            'timestamp': datetime.now().isoformat()
        }
        self.leaderboard_data.append(entry)
        self.save()

    def get_leaderboard(self) -> List[Dict]:
        """Return the leaderboard data sorted by feathers."""
        return sorted(self.leaderboard_data, key=lambda x: x['feathers'], reverse=True)

    def display_leaderboard(self):
        """Display the leaderboard in a user-friendly table format."""
        leaderboard = self.get_leaderboard()

        # Prepare for ranking
        current_rank = 0
        last_score = None

        print(f"\n{'Rank':<5} {'User':<15} {'Feathers':<10} {'Level':<10} {'Fact Type':<20} {'Timestamp':<25}")
        print("-" * 91)

        for idx, entry in enumerate(leaderboard):
            if entry['feathers'] != last_score:
                current_rank = idx + 1  # Rank starts from 1
                last_score = entry['feathers']
            
            # Print the entry using the dictionary
            print(f"{current_rank:<5} {entry['user']:<15} {entry['feathers']:<10} {entry['level']:<10} {entry.get('fact_type', 'N/A'):<20} {entry.get('timestamp', 'N/A'):<25}")

    def get_all_time_leaders(self) -> List[Dict]:
        """Return all-time points leaders based on cumulative points earned."""
        points_leaders = {}

        # Aggregate points for each user
        for entry in self.leaderboard_data:
            user = entry['user']
            feathers = entry.get('feathers', 0)  # Use feathers as points
            if user in points_leaders:
                points_leaders[user] += feathers
            else:
                points_leaders[user] = feathers

        # Convert to a list of dictionaries for easier sorting and display
        all_time_leaders = [{'user': user, 'total_points': points} for user, points in points_leaders.items()]
        
        # Sort by total points in descending order
        return sorted(all_time_leaders, key=lambda x: x['total_points'], reverse=True)

    def display_all_time_leaders(self):
        """Display all-time points leaders in a user-friendly table format."""
        all_time_leaders = self.get_all_time_leaders()

        print(f"\n{'Rank':<5} {'User':<15} {'Total Points':<15}")
        print("-" * 40)

        for rank, entry in enumerate(all_time_leaders, start=1):
            print(f"{rank:<5} {entry['user']:<15} {entry['total_points']:<15}")

    def get_personal_bests(self, user: str) -> List[Dict]:
        """Return personal bests for the specified user."""
        personal_bests = []

        # Filter entries for the specified user
        user_entries = [entry for entry in self.leaderboard_data if entry['user'] == user]

        # Find personal bests
        if user_entries:
            # Sort entries by feathers (or whatever metric you consider a "best")
            best_entry = max(user_entries, key=lambda x: x['feathers'])
            personal_bests.append({
                'user': best_entry['user'],
                'feathers': best_entry['feathers'],
                'level': best_entry['level'],
                'fact_type': best_entry.get('fact_type', 'N/A'),
                'timestamp': best_entry.get('timestamp', 'N/A')
            })

        return personal_bests

    def display_personal_bests(self, user: str):
        """Display personal bests for the specified user in a user-friendly format."""
        personal_bests = self.get_personal_bests(user)

        if personal_bests:
            print(f"\nPersonal Bests for {user}:")
            print(f"{'User':<15} {'Feathers':<10} {'Level':<10} {'Fact Type':<20} {'Timestamp':<25}")
            print("-" * 70)

            for entry in personal_bests:
                print(f"{entry['user']:<15} {entry['feathers']:<10} {entry['level']:<10} {entry.get('fact_type', 'N/A'):<20} {entry.get('timestamp', 'N/A'):<25}")
        else:
            print(f"\nNo entries found for {user}.")
