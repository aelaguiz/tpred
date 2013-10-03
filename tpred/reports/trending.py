import sys
import tpred.util.gs as gs
import tpred.reports.trending_report as trending_report


if __name__ == '__main__':
    n = int(sys.argv[1])
    sskey = sys.argv[2]

    print "Running report"
    header, output = trending_report.run_report(n)

    print "Uploading to google"
    gs.write_rows(sskey, header, output)
