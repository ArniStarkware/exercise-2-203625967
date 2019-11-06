from cli import CommandLineInterface


cli = CommandLineInterface()


@cli.command
def inc(x):
    print(int(x) + 1)


@cli.command
def add(x, y):
    print(int(x) + int(y))


if __name__ == '__main__':
    cli.main()
