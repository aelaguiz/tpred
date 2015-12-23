#!/bin/bash

echo "Uploading"
s3cmd sync spider_data/ s3://tpred/input/

echo "Deleting"
find spider_data -type f -mmin +5 -exec rm {} \;
