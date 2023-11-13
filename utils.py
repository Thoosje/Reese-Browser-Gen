import requests

import io
import os
import re

def get_reese_script(script_url: str) -> dict[str, str]:
    content = requests.get(script_url).text
    
    intterogatorScript = content.split('\n')[0]
    aih = content.split("aih':'")[1].split("'")[0]
    
    return {
        'script': intterogatorScript,
        'aih': aih,
    }
    
class WebDriverPatchException(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code    

def patch_webdriver(executable_path: str) -> None:
    with io.open(executable_path, "r+b") as fh:
        content = fh.read()
        match_injected_codeblock = re.search(rb"\{window\.cdc.*?;\}", content)
        if match_injected_codeblock:
            target_bytes = match_injected_codeblock[0]
            new_target_bytes = (
                b'{console.log("undetected chromedriver 1337!")}'.ljust(
                    len(target_bytes), b" "
                )
            )
            new_content = content.replace(target_bytes, new_target_bytes)
            if new_content == content:
                raise WebDriverPatchException('Failed to patch webdriver, could not find injected codeblock.', 'ALREADY_PATCHED')
            else:
                print(
                    "found block:\n%s\nreplacing with:\n%s"
                    % (target_bytes, new_target_bytes)
                )
                
            fh.seek(0)
            fh.write(new_content)