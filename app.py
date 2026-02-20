#!/usr/bin/env python3
from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
import threading
import json
import os
import sys
import time
from datetime import datetime
import queue
from V7ACC import *

app = Flask(__name__)
CORS(app)

# Global state management
class GeneratorState:
    def __init__(self):
        self.is_running = False
        self.thread = None
        self.log_queue = queue.Queue()
        self.stats = {
            'generated': 0,
            'target': 0,
            'rare': 0,
            'couples': 0,
            'activated': 0,
            'failed': 0,
            'speed': 0
        }
        self.start_time = None
        self.config = {}

state = GeneratorState()

# Override print function to capture logs
class LogCapture:
    def __init__(self, queue):
        self.queue = queue
        self.original_stdout = sys.stdout
        
    def write(self, text):
        if text.strip():
            self.queue.put({
                'message': text.strip(),
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'type': self.get_log_type(text)
            })
        self.original_stdout.write(text)
    
    def flush(self):
        self.original_stdout.flush()
    
    def get_log_type(self, text):
        if '✅' in text or 'success' in text.lower():
            return 'success'
        elif '❌' in text or 'error' in text.lower():
            return 'error'
        elif '⚠️' in text or 'warning' in text.lower():
            return 'warning'
        elif '💎' in text or 'rare' in text.lower():
            return 'rare'
        elif '💑' in text or 'couple' in text.lower():
            return 'couple'
        elif '🔥' in text or 'activate' in text.lower():
            return 'activation'
        else:
            return 'info'

# Redirect stdout to capture logs
log_capture = LogCapture(state.log_queue)
sys.stdout = log_capture

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start_generation():
    if state.is_running:
        return jsonify({'status': 'error', 'message': 'Already running'})
    
    config = request.json
    state.config = config
    state.is_running = True
    state.start_time = time.time()
    
    # Reset counters
    global SUCCESS_COUNTER, TARGET_ACCOUNTS, RARE_COUNTER, COUPLES_COUNTER
    global ACTIVATED_COUNTER, FAILED_ACTIVATION_COUNTER
    
    SUCCESS_COUNTER = 0
    TARGET_ACCOUNTS = int(config.get('account_count', 100))
    RARE_COUNTER = 0
    COUPLES_COUNTER = 0
    ACTIVATED_COUNTER = 0
    FAILED_ACTIVATION_COUNTER = 0
    
    # Start generation in background thread
    state.thread = threading.Thread(target=run_generator, args=(config,))
    state.thread.daemon = True
    state.thread.start()
    
    return jsonify({'status': 'success', 'message': 'Generator started'})

@app.route('/api/stop', methods=['POST'])
def stop_generation():
    global EXIT_FLAG
    EXIT_FLAG = True
    state.is_running = False
    return jsonify({'status': 'success', 'message': 'Generator stopped'})

@app.route('/api/stats')
def get_stats():
    elapsed = time.time() - state.start_time if state.start_time else 1
    speed = SUCCESS_COUNTER / elapsed if elapsed > 0 else 0
    
    state.stats = {
        'generated': SUCCESS_COUNTER,
        'target': TARGET_ACCOUNTS,
        'rare': RARE_COUNTER,
        'couples': COUPLES_COUNTER,
        'activated': ACTIVATED_COUNTER,
        'failed': FAILED_ACTIVATION_COUNTER,
        'speed': round(speed, 2),
        'is_running': state.is_running,
        'elapsed': round(elapsed, 2)
    }
    return jsonify(state.stats)

@app.route('/api/logs')
def get_logs():
    logs = []
    while not state.log_queue.empty():
        logs.append(state.log_queue.get())
    return jsonify(logs)

