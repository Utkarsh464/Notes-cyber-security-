import socket

print("simple port scanner")
print("-------------------")

target = input("enter target ip or hostname: ")
start_port = int(input("start port: "))
end_port = int(input("end port: "))

print(f"\nscanning {target} from port {start_port} to {end_port}...\n")

open_ports = []

for port in range(start_port, end_port + 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    result = s.connect_ex((target, port))
    if result == 0:
        print(f"port {port} is open")
        open_ports.append(port)
    s.close()

if open_ports:
    print(f"\nopen ports: {open_ports}")
else:
    print("\nno open ports found")
