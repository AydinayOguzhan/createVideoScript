# Video Generation from Text with Voiceover and Subtitles

This project generates a video from a text story with voiceover and subtitles. The script processes the input text, creates a voiceover, generates subtitles, and combines them with a background video to produce the final output.

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Installation

1. **Clone the Repository:**

    ```sh
    git clone https://github.com/AydinayOguzhan/createVideoScript
    cd createVideoScript
    ```

2. **Create a Virtual Environment (Optional but Recommended):**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Required Libraries:**

    Run the provided script to install all the necessary libraries:

    ```sh
    python install_requirements.py
    ```

    Alternatively, you can manually install the requirements using:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Prepare Your Background Videos:**

    Place your background videos in a folder named `background-videos` in the root directory of the project. The script will randomly select a video from this folder to use as the background.

2. **Edit the Story:**

    Modify the `story` variable in the `app.py` script with your desired text story.

3. **Run the Script:**

    Execute the main script to generate the video:

    ```sh
    python app.py
    ```

    This script performs the following steps:
    - Splits the text into smaller chunks.
    - Generates a voiceover for each chunk.
    - Creates subtitles synchronized with the voiceover.
    - Combines the background video, voiceover, and subtitles into the final video.

4. **Output:**

    The final video will be saved as `output_video.mp4` in the root directory of the project.

## Notes

- Ensure that the background videos are in `.mp4` format for compatibility.
- The script uses `pyttsx3` for text-to-speech conversion. Make sure you have the necessary voices installed on your system. On Windows, you may need to install additional voices such as "Microsoft David".
- The `.gitignore` file is configured to ignore video, sound, and subtitle files to keep the repository clean.

## Troubleshooting

- If you encounter any issues with missing voices, ensure that the required voices are installed on your system.
- For any permission errors, ensure that the script has the necessary permissions to read and write files in the project directory.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or improvements.
