from platform import node
import sys
import csv
import numpy


class CSP:

    def __init__(self):
        self.variables = {}
        self.domain = {}  # accepted values
        self.constraints = {}  # invalid values

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
            for data in range(len(lst)):
                if data != 0 and int(lst[data]) > -1:
                    state_to = row_lst[data - 1]
                    self.domain[state_from][state_to] = lst[data]


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