@app.route('/api/accounts/<category>')
def get_accounts(category):
    """Get accounts by category (all, rare, couples, activated)"""
    accounts = []
    folder_map = {
        'all': ACCOUNTS_FOLDER,
        'rare': RARE_ACCOUNTS_FOLDER,
        'couples': COUPLES_ACCOUNTS_FOLDER,
        'activated': ACTIVATED_FOLDER,
        'failed': FAILED_ACTIVATION_FOLDER
    }
    
    folder = folder_map.get(category)
    if folder and os.path.exists(folder):
        for filename in os.listdir(folder):
            if filename.endswith('.json'):
                filepath = os.path.join(folder, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            accounts.extend(data[:50])  # Limit to 50 per file
                except:
                    pass
    
    return jsonify(accounts[:100])  # Return max 100 accounts

@app.route('/api/download/<category>')
def download_accounts(category):
    """Download accounts as JSON file"""
    folder_map = {
        'all': ACCOUNTS_FOLDER,
        'rare': RARE_ACCOUNTS_FOLDER,
        'couples': COUPLES_ACCOUNTS_FOLDER,
        'activated': ACTIVATED_FOLDER
    }
    
    folder = folder_map.get(category)
    if folder and os.path.exists(folder):
        all_accounts = []
        for filename in os.listdir(folder):
            if filename.endswith('.json'):
                filepath = os.path.join(folder, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            all_accounts.extend(data)
                except:
                    pass
        
        # Create temp file for download
        temp_file = f'temp_{category}.json'
        with open(temp_file, 'w') as f:
            json.dump(all_accounts, f, indent=2)
        
        return send_file(temp_file, as_attachment=True, download_name=f'knx_{category}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    
    return jsonify({'error': 'Category not found'}), 404

def run_generator(config):
    """Run the generator with given config"""
    try:
        region = config.get('region', 'IND')
        is_ghost = (region == 'GHOST')
        if is_ghost:
            region = 'BR'
        
        account_name = config.get('name_prefix', 'KNX')
        password_prefix = config.get('password_prefix', 'KNX')
        account_count = int(config.get('account_count', 100))
        thread_count = int(config.get('thread_count', 5))
        
        global AUTO_ACTIVATION_ENABLED, RARITY_SCORE_THRESHOLD
        AUTO_ACTIVATION_ENABLED = config.get('auto_activation', True)
        RARITY_SCORE_THRESHOLD = int(config.get('rarity_threshold', 4))
        
        # Override TARGET_ACCOUNTS
        global TARGET_ACCOUNTS
        TARGET_ACCOUNTS = account_count
        
        print(f"🚀 Starting generation with {thread_count} threads...")
        print(f"📍 Region: {region} {'(GHOST MODE)' if is_ghost else ''}")
        print(f"🎯 Target: {account_count} accounts")
        print(f"⚡ Auto-activation: {'ON' if AUTO_ACTIVATION_ENABLED else 'OFF'}")
        
        # Create and start threads
        threads = []
        for i in range(thread_count):
            t = threading.Thread(target=worker, args=(region, account_name, password_prefix, account_count, i+1, is_ghost))
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Monitor threads
        while state.is_running and any(t.is_alive() for t in threads):
            if SUCCESS_COUNTER >= account_count:
                break
            time.sleep(1)
        
        state.is_running = False
        print("✅ Generation completed!")
        
    except Exception as e:
        print(f"❌ Error in generator: {e}")
        state.is_running = False

def worker(region, account_name, password_prefix, total_accounts, thread_id, is_ghost):
    """Worker thread function - uses your existing V7ACC.worker function"""
    # This calls your existing worker function from V7ACC.py
    # Make sure your V7ACC.py has the worker function defined
    try:
        # Import the worker from your V7ACC module
        from V7ACC import worker as v7_worker
        v7_worker(region, account_name, password_prefix, total_accounts, thread_id, is_ghost)
    except Exception as e:
        print(f"Thread {thread_id} error: {e}")

if __name__ == '__main__':
    # Ensure all folders exist
    setup_all_folders()
    
    # Create templates folder if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("="*50)
    print("KNX Generator Web Interface")
    print("="*50)
    print("Server starting...")
    print("Local: http://localhost:5000")
    print("Network: http://YOUR_IP:5000")
    print("="*50)
    
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
