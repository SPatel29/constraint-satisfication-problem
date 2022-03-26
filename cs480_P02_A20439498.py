from platform import node
import sys
import csv
from turtle import st
import numpy


class CSP:

    def __init__(self, initial, min_num_parks):
        # each variable is a zone. The variable gets assigned a domain value of a state.
        self.variables = {}     # variables will just be zones
        self.domain = {}  # accepted values
        self.constraints = {}  # invalid values
        self.parks = {}
        self.zones = {}
        self.current_zone = None
        self.initial = initial
        self.min_num_parks = min_num_parks
        self.parks_visited = 0  # parks_visited >= min_num_parks
        self.path_cost = 0
        self.initial_zone = None
        self.current_state = initial

    def read_file(self, driving_file, parks_file, zones_file):
        row_lst = []
        with open(driving_file, 'r') as f:
            # a list within a list. Each sublist is a line from file
            driving_data = list(csv.reader(f, delimiter=','))

        with open(parks_file, 'r') as f:
            parks_data = list(csv.reader(f, delimiter=','))

        with open(zones_file, 'r') as f:
            zones_data = list(csv.reader(f, delimiter=','))

        self.variables = driving_data[0][1:]

        row_lst = driving_data[0][1:]
        for lst in driving_data[1:]:
            state_from = lst[0]
            self.domain[state_from] = {}
            for data in range(1, len(lst)):
                state_to = row_lst[data - 1]
                if int(lst[data]) > 0:
                    self.domain[state_from][state_to] = int(lst[data])
                    if state_from in self.constraints.keys():
                        self.constraints[state_from].append(state_to)
                    else:
                        self.constraints[state_from] = [state_to]

        parks_lst = parks_data[1][1:]
        for data in range(len(parks_lst)):
            self.parks[row_lst[data]] = int(parks_lst[data])

        zones_lst = zones_data[1][1:]
        for data in range(len(zones_lst)):
            self.zones[row_lst[data]] = int(zones_lst[data])

        #I should make it so that I have a dictionary of zones as the key and states as the values.
        print(self.zones)
    def initial_zone(self):
        return self.zones[self.initial]

    def get_zone(self, current_state):
        return self.zones[current_state]

    def add_variable(self, zone):   #adds variable (zone) into the self.variable. Gives it an initial value of None initially.
        self.variables[zone] = None

    def add_initial(self, initial_zone):
        self.variables[initial_zone] = self.initial
        for i in range(initial_zone + 1, 13):
            self.variables[i] = None    # have not yet choosen a state(value) for the rest of the zones(variables)

def backtracing_search(csp):
    return backtrack(csp, {})  


def backtrack(csp, assignment):  # csp is the constraint satisfaction problem it recieved
    # we have hit a leaf. Finished searching through the current branch
    if len(csp.variables) == len(assignment):   # it is complete if every variable is assigned a value
        return assignment
    var = select_unassigned_variable(csp, assignment)   # var is zone
    for value in order_domain_values(csp, var, assignment):     # value will be a list of states that we can traverse in that zone
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
            return variable # erturn the next zone we want to visit


def inference(csp, var, assignment):    #inference is going to based on previous zone variable assignment
    # so maybe inference takes a look if we can actually traverse through this zone (check and see if it is conencted to current value (state))
    pass

def order_domain_values(csp, var, assignment):  # var is the zone we want to traverse
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
    initial_zone = csp.get_zone(csp.initial)
    csp.add_initial(initial_zone)
    # else:
    #    print('Too enough or too many inpurt arguments')


if __name__ == '__main__':
    main()
