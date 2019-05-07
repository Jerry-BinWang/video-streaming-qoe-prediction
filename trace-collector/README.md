## How to run
1. Install dependencies
    ```shell
    sh bootstrap.sh
    ```
2. Before starting, run `sudo modprobe ifb`.

3. Modify the `NIC` in `config.py`. 

4. `AWS_ACCESS_KEY=<your aws access key> AWS_SECRET_KEY=<your aws secret key> python3 run.py`