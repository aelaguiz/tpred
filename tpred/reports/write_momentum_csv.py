import sys
import csv
import cPickle as pickle
import tpred.sites as sites


def main(in_file, out_file):
    f = open(in_file, "rb")
    data = pickle.load(f)
    f.close()

    f = open(out_file, "wb")
    w = csv.writer(f)

    w.writerow(["topic_id", "topic"] + sites.site_names)
 
    for topic_id, topic, momentum in data:
        w.writerow([str(topic_id), topic.encode("utf8")] + [str(i) for i in momentum])

    f.close()


if __name__ == '__main__':
    in_file = sys.argv[1]
    out_file = sys.argv[2]

    main(in_file, out_file)
