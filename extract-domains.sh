#!/bin/bash

# Check for the correct number of arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <input_file> <output_file> <method_number>"
    exit 1
fi

input_file=$1
output_file=$2
method_number=$3

# Check if the input file exists
if [ ! -f "$input_file" ]; then
    echo "Error: Input file does not exist."
    exit 1
fi

# Define the function for Method 1
function method1() {
    # Use grep to extract URLs or domain-like strings from the input file
    grep -oE 'https?://[^/]+|[^/]+\.[^/]+|^www\.[^/]+' "$input_file" | \
    
    # Remove any http or https protocols to simplify domain processing
    sed -E 's|https?://||g' | \
    
    # Remove trailing dots or slashes that might affect domain extraction
    sed 's|[./]$||' | \
    
    # Use awk to extract second-level and top-level domains, convert to lowercase
    awk -F'.' '{if (NF > 1) print tolower($(NF-1)) "." tolower($NF)}' | \
    
    # Sort results and remove duplicates to clean up the output
    sort | uniq > "$output_file"
}

function method2() {
    # Use grep to extract URLs or domain-like strings from the input file
    grep -oE 'https?://[^/]+|[^/]+\.[^/]+|^www\.[^/]+' "$input_file" | \
    
    # Convert all characters to lowercase to ensure uniformity
    tr '[:upper:]' '[:lower:]' | \
    
    # Remove protocols, trailing slashes, and periods
    sed -E 's|https?://||g; s|[/.]$||' | \
    
    # Extract the last two segments of the domain names, ensuring no subdomains are included
    awk -F'.' '{if (NF > 1) print $(NF-1) "." $NF}' | \
    
    # Sort results and remove duplicates to clean up the output
    sort | uniq > "$output_file"
}

# Execute the chosen method
case $method_number in
    1) method1 ;;
    2) method2 ;;
    *) echo "Invalid method number. Please choose 1 or 2."; exit 1 ;;
esac

echo "Domains have been extracted successfully."
