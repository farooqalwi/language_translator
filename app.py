from langdetect import detect
from googletrans import Translator
from flask import Flask, request, jsonify

app = Flask(__name__)

# API endpoint to handle translation requests


@app.route('/translate', methods=['POST'])
def translate_input():
    # parse JSON request body
    try:
        request_body = request.get_json()
        if not request_body or 'text' not in request_body or 'language' not in request_body:
            raise ValueError('Invalid request body.')
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    # get user input
    try:
        user_input = request_body['text']
        if user_input is None or not user_input.strip():
            return jsonify({'error': 'Text field missing from request body.'}), 400
    except KeyError:
        return jsonify({'error': 'Text field missing from request body.'}), 400

    # detect input language
    try:
        input_language = detect(user_input)
    except Exception:
        return jsonify({'error': 'Could not detect input language.'}), 400

    # perform translation
    try:
        target_language = request_body['language']
        translator = Translator()
        translation = translator.translate(
            user_input, src=input_language, dest=target_language)
    except KeyError:
        return jsonify({'error': 'Language field missing from request body.'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid language.'}), 400
    except Exception:
        return jsonify({'error': 'Translation failed.'}), 500

    # return translation result as JSON response
    return jsonify({'translation': translation.text}), 200


# run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
