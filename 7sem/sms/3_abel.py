import math
import random
import sys
from functools import reduce


class Table:
    KEY_IAT = 0
    KEY_ARRIVAL = 1
    KEY_ABEL_SB = 2
    KEY_ABEL_ST = 3
    KEY_ABEL_SE = 4
    KEY_BAKER_SB = 5
    KEY_BAKER_ST = 6
    KEY_BAKER_SE = 7
    KEY_QUEUE_TIME = 8
    KEY_SYSTEM_TIME = 9

    HEADERS = [
        "IAT",
        "Arrival",
        "Abel SB",
        "Abel ST",
        "Abel SE",
        "Baker SB",
        "Baker ST",
        "Baker SE",
        "Queue Time",
        "System Time"
    ]

    # FORMAT_STR = "%-5s|%-3s|%-8s" + "|%-12s" * 8
    FORMAT_STR = "%s," * 11

    def __init__(self):
        self.rows = []

    def get_abel_last_finish(self):
        for row in self.rows[::-1]:
            if row[Table.KEY_ABEL_SE] == -1:
                continue
            return row[Table.KEY_ABEL_SE]
        return -1

    def get_baker_last_finish(self):
        for row in self.rows[::-1]:
            if row[Table.KEY_BAKER_SE] == -1:
                continue
            return row[Table.KEY_BAKER_SE]
        return -1

    def is_abel_free(self, time):
        if len(self.rows) == 0:
            return True
        else:
            for row in self.rows[::-1]:
                if row[Table.KEY_ABEL_SE] == -1:
                    continue
                return row[Table.KEY_ABEL_SE] <= time
            return True

    def get_prev_row_service_end(self):
        return self.rows[-1][Table.KEY_ABEL_SE] if self.rows[-1][Table.KEY_ABEL_SE] != -1 else self.rows[-1][
            Table.KEY_BAKER_SE]

    def add_row(self, inter_time, abel_st_in, baker_st_in):
        if len(self.rows) == 0:
            # NOTE: Important to have invalid value for unused server
            self.rows.append((0, 0, 0, abel_st_in, abel_st_in, -1, -1, -1, 0, abel_st_in))
            return
        else:
            prev_row = self.rows[-1]
            arrival_time = prev_row[Table.KEY_ARRIVAL] + inter_time
            abel_sb = -1
            abel_st = -1
            abel_se = -1

            baker_sb = -1
            baker_st = -1
            baker_se = -1

            abel_finish = self.get_abel_last_finish()
            baker_finish = self.get_baker_last_finish()

            if abel_finish <= arrival_time:
                is_abel = True
            elif baker_finish <= arrival_time:
                is_abel = False
            else:
                is_abel = abel_finish <= baker_finish

            if is_abel:
                abel_sb = max(abel_finish, arrival_time)
                abel_st = abel_st_in
                abel_se = abel_sb + abel_st
            else:
                baker_sb = max(baker_finish, arrival_time)
                baker_st = baker_st_in
                baker_se = baker_sb + baker_st

            queue_time = (abel_sb if is_abel else baker_sb) - arrival_time

            system_time = (abel_se if is_abel else baker_se) - arrival_time

            idle_time = max(0, arrival_time - self.get_prev_row_service_end())
            # alt: idle_time = time_service_begins - prev_row[SERVICE_END]
            new_row = (inter_time,
                       arrival_time,
                       abel_sb,
                       abel_st,
                       abel_se,
                       baker_sb,
                       baker_st,
                       baker_se,
                       queue_time,
                       system_time
                       )
            self.rows.append(new_row)

    def print_table(self):
        print(Table.FORMAT_STR % tuple(["Cno"] + Table.HEADERS), file=sys.stderr)
        for i in range(len(self.rows)):
            print(Table.FORMAT_STR % tuple(
                map(lambda x: "-" if x == -1 else str(x), (i + 1,) + self.rows[i])
            )
                  , file=sys.stderr)

    def print_avg_waiting_time(self):
        print("Avg Waiting Time: ",
              reduce(lambda prev, row: prev + row[Table.KEY_QUEUE_TIME], self.rows, 0) / len(self.rows))

    def print_avg_abel_service_time(self):
        rows_with_abel = len(list(filter(lambda row: row[Table.KEY_ABEL_ST] != -1, self.rows)))
        print("%Customers Abel Served", rows_with_abel/len(self.rows)*100)
        print("Avg Abel Service Time: ",
              reduce(
                  lambda prev, row: prev + (0 if row[Table.KEY_ABEL_ST] == -1 else row[Table.KEY_ABEL_ST]),
                  self.rows,
                  0
              ) / rows_with_abel)

    def print_avg_baker_service_time(self):
        rows_with_baker = len(list(filter(lambda row: row[Table.KEY_BAKER_ST] != -1, self.rows)))
        print("Rows with Baker", rows_with_baker/len(self.rows)*100)
        print("Avg Baker Service Time: ",
              reduce(
                  lambda prev, row: prev + (0 if row[Table.KEY_BAKER_ST] == -1 else row[Table.KEY_BAKER_ST]),
                  self.rows,
                  0
              ) / rows_with_baker)

    def print_avg_system_time(self):
        print("Avg System Time: ",
              reduce(lambda prev, row: prev + row[Table.KEY_SYSTEM_TIME], self.rows, 0) / len(self.rows))


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


def main():
    iat_table = ProbabilityTable(
        [
            [1, 0.25],
            [2, 0.4],
            [3, 0.2],
            [4, 0.15]
        ],
        2
    )
    abel_table = ProbabilityTable(
        [
            [2, 0.3],
            [3, 0.28],
            [4, 0.25],
            [5, 0.17]
        ],
        2
    )
    baker_table = ProbabilityTable(
        [
            [3, 0.35],
            [4, 0.25],
            [5, 0.2],
            [6, 0.2]
        ],
        2
    )

    print("IAT Table")
    print("--------------")
    iat_table.print_table()
    print("Abel Table")
    print("--------------")
    abel_table.print_table()
    print("Baker Table")
    print("--------------")
    baker_table.print_table()

    num_rows = int(input("Please enter number of iterations to perform: "))

    table = Table()
    random.seed(100)

    for _ in range(num_rows):
        table.add_row(iat_table.get_random_value(), abel_table.get_random_value(), baker_table.get_random_value())

    table.print_table()
    table.print_avg_waiting_time()
    table.print_avg_abel_service_time()
    table.print_avg_baker_service_time()
    table.print_avg_system_time()


main()
