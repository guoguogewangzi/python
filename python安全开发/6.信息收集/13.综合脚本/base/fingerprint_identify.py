import subprocess
import json
import re


class FingerprintID:
    def wappalyzer(self, domain):
        s = subprocess.run(["wappalyzer", "http://" + domain], shell=True, capture_output=True)
        output = s.stdout.decode()
        fingerprint = json.loads(output)

        # is_web = not bool(list(fingerprint["urls"].values())[-1].get("error"))
        is_web = not bool(re.search(r"error", output))
        return is_web, fingerprint


if __name__ == '__main__':
    res = wappalyzer("192.168.29.129:22")
    print(res)
