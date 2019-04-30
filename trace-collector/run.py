from selenium import webdriver

TEMPLATE_FOLDER = "templates/"
TEMPLATE_FILE = "stream.html.j2"


def generate_video_playback_html(vidoe_id, output_file):
    from jinja2 import Environment, FileSystemLoader

    env = Environment(loader=FileSystemLoader(TEMPLATE_FOLDER))
    template = env.get_template(TEMPLATE_FILE)
    with open(output_file, "w") as fout:
        print(template.render(video_id=vidoe_id), file=fout)


def set_network_condition():
    pass


def playback(file):
    from pathlib import Path
    from time import sleep

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    uri = Path(file).absolute().as_uri()
    driver.get(uri)

    # print(driver.page_source)

    driver.find_element_by_id("player").click()

    while True:
        playback_status = driver.execute_script("return player.getPlayerState()")
        playback_time = driver.execute_script("return player.getCurrentTime()")
        playback_quality = driver.execute_script("return player.getPlaybackQuality()")
        print("playback time:{}, status:{}, rate: {}".format(playback_time, playback_status, playback_quality))
        sleep(1)

    driver.close()


if __name__ == "__main__":
    video_id = "TcMBFSGVi1c"
    playback_file = "stream.html"
    generate_video_playback_html(video_id, playback_file)
    set_network_condition()
    playback(playback_file)
