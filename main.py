import platform
import random
import sys
import threading
import time
import requests
import tarfile
import pgpy
import logging
import warnings
import os
import subprocess
import shutil
import socket
import msvcrt
import socks

logging.basicConfig(level=logging.ERROR)
warnings.simplefilter("ignore")

OUTPUT_COLORS = [
    "",
    " [\033[0;34mr \033[0m] ",
    " [\033[0;35mR \033[0m] ",
    " [\033[0;31mt \033[0m] ",
    " [\033[0;33mTi\033[0m] ",
    " [\033[0;32mT \033[0m] "
]


def p(c, *args, **kwargs):
    kwargs["flush"] = True

    print(OUTPUT_COLORS[c], end="", flush=True)
    print(*args, **kwargs)
    time.sleep(0.2)


def i(c, *args, **kwargs):
    kwargs["flush"] = True
    kwargs["end"] = ""

    print(OUTPUT_COLORS[c], end="", flush=True)
    print(*args, **kwargs)
    inp = input()
    time.sleep(0.2)
    return inp


def reinstall_tor():
    p(1, "Reinstalling Tor")

    TorKey = """
-----BEGIN PGP PUBLIC KEY BLOCK-----
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
IXALDCLwHP4mQfdN4NmceXquFF4wNUFEWkcjAsGMId54G+ifqyADG6u9CVnMEg9p
8OScJk4LQeFs5yyK7JisH8v/Vgo7OFjz4LkCDQRUjrBWARAAwe/WL4gxY2OpsIxQ
9LsNdObgkbDUXzyB/dgdXBIXt1l9R0dLh9vrl9WzgA9p8pmpCtqXSqMMiwjahmC5
53bj8gMX0khhZf4qSzlZsck/eTsaTrzANwYGcYxKhoq85C1z8vf/sAeeHGcW+2wP
xrJ21R8E0gEGI3MBex+k/9Z/60ZXrP7tT4JPvATdQKi3YStv9R3k9VKrwYwdlH4i
jjldsNkQcK2ZaCzeX7PzOHgucV/cc/5S4M2XY8KbECqX5Zc4jc1sHrjQ77hjiwjG
3TwLfDLMq4YfqQiVG9ca9juQL4k1+fygwbWScp47tZ/d0PO5Qr1C8IbE2bbPI5u/
PO336UK+Mmd2k0RQQOV7xujfFqNAF7GboIVgjeW5mMRssowjYVjRaXdHZsSYKTcb
6eVCWZz/7mzuqZhlKj9me+ChQNNQyG9XKmBOTJ0rj7OhC7J3qoUdt4pZo+vp5kiN
07kne3m/7ZZsWMCpdb/z2se/1pVpmJYvsOSyasGC/FYgeuJN3Cm0N81h4U6cgJCQ
IepShZDZaCtYO66hez63Rs6dro0kcpI1mfYbiYdmqLy1S/bYiaRhohVUOaSgZyJ1
s+/XqcO+ehTqbbZ+L0IqiqgVU0rDItHPu31WoIzZnZOqpzk8a/Deh/VyGog5XXwA
P9+TWQe18pyf0v0D1f5te4VSD50AEQEAAYkEWwQYAQoADwIbAgUCVd2iawUJBRFZ
EAJACRBOLG6HkymCkMFdIAQZAQoABgUCVI6wVgAKCRAuGsaO1AgU4JKjEACXrUoJ
M4iskF/tRCc67bl/QWVy4RDQlVhcCfnUAnuIr76f3EjuYqrD6c8QacbTFzggTwtt
YXx09Mf3A388T/jZHV/9HkPG3cxpgpNmq/YiQhxCVvdvHo/IGkpS9UMt4f7hFjsL
7dlW157ys8OQ8cgRSQ0A/FEeMvzE6uni7cYZ4lfLkrS896o0layi/uCg7BKRhz44
a9lYWpQ+d7BFC+rmMEk7nhWgUeLjb+oL22MsVunbRE4clEKYvyT63B4imtmzJsdG
iQPK/+xzCcwYqtROI9r7dOjSHKI5U0s1P/PvXbZipzyhNFxTPL8fORW8DJSW6dhd
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
7OCwu3RB
=omt+
-----END PGP PUBLIC KEY BLOCK-----
    """

    if os.path.exists("tor"):
        p(1, "Clearing old folders")
        shutil.rmtree("tor")
    else:
        p(1, "Old Tor install not found")

    p(1, "Fetching download links")
    data = requests.get("https://www.torproject.org/download/tor/")
    data = data.text.split("\n")
    links = [
        _.strip()
        .split("downloadLink")[1][8:]
        .split("\"")[0]
        for _ in data if "downloadLink" in _
    ]
    p(1, "Attempting to autodetect OS")

    operating_system = platform.system()
    architecture, _ = platform.architecture()
    search_query = ""

    if operating_system == "Windows" and architecture == "64bit":
        search_query = "windows-x86_64"

    if search_query:
        p(1, "Detected", operating_system, architecture)

        links = [_ for _ in links if search_query in _]

    else:
        p(1, "Unable to detect OS")

    p(1, "Please select download:")

    for _ in range(0, len(links), 4):
        p(0, end="     ")
        for __, link in enumerate(links[_:_ + 4]):
            name = link.split('/')[-1].strip('tor-expert-bundle-').strip('.tar.gz').replace("-", " ")
            p(0, f"{str(_ + __):>2s}: {name:30s}", end="")
            time.sleep(0.2)
        p(0)

    download_link = int(i(1, "download << "))

    download_link = links[download_link]
    download_location = download_link.split("/")[-1]

    p(1, "Downloading Tor")
    tor_zip = requests.get(download_link)

    with open(download_location, "wb") as file:
        file.write(tor_zip.content)

    p(1, "Downloading Tor signature")
    signature = requests.get(download_link + ".asc")

    p(1, "Verifying Tor signature")
    signature = pgpy.PGPSignature.from_blob(signature.text.encode())

    with open(download_location, "rb") as file:
        message = pgpy.PGPMessage.new(file.read())

    message |= signature

    key, _ = pgpy.PGPKey.from_blob(TorKey)

    if not key.verify(message):
        p(1, "Unable to verify downloaded file")
        sys.exit(-1)
    p(1, "Tor download verified")
    p(1, "Un-Archiving Tor")
    with tarfile.open(download_location, "r:gz") as archive:
        archive.extractall()

    p(1, "Cleaning Tor archive")
    os.remove(download_location)

    p(1, "Rearranging Data folder")
    shutil.move("data", "tor/")
    os.mkdir("tor/HSD")
    os.mkdir("tor/lib")

    p(1, "Completed reinstall")


