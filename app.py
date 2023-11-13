from flask import Flask, request, jsonify
import time
import os

from utils import get_reese_script, patch_webdriver
from generator.queue import Queue


# Stats variables
startTime = time.time()
cookies_generated = 0
    
# Init browsers
exe_path = os.path.abspath('./files/chromedriver.exe')
#patch_webdriver(exe_path)
queue = Queue(exe_path=exe_path, amount_of_workers=1)

app = Flask(__name__)
    
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/stats', methods=['GET'])
def stats():
    global cookies_generated 

    data = {
        "uptime": time.time() - startTime,
        "cookies_generated": cookies_generated
    }
    return jsonify(data), 200

@app.route('/gen', methods=['POST'])
def gen():
    global cookies_generated 
    global queue 
    
    data = request.json
    reese_script_url = data.get('reese')

    if not reese_script_url:
        return jsonify({"error": "Missing reese script url."}), 400

    try:
        data = get_reese_script(reese_script_url)
        cookie_data = queue.get_cookie(data['aih'], data['script'])
        cookies_generated += 1
        
        return jsonify({"success": True, "data": cookie_data}), 200
    except Exception as ex:
        return jsonify({"success": False, "message": "Error: %s" % str(ex)}), 200

if __name__ == '__main__':
    app.run(debug=True)