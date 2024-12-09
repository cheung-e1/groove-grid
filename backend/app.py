# Main python server file

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(
    __name__,
    template_folder = '../frontend/templates',
    static_folder = '../frontend/static'
)

# Logic App URLs for each endpoint
ENDPOINTS = {
    # User endpoints
    "user-CNU": "https://prod-30.northcentralus.logic.azure.com/workflows/ad6809e5e3ef4bc4a57597eb3d83977d/triggers/When_a_HTTP_request_is_received/paths/invoke/rest/v1/users?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=FHnH34FBhwfWfu9dNmHQsIi2NdIU3uJOF_QPU3yrZHA",
    "user-RAU": "https://prod-15.northcentralus.logic.azure.com/workflows/a0bc4f156a074441bcf24ea6cbe04061/triggers/When_a_HTTP_request_is_received/paths/invoke/rest/v1/users?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=Pww_xqr1JkqVz62D3LvNG8eT8GsZZu_DeocwmaZsOoA",
    "user-RIU": "https://prod-08.northcentralus.logic.azure.com/workflows/2b8bf8ae8b054b0e8c727bb20a22c036/triggers/When_a_HTTP_request_is_received/paths/invoke/rest/v1/users/{id}?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=DqLhTSg4XlCmg1Oi37Sf-Kp7A7pg__91xG-VZvAbUQo",
    "user-UIU": "https://prod-15.northcentralus.logic.azure.com/workflows/876809da191f4e468efbffd41e177dd5/triggers/When_a_HTTP_request_is_received/paths/invoke/rest/v1/users/{id}?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=tS8lxt-rQTg4Byg786kCgyPgrdB1W9ClOemAMOB65NI",
    "user-DIU": "https://prod-26.northcentralus.logic.azure.com/workflows/b4d4ffb5eab240c189c55b629e165c26/triggers/When_a_HTTP_request_is_received/paths/invoke/rest/v1/users/{id}?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=oVjNoBXvrJvJ7rPGvxZbfHEKmNb_69DOBsBhH4nACwQ",

    # Album endpoints
    "album-CNA": "https://prod-24.northcentralus.logic.azure.com/workflows/0ad13dade75c48c1a6a06c81f3fcd89d/triggers/When_a_HTTP_request_is_received/paths/invoke/rest/v1/albums?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=WgcynzAZFCf_uEE0NFKlgD5PnUf4PCzETIFvhS3XMp4",
    "album-RAA": "https://prod-15.northcentralus.logic.azure.com/workflows/62df8701da6b49279f815573802b49e1/triggers/When_a_HTTP_request_is_received/paths/invoke/rest/v1/albums?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=NZjz1WMh6xI5pPlr3cAS9eP_ze9vFSXARgz2bDox3ds",
    "album-RIA": "https://prod-27.northcentralus.logic.azure.com/workflows/a258bc043b284f5186ce62925af394a2/triggers/When_a_HTTP_request_is_received/paths/invoke/rest/v1/albums/{id}?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=y2Qa6OZe2eOsKlXcifmCy8NaWR0m3Dbym4qKhYr2CvM",
    "album-UIA": "https://prod-07.northcentralus.logic.azure.com/workflows/a42bfd067a7a4d939b8f8a0182e07c94/triggers/When_a_HTTP_request_is_received/paths/invoke/rest/v1/albums/{id}?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=0rgEOUco4LgDtPWeWuV3Edpv6JrdEeZP_fNj0i5wvhs",
    "album-DIA": "https://prod-22.northcentralus.logic.azure.com/workflows/6399b11c5a86472197dae104fd158e87/triggers/When_a_HTTP_request_is_received/paths/invoke/rest/v1/albums/{id}?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=-35KpKgUihKKZpMghYTKoqyJIM5DjkWSzvTq8Agk6OA",
    "album-RAUA": "https://prod-11.northcentralus.logic.azure.com/workflows/986434b506174035a911de43c971d1b7/triggers/When_a_HTTP_request_is_received/paths/invoke/rest/v1/users/{id}/albums?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=nE3rcHgPAB3odLndMtlOOBTrQuD31WuN-PSDANulhCE",
    "album-upload-image": "https://prod-09.northcentralus.logic.azure.com/workflows/2a46bbf86a464c99b5ea5e73a0c928e3/triggers/When_a_HTTP_request_is_received/paths/invoke/rest/v1/albums/{id}/image?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=POTYafGVd0nOSeMdgvYNP37QHcRX4ngY-0s9iZrEhjs",

    # Track endpoints
    "track-CNT": "https://prod-16.northcentralus.logic.azure.com/workflows/dbe2681ba9814a4fab9fdaaa3d18fd5c/triggers/When_a_HTTP_request_is_received/paths/invoke/rest/v1/albums/{album_id}/tracks?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=cTJGrxjlZrhS414Cd2ovpSGEBxieGgTxHYDgge3e9A0",
    "track-RAT": "https://prod-06.northcentralus.logic.azure.com/workflows/69fe0913d3ec47be86943dfa61e36a9a/triggers/When_a_HTTP_request_is_received/paths/invoke/rest/v1/albums/{album_id}/tracks?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=-bBsUQAia_pl451H9eAgLIA8ql_Sz2P1c5zkfVTUUEE",
    "track-RIT": "https://prod-08.northcentralus.logic.azure.com/workflows/44e6803fa7404de5a13d80fa90692d2e/triggers/When_a_HTTP_request_is_received/paths/invoke/rest/v1/albums/{album_id}/tracks/{track_id}?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=Z0GhH9U6CRvuULK2WNWRSXIraXTj-q0Dam2xRIGpIyU",
    "track-UIT": "https://prod-18.northcentralus.logic.azure.com/workflows/755cdf73a3f5491e82f05add326afc46/triggers/When_a_HTTP_request_is_received/paths/invoke/rest/v1/albums/{album_id}/tracks/{track_id}?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=JWZL2eMAhCGg9X0ITE3RfWU5wGDrKdAqDcOWpGjuaL0",
    "track-DIT": "https://prod-00.northcentralus.logic.azure.com/workflows/c37ce91934b04f2b86279cc0d22e59e6/triggers/When_a_HTTP_request_is_received/paths/invoke/rest/v1/albums/{album_id}/tracks/{track_id}?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=1eZ-VPYRwmHpaGtE8rdeb49eIri36XqZEr76VSMHZZM",
    "track-upload-audio": "https://prod-02.northcentralus.logic.azure.com/workflows/89d0d4830dda46429d25243652f09ba2/triggers/When_a_HTTP_request_is_received/paths/invoke/rest/v1/albums/{album_id}/tracks/{track_id}/audio?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=VdwErP_i6AhszHwlyQSt0uiMfw-OsaejAy7MxpKTKd4"
}


