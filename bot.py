import subprocess

class VideoBot:
    def __init__(self):
        self.subtitle_path = ''
        self.input_video_path = 'input_video.mp4'
        self.output_video_path = 'output_video_with_subtitles.mp4'

    def handle_command(self, command):
        if command.startswith('/set_subtitle '):
            # Extract subtitle path from the command
            subtitle_path = command[len('/set_subtitle '):]
            self.subtitle_path = subtitle_path
            return "Subtitle path set. Use /burn_subtitles to start the process."

        elif command == '/burn_subtitles':
            if not self.subtitle_path:
                return "Please set the subtitle path first using /set_subtitle."
            
            # Call the burn_subtitles function
            self.burn_subtitles()

            return "Subtitle burning process initiated. Check the logs for details."

        else:
            return "Invalid command. Use /set_subtitle to set the subtitle path or /burn_subtitles to start the process."

    def burn_subtitles(self):
        print("Starting Handbrake process...")

        command = [
            'HandbrakeCLI',
            '-i', self.input_video_path,
            '-o', self.output_video_path,
            '--subtitle', self.subtitle_path,
            '--subtitle-burn',
            '--preset', 'Very Fast 720p',
        ]

        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                print("Subtitles burned successfully.")
            else:
                print(f"Error: {stderr}")

            with open('handbrake_log.txt', 'w') as log_file:
                log_file.write(stdout)

        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

# Example usage
bot = VideoBot()

# Simulate user interaction with commands
commands = [
    '/set_subtitle subtitles.srt',
    '/burn_subtitles',
]

for command in commands:
    response = bot.handle_command(command)
    print(response)
