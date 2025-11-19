from cloudinary_setup import cloudinary_config
import os
import cloudinary.uploader

cloudinary_config()

folder = "uploads"
folder_cloud = "ClickAndDrive"

for file in os.listdir(folder):

    filepath = os.path.join(folder, file)

    if not os.path.isfile(filepath):
        continue

    nome, _ = os.path.splitext(file)

    public_id = f"{folder_cloud}/{nome}"

    result = cloudinary.uploader.upload(
        filepath,
        public_id=public_id,
        use_filename=True,
        unique_filename=False
    )

    print("Updloaded:", result["secure_url"])