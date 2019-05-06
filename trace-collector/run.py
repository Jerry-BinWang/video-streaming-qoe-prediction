import datetime
import json
import os
import subprocess
import yaml
import csv
from selenium import webdriver

import config


class ExperimentRunner:
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
        import random
        self.manifest["video_id"] = random.choice(config.VIDEO_ID_LIST)

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
            else:
                elapsed_time = datetime.datetime.utcnow() - self.manifest["start_time"]
                if elapsed_time.total_seconds() >= config.TIMEOUT:
                    driver.execute_script("player.pauseVideo()")
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
        self.playback_record = json.loads(driver.execute_script("return JSON.stringify(changes)"))
        driver.close()

    def record_results(self):
        with open(os.path.join(config.RESULTS_FOLDER, config.MANIFEST_FILE), "w") as fout:
            yaml.dump(self.manifest, stream=fout, default_flow_style=False)

        with open(os.path.join(config.RESULTS_FOLDER, config.PLAYBACK_ROCORD_FILE), "w") as fout:
            writer = csv.writer(fout)
            writer.writerows(self.playback_record)

    @staticmethod
    def start_packet_capture():
        packet_capture_file = os.path.join(config.RESULTS_FOLDER, config.PACKET_CAPTURE_FILE)
        subprocess.Popen(["sudo", "tcpdump", "-U", "-w", packet_capture_file])

    @staticmethod
    def stop_packet_capture():
        subprocess.check_call(["sudo", "pkill", "tcpdump"])


class ResultsUploader:
    @staticmethod
    def zip_and_upload():
        import boto3
        import uuid
        import zipfile

        file_name = "{}.zip".format(uuid.uuid1())
        with zipfile.ZipFile(file_name, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(os.path.join(config.RESULTS_FOLDER, config.MANIFEST_FILE))
            zipf.write(os.path.join(config.RESULTS_FOLDER, config.PACKET_CAPTURE_FILE))
            zipf.write(os.path.join(config.RESULTS_FOLDER, config.PLAYBACK_ROCORD_FILE))

        s3 = boto3.client("s3",
                          aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
                          aws_secret_access_key=os.environ["AWS_SECRET_KEY"])
        s3.upload_file(file_name, config.BUCKET_NAME, file_name)

        os.remove(file_name)


if __name__ == "__main__":
    runner = ExperimentRunner()
    runner.run()
    ResultsUploader().zip_and_upload()
