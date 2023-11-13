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
                raise Exception('Failed to patch webdriver, could not find injected codeblock.')
            else:
                print(
                    "found block:\n%s\nreplacing with:\n%s"
                    % (target_bytes, new_target_bytes)
                )
                
            fh.seek(0)
            fh.write(new_content)