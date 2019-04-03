from subprocess import PIPE, Popen

# file = open("output.txt", "w+")
process = Popen('cmd',
                # shell=True,
                universal_newlines=True,
                stdin=PIPE,
                stdout=PIPE,
                stderr=PIPE
                )
while True:
    stdout = process.stdout.readline()
    print(repr(stdout))


def run(cmd):
    message = (cmd + '\n')
    print(message)
    process.stdin.write(message)
    process.stdin.flush()

    process.stdout.readable()

    # print(repr(stderr))


run('dir')
run('cd ..')
run('dir')

print("done")
# file.close()
