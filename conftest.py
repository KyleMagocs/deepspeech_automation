import logging
import os
import pytest
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
console_logger = logging.getLogger('console')

reports_dir = 'reports/'
cur_timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
current_reports_dir = os.path.join(reports_dir, cur_timestamp)
# clear out the old reports
if not os.path.exists(reports_dir):
    os.makedirs(reports_dir)
if not os.path.exists(current_reports_dir):
    os.makedirs(current_reports_dir)

'''
this is an autouse fixture that will automatically
create a logger/file for each individual test
'''
@pytest.fixture
def test_logger(request):
    if 'audio_file_name' not in request.node.funcargs:
        raise Exception(f'Could not create log for test-- test name invalid- {request.node.name}')
    else:
        log_path = os.path.join(current_reports_dir, request.node.funcargs["audio_file_name"] + '.log')
        logger = logging.getLogger('test_data_logger')
        logger.handlers = [] # clear handlers just in case
        logger.addHandler(logging.FileHandler(log_path))
        logger.propagate = False
        yield logger


'''
auto-runs after all tests are done
Imports results from individual test results
Averages, writes to test report
'''
@pytest.fixture(scope='session', autouse=True) # session may be too broad of scope, depending on test expansion
def generate_test_report(request):
    yield  # wait for test session to complete

    report_filename = os.path.join(current_reports_dir, '_test_report.txt')
    report_logger = logging.getLogger('report')
    report_logger.addHandler(logging.FileHandler(report_filename))

    time_data = []
    accuracy_data = []
    cpu_data = []

    if not os.listdir(current_reports_dir):
        console_logger.error(f'Could not find any log files in {current_reports_dir}, not generating session stats')
        return
    for filename in os.listdir(current_reports_dir):
        with open(os.path.join(current_reports_dir, filename), 'r') as f:
            for line in f.readlines():
                if 'Time elapsed' in line:
                    time_data.append(float(line.split(':')[1]))
                elif 'CPU Usage' in line:
                    cpu_data.append(float(line.split(':')[1]))
                elif 'Accuracy' in line:
                    accuracy_data.append(float(line.split(':')[1]))

    report_logger.info(f'Test stats:')
    report_logger.info(f'\t{"Average elapsed time:":<25}{sum(time_data)/len(time_data):>9.3}s')
    report_logger.info(f'\t{"Average CPU usage:":<25}{sum(cpu_data)/len(cpu_data):>9.4}%')
    report_logger.info(f'\t{"Average Accuracy:":<25}{sum(accuracy_data)/len(accuracy_data):>10.2%}')
    console_logger.info(f'Test reports available at {current_reports_dir}')
    console_logger.info(f'   Session report available at {report_filename}')


