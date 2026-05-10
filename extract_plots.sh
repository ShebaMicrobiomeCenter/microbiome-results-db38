#!/bin/bash
mkdir -p plots
for qzv in *.qzv core-metrics-results/*.qzv; do
    if [ -f "$qzv" ]; then
        plot_name=$(basename "$qzv" .qzv)
        echo "Extracting $qzv to plots/$plot_name..."
        mkdir -p "plots/$plot_name"
        # Extract the data/ directory from the qzv zip file
        # qzv files have a root directory with a UUID, so we need to find it
        uuid_dir=$(unzip -l "$qzv" | head -n 4 | tail -n 1 | awk '{print $4}' | cut -d/ -f1)
        unzip -o "$qzv" "$uuid_dir/data/*" -d "plots/$plot_name"
        # Move files from uuid_dir/data/ to plots/$plot_name/
        cp -r plots/"$plot_name/$uuid_dir/data/"* plots/"$plot_name/"
        rm -rf plots/"$plot_name/$uuid_dir"
    fi
done
