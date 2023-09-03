from flask import Flask, jsonify
import subprocess
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

ssh_commands = {
    "/dev": "ssh user1@host_name_1 'rsync -avz --stats /path/to/files/from/where/transferred/* user2@host_name_2:/path/to/files/to/where/transferred/'",
    "/dev1": "ssh user2@host_name_2 'rsync -avz --stats /path/to/files/from/where/transferred/* user2@host_name_2:/path/to/files/to/where/transferred/'",
    "/dev2": "ssh user3@host_name_3 'rsync -avz --stats /path/to/files/from/where/transferred/* user2@host_name_2:/path/to/files/to/where/transferred/'"
}
@app.route('/<path>', methods=['POST'])
def webhook(path):
    logging.info(f'Request received for hook: {path}')
    
    ssh_command = ssh_commands.get('/' + path)
    if not ssh_command:
        return jsonify({"message": "Invalid route"}), 400

    result = subprocess.run(ssh_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    logging.info(result.stdout)

    response_data = {
        "ok": "success"
    }
    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
