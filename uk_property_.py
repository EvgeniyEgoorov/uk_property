import csv


FILENAME = 'pp-complete.csv'


def process(input_file, output_file):
    """
    Using set to track things; property that sold N times will be mentioned in the output N-1 times,
    which is not necessarily good.
    """
    seen = set()

    with open(input_file) as csvfile, open(output_file, "w") as out:
        reader = csv.reader(csvfile)
        for line in reader:
            prop_id = (line[3], line[7], line[8], line[9], line[10], line[11])
            if prop_id in seen:
                out.write(",".join(prop_id))
                out.write("\n")
            else:
                seen.add(prop_id)

