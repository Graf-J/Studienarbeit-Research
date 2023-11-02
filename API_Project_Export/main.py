import os
import shutil
import tempfile
import zipfile
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

async def generate_example_files(output_folder):
    # Create a temporary directory to generate example files
    with tempfile.TemporaryDirectory() as temp_dir:
        example_files = [os.path.join(temp_dir, f"example_file_{i}.txt") for i in range(1, 4)]

        # Generate example files
        for file_path in example_files:
            with open(file_path, "w") as file:
                file.write(f"This is an example file: {file_path}")

        # Copy the example files to the output folder
        for file_path in example_files:
            shutil.copy(file_path, os.path.join(output_folder, os.path.basename(file_path)))

def zip_folder(folder_path):
    shutil.make_archive(folder_path, 'zip', folder_path)

@app.get("/build")
async def build():
    output_folder = "output_folder"
    os.makedirs(output_folder, exist_ok=True)

    # Generate example files and copy them to the output folder
    await generate_example_files(output_folder)

    # Create a ZIP file in the current working directory
    zip_folder(output_folder)

    # Zip the folder if it hasn't been zipped already
    return FileResponse("output_folder.zip", headers={"Content-Disposition": "attachment; filename=output_folder.zip"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)