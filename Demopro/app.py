from flask import Flask, render_template, request, redirect, url_for, send_file
import pytesseract
from PIL import Image
import os


# For Windows, explicitly set the tesseract executable path
# For Windows, explicitly set the tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize Flask app
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

# Ensure the upload folder exists
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

# OCR function to extract text from the image


def extract_text(image_path):
    # Set to recognize both Hindi and English
    custom_config = r'--oem 3 --psm 6 -l eng+hin'
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, config=custom_config)
    return text

# Home route to upload image and display form

# Ensure this is included at the start of the index function


# uploaded_filename = file.filename if file else None


@app.route("/", methods=["GET", "POST"])
def index():
    extracted_text = ""
    search_result = ""
    uploaded_filename = None

    if request.method == "POST":
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        keyword = request.form.get("keyword", "")

        if file.filename == "":
            return redirect(request.url)

        if file:
            # Save the uploaded image
            file_path = os.path.join(
                app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)

            # Extract text from the image
            extracted_text = extract_text(file_path)

            # Search for the keyword in the extracted text
            if keyword:
                if keyword.lower() in extracted_text.lower():
                    search_result = extracted_text.replace(
                        keyword, f"<mark>{keyword}</mark>")
                else:
                    search_result = "Keyword not found."

    return render_template("index.html", extracted_text=extracted_text, search_result=search_result, uploaded_filename=uploaded_filename)

# Route to download extracted text


@app.route("/download/<filename>")
def download_file(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    return send_file(file_path, as_attachment=True)


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
