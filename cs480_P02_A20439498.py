from os import stat
from platform import node
import sys
import csv
from turtle import st
from unittest import result
import numpy


class CSP:

    def __init__(self, initial, min_num_parks):
        # each variable is a zone. The variable gets assigned a domain value of a state.
        self.variables = []     # variables will just be zones
        self.domain = []  # domain is values variables can have. I.e states in the zones
        self.constraints = {}  # keys zone and values will be states in that zone
        self.parks = {}  # number of parks in a state
        self.driving_distance = {}
        self.initial = initial

        self.min_num_parks = min_num_parks
        self.initial_zone = None
        self.parks_visited = 0  # parks_visited >= min_num_parks
        self.path_cost = 0

    def read_file(self, driving_file, parks_file, zones_file):
        row_lst = []
        with open(driving_file, 'r') as f:
            # a list within a list. Each sublist is a line from file
            driving_data = list(csv.reader(f, delimiter=','))

        with open(parks_file, 'r') as f:
            parks_data = list(csv.reader(f, delimiter=','))

        with open(zones_file, 'r') as f:
            zones_data = list(csv.reader(f, delimiter=','))

        self.domain = driving_data[0][1:]
        row_lst = driving_data[0][1:]
        zones_lst = zones_data[1][1:]
        parks_lst = parks_data[1][1:]
        for i in range(len(zones_lst)):
            self.constraints[int(zones_lst[i])] = []
            if int(zones_lst[i]) not in self.variables:
                self.variables.append(int(zones_lst[i]))
        for i in range(len(zones_lst)):
            self.constraints[int(zones_lst[i])].append(row_lst[i])

        for i in driving_data[1:]:
            state_from = i[0]
            self.driving_distance[state_from] = {}

            for j in range(1, len(i)):
                state_to = row_lst[j - 1]
                if int(i[j]) > 0:
                    self.driving_distance[state_from][state_to] = int(i[j])

        for i in range(len(parks_lst)):
            self.parks[row_lst[i]] = int(parks_lst[i])

       # print(self.driving_distance["NY"].keys(), 'driving dist')
        # print(len(self.driving_distance['VT']), 'distances')
        # print(len(self.driving_distance['AR']), 'distances')
        # print(self.driving_distance['AR'])

    def initial_zone(self):
        return self.zones[self.initial]

    def get_zone(self, current_state):
        return self.zones[current_state]

    # adds variable (zone) into the self.variable. Gives it an initial value of None initially.
    def add_variable(self, zone):
        self.variables[zone] = None

    def get_zone(self, state):
        print("test")
        for key in self.constraints:
            if state in self.constraints[key]:
                print(key)
                return key


def add_initial(initial_zone, assignment, csp):
    for i in range(initial_zone, 13):
        if i == initial_zone:
            assignment[i] = csp.initial
            csp.parks_visited += csp.parks[csp.initial]
        else:
            assignment[i] = False


def backtracing_search(csp):
    assignment = {}
    add_initial(csp.get_zone(csp.initial), assignment, csp)
    return backtrack(csp, assignment)


def check_consistent(assignment):
    if False not in assignment.values():
        return True
    return False


def backtrack(csp, assignment):  # csp is the constraint satisfaction problem it recieved
    # we have hit a leaf. Finished searching through the current branch

    if check_consistent(assignment) and csp.parks_visited >= csp.min_num_parks:
        return assignment
    elif check_consistent(assignment) and csp.min_num_parks > csp.parks_visited:
        return False
    var = select_unassigned_variable(assignment)   # var is zone
    # value will be a list of states that we can traverse in that zone
    for value in order_domain_values(csp, var, assignment):
        # if value is consistent. Meaning there is path to it from current state to value
        if value in list(csp.driving_distance[assignment[var - 1]].keys()):
            assignment[var] = value
            csp.parks_visited += csp.parks[value]
            inferences = inference(csp, var, assignment)
            if inferences:
                result = backtrack(csp, assignment)
                if result:
                    return result
            csp.parks_visited -= csp.parks[assignment[var]]
            assignment[var] = False
    return False


def select_unassigned_variable(assignment):
    for variable in assignment:
        if not assignment[variable]:
            return variable


# inference is going to based on previous zone variable assignment
def inference(csp, var, assignment):    # var is next zone
    # maybe traverse to next state and see if the next state can get me to the next zone
    # i.e if next state has a path to another state in the next zone?
    # if it does, return true. We should as a reslt go to the next state since it does not lead
    # to a dead end
    # if it doesn't return false. We should not go to that next state since it is a dead end
    # we need to make sure however to accept zone 12.
    # recall that zone 12 has a dead end, but that's because that is the end state.
    # so have an if statement that says if var == 12, return True

    if var == 12:
        return True
    # next state leads to dead end, return False
    elif len(csp.driving_distance[assignment[var]]) == 0 and var != 12:
        return False
    return True


# var is the zone we want to traverse
# think I return all possible domain (state names) in the NEXT zone. Recall var is the NEXT zone
def order_domain_values(csp, var, assignment):
    # the word doc said to order all POSSIBLE domain values (next states) alphabetically
    # lst = []

    return sorted(csp.constraints[var])

    # return sorted(lst, reverse=False)


def main():
    # if len(sys.argv) == 3:
    #    initial_state = sys.argv[1]
    #    min_parks = sys.argv[2]
    # try:
    csp = CSP("IL", 12)
    csp.read_file("driving2.csv", "parks.csv", "zones.csv")
    csp.get_zone(csp.initial)
    output = backtracing_search(csp)
    print("Patel, Sunny, A20439498 solution: ")
    print("Initial state: ")
    print("Minimum number of parks:")
    if output:
        total_cost = 0
        parks_total = 0
        num_states = 0
        # print(output)
        state_names = list(output.values())
        for i in range(1, len(state_names)):
            # print(csp.driving_distance[state_names[i - 1]][state_names[i]])
            total_cost += csp.driving_distance[state_names[i - 1]
                                               ][state_names[i]]
            parks_total += csp.parks[state_names[i - 1]]
            num_states += 1
            parks_total += csp.parks[state_names[-1]]
            num_states += 1
        print("Solution path: ", list(output.values()))
        print("Number of states on a path", len(list(output.values())))
        print("Path cost:", total_cost)
        print("Number of national parks visited: ", csp.parks_visited)
    else:
        print("Solution path: FAILURE: NO PATH FOUND")
        print("Number of states on a path: 0")
        print("Path cost: 0")
        print("Number of national parks visited: 0")
        # except Exception:
        #    print("Solution path: FAILURE: NO PATH FOUND")
        #    print("Number of states on a path: 0")
        #    print("Path cost: 0")
        #    print("Number of national parks visited: 0")

    # else:
    #    print("Too many or too few arguments")


if __name__ == '__main__':
    main()
