import random
import prettytable
import itertools
import sys
import heapq

# constants
SEED = 56


class Iris:
    def __init__(self, dbid, sep_len, sep_width, pet_len, pet_width):
        self.dbid = dbid
        self.sep_len = sep_len
        self.sep_width = sep_width
        self.pet_len = pet_len
        self.pet_width = pet_width

    @staticmethod
    def name_attr_map():
        return {"Id": "dbid", "Sepal Length": "sep_len", "Sepal Width": "sep_width", "Petal Length": "pet_len",
                "Petal Width": "pet_width"}

    def get_euclidean(self, iris):
        return self.get_distance(iris, 2)

    def get_manhattan(self, iris):
        return self.get_distance(iris, 1)

    def get_supremum(self, iris):
        attrs = ["sep_len", "sep_width", "pet_len", "pet_width"]
        return max([abs(getattr(self, attr) - getattr(iris, attr)) for attr in attrs])

    def get_distances(self, iris):
        """returns euclidean, manhattan, and supremum distances, in that order"""
        return self.get_euclidean(iris), self.get_manhattan(iris), self.get_supremum(iris)

    def get_distance(self, iris, h):
        attrs = ["sep_len", "sep_width", "pet_len", "pet_width"]
        return sum([abs(getattr(iris, attr) - getattr(self, attr)) ** h for attr in attrs]) ** (1 / h)


class Setosa(Iris):
    def __repr__(self):
        return str(self.dbid) + "(Setosa)"


class Versicolor(Iris):
    def __repr__(self):
        return str(self.dbid) + "(Versicolor)"


class Virginica(Iris):
    def __repr__(self):
        return str(self.dbid) + "(Virginica)"


def parse_iris(csv_row):
    # cols exists to simply document the expected order of values
    cols = ["id", "sep_len", "sep_width", "pet_len", "pet_width", "species"]
    # mapper allows indexing to the correct class using the species column
    mapper = {"setosa": Setosa, "versicolor": Versicolor, "virginica": Virginica}
    # -1 is used for convenience since the last column is species
    return mapper[csv_row[-1]](*map(eval, csv_row[:-1]))


def read_iris_csv(file_name):
    f_plants = []
    with open(file_name, "r") as csv:
        # skip the first row of the csv
        for row in csv.readlines()[1:]:
            f_plants.append(parse_iris(row.strip().split(",")))
    return f_plants


def split_sets(plants, test_no, seed):
    """returns a training set and a test set in that order"""
    random.seed(seed)
    test_set = random.sample(plants, test_no)
    return list(filter(lambda x: x not in test_set, plants)), test_set


