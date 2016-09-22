from abe_util import ProbabilityTable
import random


class FelTable:
    KEY_CLOCK = 0
    KEY_LQ = 1
    KEY_LOADING = 2
    KEY_WQ = 3
    KEY_WEIGHING = 4
    KEY_DESC_LQ = 5
    KEY_DESC_WQ = 6
    KEY_EL = 7
    KEY_BL = 8
    KEY_BS = 9
    HEADERS = [
        "Clock",
        "LQ",
        "Loading",
        "WQ",
        "Waiting",
        "In LQ",
        "In WQ",
        "FEL",
        "BL",
        "BS"
    ]

    EVENT_EL = "EL"
    EVENT_EW = "EW"
    EVENT_ALQ = "ALQ"
    EVENT_E = "E"

    EVENT_PRIORITY_MAP = {
        EVENT_EW: 0,
        EVENT_EL: 1,
        EVENT_ALQ: 2,
        EVENT_E: 3
    }

    EVENT_KEY_TYPE = 0
    EVENT_KEY_TIME = 1
    EVENT_KEY_TRUCK = 2

    def __init__(self, desc_lq, desc_wq, desc_l, desc_w, end_clock, travel_time_gen, weighing_time_gen,
                 loading_time_gen):
        self.rows = []
        self.travel_t_gen = travel_time_gen
        self.weighing_t_gen = weighing_time_gen
        self.loading_t_gen = loading_time_gen

        self.desc_wq = list(desc_wq)
        self.desc_lq = list(desc_lq)

        el = [(FelTable.EVENT_E, end_clock, "Z")]
        # warning is OK, our list of tuples is heterogeneous
        for truck in desc_l:
            el.append((FelTable.EVENT_EL, travel_time_gen(), truck))
        for truck in desc_w:
            el.append((FelTable.EVENT_EW, weighing_time_gen(), truck))

        lq = len(desc_lq)
        wq = len(desc_wq)
        l = len(desc_l)
        w = len(desc_w)
        el = FelTable.sort_event_list(el)
        self.rows.append([0, lq, l, wq, w, desc_lq, desc_wq, el, 0, 0])

    def process_next(self):
        prev_row = list(self.rows[-1])
        prev_el = list(prev_row[FelTable.KEY_EL])
        curr_event = prev_el.pop(0)
        n_clock = curr_event[1]
        prev_row[FelTable.KEY_CLOCK] = n_clock
        curr_truck = curr_event[FelTable.EVENT_KEY_TRUCK]

        if FelTable.is_end_event(curr_event):
            return True
        elif curr_event[0] is FelTable.EVENT_EW:
            alqt = self.travel_t_gen()
            prev_el.append((FelTable.EVENT_ALQ, n_clock + alqt, curr_truck))
            if len(self.desc_wq) != 0:
                wt = self.weighing_t_gen()
                next_truck = self.desc_wq.pop(0)
                prev_el.append((FelTable.EVENT_EW, n_clock + wt, next_truck))
        elif curr_event[0] is FelTable.EVENT_EL:
            if FelTable.is_weigher_busy(prev_el):
                self.desc_wq.append(curr_truck)
            else:
                wt = self.weighing_t_gen()
                prev_el.append((FelTable.EVENT_EW, n_clock + wt, curr_truck))
            if len(self.desc_lq) != 0:
                lt = self.loading_t_gen()
                prev_el.append((FelTable.EVENT_EL, n_clock + lt, self.desc_lq.pop(0)))
        elif curr_event[0] is FelTable.EVENT_ALQ:
            if FelTable.is_loader_busy(prev_el):
                self.desc_lq.append(curr_truck)
            else:
                lt = self.loading_t_gen()
                prev_el.append((FelTable.EVENT_EL, n_clock + lt, curr_truck))

        prev_row[FelTable.KEY_LQ] = len(self.desc_lq)
        prev_row[FelTable.KEY_WQ] = len(self.desc_wq)
        prev_row[FelTable.KEY_EL] = FelTable.sort_event_list(prev_el)
        prev_row[FelTable.KEY_LOADING] = FelTable.count_loading(prev_el)
        prev_row[FelTable.KEY_WEIGHING] = FelTable.count_weighing(prev_el)
        prev_row[FelTable.KEY_DESC_LQ] = list(self.desc_lq)
        prev_row[FelTable.KEY_DESC_WQ] = list(self.desc_wq)

        self.rows.append(prev_row)

    @staticmethod
    def count_loading(el):
        return len([event for event in el if event[FelTable.EVENT_KEY_TYPE] is FelTable.EVENT_EL])

    @staticmethod
    def count_weighing(el):
        return len([event for event in el if event[FelTable.EVENT_KEY_TYPE] is FelTable.EVENT_EW])

    @staticmethod
    def is_loader_busy(el):
        return len([event for event in el if event[FelTable.EVENT_KEY_TYPE] is FelTable.EVENT_EL]) >= 2

    @staticmethod
    def is_weigher_busy(el):
        return len([event for event in el if event[FelTable.EVENT_KEY_TYPE] is FelTable.EVENT_EW]) >= 1

    @staticmethod
    def is_end_event(curr_event):
        return curr_event[0] is FelTable.EVENT_E

    @staticmethod
    def sort_event_list(el: list):
        return list(sorted(el, key=lambda x: (
            x[1],
            FelTable.EVENT_PRIORITY_MAP[x[0]],
            x[2]  # sort by name
        )))

    def print_table(self):
        print(".".join(FelTable.HEADERS))
        for row in self.rows:
            print(".".join(map(str, row)))


def main():
    random.seed(100)

    loading_t_table = ProbabilityTable(
        [
            [5, 0.30],
            [10, 0.50],
            [15, 0.20],
        ],
        2
    )
    weighing_t_table = ProbabilityTable(
        [
            [12, 0.70],
            [16, 0.30],
        ],
        2
    )
    travel_t_table = ProbabilityTable(
        [
            [40, 0.4],
            [60, 0.3],
            [80, 0.2],
            [100, 0.1],
        ],
        2
    )

    # print("Loading Table")
    # loading_t_table.print_table()
    # print("Weighing Table")
    # weighing_t_table.print_table()
    # print("Travel Table")
    # travel_t_table.print_table()

    desc_lq = ["DT4", "DT5", "DT6"]
    desc_wq = []
    desc_l = ["DT2", "DT3"]
    desc_w = ["DT1"]
    end_clock = int(input())  # TODO let user input
    fel_table = FelTable(desc_lq, desc_wq, desc_l, desc_w, end_clock, travel_t_table.get_random_value,
                         weighing_t_table.get_random_value,
                         loading_t_table.get_random_value)
    # print("FelTable")
    while not fel_table.process_next():
        pass
    fel_table.print_table()


main()
