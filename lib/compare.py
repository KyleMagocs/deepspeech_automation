import logging
from jiwer import wer

console_logger = logging.getLogger('console')

def get_accuracy_of_transcription(expected, actual):
    console_logger.debug(f'expected: {expected}')
    console_logger.debug(f'actual: {actual}')

    accuracy = f'{1 - wer(actual, expected):.2f}'

    console_logger.debug(f'Accuracy of transcription:{accuracy}')
    test_logger = logging.getLogger('test_data_logger')
    test_logger.info(f'Accuracy of transcription:{accuracy}')

    return float(accuracy)
