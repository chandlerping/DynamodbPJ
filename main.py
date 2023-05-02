from src.fuzzer import Fuzzer


def main():
    fuzzer = Fuzzer()
    fuzzer.set_dirs("./demo")
    fuzzer.run()


if __name__ == "__main__":
    main()
