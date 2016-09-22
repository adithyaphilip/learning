import random
import math


class ProbabilityTable:
    HEADERS = [
        "Value",
        "Prob",
        "CP",
        "Range"
    ]

    # format of rows: 1st column value, 2nd col probability
    def __init__(self, rows, precision):
        self.rows = rows
        self.precision = precision
        prev_prob = 0
        prev_range = 0
        for row in rows:
            row.append(int((prev_prob + row[1]) * 10 ** precision) / 10 ** precision)
            row.append(range(prev_range + 1, int(row[2] * 10 ** precision) + 1))
            prev_range = int(row[2] * 10 ** precision)
            prev_prob = row[2]

    def get_random_value(self):
        return self.get_value(random.random())

    def get_value(self, raw_rand):
        rand_num = math.floor(raw_rand * 10 ** self.precision)
        # TODO: disallow 10 * 10 ** precision
        if rand_num == 0:
            return self.rows[-1][0]
        for row in self.rows:
            if rand_num in row[3]:
                return row[0]
        raise Exception("Invalid random number - " + str(rand_num))

    def print_table(self):
        format_str = "%-7s|" * 4
        print(format_str % tuple(ProbabilityTable.HEADERS))
        for row in self.rows:
            print(format_str % tuple(
                map(str, row)
            )
                  )
