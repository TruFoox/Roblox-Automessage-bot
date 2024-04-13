def remove_after_colon(line):
    index = line.find(":")
    if index != -1:
        second_index = line.find(":", index + 1)
        if second_index != -1:
            removed = line[second_index:]
            return removed[1:]
    return line

# Read and modify the file
file_path = "cookies.txt"

with open(file_path, "r+") as file:
    lines = file.readlines()  # Read all lines into a list
    file.seek(0)  # Move the file pointer to the beginning

    for line in lines:
        modified_line = remove_after_colon(line.strip())  # Remove trailing newline and apply the function
        file.write(modified_line + "\n")

    file.truncate()  # Remove any remaining content after the modified lines