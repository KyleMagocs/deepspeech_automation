# DEEPSPEECH AUTOMATION

## 1.  Running

For the purposes of this code, runtests.sh has been provided

Usage:
```
source runtests.sh
```
this script will do the following:
1. Create a new virtual environment (if not exists)
    `python3 -m venv virtual_env`
2. Activate that virtual environment
    `source virtual_env/bin/activate`
3. Install all of the required testing dependencies (if new environment)
    `pip install -r requirements.txt` (also sets pypi as a trusted host)
4. Invoke pytest on the test directory
    `pytest Tests` (command line options handled via pytest.ini)
5. Deactivate the virtual environment
    `deactivate`

## 2. Reporting
Example reports can be found at reports/EXAMPLE/
Individual test data shall be stored in `<x>.wav.log`
Aggregate report for test session can be found in `_test_report.txt`

Each test run will generate its own reporting folder, with a timestamp, e.g. `reports/2021-09-02-16-33-20/`

## 3. File descriptions

reports/EXAMPLE
> this is an example of the output from a test run.  There is an individual data log for each test, as well as an aggregate for the test session.  Future runs can be found in reports/<execution time>

lib/compare
> uses jiwer package to check WER in expected/actual output, logs accuracy to log file

lib/deepspeech
> invokes deepspeech docker image, logs runtime, profiles CPU Usage

TestData/expected_transcripts
> contains a dictionary of wav files and corresponding expected transcription

Tests/test_deepspeech_transcription
> relatively barebones pytest test

conftest
> pytest conftest file.  Contains definitions for test fixtures, test setup, etc

pytest.ini
> pytest config file.  Contains several flags necessary for desired run state

requirements.txt
> pip requirements file.  can be installed with `pip -r requirements.txt`

runtests.sh
> bash script to execute tests.  see 1. Running for more details

## 4.  Notes
Several notes for this project--

- input .wav file size is not tracked or logged.
    >Research suggests the only way to get this information is to export the image, unzip the tarball, and then search for the file.
    This is a lot of overhead and time spent for a minor bit of log data.
    Ideally this project would be running against source rather than a pre-compiled docker image, where input files would be freely accessible.

- average CPU usage may be over 100%
    >Tracking the CPU usage of a docker container follows other linux patterns, and does not present itself on a per-core basis.  As such, two cores running at 60% each would result in a CPU usage of 120%

- writing results isn't the cleanest
    >Using python's logging module is a quick and easy way to dump data to different log files as well as to the console at runtime.
    Ideally, this would be replaced with some sort of file stream factory

- documentation is relatively limited
    >only some short docstrings and line comments.  Ideally these would be replaced with google docstrings

- test data is hardcoded in a python dict
    >Ideal state, given access to test .wav files, would be to have .wav and .txt files locally and have a function dynamically pull test data from a directory.  See point about .wave files above.