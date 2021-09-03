import json
import logging
import os
import psutil
import subprocess
from datetime import datetime
import docker
import time

console_logger = logging.getLogger('console')

'''
runs deepspeech test container against a given audio file
returns deepspeech's transcript
'''
def call_deepspeech(audio_path):
    test_data_logger = logging.getLogger('test_data_logger')

    client = docker.from_env()  # create docker client

    # run docker container
    start = datetime.now()
    container = client.containers.run('harbor.ops.veritone.com/challenges/deepspeech', f'--audio {audio_path}', '--cpus=1',
                                      detach=True)

    cpu_loads = wait_for_docker_process_end(container)
    end = datetime.now()

    elapsed = f'{(end-start).total_seconds():.3f}'
    test_data_logger.info(f'Time elapsed:{elapsed}')
    console_logger.debug(f'Transcription completed in {elapsed}')

    cpu_usage = sum(x for x in cpu_loads) / len(cpu_loads)
    console_logger.debug(f'Process completed successfully with avg CPU utilization of {cpu_usage}')
    test_data_logger.info(f'CPU Usage:{cpu_usage}')

    output = str(container.logs()).split('\\n')[-2]
    console_logger.debug(f'Output from Process:')
    console_logger.debug(f'\t{output}')
    console_logger.debug(f'Full output:')
    console_logger.debug(f'\t{container.logs()}')
    return output

'''
Checks docker stats for CPU usage and container state
Returns list of observed CPU utilization (may be over 100, does not account for # cores active)
'''
def wait_for_docker_process_end(container):
    cpu_load_list = []
    container.reload()  # container attrs are cached, so we need to reload
    # profile while container is running
    while container.attrs['State']['Running']:
        stdout, stderr = subprocess.Popen(['docker', 'stats', '--no-stream', '--format', '{{.CPUPerc}}'], stdout=subprocess.PIPE).communicate()
        console_logger.debug(f'Current CPUPerc: {stdout}')
        if stdout:
            usage = float(stdout[:-2])
            cpu_load_list.append(usage)
        container.reload()  # container attrs are cached, so we need to reload

    return cpu_load_list