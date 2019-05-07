sudo apt update
sudo apt install -y python3-pip unzip
pip3 install selenium
pip3 install boto3
pip3 install tcconfig

# Set permission for tcconfig to work properly
sudo setcap cap_net_admin+ep /sbin/tc
sudo setcap cap_net_raw,cap_net_admin+ep /bin/ip
sudo setcap cap_net_raw,cap_net_admin+ep /sbin/xtables-multi

# Download WebDriver for Chrome
wget -q https://chromedriver.storage.googleapis.com/74.0.3729.6/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mkdir -p ~/.local/bin && mv chromedriver ~/.local/bin

# Install Chrome
sudo apt install -y libxss1 libappindicator1 libindicator7
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
