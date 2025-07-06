from flask import Flask, request, jsonify
import threading
import UI  
from flask_cors import CORS
import logging
from flask import redirect
import time


app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# Create a global reference that can be accessed across functions
gui_instance = None

def launch_gui():
    global gui_instance
    logging.info("Launching GUI...")
    gui_instance = UI.CustomGUI()  # Assign to the global instance
    gui_instance.run()
    logging.info("GUI launched.")

@app.route('/')
def home():
    return redirect('/start-gui')



@app.route('/start-gui')
def start_gui():
    if not gui_instance:
        threading.Thread(target=launch_gui).start()
        return "GUI is starting..."
    else:
        return "GUI already running."

@app.route('/trigger-sendToApi')
def trigger_sendToApi():
    if gui_instance:
        # Get model choice from query parameter, default to GPT (2)
        model_choice = request.args.get('model', default=2, type=int)
        gui_instance.sendToApi(model_choice)
        return "sendToApi triggered"
    else:
        return "Something went wrong trigger-sendtoapi"


@app.route('/trigger-sendToApi-android-post', methods=['POST'])
def trigger_sendToApi_android_post():
    logging.info(f"Android POST raw data: {request.get_data(as_text=True)}")
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
        
    if gui_instance:
        try:
            # Get model choice from request data, default to GPT (2)
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON data"}), 400
                
            model_choice = data.get('model', 2)
            
            # Add log for Android request
            gui_instance.add_log(f"Received request from Android - Model: {model_choice}")
            
            # Get the response directly without async
            answer = gui_instance.sendToApi(model_choice)
            
            # If the answer is "Processing request...", start a background task
            if answer == "Processing request...":
                def background_task():
                    start_time = time.time()
                    while time.time() - start_time < 60:  # 60 seconds timeout
                        if gui_instance.last_response and gui_instance.last_response != "Processing request...":
                            return gui_instance.last_response
                        time.sleep(1)  # Check every second
                    return "Request timeout after 60 seconds"
                
                # Start the background task
                thread = threading.Thread(target=background_task)
                thread.start()
                thread.join(timeout=60)  # Wait up to 60 seconds
                
                if thread.is_alive():
                    gui_instance.add_log("Android request timed out after 60 seconds")
                    return jsonify({"error": "Request timeout after 60 seconds"}), 408
                
                final_response = gui_instance.last_response
                if final_response == "Processing request...":
                    gui_instance.add_log("No response received for Android request")
                    return jsonify({"error": "No response received"}), 408
                    
                gui_instance.add_log("Successfully processed Android request")
                return jsonify({"result": final_response})
            
            return jsonify({"result": str(answer)})
        except Exception as e:
            gui_instance.add_log(f"Error processing Android request: {str(e)}")
            return jsonify({"error": str(e)}), 400
    else:
        return jsonify({"error": "Something went wrong android-post"}), 500


@app.route('/take-shot1')
def takeShot1():
    if gui_instance:
        gui_instance.sendScreenShotData1()
        return "screenshot1 taken as shot1.png"
    
    else:
        return "Something went wrong take-shot1"
    


@app.route('/take-shot2')
def takeShot2():
    if gui_instance:
        gui_instance.sendScreenShotData2()
        return "screenshot2 taken as shot2.png"
    
    else:
        return "Something went wrong take-shot2"
    



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)







