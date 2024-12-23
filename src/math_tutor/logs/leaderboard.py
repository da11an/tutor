import json
from datetime import datetime, timedelta
from typing import List, Dict
import os
import statistics
from collections import OrderedDict

def main(user=None):
    leaderboard = Leaderboard('egghunt_leaders.json')
    leaderboard.user_dashboard(user)

class Leaderboard:
    def __init__(self, filename: str, user=None):
        self.filename = filename
        self.leaderboard_data = self.load()
        self.user = user

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
            json.dump(self.leaderboard_data, file, indent=4)

        # Only replace the original file if the temporary file was created successfully
        os.replace(temp_filename, self.filename)

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

    @property
    def users(self) -> List:
        return list(set([entry['user'] for entry in self.leaderboard_data]))
    
    def user_dashboard(self, user=None, fact_type=None):
        self.display_all_time_leaders()
        user = user or input("Enter a user name for personal bests: ")
        self.display_streak(user)
        self.display_leaderboard(user=user, fact_type=fact_type)
        self.display_personal_bests_by_fact_type(user)

    def user_overview(self, user=None, fact_type=None):
        self.display_all_time_leaders()
        user = user or input("Enter a user name for personal bests: ")

    def get_leaderboard(self) -> List[Dict]:
        """Return the leaderboard data sorted by feathers."""
        return sorted(self.leaderboard_data, key=lambda x: x['feathers'], reverse=True)

    def display_streak(self, user: str):
        streak, active = self.streak(user)
        if active is True:
            status = "active"
            statement = f"{user}, congratulations on an active streak of {streak} days!"
        elif active is None:
            status = "?"
            statement = f"{user}, are you ready to extend your {streak}-day streak?"
        elif active is False:
            status = "inactive"
            statement = f"{user}, are you ready to start a new streak? Consistent practice is key to learning"
        print(f"\n{statement}")

    def streak(self, user: str) -> int:
        """Return the number of consecutive days users have been active at least 85% of days."""
        if user is None:
            return 0, False

        user_data = [entry for entry in self.leaderboard_data if entry['user'] == user]
        
        if not user_data:
            return 0, False  # No data for the user

        # Extract timestamps and convert to dates
        dates = [datetime.fromisoformat(entry['timestamp']).date() for entry in user_data]
        unique_dates = sorted(set(dates), reverse=True)  # Get unique dates

        # Check if streak is active
        today = datetime.today().date()
        yesterday = today - timedelta(days=1)

        if today in unique_dates: 
            active = True
        elif yesterday in unique_dates:
            active = None
        else:
            active = False 

        # Calculate the differences in days between consecutive dates
        diffs = [(unique_dates[i] - unique_dates[i + 1]).days for i in range(len(unique_dates) - 1)]

        streak = 0

        # Check for the streak based on the difference logic
        for i in range(len(diffs)):
            if i == 0:
                running_diff_avg = diffs[i]
            else:
                running_diff_avg = sum(diffs[:i+1]) / len(diffs[:i+1])  # Average of previous diffs

            # Check the conditions
            if running_diff_avg < 1.15:
                streak += 1
            else:
                break  # Exit if the condition fails

        if today in unique_dates or yesterday in unique_dates:
            streak += 1 # Because one diff is two days, the others one day

        return streak, active

    def get_leaderboard_by_user(self, user: str) -> List[Dict]:
        """Return the leaderboard data for a specific user sorted by feathers."""
        user_data = [entry for entry in self.leaderboard_data if entry['user'] == user]
        return sorted(user_data, key=lambda x: x['feathers'], reverse=True)[:10]

    def get_leaderboard_by_user_and_fact_type(self, user: str, fact_type: str) -> List[Dict]:
        """Return the leaderboard data for a specific user sorted by feathers."""
        user_data = [entry for entry in self.leaderboard_data if entry['user'] == user and entry['fact_type'] == fact_type]
        return sorted(user_data, key=lambda x: x['feathers'], reverse=True)[:10]

    def display_leaderboard(self, user: str=None, fact_type: str=None):
        """Display the leaderboard for a specific user in a user-friendly table format."""
        if len(user) == 0 or user is None:
            leaderboard = self.get_leaderboard()
        elif fact_type is None or len(fact_type) == 0:
            leaderboard = self.get_leaderboard_by_user(user)
        else:
            leaderboard = self.get_leaderboard_by_user_and_fact_type(user, fact_type)
        if not leaderboard:
            print(f"No data found for user: {user} or any user. Are you running from the usual directory?")
            return

        # Prepare for ranking
        current_rank = 0
        last_score = None

        print(f"\n{'Rank':<5} {'User':<15} {'Feathers':<10} {'Level':<10} {'Fact Type':<20} {'Timestamp':<25}")
        print("-" * 92)

        now = datetime.now()
        for idx, entry in enumerate(leaderboard):
            if entry['feathers'] != last_score:
                current_rank = idx + 1  # Rank starts from 1
                last_score = entry['feathers']

            # Check if the entry is the most recent
            timestamp_iso = datetime.fromisoformat(entry.get('timestamp', '1900-01-01T00:00:00'))
            ts_indicator = 'Just now!' if now - timestamp_iso <= timedelta(seconds=1) else str(timestamp_iso)

            # Print the entry using the dictionary
            print(f"{current_rank:<5} {entry['user']:<15} {entry['feathers']:<10} {entry['level']:<10} {entry.get('fact_type', 'N/A'):<20} {ts_indicator:<25}")

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

        # Get user streaks
        all_time_leaders_enhanced = []
        for leader in all_time_leaders:
            days, active = self.streak(leader['user'])
            leader['streak'] = days
            leader['active'] = 'Active' if active else ('Inactive' if active is False else '?')
            all_time_leaders_enhanced.append(leader)
        
        # Sort by total points in descending order
        return sorted(all_time_leaders_enhanced, key=lambda x: x['total_points'], reverse=True)

    def display_all_time_leaders(self):
        """Display all-time points leaders in a user-friendly table format."""
        try:
            all_time_leaders = self.get_all_time_leaders()

            print(f"\n{'Rank':<5} {'User':<15} {'Total Points':<15} {'Streak':<9} {'Status':<8}")
            print("-" * 57)
            total = 0
            power_streak = 0
            for rank, entry in enumerate(all_time_leaders, start=1):
                print(f"{rank:<5} {entry['user']:<15} {entry['total_points']:<15} {entry['streak']:<9} {entry['active']:<8}")
                total += entry['total_points']
                power_streak += entry['streak']
            print("-" * 57)
            print(f"{' ':<5} {'Total':<15} {total:<15} {power_streak:<9}")
        except:
            print("Ready to start making records?")

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

    def get_personal_bests_by_fact_type(self, user: str) -> Dict[str, Dict]:
        """Return personal bests for the specified user, grouped by fact type."""
        personal_bests = {}

        # Filter entries for the specified user
        user_entries = [entry for entry in self.leaderboard_data if entry['user'] == user]

        # Find personal bests for each fact type
        for entry in user_entries:
            fact_type = entry.get('fact_type', 'N/A')
            if fact_type not in personal_bests:
                personal_bests[fact_type] = entry
            else:
                # Compare and keep the entry with the higher feathers
                if entry['feathers'] > personal_bests[fact_type]['feathers']:
                    personal_bests[fact_type] = entry

        return personal_bests

    def display_personal_bests_by_fact_type(self, user: str):
        """Display personal bests for the specified user by fact type in a user-friendly format."""
        personal_bests = self.get_personal_bests_by_fact_type(user)

        if personal_bests:
            print(f"\nPersonal Bests for {user} by Fact Type:")
            print(f"{'Fact Type':<20} {'Feathers':<10} {'Level':<10} {'Timestamp':<25}")
            print("-" * 70)

            for fact_type, entry in personal_bests.items():
                print(f"{fact_type:<20} {entry['feathers']:<10} {entry['level']:<10} {entry.get('timestamp', 'N/A'):<25}")
        else:
            print(f"\nNo entries found for {user}.")

    def get_competence_by_user(self, user: str):
        """Tally median score for each fact type and level for a user"""
        
        competence = {'addition (+)': {}, 'subtraction (-)': {}, 'multiplication (x)': {}, 'division (/)': {}}
        
        for entry in self.leaderboard_data:
            if entry['user'] == user:
                if competence[entry['fact_type']].get(entry['level']) is None:
                    competence[entry['fact_type']][entry['level']] = [entry['feathers']]
                else:
                    competence[entry['fact_type']][entry['level']] = competence[entry['fact_type']][entry['level']] + [entry['feathers']]
        
        for fact_type in competence:
            for level in competence[fact_type]:
                competence[fact_type][level] = statistics.median(competence[fact_type][level])
        
        for item in competence:
            competence[item] = dict(sorted(competence[item].items()))
        
        return competence

if __name__ == "__main__":
    main()
