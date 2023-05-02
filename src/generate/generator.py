from src.parse import dbparser
from src import config
from src.utils import *


def generate_seed(file_dir_seed):
    template_dir = "./src/generate/template/foo_temp.py"
    lines = dbparser.load_file(template_dir)
    # locate starting point
    loc = 0
    for i in range(len(lines)):
        if "# operations" in lines[i]:
            loc = i
    loc += 1
    # insert operations
    for i in range(len(config.seed_flow)):
        count_writers = config.seed_flow[i][0]
        count_readers = config.seed_flow[i][1]
        count_threads = config.seed_flow[i][2]
        lines_new = [' ' * 4 + "with ThreadPoolExecutor(max_workers={}) as executor:\n".format(str(count_threads))]
        for j in range(count_writers):
            lines_new.append(' ' * 8 + "write_op.expr_attr_val = {{':r': generate_random_string({})}}\n".format(str(config.string_len)))
            lines_new.append(' ' * 8 + "executor.submit(update_item_db, table, write_op)\n")
        for j in range(count_readers):
            lines_new.append(' ' * 8 + "executor.submit(get_item_db, table, read_op)\n")
        lines_new.append(' ' * 8 + "counter += executor.submit(checker_db, table, read_op).result()\n")
        lines_new.append('\n')
        lines[loc:loc] = lines_new
        loc += len(lines_new)
    # write to seed file
    f = open(file_dir_seed + "/seed.py", "w+")
    f.writelines(lines)
    f.close()
