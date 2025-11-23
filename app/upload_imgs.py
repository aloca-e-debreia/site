from cloudinary_setup import cloudinary_config
import os, pathlib, cloudinary.uploader

cloudinary_config()

folder = "uploads"
folder_cloud = "ClickAndDrive"

for file in os.listdir(folder):

    filepath = os.path.join(folder, file)

    if not os.path.isfile(filepath):
        continue

    public_id, _ = os.path.splitext(file)
    extension = pathlib.Path(filepath).suffix

    with open(filepath, "rb") as f:
        result = cloudinary.uploader.upload(
            f,
            upload_preset="ClickAndDrive_preset",
            folder=folder_cloud,
            public_id=public_id,
            use_filename=False,
            unique_filename=False,
            overwrite=True,
            resource_type="image",
            format=extension[1:]
        )

    print("Uploaded:", result["secure_url"])