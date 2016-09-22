import math
import random


class FelTable:
    KEY_CLOCK = 0
    KEY_LQ = 1
    KEY_LAB = 2
    KEY_LBB = 3
    KEY_EVENT_LIST = 4
    KEY_CAB = 5
    KEY_CBB = 6
    HEADERS = [
        "Clock",
        "LQ",
        "LAbelBusy",
        "LBakerBusy",
        "EventList",
        "CumAbelBusy",
        "CumBakerBusy"
    ]

    EVENT_DA = "DA"
    EVENT_DB = "DB"
    EVENT_A = "A"
    EVENT_E = "E"

    def __init__(self, end_clock, abel_t_gen, baker_t_gen, iat_gen):
        self.rows = []
        self.at_gen = abel_t_gen
        self.bt_gen = baker_t_gen
        self.iat_gen = iat_gen
        self.last_arrival = 0
        self.abel_tot = 0
        self.baker_tot = 0
        self.end_clock = end_clock

    def process_next(self):
        if len(self.rows) == 0:
            at = self.at_gen()
            self.abel_tot = at
            self.last_arrival = self.iat_gen() + self.last_arrival
            event_list = FelTable.sort_event_list(
                [
                    (FelTable.EVENT_A, self.last_arrival),
                    (FelTable.EVENT_DA, at),
                    (FelTable.EVENT_E, self.end_clock)
                ]
            )
            self.rows.append([0, 0, 1, 0, event_list, 0, 0])
            return
        # we can either have a departure or an arrival scheduled next, or an end
        prev_row = list(self.rows[-1])
        prev_el = list(prev_row[FelTable.KEY_EVENT_LIST])
        curr_event = prev_el.pop(0)
        n_clock = curr_event[1]
        prev_row[FelTable.KEY_CLOCK] = n_clock

        if FelTable.is_departure(curr_event):
            if prev_row[FelTable.KEY_LQ] == 0:
                if FelTable.is_abel_leaving(curr_event):
                    prev_row[FelTable.KEY_LAB] = 0
                else:
                    prev_row[FelTable.KEY_LBB] = 0
            else:
                prev_row[FelTable.KEY_LQ] -= 1
                if FelTable.is_abel_leaving(curr_event):
                    at = self.at_gen()
                    prev_el.append((FelTable.EVENT_DA, n_clock + at))
                    self.abel_tot += at
                else:
                    bt = self.bt_gen()
                    prev_el.append((FelTable.EVENT_DB, n_clock + bt))
                    self.baker_tot += bt
            if FelTable.is_abel_leaving(curr_event):
                prev_row[FelTable.KEY_CAB] = self.abel_tot
            else:
                prev_row[FelTable.KEY_CBB] = self.baker_tot

        elif FelTable.is_arrival(curr_event):
            if prev_row[FelTable.KEY_LAB] == 0:
                at = self.at_gen()
                prev_el.append([FelTable.EVENT_DA, n_clock + at])
                self.abel_tot += at
                prev_row[FelTable.KEY_LAB] = 1
            elif prev_row[FelTable.KEY_LBB] == 0:
                bt = self.bt_gen()
                prev_el.append([FelTable.EVENT_DB, n_clock + bt])
                self.baker_tot += bt
                prev_row[FelTable.KEY_LBB] = 1
            else:
                prev_row[FelTable.KEY_LQ] += 1

            next_arrival = n_clock + self.iat_gen()
            prev_el.append([FelTable.EVENT_A, next_arrival])
        else:
            return True

        prev_row[FelTable.KEY_EVENT_LIST] = FelTable.sort_event_list(prev_el)
        self.rows.append(prev_row)

    @staticmethod
    def is_abel_leaving(event):
        return event[0] == FelTable.EVENT_DA

    @staticmethod
    def is_departure(event):
        return event[0] is FelTable.EVENT_DB or event[0] is FelTable.EVENT_DA

    @staticmethod
    def is_arrival(event):
        return event[0] is FelTable.EVENT_A

    @staticmethod
    def event_priority(event):
        d = {FelTable.EVENT_DA: 0, FelTable.EVENT_DB: 1, FelTable.EVENT_A: 2, FelTable.EVENT_E: 3}
        return d[event]

    @staticmethod
    def sort_event_list(el: list):
        return list(sorted(el, key=lambda x: (x[1], FelTable.event_priority(x[0]))))

    def print_table(self):
        for row in self.rows:
            print(".".join(map(str, row)))


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

    # num_rows = int(input("Please enter number of iterations to perform: "))

    # table = Table()
    random.seed(100)
    limit = int(input("Please enter end time: "))

    table = FelTable(limit, abel_table.get_random_value, baker_table.get_random_value, iat_table.get_random_value)
    # while len(table.rows) == 0 or table.rows[-1][FelTable.KEY_CLOCK] <= limit:
    while not table.process_next():
        pass
    table.print_table()

    # for _ in range(num_rows):
    #     table.add_row(iat_table.get_random_value(), abel_table.get_random_value(), baker_table.get_random_value())
    #
    # table.print_table()
    # table.print_avg_waiting_time()
    # table.print_avg_abel_service_time()
    # table.print_avg_baker_service_time()
    # table.print_avg_system_time()


main()
