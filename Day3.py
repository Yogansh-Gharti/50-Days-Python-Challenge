import os
from rembg import remove

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

images = [
    f for f in os.listdir(INPUT_FOLDER)
    if f.lower().endswith((".png", ".jpg", ".jpeg"))
]

if not images:
    print("No images found.")
    exit()

for image in images:

    input_path = os.path.join(INPUT_FOLDER, image)

    output_path = os.path.join(
        OUTPUT_FOLDER,
        os.path.splitext(image)[0] + ".png"
    )

    with open(input_path, "rb") as inp:
        image_data = inp.read()

    output = remove(image_data)

    with open(output_path, "wb") as out:
        out.write(output)

    print(f"✔ Background Removed: {image}")

print("\n✅ All Images Processed Successfully!")
