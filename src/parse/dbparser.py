def load_file(file_dir):
    lines = []
    file1 = open(file_dir, 'r')
    for line in file1:
        lines.append(line)
    return lines


def parse(lines):
    write_locs = []
    read_locs = []
    assign_locs = []
    threading_locs = []
    count_checker = 0
    for i in range(len(lines)):
        line = lines[i]
        if "(update_item_db" in line:
            write_locs.append(i)
        elif "(get_item_db" in line:
            read_locs.append(i)
        elif "expr_attr_val" in line:
            assign_locs.append(i)
        elif "max_workers" in line:
            threading_locs.append(i)
        elif "counter +=" in line:
            count_checker += 1
            read_locs.append(i)
    return write_locs, read_locs, assign_locs, threading_locs, count_checker
