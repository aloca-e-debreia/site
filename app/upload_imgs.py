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

    name, _ = os.path.splitext(file)

    public_id = f"{folder_cloud}/{name}"

    result = cloudinary.uploader.upload(
        filepath,
        folder=folder_cloud,
        public_id=public_id,
        use_filename=False,
        unique_filename=False,
        overwrite=True
    )

    print("Updloaded:", result["secure_url"])