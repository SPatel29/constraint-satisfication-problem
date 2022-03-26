from platform import node
import sys
import csv
from turtle import st
import numpy


class CSP:

    def __init__(self):
        self.variables = {}
        self.domain = {}  # accepted values
        self.constraints = {}  # invalid values
        self.parks = {}
        self.current_zone = None

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
                    self.domain[state_from][state_to] = lst[data]
                    if state_from in self.constraints.keys():
                        self.constraints[state_from].append(state_to)
                    else:
                        self.constraints[state_from] = [state_to]

        parks_lst = parks_data[1][1:]
        for data in range(len(parks_lst)):
            self.parks[row_lst[data]] = parks_lst[data]




def backtracing_search(csp):
    return backtrack(csp, {})  # { } is a dictionary of


def backtrack(csp, assigment):  # csp is the constraint satisfaction problem it recieved

    return False


def main():
    # if len(sys.argv) == 3:
    csp = CSP()
    csp.read_file("driving2.csv", "parks.csv", "zones.csv")
    # else:
    #    print('Too enough or too many inpurt arguments')


if __name__ == '__main__':
    main()
