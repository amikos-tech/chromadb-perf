#!/bin/bash

# Define your configurations
batch_sizes=(10 100 1000 10000)

for size in "${batch_sizes[@]}"
do
    # Set environment variable or modify config file for batch size
    export BATCH_SIZE=$size
    export DIMENSIONS=1536

    # Run Locust with the current configuration, output results to CSV
    locust -f locust_t.py --headless -u 1 -r 1 --run-time 1m --csv=results_${size}
done
