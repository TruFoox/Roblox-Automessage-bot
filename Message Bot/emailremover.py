def remove_after_second_colon_in_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file:
        lines = input_file.readlines()

    new_lines = []
    for line in lines:
        first_colon = line.find(':')
        second_colon = line.find(':', first_colon + 1)
        if second_colon != -1:
            new_line = line[:second_colon] + '\n'
        else:
            new_line = line
        new_lines.append(new_line)

    with open(output_file_path, 'w') as output_file:
        output_file.writelines(new_lines)

# Provide the input file path and output file path
input_file_path = 'cookies.txt'  # Replace with your input file path
output_file_path = 'cookies.txt'  # Replace with your desired output file path

remove_after_second_colon_in_file(input_file_path, output_file_path)
