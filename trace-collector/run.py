import datetime
import os
import subprocess
from yaml import dump
from selenium import webdriver

import config


class ExperimentRunner():
    def __init__(self):
        self.manifest = {}

    def run(self):
        self.select_video_id()
        self.generate_playback_file()
        self.set_network_condition()
        self.prepare_results_folder()
        self.start_packet_capture()
        self.playback()
        self.stop_packet_capture()
        self.record_results()

    def select_video_id(self):
        self.manifest["video_id"] = "LzD79LJPNUE"

    def generate_playback_file(self):
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader(config.PLAYBACK_TEMPLATE_FOLDER))
        template = env.get_template(config.PLAYBACK_TEMPLATE_FILE)
        with open(config.PLAYBACK_RENDERED_FILE, "w") as fout:
            print(template.render(video_id=self.manifest["video_id"]), file=fout)

    @staticmethod
    def set_network_condition():
        pass

    @staticmethod
    def prepare_results_folder():
        import shutil

        if os.path.exists(config.RESULTS_FOLDER):
            shutil.rmtree(config.RESULTS_FOLDER)
        os.mkdir(config.RESULTS_FOLDER)

    def playback(self):
        from pathlib import Path
        from time import sleep

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        uri = Path(config.PLAYBACK_RENDERED_FILE).absolute().as_uri()
        driver.get(uri)

        self.manifest["start_time"] = datetime.datetime.utcnow()
        driver.find_element_by_id("player").click()
        while True:
            playback_status = driver.execute_script("return player.getPlayerState()")
            if playback_status == 0:  # if playback has finished
                break

            if config.DEBUG:
                playback_time = driver.execute_script("return player.getCurrentTime()")
                playback_quality = driver.execute_script("return player.getPlaybackQuality()")
                print("Playback time: {playback_time}, status: {playback_status}, quality: {playback_quality}"
                      .format(playback_time=playback_time,
                              playback_status=playback_status,
                              playback_quality=playback_quality))

            sleep(5)  # if playback has not finished, sleep for 5 seconds and then check again

        self.manifest["end_time"] = datetime.datetime.utcnow()
        driver.close()

    def record_results(self):
        with open(os.path.join(config.RESULTS_FOLDER, config.MANIFEST_FILE), "w") as fout:
            dump(self.manifest, stream=fout)

    @staticmethod
    def start_packet_capture():
        packet_capture_file = os.path.join(config.RESULTS_FOLDER, config.PACKET_CAPTURE_FILE)
        subprocess.Popen(["sudo", "tcpdump", "-U", "-w", packet_capture_file])

    @staticmethod
    def stop_packet_capture():
        subprocess.check_call(["sudo", "pkill", "tcpdump"])


if __name__ == "__main__":
    runner = ExperimentRunner()
    runner.run()