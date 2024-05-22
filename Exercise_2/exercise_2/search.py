import re
from collections import Counter

# Step 1: Read the contents of the "output" file
file_path = 'output.txt'  # Assuming the file is in the same directory

try:
    with open(file_path, 'r', encoding='utf-16') as file:
        content = file.read()
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    # Handle the error as needed, e.g., exit the script or provide a default value for 'content'
    content = ""
except Exception as e:
    print(f"Error: Unable to read the file '{file_path}'.")
    print(f"Details: {e}")
    # Handle the error as needed, e.g., exit the script or provide a default value for 'content'
    content = ""

# Check if the file was read successfully
if content:
    # Step 2: Extract lines that contain the error pattern
    error_pattern = re.compile(r'line (\d+), in interpret')
    matches = error_pattern.findall(content)
    # Step 3: Count the occurrences of each unique error line
    error_lines = Counter(matches)
    print(error_lines)
    # Step 4: Find the top 5 most repeated error lines
    top_errors = error_lines.most_common(5)

    # Step 5: Print or store the results
    print("Top 5 most repeated error lines:")
    for error, count in top_errors:
        print(f"Error Line {error}, {count} occurrences")
else:
    print("File read unsuccessful. Check for errors in the file path or content.")
