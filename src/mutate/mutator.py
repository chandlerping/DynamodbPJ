import random
from src import config
from src.utils import *


def mutate_add_checker(lines, write_locs, read_locs):
    locs = write_locs + read_locs
    read_id = random.choice(locs)
    line_new = ' ' * 8 + "counter += executor.submit(checker_db, table, read_op).result()\n"
    lines[read_id + 1:read_id + 1] = line_new
    return lines


def mutate_add_writer(lines, write_locs):
    write_id = random.choice(write_locs)
    lines_new = [lines[write_id - 1], lines[write_id]]
    lines[write_id + 1:write_id + 1] = lines_new
    return lines


def mutate_replace(lines, assign_locs):
    assign_id = random.choice(assign_locs)
    string_len_new = random.randint(config.string_len_new_l, config.string_len_new_h)
    count_space = count_spaces(lines[assign_id])
    line_new = ' ' * count_space + "write_op.expr_attr_val = {{':r': generate_random_string({})}}\n".format(str(string_len_new))
    lines[assign_id] = line_new
    return lines


def mutate_change_threading(lines, threading_locs):
    threading_id = random.choice(threading_locs)
    thread_num_new = random.randint(config.thread_num_new_l, config.thread_num_new_h)
    line_new = ' ' * 4 + "with ThreadPoolExecutor(max_workers={}) as executor:\n".format(str(thread_num_new))
    lines[threading_id] = line_new
    return lines


def mutate_swap(lines, write_locs, read_locs):
    read_id = random.choice(read_locs)
    write_id = random.choice(write_locs)
    lines[read_id], lines[write_id] = lines[write_id], lines[read_id]
    line_prev = lines[write_id - 1]
    if write_id > read_id:
        lines.pop(write_id - 1)
        lines.insert(read_id, line_prev)
    else:
        lines.insert(read_id, line_prev)
        lines.pop(write_id - 1)
    return lines