def create_tor_bridge(external_port, internal_port, socks_port):
    p(3, "Creating Tor bridge")
    control_port = socks_port + 1

    working_dir = sys.path[0]
    password = random.randbytes(16).hex()

    p(3, "Generating password hash")

    hashed_password = subprocess.getoutput(fr'"{working_dir}\tor\tor.exe" -f "{working_dir}\tor\torrc" --hash-password {password}')
    hashed_password = hashed_password.strip().split("\n")[-1].split("16:")[1]

    p(3, "Creating TorRc file")
    p(3, "Mapping {external_port} -> TOR -> {internal_port}")

    tor_rc = fr"""
SOCKSPort {socks_port}
Log notice file {working_dir}\tor\log.log
DataDirectory {working_dir}\tor\lib
HashedControlPassword 16:{hashed_password}
ControlPort {control_port}
GeoIPFile {working_dir}\tor\data\geoip
GeoIPv6File {working_dir}\tor\data\geoip6
HiddenServiceDir {working_dir}\tor\HSD
HiddenServicePort {external_port} 127.0.0.1:{internal_port}
"""

    with open("tor/torrc", "w") as file:
        file.write(tor_rc)

    if not os.path.exists("tor/log.log"):
        open("tor/log.log", "w").close()

    command = f"\"{working_dir}\\tor\\tor.exe\" -f \"{working_dir}\\tor\\torrc\""

    with open("tor/initial_log.log", "w") as file:
        file.write("")

    with open("tor/log.log", "w") as file:
        file.write("")

    class TorEr(threading.Thread):
        def __init__(self):
            super(TorEr, self).__init__()
            self.daemon = True
            self.process: subprocess.Popen | None = None
            self.start()

        def run(self) -> None:
            out_file = open("tor/initial_log.log", "w")
            self.process = subprocess.Popen(command, stdout=out_file)
            out_file.close()

        def terminate(self):
            self.process.terminate()

    p(3, "Starting Tor thread.")
    process = TorEr()

    p(3, "Waiting for network to establish, this may take up to 2 minutes.")
    waiting_for_bootstrap = True
    timeout = 240  # 2 lookups per second; 60 tries == 30 seconds

    printed = []

    while waiting_for_bootstrap:
        with open("tor/initial_log.log", "r") as file:
            log = file.readlines()

        for item in log:
            if item in printed:
                continue

            p(4, item.strip())
            printed.append(item)

        with open("tor/log.log", "r") as file:
            log = file.readlines()

        for item in log:
            if item in printed:
                continue

            p(5, item.strip())
            printed.append(item)

            if "Bootstrapped 100% (done)" in item:
                waiting_for_bootstrap = False

        time.sleep(0.5)
        timeout -= 1
        if timeout < 0:
            p(3, "Unable to launch tor")
            time.sleep(0.2)
            sys.exit(-1)

    return process


if __name__ == '__main__':
    p(2, "Checking path")

    if not os.path.exists("tor/"):
        reinstall_tor()

    p(2, "Proceeding with tor/")

    socks_port = random.randint(10_001, 12_000)
    port = random.randint(12_001, 14_000)
    bridge = create_tor_bridge(
        external_port=153,
        internal_port=port,
        socks_port=socks_port
    )

    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", socks_port)
    socket.socket = socks.socksocket

    with open("tor/HSD/hostname", "r") as file:
        addr = file.read()

    print("you are", addr)


    class Listener(threading.Thread):
        def __init__(self):
            super(Listener, self).__init__()
            self.daemon = True
            self.start()

        def run(self) -> None:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("127.0.0.1", port))

            sock.listen(5)

            client, _ = sock.accept()

            while True:
                data = client.recv(1024)
                print(">" + data.decode())


    Listener()

    address = input("friend to connect to")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    input("Press enter to attempt to connect to friend")

    sock.connect((address, 153))

    try:
        while True:
            t = input("<")
            sock.send(t.encode())

    except KeyboardInterrupt:
        ...

    bridge.terminate()
    sys.exit(0)
