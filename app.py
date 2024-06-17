# importing flask App
from flask import Flask, jsonify, request
from flask_cors import CORS
# import OCR script
from scripts import OCR_script

# initial flask object
app = Flask(__name__)
CORS(app)

# extract nationalId API
@app.route('/extract_nationalId', methods=['POST'])
def get_nationalId():
    try:
        # Check if the request contains a file
        if 'file' not in request.files:
            return jsonify({'status':False, 'message': 'image is required'}), 400
        
        # Check if the file is empty
        file = request.files['file']
        if file.filename == '':
            return jsonify({'status':False,'message': 'image is required'}), 400

        # extract nationalId from image
        nationalId = OCR_script.extract_nationalId(file)
        if len(nationalId)>=10:
            return jsonify({'status':True, 'nationalId': nationalId})
        return jsonify({'status':False, 'message':"couldn't extract nationalId"}), 400
    
    except Exception as e:
        return jsonify({'status':False, 'message':str(e)})


# run server
if __name__ == '__main__':
    app.run(debug = True, use_reloader=False)