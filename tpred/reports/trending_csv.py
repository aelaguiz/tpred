import sys
import csv
import tpred.reports.trending_report as trending_report


if __name__ == '__main__':
    n = int(sys.argv[1])
    out_path = sys.argv[2]

    header, output = trending_report.run_report(n)

    f = open(out_path, "wb")
    w = csv.writer(f)

    w.writerow(header)
    for row in output:
        w.writerow([str(r.encode("utf8")) for r in row])

    f.close()
