import os

exports_folder = os.path.join(os.getcwd(), "tests", "exports")

# Making sure the folder exists
os.makedirs(exports_folder, exist_ok=True)
