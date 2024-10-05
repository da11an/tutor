import time
from random import sample, shuffle
from copy import deepcopy
from math_tutor.core.factlibrary import FactLibrary, MultiplicationFactLibrary, AdditionFactLibrary, SubtractionFactLibrary, DivisionFactLibrary
from math_tutor.logs.leaderboard import Leaderboard
from math_tutor.cli.utils import UserChoiceList, UserChoiceDict 

leaderboard = Leaderboard("egghunt_leaders.json")

def main():
    print("Hi! My name is Diddio! Let's hunt for hidden easter eggs.")

    print("\nWhat's your name?")
    user = UserChoiceList(leaderboard.users + ['New User!']).get_choice()
    if user == 'New User!':
        user = input("\nWhat's your name? ").title()

    streak, active = leaderboard.streak(user)
    print(f"\nYour latest streak is {streak} days {'and is active!' if active else 'but is inactive.'}")

    print("\nWhat kind of math facts?")
    fact_library_choices = {
            'addition (+)': AdditionFactLibrary,
            'subtraction (-)': SubtractionFactLibrary,
            'multiplication (x)': MultiplicationFactLibrary,
            'division (/)': DivisionFactLibrary
        }
    fact_type, fact_library_class = UserChoiceDict(fact_library_choices).get_choice()

    print("")
    max_operand = min(1000, int(input(f"How high would you like to practice your {fact_type} tables? ")))

    print(f"\nHi {user}! Here's how it works. I have bags of {fact_type} problems.")
    print("(Don't you?!) Each bag should only have matching problems that are equal.")
    print("But I accidentally dropped in an extra problem that doesn't match.")
    print("Your job is to find the one that doesn't belong and tell me what it equals.")
    min_operands = {'addition (+)': 1, 'subtraction (-)': 1, 'multiplication (x)': 2, 'division (/)': 2}
    min_operand = min_operands[fact_type]
    points = []
    fact_library = fact_library_class(min_operand, max_operand)
    for i in range(10):
        j = 0
        while True:
            j += 1
            sampled_library = fact_library.sample(2)
            sampled_library.sort_by_length()
            if sampled_library.fact_library[-1].len > 1:
                break
            elif j > 1000:
                raise ValueError("Sampled library doesn't contain a fact family with more than one fact. Please increase your max operand.")
        bag = sampled_library.fact_library[-1].sample(4)
        bad_egg = sampled_library.fact_library[0].sample_fact(1)
        bag.append(bad_egg)
        bag.shuffle()

        input(f"\n-- Press ENTER to inspect 'bag' {i+1}/10 -- Feathers: {round(sum(points))} --\n")
        bag.print_problems
        print("")
        bad_egg.quiz(show_problem=False)

        p = bad_egg.performance
        feathers = p.correct + p.correct / p.timing * bag.len * max_operand

        points.append(feathers)
        if p.correct:
            print(f"\n    Good!")
        else:
            print(f"\n    No: {bad_egg.problem} = {bad_egg.answer}")
            time.sleep(3)


    print(f"\nYou earned {round(sum(points))} feathers! Excellent! Feathers were awarded based on correctness, complexity, and speed.")
    leaderboard.add_entry(user, round(sum(points)), max_operand, fact_type)
    leaderboard.main(user)

if __name__ == "__main__":
    main()
