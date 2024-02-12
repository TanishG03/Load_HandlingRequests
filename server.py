from flask import Flask, jsonify
import time
import random

app = Flask(__name__)

@app.route('/<path:subpath>')
def get_data(subpath):
    # Set a specific response time for get_photos
    if subpath == 'photos':
        time.sleep(2)  # Set a specific response time for get_photos
    if subpath=='albums':
        time.sleep(2.5)
    else:
        time.sleep(random.uniform(0.5, 2.0))

    return jsonify({"server": "Server1", "data": f"Some data from {subpath}"})

if __name__ == '__main__':
    app.run(port=3000)

