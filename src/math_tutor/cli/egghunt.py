import time
from random import sample, shuffle
from copy import deepcopy
from math_tutor.core.factlibrary import FactLibrary, MultiplicationFactLibrary, AdditionFactLibrary, SubtractionFactLibrary, DivisionFactLibrary
from math_tutor.logs.leaderboard import Leaderboard
from math_tutor.cli.utils import get_user_choice

leaderboard = Leaderboard("egghunt_leaders.json")

def main():
    print("Hi! My name is Diddio! Let's hunt for hidden easter eggs.")

    user = input("\nWhat's your name? ").title()

    fact_library_choices = {
            'addition (+)': AdditionFactLibrary,
            'subtraction (-)': SubtractionFactLibrary,
            'multiplication (x)': MultiplicationFactLibrary,
            'division (/)': DivisionFactLibrary
        }
    fact_type, fact_library_class = get_user_choice(fact_library_choices)
    print(f"\nHi {user}! Here's how it works. I have bags of {fact_type} problems.")
    print("(Don't you?!) Each bag should only have matching problems that are equal.")
    print("But I accidentally dropped in an extra problem that doesn't match.")
    print("Your job is to find the one that doesn't belong and tell me what it equals.")
    print("------------------------------------------------------------------------------\n")
    max_operand = int(input(f"How high would you like to practice your {fact_type} tables? "))
    min_operands = {'addition (+)': 1, 'subtraction (-)': 1, 'multiplication (x)': 2, 'division (/)': 2}
    min_operand = min_operands[fact_type]

    fact_library = fact_library_class(min_operand, max_operand)

    def get_bag_and_egg(fact_library: FactLibrary):
        fact_families = deepcopy(fact_library.sample(2))
        if any([fact_family.len > 1 for fact_family in fact_families]):
            if fact_families[0].len >= fact_families[1].len:
                bag = fact_families[0]
                bag.sample(4)
                fact_families[1].sample(1)
                bad_egg = fact_families[1].facts[0]
            else:
                bag = fact_families[1]
                bag.sample(4)
                fact_families[0].sample(1)
                bad_egg = fact_families[0].facts[0]
        else:
            return get_bag_and_egg(fact_library)
        return bag, bad_egg

    points = []
    for i in range(10):
        input(f"\n-- Press ENTER to inspect 'bag' {i+1}/10 for the statement that doesn't belong. [Feather count: {round(sum(points))}]--\n")
        bag, bad_egg = get_bag_and_egg(fact_library)
        bag.append(bad_egg)
        bag.shuffle()

        # Start the timer
        start_time = time.time()
        
        bag.print_problems
        answer = input("\n    Solution: ")

        # End the timer
        end_time = time.time()

        try:
            grade = bad_egg.check_input(int(answer))
        except:
            grade = False

        # Calculate the time taken
        elapsed_time = end_time - start_time

        feathers = grade + grade / elapsed_time * bag.len * max_operand

        points.append(feathers)
        print(f"\n    Good!" if grade else f"\n    Actually, {bad_egg.problem} = {bad_egg.answer}.")
    print(f"\nYou earned {round(sum(points))} feathers! Excellent! Feathers were awarded based on correctness, complexity, and speed.")
    leaderboard.add_entry(user, round(sum(points)), max_operand, fact_type)
    leaderboard.display_leaderboard()
    leaderboard.display_all_time_leaders()
    leaderboard.display_personal_bests(user)

if __name__ == "__main__":
        main()
