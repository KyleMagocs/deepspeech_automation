import logging
import pytest

from ..TestData.expected_transcripts import test_data
from ..lib.compare import get_accuracy_of_transcription
from ..lib.deepspeech import call_deepspeech

console_logger = logging.getLogger('console')

accuracy_threshold = 0.8

@pytest.mark.parametrize('audio_file_name,expected_result', list(test_data.items()),
                         ids=list(test_data.keys()))
def test_audio_transcription(audio_file_name, expected_result, test_logger, request):
    console_logger.info(f'Beginning execution of test for {request.node.callspec.id}')
    # GIVEN: a trained deepspeech model
    #   AND: a test dataset

    #  WHEN: I execute deepspeech against the data
    result = call_deepspeech(audio_file_name)

    #  THEN: I should receive the transcription
    #   AND: It should match the manual transcript to 80%
    accuracy = get_accuracy_of_transcription(expected_result, result)
    console_logger.info(f'Test completed with accuracy of {accuracy:.2}')

    assert accuracy > accuracy_threshold, f'Accuracy of {accuracy:.2} less than {accuracy_threshold:.2}'
