import subprocess
import re


has_waf = r"\[\*\] The site .* seems to be behind a WAF or some sort of security solution"


def waf(domain):
    s = subprocess.run(["python", "-m", "wafw00f.main", f"http://{domain}"], shell=True, capture_output=True)
    output = s.stdout.decode()
    r = re.search(has_waf, output)
    return bool(r)


if __name__ == '__main__':
    domain = "www.bilibili.com"
    if waf(domain):
        print(f"{domain} has waf.")
