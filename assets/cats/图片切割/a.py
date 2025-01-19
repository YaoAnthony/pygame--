from PIL import Image
import os

def split_and_save_image(image_path, output_dir, rows, cols, naming_pattern=None, flip_horizontal=False, direction=None):
    """
    Function to split an image into smaller frames and save them.

    :param image_path: Path to the input image.
    :param output_dir: Directory to save the split images.
    :param rows: Number of rows to split the image into.
    :param cols: Number of columns to split the image into.
    :param naming_pattern: Naming pattern for output files.
    :param flip_horizontal: If True, creates a horizontally flipped version of the frames.
    :param direction: Direction label for animations (down, left, right, up).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    img = Image.open(image_path)
    width, height = img.size
    frame_width = width // cols
    frame_height = height // rows

    for row in range(rows):
        for col in range(cols):
            left = col * frame_width
            upper = row * frame_height
            right = left + frame_width
            lower = upper + frame_height
            cropped_img = img.crop((left, upper, right, lower))

            # Naming according to the given naming pattern
            if naming_pattern:
                frame_name = naming_pattern.format(index=col + 1, direction=direction if direction else "")
            else:
                frame_name = f"frame_{row}_{col}.png"

            cropped_img.save(os.path.join(output_dir, frame_name))

            # If flip_horizontal is True, create the flipped right idle frames
            if flip_horizontal:
                flipped_output_dir = output_dir.replace("left", "right")
                if not os.path.exists(flipped_output_dir):
                    os.makedirs(flipped_output_dir)

                flipped_img = cropped_img.transpose(Image.FLIP_LEFT_RIGHT)
                flipped_frame_name = frame_name.replace("left", "right")
                flipped_img.save(os.path.join(flipped_output_dir, flipped_frame_name))

def batch_process_images():
    """
    Batch processes multiple images for different animations.
    """
    image_configs = [
        {
            "image_path": "walk.png",
            "output_dir": "output/walk",
            "rows": 4,
            "cols": 4,
            "naming_pattern": "walk_{direction}_{index}.png",
            "direction": "down"
        },
        {
            "image_path": "down.png",
            "output_dir": "output/idle/down",
            "rows": 1,
            "cols": 4,
            "naming_pattern": "idle_down_{index}.png",
            "direction": "down"
        },
        {
            "image_path": "White_Dig.png",
            "output_dir": "output/idle/left",
            "rows": 1,
            "cols": 4,
            "naming_pattern": "idle_left_{index}.png",
            "flip_horizontal": True,  # Automatically create right idle frames by flipping left frames
            "direction": "left"
        },
        {
            "image_path": "up.png",
            "output_dir": "output/idle/up",
            "rows": 1,
            "cols": 4,
            "naming_pattern": "idle_up_{index}.png",
            "direction": "up"
        },
        {
            "image_path": "White_Sleep2.png",
            "output_dir": "output/sleep/sleep1",
            "rows": 1,
            "cols": 4,
            "naming_pattern": "sleep1_{index}.png",
            "direction": "sleep"
        },
        {
            "image_path": "White_Sleep3.png",
            "output_dir": "output/sleep/sleep2",
            "rows": 1,
            "cols": 4,
            "naming_pattern": "sleep2_{index}.png",
            "direction": "sleep"
        },
        {
            "image_path": "Glay_Stretch.png",
            "output_dir": "output/stretch",
            "rows": 1,
            "cols": 4,
            "naming_pattern": "stretch_{index}.png",
            "direction": "stretch"
        }
    ]

    for config in image_configs:
        split_and_save_image(
            image_path=config["image_path"],
            output_dir=config["output_dir"],
            rows=config["rows"],
            cols=config["cols"],
            naming_pattern=config.get("naming_pattern"),
            flip_horizontal=config.get("flip_horizontal", False),
            direction=config.get("direction")
        )

if __name__ == "__main__":
    batch_process_images()
