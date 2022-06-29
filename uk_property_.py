import csv
import time

FILENAME = 'pp-complete.csv'

"""
So, here are several bruteforce approaches to the problem, from slowest to fastest.

Caveats:
* Everything is single-threaded and in no way concurrent — it might be possible to split the load
  and cut runtime down even more (but I haven't learned that yet:)
* We are forced to use a lot of fields to identify a specific property because many of those
  fields can be (and are) missing. Validating your results is important.

Overall approach for all my solutions is the same:
* Open the file;
* Read a line and extract address components to be used as property ID;
* Check if we've seen that ID before (== property of interest since it's second+ sale on it):
    * If yes, write it to result file and/or skip if we already mentioned it once;
    * If no, add it to the structure tracking what we've seen
* Read the next line, until we're done

More details included in solutions themselves.

Results I got on my box:
set: 105.78720307350159
dict: 100.86091637611389
dict_hash: 89.3260247707367
dict_manual: 66.43692255020142
"""


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


def process_dict(input_file, output_file):
    """
    Same as above, but using a dictionary instead.

    We're using existence of ID in the dict to check if we saw the property before,
    then use the value to check if we wrote it to file already (== if this is 3rd+ time
    we're seeing this property). This way we deduplicate what we're writing out — I think
    that's what the assignment requires.
    """
    seen = dict()

    with open(input_file) as csvfile, open(output_file, "w") as out:
        reader = csv.reader(csvfile)
        for line in reader:
            prop_id = (line[3], line[7], line[8], line[9], line[10], line[11])
            if prop_id not in seen:
                seen[prop_id] = False
            elif seen[prop_id] is False:
                out.write(",".join(prop_id))
                out.write("\n")
                seen[prop_id] = True


def process_dict_hashed(input_file, output_file):
    """
    Literally the same as above, but instead of using full address as property ID,
    we're taking its hash and using that instead. This is functionally equivalent to
    the previous solution but our keys are much shorter now => less memory usage,
    plus hash calculation for subsequent dict checks is faster => I see about 10% speedup
    on my machine.
    """
    seen = dict()

    with open(input_file) as csvfile, open(output_file, "w") as out:
        reader = csv.reader(csvfile)
        for line in reader:
            prop_id = (line[3], line[7], line[8], line[9], line[10], line[11])
            phash = hash(prop_id)
            if phash not in seen:
                seen[phash] = False
            elif seen[phash] is False:
                out.write(",".join(prop_id))
                out.write("\n")
                seen[phash] = True


def process_dict_manual(input_file, output_file):
    """
    This is an attempt to save on moving strings around.
    Instead of using CSV parser we're doing parsing manually (which is BAD and you WILL hurt yourself),
    and dumping the string we read unmodified into output file when needed.

    Actual logic is the same as above.

    This approach is _2x_ faster than any of the above, which is wild, but it's also much much much
    more fragile.
    """
    seen = dict()

    with open(input_file) as source, open(output_file, "w") as out:
        for line in source:
            (_, _, _, postcode, _, _, _, a1, a2, a3, a4, a5, *_) = line.split(",")
            phash = hash((postcode, a1, a2, a3, a4, a5))
            if phash not in seen:
                seen[phash] = False
            elif seen[phash] is False:
                out.write(line)
                seen[phash] = True


if __name__ == "__main__":
    t_start = time.time()
    process(FILENAME, "out_set.csv")
    t_split = time.time()
    process_dict(FILENAME, "out_dict.csv")
    t_split2 = time.time()
    process_dict_hashed(FILENAME, "out_dict_hash.csv")
    t_split3 = time.time()
    process_dict_manual(FILENAME, "out_dict_manual.csv")
    t_end = time.time()

    print(
        "set: {}\ndict: {}\ndict_hash: {}\ndict_manual: {}\n".format(
            t_split - t_start,
            t_split2 - t_split,
            t_split3 - t_split2,
            t_end - t_split3,
        )
    )
