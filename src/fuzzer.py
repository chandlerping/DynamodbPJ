from src.parse import dbparser
from src.utils import get_ave_result
from src.mutate import mutator
from src.generate import generator
from src.config import fuzz_ops, num_itr
import shutil


class Fuzzer:
    file_dir_fuzz = ""
    file_dir_tmp = ""
    dir_seed = ""
    ir_old = 0
    count_mutations = 0

    # should be run first
    def set_dirs(self, dir_seed):
        self.dir_seed = dir_seed
        self.file_dir_tmp = self.dir_seed + '/mutation_tmp.py'
        self.file_dir_fuzz = self.dir_seed + '/mutation_fuzz.py'

    def generate_seed(self):
        generator.generate_seed(self.dir_seed)
        shutil.copy(self.dir_seed + '/seed.py', self.file_dir_tmp)
        shutil.copy(self.dir_seed + '/seed.py', self.file_dir_fuzz)

        lines_tmp = dbparser.load_file(self.dir_seed + '/seed.py')
        _, _, _, _, count_checker = dbparser.parse(lines_tmp)
        self.ir_old = get_ave_result(self.dir_seed + '/seed.py') / count_checker
        print("initial ", self.ir_old)

    def fuzz(self):
        # parse the file
        sign = 0
        lines_tmp = []
        while sign == 0:
            # print('.')
            self.count_mutations += 1
            # print(self.count_mutations)
            lines_tmp = dbparser.load_file(self.file_dir_fuzz)
            write_locs, read_locs, assign_locs, threading_locs, count_checker = dbparser.parse(lines_tmp)

            # mutate
            for i in range(fuzz_ops[0]):
                lines_tmp = mutator.mutate_replace(lines_tmp, assign_locs)
            for i in range(fuzz_ops[1]):
                lines_tmp = mutator.mutate_change_threading(lines_tmp, threading_locs)
            for i in range(fuzz_ops[2]):
                lines_tmp = mutator.mutate_swap(lines_tmp, write_locs, read_locs)
            for i in range(fuzz_ops[3]):
                write_locs, read_locs, assign_locs, threading_locs, count_checker = dbparser.parse(lines_tmp)
                lines_tmp = mutator.mutate_add_writer(lines_tmp, write_locs)
            for i in range(fuzz_ops[4]):
                write_locs, read_locs, assign_locs, threading_locs, count_checker = dbparser.parse(lines_tmp)
                lines_tmp = mutator.mutate_add_checker(lines_tmp, write_locs, read_locs)

            # check consistency rate
            with open(self.file_dir_tmp, "w+") as file:
                for line in lines_tmp:
                    file.write(line)
            _, _, _, _, count_checker = dbparser.parse(lines_tmp)
            ir = get_ave_result(self.file_dir_tmp) / count_checker

            print(self.count_mutations, ' - ', ir)

            if ir > self.ir_old + 0.001:
                self.ir_old = ir
                sign = 1
        # write back
        print('mutated ', self.ir_old)
        with open(self.file_dir_fuzz, "w+") as file:
            for line in lines_tmp:
                file.write(line)

    def run(self):
        self.generate_seed()
        for i in range(num_itr):
            self.fuzz()
