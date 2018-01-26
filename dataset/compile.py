#!/usr/bin/python

import glob
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# Name of dataset file
filename = "dataset.csv"

# News categories
category = ['business', 'entertainment' ,'politics', 'sport', 'tech']

# Is the header written?
hasWritten = False

# Start counting
count = 1

for i in range(len(category)):

    # Open the files
    txt = glob.glob("bbc/{}/*.txt".format(category[i]))
    with open(filename, "a") as outfile:

        if hasWritten == False:
            outfile.write("id,title,content,category\n")
            hasWritten = True

        for f in txt:
            with open(f, "rb") as infile:

                # Get news title
                title = str(next(infile).decode()).rstrip().replace(',', '')

                content = ""

                for line in infile:
                    # Get news content
                    if line != "\n":
                        content = content+line.rstrip().replace(',', '')

                # Compile the dataset
                outfile.write("%s,%s,%s,%s\n" % (str(count), title, content, category[i]))
                count += 1