# Set allowed file types for image and audio
ALLOWED_EXTENSIONS = {
    'jpeg',
    'jpg',
    'png',
    'mpeg',
    'mp3',
    'm4a'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Azure Translator settings
TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com/translate"
TRANSLATOR_KEY = "EiVDiiymCG4nNbDjejOiLTWTHbPg1xuh8J9KUupHMzCMimppkqPeJQQJ99ALACmepeSXJ3w3AAAbACOGrwWX"
TRANSLATOR_REGION = "uksouth"

# ***** FRONTEND ROUTES *****

# Index
@app.route('/')
def index():
    return render_template('index.html')

# Users
@app.route('/users')
def users_page():
    try:
        response = requests.get(ENDPOINTS['user-RAU'])
        users = response.json()  # Fetch all users
        return render_template('users.html', users=users)
    except Exception as e:
        return render_template('error.html', message=str(e))
    
# Single User
@app.route('/users/<int:user_id>')
def user_details(user_id):
    try:
        response = requests.get(ENDPOINTS['user-RIU'].replace("{id}", str(user_id)))
        user = response.json()  # Fetch single user
        return render_template('user_details.html', user=user)
    except Exception as e:
        return render_template('error.html', message=str(e))

# Albums
@app.route('/albums')
def albums_page():
    try:
        response = requests.get(ENDPOINTS['album-RAA'])
        albums = response.json()
        return render_template('albums.html', albums=albums)
    except Exception as e:
        return render_template('error.html', message=str(e))
    
# Single Album
@app.route('/albums/<int:album_id>')
def album_details(album_id):
    try:
        response = requests.get(ENDPOINTS['album-RIA'].replace("{id}", str(album_id)))
        album = response.json()  # Fetch album details
        return render_template('album_details.html', album=album)
    except Exception as e:
        return render_template('error.html', message=str(e))
    
# Update Album
@app.route('/albums/<int:album_id>/update', methods=['GET'])
def update_album(album_id):
    try:
        # Fetch the album details using your existing logic
        response = requests.get(ENDPOINTS['album-RIA'].replace("{id}", str(album_id)))
        if response.status_code == 200:
            album = response.json()
            # Render the update_album.html template with album data
            return render_template('update_album.html', album=album)
        else:
            return jsonify({"error": "Album not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ***** BACKEND ROUTES *****

# ***** USER ROUTES *****

# User-CNU
@app.route('/api/users', methods=['POST'])
def create_new_user():
    try:
        # Extract data from the form
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        address = request.form.get('address')

        if not username or not first_name or not last_name or not password:
            return jsonify({"error": "username, first_name, last_name, and password are required fields"}), 400

        # Prepare the data for forwarding to the Logic App
        user_data = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "address": address
        }

        # Forward the request to the Logic App endpoint
        response = requests.post(ENDPOINTS['user-CNU'], json=user_data)

        # Return the response from the Logic App back to the client
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        # Handle exceptions
        return jsonify({"error": str(e)}), 500

# User-RAU
@app.route('/api/users', methods=['GET'])
def retrieve_all_users():
    try:
        response = requests.get(ENDPOINTS['user-RAU'])
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        # Handle exceptions
        return jsonify({"error": str(e)}), 500

# User-RIU
@app.route('/api/users/<int:user_id>', methods=['GET'])
def retrieve_individual_user(user_id):
    try:
        url = ENDPOINTS['user-RIU'].replace("{id}", str(user_id))
        response = requests.get(url)
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        # Handle exceptions
        return jsonify({"error": str(e)}), 500

# User-UIU
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_individual_user(user_id):
    try:
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        address = request.form.get('address')

        if not username or not first_name or not last_name or not password:
            return jsonify({"error": "username, first_name, last_name, and password are required fields"}), 400

        user_data = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "address": address
        }

        url = ENDPOINTS['user-UIU'].replace("{id}", str(user_id))
        response = requests.put(url, json=user_data)

        # Handle possible empty responses
        try:
            return jsonify(response.json()), response.status_code
        except:
            return jsonify({"message": "User updated successfully"}), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# User-DIU
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_individual_user(user_id):
    try:
        url = ENDPOINTS['user-DIU'].replace("{id}", str(user_id))
        response = requests.delete(url)
        
        # Handle possible empty responses
        try:
            return jsonify(response.json()), response.status_code
        except:
            return jsonify({"message": "User deleted successfully"}), response.status_code
        
    except Exception as e:
        # Handle exceptions
        return jsonify({"error": str(e)}), 500


# ***** ALBUM ROUTES *****

# Album-CNA
@app.route('/api/albums', methods=['POST'])
def create_new_album():
    try:
        name = request.form.get('name')
        format_type = request.form.get('format_type')
        release_date = request.form.get('release_date')
        genre = request.form.get('genre')
        artist_name = request.form.get('artist_name')
        description = request.form.get('description')
        user_id = request.form.get('user_id')

        if not name or not format_type or not release_date or not genre or not artist_name or not user_id:
            return jsonify({"error": "name, format_type, release_date, genre, artist_name, and user_id are required fields"}), 400

        album_data = {
            "name": name,
            "format_type": format_type,
            "release_date": release_date,
            "genre": genre,
            "artist_name": artist_name,
            "description": description,
            "user_id": int(user_id)
        }

        response = requests.post(ENDPOINTS['album-CNA'], json=album_data)
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Album-RAA
@app.route('/api/albums', methods=['GET'])
def retrieve_all_albums():
    try:
        response = requests.get(ENDPOINTS['album-RAA'])
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        # Handle exceptions
        return jsonify({"error": str(e)}), 500

# Album-RIA
@app.route('/api/albums/<int:album_id>', methods=['GET'])
def retrieve_individual_album(album_id):
    try:
        url = ENDPOINTS['album-RIA'].replace("{id}", str(album_id))
        response = requests.get(url)
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        # Handle exceptions
        return jsonify({"error": str(e)}), 500

# Album-UIA
@app.route('/api/albums/<int:album_id>', methods=['PUT'])
def update_individual_album(album_id):
    try:
        name = request.form.get('name')
        format_type = request.form.get('format_type')
        release_date = request.form.get('release_date')
        genre = request.form.get('genre')
        artist_name = request.form.get('artist_name')
        description = request.form.get('description')
        user_id = request.form.get('user_id')

        if not name or not format_type or not release_date or not genre or not artist_name or not user_id:
            return jsonify({"error": "name, format_type, release_date, genre, artist_name, and user_id are required fields"}), 400

        album_data = {
            "name": name,
            "format_type": format_type,
            "release_date": release_date,
            "genre": genre,
            "artist_name": artist_name,
            "description": description,
            "user_id": int(user_id)
        }

        url = ENDPOINTS['album-UIA'].replace("{id}", str(album_id))
        response = requests.put(url, json=album_data)
        
        # Handle possible empty responses
        try:
            return jsonify(response.json()), response.status_code
        except:
            return jsonify({"message": "Album updated successfully"}), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Album-DIA
@app.route('/api/albums/<int:album_id>', methods=['DELETE'])
def delete_individual_album(album_id):
    try:
        url = ENDPOINTS['album-DIA'].replace("{id}", str(album_id))
        response = requests.delete(url)
        
        # Handle possible empty responses
        try:
            return jsonify(response.json()), response.status_code
        except:
            return jsonify({"message": "Album deleted successfully"}), response.status_code
    
    except Exception as e:
        # Handle exceptions
        return jsonify({"error": str(e)}), 500

# Album-RAUA
@app.route('/api/users/<int:user_id>/albums', methods=['GET'])
def retrieve_all_user_albums(user_id):
    try:
        url = ENDPOINTS['album-RAUA'].replace("{id}", str(user_id))
        response = requests.get(url)
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Album-upload-image
@app.route('/api/albums/<int:album_id>/image', methods=['POST'])
def upload_album_image(album_id):
    try:
        # Get form data
        user_id = request.form.get('user_id')       # Extract user_id from the form
        username = request.form.get('username')     # Extract username from the form
        file_name = request.form.get('fileName')    # Extract fileName from the form
        file = request.files['file']                # Extract the file itself

        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400

        # Prepare the files and form data for the Logic App
        form_data = {
            'user_id': int(user_id),
            'username': username,
            'fileName': file_name
        }
        files = {
            'file': (file.filename, file.stream, file.mimetype)
        }

        url = ENDPOINTS['album-upload-image'].replace("{id}", str(album_id))
        response = requests.post(url, files=files, data=form_data)
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# ***** TRACK ROUTES *****

# Track-CNT
@app.route('/api/albums/<int:album_id>/tracks', methods=['POST'])
def create_new_track(album_id):
    try:
        track_title = request.form.get('track_title')
        duration = request.form.get('duration')

        if not track_title or not duration:
            return jsonify({"error": "track_title and duration are required fields"}), 400
        
        data = {
            "track_title": track_title,
            "duration": duration
        }

        url = ENDPOINTS['track-CNT'].replace("{album_id}", str(album_id))
        response = requests.post(url, json=data)
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Track-RAT
@app.route('/api/albums/<int:album_id>/tracks', methods=['GET'])
def retrieve_all_tracks(album_id):
    try:
        url = ENDPOINTS['track-RAT'].replace("{album_id}", str(album_id))
        response = requests.get(url)
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        # Handle exceptions
        return jsonify({"error": str(e)}), 500

# Track-RIT
@app.route('/api/albums/<int:album_id>/tracks/<int:track_id>', methods=['GET'])
def retrieve_individual_track(album_id, track_id):
    try:
        url = ENDPOINTS['track-RIT'].replace("{album_id}", str(album_id)).replace("{track_id}", str(track_id))
        response = requests.get(url)
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        # Handle exceptions
        return jsonify({"error": str(e)}), 500

# Track-UIT
@app.route('/api/albums/<int:album_id>/tracks/<int:track_id>', methods=['PUT'])
def update_individual_track(album_id, track_id):
    try:
        track_title = request.form.get('track_title')
        duration = request.form.get('duration')

        if not track_title or not duration:
            return jsonify({"error": "track_title and duration are required fields"}), 400
        
        data = {
            "track_title": track_title,
            "duration": duration
        }

        url = ENDPOINTS['track-UIT'].replace("{album_id}", str(album_id)).replace("{track_id}", str(track_id))
        response = requests.put(url, json=data)

        # Handle possible empty responses
        try:
            return jsonify(response.json()), response.status_code
        except:
            return jsonify({"message": "Track updated successfully"}), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Track-DIT
@app.route('/api/albums/<int:album_id>/tracks/<int:track_id>', methods=['DELETE'])
def delete_individual_track(album_id, track_id):
    try:
        url = ENDPOINTS['track-DIT'].replace("{album_id}", str(album_id)).replace("{track_id}", str(track_id))
        response = requests.delete(url)

        # Handle possible empty responses
        try:
            return jsonify(response.json()), response.status_code
        except:
            return jsonify({"message": "Track deleted successfully"}), response.status_code
    
    except Exception as e:
        # Handle exceptions
        return jsonify({"error": str(e)}), 500

# Track-upload-audio
@app.route('/api/albums/<int:album_id>/tracks/<int:track_id>/audio', methods=['POST'])
def upload_track_audio(album_id, track_id):
    try:
        user_id = request.form.get('user_id')       # Extract user_id from the form
        username = request.form.get('username')     # Extract username from the form
        file_name = request.form.get('fileName')    # Extract fileName from the form
        file = request.files['file']                # Extract the file itself
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400

        form_data = {
            'user_id': int(user_id),
            'username': username,
            'fileName': file_name
        }
        files = {
            'file': (file.filename, file.stream, file.mimetype)
        }

        url = ENDPOINTS['track-upload-audio'].replace("{album_id}", str(album_id)).replace("{track_id}", str(track_id))
        response = requests.post(url, files=files, data=form_data)
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# ***** Translate Text Route *****
@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        # Extract text and target language from the request body
        data = request.get_json()
        text = data.get("text")
        target_language = data.get("to", "en")  # Default to English if not provided

        # Ensure text is provided
        if not text:
            return jsonify({"error": "Text is required"}), 400

        # Set headers and body for the translation API
        headers = {
            "Ocp-Apim-Subscription-Key": TRANSLATOR_KEY,
            "Ocp-Apim-Subscription-Region": TRANSLATOR_REGION,
            "Content-Type": "application/json"
        }
        body = [{"text": text}]
        params = {"api-version": "3.0", "to": target_language}

        # Make a POST request to the Azure Translator API
        response = requests.post(TRANSLATOR_ENDPOINT, headers=headers, params=params, json=body)

        # Check response status and parse the result
        if response.status_code == 200:
            translation = response.json()[0]["translations"][0]["text"]
            return jsonify({"translated_text": translation}), 200
        else:
            return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)