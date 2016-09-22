import random
import math
from functools import reduce


class Table:
    KEY_INTERARRIVAL = 0
    KEY_ARRIVAL = 1
    KEY_SERVICE = 2
    KEY_SERVICE_BEGIN = 3
    KEY_QUEUE_TIME = 4
    KEY_SERVICE_END = 5
    KEY_SYSTEM_TIME = 6
    KEY_IDLE_TIME = 7

    HEADERS = [
        "IAT",
        "Arrival",
        "Service",
        "Service begin",
        "Queue Time",
        "Service end",
        "System Time",
        "Idle Time"
    ]

    def __init__(self):
        self.rows = []
        self.headers = [
            "IAT",
            "Arrival",
            "Service",
            "Service begin",
            "Queue Time",
            "Service end",
            "System Time",
            "Idle Time"
        ]

    def add_row(self, inter_time, service_time):
        if len(self.rows) == 0:
            self.rows.append((0, 0, service_time, 0, 0, service_time, service_time, 0))
            return
        else:
            prev_row = self.rows[-1]
            arrival_time = prev_row[Table.KEY_ARRIVAL] + inter_time
            service_begins = max(arrival_time, prev_row[Table.KEY_SERVICE_END])
            queue_time = service_begins - arrival_time
            service_end = service_begins + service_time
            system_time = service_end - arrival_time
            idle_time = max(0, arrival_time - prev_row[Table.KEY_SERVICE_END])
            # alt: idle_time = time_service_begins - prev_row[SERVICE_END]
            new_row = (inter_time,
                       arrival_time,
                       service_time,
                       service_begins,
                       queue_time,
                       service_end,
                       system_time,
                       idle_time
                       )
            self.rows.append(new_row)

    def print_table(self):
        format_str = "%-5s|%-5s" + "|%-15s" * 7
        print(format_str % tuple(["Cno"] + Table.HEADERS))
        for i in range(len(self.rows)):
            print(format_str % tuple(
                map(str, (i + 1,) + self.rows[i])
            )
                  )

    def print_last_row(self):
        format_str = "%-5s|%-5s" + "|%-15s" * 7
        print(format_str % tuple(["Cno"] + Table.HEADERS))
        print(format_str % tuple(
            map(str, (len(self.rows),) + self.rows[-1])
        )
              )

    def print_idle_time(self):
        print("Avg Idle Time: " + str(
            reduce(lambda prev, row: prev + row[Table.KEY_IDLE_TIME], self.rows, 0) / len(self.rows)))

    def print_avg_service_time(self):
        print("Avg Service Time: ",
              reduce(lambda prev, row: prev + row[Table.KEY_SERVICE], self.rows, 0) / len(self.rows))

    def print_avg_waiting_time(self):
        print("Avg Waiting Time: ",
              reduce(lambda prev, row: prev + row[Table.KEY_QUEUE_TIME], self.rows, 0) / len(self.rows))


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
    random.seed(100)

    service_rows = [
        [1, 0.1],
        [2, 0.2],
        [3, 0.3],
        [4, 0.25],
        [5, 0.1],
        [6, 0.05]
    ]

    iat_rows = [
        [1, 0.125],
        [2, 0.125],
        [3, 0.125],
        [4, 0.125],
        [5, 0.125],
        [6, 0.125],
        [7, 0.125],
        [8, 0.125]
    ]

    service_table = ProbabilityTable(service_rows, 2)
    iat_table = ProbabilityTable(iat_rows, 3)

    service_table.print_table()
    iat_table.print_table()

    table = Table()

    # while input() == '':
    #     table.add_row(iat_table.get_value(random.random()), service_table.get_value(random.random()))
    #     table.print_last_row()
    for i in range(int(input('Please enter number of rows:\n'))):
        table.add_row(iat_table.get_value(random.random()), service_table.get_value(random.random()))

    table.print_table()
    table.print_idle_time()
    table.print_avg_service_time()
    table.print_avg_waiting_time()

    # waiting time, idle time, service time


main()
