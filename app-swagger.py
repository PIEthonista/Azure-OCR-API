from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, render_template
from flask_restx import Api, Resource, fields
from analyze import read_image


app = Flask(__name__, template_folder='templates')
api = Api(
    app, 
    version="1.0", 
    title="Azure OCR API", 
    description="API for analyzing images using Azure OCR"
)

@app.route("/")
def home():
    return render_template('index.html')



namespace = api.namespace('api/v1', description='Image Analysis Operations')

# JSON & Swagger UI input model
image_input = namespace.model('ImageInput', {
    'uri': fields.String(required=True, description='URI of the image to analyze')
})

@namespace.route("/analysis")
class ImageAnalysis(Resource):
    @namespace.expect(image_input)  # expects JSON input based on model defined above
    @namespace.doc(description="Analyze an image URI using Azure OCR")
    def post(self):
        # Try to get the URI from the JSON
        try:
            get_json = request.get_json()
            image_uri = get_json['uri']
        except:
            return jsonify({'error': 'Missing URI in JSON'}), 400
        
        # Try to get the text from the image
        try:
            res = read_image(image_uri)
            
            response_data = {
                "text": res
            }
        
            return response_data, 200
        except:
            return jsonify({'error': 'Error in processing'}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
