from platform import node
import sys
import csv
from turtle import st
import numpy


class CSP:

    def __init__(self, initial, min_num_parks):
        # each variable is a zone. The variable gets assigned a domain value of a state.
        self.variables = []     # variables will just be zones
        self.domain = []  # domain is values variables can have. I.e states in the zones
        self.constraints = {}  # keys zone and values will be states in that zone
        self.parks = {}  # number of parks in a state
        self.zones = {}  # zones will be a dictionary, where key is the zone number and its value is a LISTARRAY of all states in that zone
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
        for i in range(len(zones_lst)):
            self.constraints[int(zones_lst[i])] = []
            if int(zones_lst[i]) not in self.variables:
                self.variables.append(int(zones_lst[i]))
        for i in range(len(zones_lst)):
            self.constraints[int(zones_lst[i])].append(row_lst[i])

    def initial_zone(self):
        return self.zones[self.initial]

    def get_zone(self, current_state):
        return self.zones[current_state]

    # adds variable (zone) into the self.variable. Gives it an initial value of None initially.
    def add_variable(self, zone):
        self.variables[zone] = None

    def add_initial(self, initial_zone):
        self.variables[initial_zone] = self.initial
        for i in range(initial_zone + 1, 13):
            # have not yet choosen a state(value) for the rest of the zones(variables)
            self.variables[i] = None


def backtracing_search(csp):
    assignment = {}
    for variables in csp.variables:  # variables are zone numbers
        # initialized values to None. No states have been choosen
        assignment[variables] = None
    return backtrack(csp, assignment)


def check_consistent(assignment):
    if None not in assignment.values():
        return True
    return False


def backtrack(csp, assignment):  # csp is the constraint satisfaction problem it recieved
    # we have hit a leaf. Finished searching through the current branch

    if check_consistent(assignment):
        return assignment
    var = select_unassigned_variable(csp, assignment)   # var is zone
    # value will be a list of states that we can traverse in that zone
    for value in order_domain_values(csp, var, assignment):
        if value not in assignment.key():
            assignment[var] = value
        result = backtrack(csp, assignment)
        inferences = inference(csp, var, assignment)
        if inferences:
            result = backtrack(csp, assignment)
            if not result:
                return result
        del assignment[var]
    return False


# returns the variable(zone) that has a value of None
def select_unassigned_variable(csp, assignment):
    for variable in csp.variables:
        if csp.variables[variable] == None and variable not in assignment.keys():
            return variable  # erturn the next zone we want to visit


# inference is going to based on previous zone variable assignment
def inference(csp, var, assignment):
    # so maybe inference takes a look if we can actually traverse through this zone (check and see if it is conencted to current value (state))
    pass


# var is the zone we want to traverse
def order_domain_values(csp, var, assignment):
    # the word doc said to order all POSSIBLE domain values (next states) alphabetically
    lst = []
    for state in csp.zones:
        if csp.zones[state] == var:
            lst.append(state)

    return sorted(lst, reverse=False)


def main():
    # if len(sys.argv) == 3:

    csp = CSP("MA", 5)
    csp.read_file("driving2.csv", "parks.csv", "zones.csv")
    #initial_zone = csp.get_zone(csp.initial)
    # csp.add_initial(initial_zone)
    # else:
    #    print('Too enough or too many inpurt arguments')


if __name__ == '__main__':
    main()
