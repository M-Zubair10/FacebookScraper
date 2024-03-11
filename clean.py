def remove_duplicates(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        lines = [x[:x.find('?')] for x in lines]

    # Remove duplicates
    unique_lines = list(set(lines))
    print(len(lines), len(unique_lines))

    with open('cleaned-' + file_path, 'w') as file:
        file.writelines([x + '\n' for x in unique_lines])


# Example usage:
file_path = 'merge.txt'  # Change this to your file path
remove_duplicates(file_path)