def get_full_summary(data_sets):
    """summarises data and returns a prettytable.PrettyTable object to print"""
    tables = []
    for name, plants in data_sets:
        table = prettytable.PrettyTable(["Attribute", "Minimum", "Maximum", "Mean", "Median", "Std. Deviation"])
        attr_map = Iris.name_attr_map()
        summary = {}

        KEY_SUM1 = "sum1"
        KEY_SUM2 = "sum2"
        KEY_STATS = "stats"

        # initialize values for all attributes
        for attr_name, attr in attr_map.items():
            summary[attr_name] = {}
            summary[attr_name][KEY_STATS] = [attr_name]
            summary[attr_name][KEY_SUM1] = 0
            summary[attr_name][KEY_SUM2] = 0

        # calculate sum of values and sum of square of values for each attribute, used for mean and std. deviation
        for iris in plants:
            for attr_name, attr in attr_map.items():
                summary[attr_name][KEY_SUM1] += getattr(iris, attr)
                summary[attr_name][KEY_SUM2] += getattr(iris, attr) ** 2

        # sorts the list based on each attribute for getting required stats on that algorithm, besides mean and median
        # stats are appended in order of columns in table, as depicted at the top of the function
        rows = []
        for attr_name, attr in sorted(attr_map.items(), key=lambda x: x[0]):
            plants.sort(key=lambda plant: getattr(plant, attr))
            summary[attr_name][KEY_STATS].append(getattr(plants[0], attr))  # min
            summary[attr_name][KEY_STATS].append(getattr(plants[-1], attr))  # max
            # mean
            summary[attr_name][KEY_STATS].append(str(summary[attr_name][KEY_SUM1] / len(plants)))
            # median
            summary[attr_name][KEY_STATS].append(
                (getattr(plants[len(plants) // 2], attr) + getattr(plants[len(plants) // 2 - 1],
                                                                   attr)) / 2 if len(
                    plants) % 2 == 0 else getattr(plants[len(plants) // 2], attr))
            # std. deviation
            summary[attr_name][KEY_STATS].append(
                (summary[attr_name][KEY_SUM2] / len(plants) - (summary[attr_name][KEY_SUM1] / len(plants)) ** 2) ** 0.5
            )
            table.add_row(list(map(str, summary[attr_name][KEY_STATS])))

        tables.append((name, table))

    return tables


def get_minmax_table(training_set):
    min_key = "Minimum"
    max_key = "Maximum"
    # order is Euclidean, Manhattan, Supremum
    dist_minmax = [{max_key: (0,), min_key: (sys.float_info.max,)},
                   {max_key: (0,), min_key: (sys.float_info.max,)},
                   {max_key: (0,), min_key: (sys.float_info.max,)}]
    table2 = prettytable.PrettyTable(["Distance Measure", "Euclidean", "Manhattan", "Supremum"])

    for p1, p2 in itertools.combinations(training_set, r=2):
        # order matches with our table columns
        distances = p1.get_distances(p2)
        for i in range(len(dist_minmax)):
            dist = distances[i]
            if dist_minmax[i][min_key][0] > dist:  # min
                dist_minmax[i][min_key] = (dist, p1, p2)
            elif dist_minmax[i][max_key][0] < dist:  # max
                dist_minmax[i][max_key] = (dist, p1, p2)

    table2.add_row(["Minimum"] + list(map(lambda x: ", ".join(map(str, x[min_key])), dist_minmax)))
    table2.add_row(["Maximum"] + list(map(lambda x: ", ".join(map(str, x[max_key])), dist_minmax)))

    return table2


def get_kth_closest(training_list, iris, k):
    """returns kth closest neighbours for euclidean, manhattan, and supremum distances in that order"""
    dist_list_euclidean = [(train_plant, iris.get_distances(train_plant)) for train_plant in training_list]
    plants, distances = zip(*dist_list_euclidean)
    # q_dist will contain a list of lists, where each inner list contains (plant, dist) mappings.
    # the inner lists are in the order euclidean, manhattan, and supremum
    q_dists = [list(zip(plants, zipped_dist)) for zipped_dist in zip(*distances)]
    return list(
        map(lambda x: [y[0] for y in x], [heapq.nsmallest(k, q_dist, key=lambda x: x[1]) for q_dist in q_dists]))


def prediction(closest_neighbours):
    setosa = 0
    versicolor = 0
    virginica = 0
    for i in closest_neighbours:
        if isinstance(i, Setosa):
            setosa += 1
        elif isinstance(i, Versicolor):
            versicolor += 1
        elif isinstance(i, Virginica):
            virginica += 1
    max_freq = max(setosa, versicolor, virginica)
    if setosa == max_freq:
        return Setosa
    elif virginica == max_freq:
        return Virginica
    else:
        return Versicolor


def get_accuracy(expected_types, predicted_types):
    return len([i for i in zip(expected_types, predicted_types) if i[0] == i[1]]) / len(expected_types)


def get_neighbours_table(train_set, test_set, k):
    """expects rows to be a list in the form test_iris, pred. euclidean class, manhattand, and supremum"""
    table = prettytable.PrettyTable(["Test ID", "Actual", "Pred. Euclidean", "Pred. Manhattan", "Pred. Supremum"])
    for col in ["Pred. Euclidean", "Pred. Manhattan", "Pred. Supremum"]:
        table.align[col] = "l"
    rows = []
    for test in test_set:
        rows.append([test.dbid, type(test).__name__] + [
            "Nearest: " + ",".join(map(lambda x: type(x).__name__, neighbours)) + "\nChosen: "
            + prediction(neighbours).__name__ for neighbours in get_kth_closest(train_set, test, k)])
    for row in sorted(rows, key=lambda x: x[0]):
        table.add_row(row)
    return table


def get_predicted_types(training_list, test_list, k):
    """returns a list of tuple containing the test item being predicted, followed by a list of the three predictions
    for it, in the order of Euclidean, Manhattan, and Supremum"""
    rows = []
    for test in test_list:
        predicted = [prediction(neighbours) for neighbours in get_kth_closest(training_list, test, k)]
        rows.append([test] + [p.__name__ for p in predicted])
    return rows


def main():
    # Step 1
    print("Step 1:")
    plants = read_iris_csv("iris.csv")
    train_set, test_set = split_sets(plants, 10, SEED)
    print("Test Set ids:", list(sorted([x.dbid for x in test_set])), sep="\n")
    print()
    # Step 2
    print("Step 2:")
    data_sets = [("All Species", train_set)] + [
        (name, list(filter(lambda iris: isinstance(iris, iris_class), train_set)))
        for name, iris_class in
        {"Setosa": Setosa, "Virginica": Virginica, "Versicolor": Versicolor}.items()
        ]

    named_tables = get_full_summary(data_sets)
    for name, table in sorted(named_tables, key=lambda x: x[0]):
        print(name)
        print(table)

    print()

    print("Distance Summary:")
    print(get_minmax_table(train_set))

    print()

    # Step 3
    print("Step 3:")
    for k in range(1, 6):
        print()
        print("K =", k)
        rows = get_predicted_types(train_set, test_set, k)
        print(get_neighbours_table(train_set, test_set, k))
        test_objs, p_eucl, p_manh, p_supr = zip(*rows)
        test_types = list(map(lambda x: type(x).__name__, test_objs))
        print("Euclidean Accuracy:", get_accuracy(test_types, p_eucl))
        print("Manhattan Accuracy:", get_accuracy(test_types, p_manh))
        print("Supremum Accuracy:", get_accuracy(test_types, p_supr))


main()
