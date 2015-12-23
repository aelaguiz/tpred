#!/bin/bash

echo "Uploading"
s3cmd sync spider_data/ s3://tpred/input/

echo "Deleting"
find spider_data -type f -mtime +5m -exec rm {} \;
