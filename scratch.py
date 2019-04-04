from sarge import Command, Capture
from subprocess import PIPE, getstatusoutput
import platform, time

print(platform.system())


status, result = getstatusoutput('bash')

p = Command('powershell',
            stdout=Capture(buffer_size=-1),
            )

p.run(input=PIPE, async_=True)
time.sleep(5)
print(p.stdout.read())
p.stdin.write(b'dir\n')
p.stdin.flush()
print(p.stdout.read().decode())
p.stdin.write(b'cd ..\n')
p.stdin.flush()
print(p.stdout.read().decode())
p.stdin.write(b'dir\n')
p.stdin.flush()
print(p.stdout.read().decode())
print(p.returncode)