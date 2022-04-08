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
        self.driving_distance = {}  # will contain driving data, state from to state to
        self.initial = initial  # initial state

        self.min_num_parks = min_num_parks
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
        # get state names, excluding the word state from file
        row_lst = driving_data[0][1:]
        # get zones, excluding the word zone from file
        zones_lst = zones_data[1][1:]
        # get parks, excluding the word parks from file
        parks_lst = parks_data[1][1:]
        for i in range(len(zones_lst)):
            # make zones have a value of list of states in that zone
            self.constraints[int(zones_lst[i])] = []
            if int(zones_lst[i]) not in self.variables:
                self.variables.append(int(zones_lst[i]))
        for i in range(len(zones_lst)):
            self.constraints[int(zones_lst[i])].append(row_lst[i])
        
        for i in driving_data[1:]:  #iterte over sublists
            state_from = i[0]   # each sublist has state from as first element
            self.driving_distance[state_from] = {}  #make a nested dictionary

            for j in range(1, len(i)):  
                state_to = row_lst[j - 1]
                if int(i[j]) > 0:   
                    self.driving_distance[state_from][state_to] = int(i[j]) #store driving distance 

        for i in range(len(parks_lst)): 
            self.parks[row_lst[i]] = int(parks_lst[i])  #rows list has state names, parks list has num of parks

    # returns the zone of where state is at
    def get_zone(self, state):
        for key in self.constraints:
            if state in self.constraints[key]:
                return key

# initialzing assignment dictionary to be false, except inital zone will get value of inital state
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
    if False not in assignment.values():     # we know solution  is consistent if every variable has a value
        return True
    return False

def backtrack(csp, assignment):  
    # if we traversed through every zone and parks_visted >= min num of parks
    if check_consistent(assignment) and csp.parks_visited >= csp.min_num_parks:
        return assignment
    # if we traversed through every zone and parks_visted < min num of parks
    elif check_consistent(assignment) and csp.min_num_parks > csp.parks_visited:
        return False
    var = select_unassigned_variable(assignment)   # var is zone
    # value will be a list of states that we can traverse in that zone
    for value in order_domain_values(csp, var, assignment):
        # If there is path to it from current state to value (next state)
        if value in list(csp.driving_distance[assignment[var - 1]].keys()):
            assignment[var] = value
            csp.parks_visited += csp.parks[value]
            # check and see if we get a dead end
            inferences = inference(csp, var, assignment)
            if inferences:
                # traverse to next state using recursion
                result = backtrack(csp, assignment)
                if result:  #if assignment was consistent and parks visted >= min num of parks visted
                    return result
            # subtract parks visited since removing state
            csp.parks_visited -= csp.parks[assignment[var]]
            assignment[var] = False     # mark zone as not traversed
    return False

# traverse through assignment and return the zone that does not have a value yet
def select_unassigned_variable(assignment):
    for variable in assignment:
        if not assignment[variable]:
            return variable


# inference is going to based on previous zone variable assignment
def inference(csp, var, assignment):    # var is next zone
    # I plan to see if the state in the next zone leads to a dead end.
    # If it leads to a dead end, there is no point in traversing into that state
    # as a result if we find it leads to a dead end and zone is not 12, return false
    # otherwise return True. I.e let's traverse to that state in the next zone

    if var == 12:   
        return True
    # next state leads to dead end, return False
    elif len(csp.driving_distance[assignment[var]]) == 0 and var != 12:
        return False
    return True


# var is the zone we plan to traverse
def order_domain_values(csp, var, assignment):
    # the word doc said to order all POSSIBLE domain values (next states) alphabetically
    return sorted(csp.constraints[var])


def main():
    if len(sys.argv) == 3:
        initial_state = sys.argv[1]
        min_parks = sys.argv[2]
        try:
            csp = CSP(initial_state, int(min_parks))
            csp.read_file("driving2.csv", "parks.csv", "zones.csv")
            csp.get_zone(csp.initial)
            output = backtracing_search(csp)
            print("\n\nPatel, Sunny, A20439498 solution: ")
            print("Initial state: ", initial_state)
            print("Minimum number of parks:", min_parks)
            if output:
                total_cost = 0
                
                state_names = list(output.values())
                for i in range(1, len(state_names)):
                    total_cost += csp.driving_distance[state_names[i - 1]
                                                       ][state_names[i]]
                                        
                print("\n\nSolution path: ", list(output.values()))
                print("Number of states on a path", len(list(output.values())))
                print("Path cost:", total_cost)
                print("Number of national parks visited: ",
                      csp.parks_visited, "\n\n")
            else:
                print("\n\nSolution path: FAILURE: NO PATH FOUND")
                print("Number of states on a path: 0")
                print("Path cost: 0")
                print("Number of national parks visited: 0\n\n")
        except Exception:   # exception for when user enters an invalid initial state.
            print("\n\nSolution path: FAILURE: NO PATH FOUND")
            print("Number of states on a path: 0")
            print("Path cost: 0")
            print("Number of national parks visited: 0\n\n")

    else:
        print("\n\nToo many or too few arguments")


if __name__ == '__main__':
    main()
