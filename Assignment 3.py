#!/usr/bin/env python
# -*- coding: utf-8 -*-
"Assignment 3"

import re
import sys
import csv
import urllib2
import argparse
from datetime import datetime
from operator import itemgetter


def process_time_stats(rows):
    hour_dict = {
        0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0,
        10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0,
        19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0
    }
    for row in rows:
        full_time = row[1]
        parsed_time = datetime.strptime(full_time, "%Y-%m-%d %H:%M:%S")
        hour_dict[parsed_time.hour] += 1
    for hour, hits in sorted(hour_dict.items(),
                             key=itemgetter(1),
                             reverse=True):
        print "Hour %.2d has %d hits" % (hour, hits)


def process_browser_stats(rows):
    msie = 0.0
    firefox = 0.0
    chrome = 0.0
    safari = 0.0

    for row in rows:
        user_agent = row[2].lower()

        if re.match(r'.*msie.*', user_agent):
            msie += 1
        elif re.match(r'.*firefox.*', user_agent):
            firefox += 1
        elif re.match(r'.*chrome.*', user_agent):
            chrome += 1
        elif re.match(r'.*safari.*', user_agent):
            safari += 1

    most_hits = max(msie, firefox, chrome, safari)

    if most_hits == msie:
        most_popular = "Microsoft Internet Explorer"
    elif most_hits == firefox:
        most_popular = "Mozilla Firefox"
    elif most_hits == chrome:
        most_popular = "Google Chrome"
    elif most_hits == safari:
        most_popular = "Safari"

    print "The most popular browser was %s" % most_popular


def process_image_stats(rows):
    image_hits = 0.0
    total_hits = 0.0

    for row in rows:
        path = row[0].lower()
        if len(re.findall(r'jpg|png|gif', path)) > 0:
            image_hits += 1
        total_hits += 1

    image_hits_percent = image_hits / total_hits * 100

    print "Image requests account for %.1f%% of all requests" % image_hits_percent


def read_csv_file():
    rows = []
    with open("temp.csv", "rb") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    return rows


def download_csv_file(url):
    print "Downloading CSV file from %s" % url

    try:
        response = urllib2.urlopen(url)
        data = response.read()

        csv_file = open("temp.csv", "w")
        csv_file.write(data)
        csv_file.close()
    except:
        print "Error while reading from that URL"
        sys.exit()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url", help="the URL from which the CSV file is downloaded")
    args = parser.parse_args()

    if args.url is None:
        print "No URL provided. Using default value."
        args.url = "http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv"

    download_csv_file(args.url)
    rows = read_csv_file()
    process_image_stats(rows)
    process_browser_stats(rows)
    # extra credits
    process_time_stats(rows)

main()
