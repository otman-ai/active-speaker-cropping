from google.protobuf import empty_pb2 as _empty_pb2
from nvidia.ai4m.audio.v1 import audio_pb2 as _audio_pb2
from nvidia.ai4m.common.v1 import common_pb2 as _common_pb2
from nvidia.ai4m.common.v1 import service_info_pb2 as _service_info_pb2
from nvidia.ai4m.video.v1 import video_pb2 as _video_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AudioSourceConfig(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AUDIO_SOURCE_CONFIG_UNSPECIFIED: _ClassVar[AudioSourceConfig]
    AUDIO_SOURCE_CONFIG_SEPARATE_STREAM: _ClassVar[AudioSourceConfig]
    AUDIO_SOURCE_CONFIG_EMBEDDED_IN_VIDEO: _ClassVar[AudioSourceConfig]

class VoiceActivitySmoothing(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VOICE_ACTIVITY_SMOOTHING_UNSPECIFIED: _ClassVar[VoiceActivitySmoothing]
    VOICE_ACTIVITY_SMOOTHING_OFF: _ClassVar[VoiceActivitySmoothing]
    VOICE_ACTIVITY_SMOOTHING_LOW: _ClassVar[VoiceActivitySmoothing]
    VOICE_ACTIVITY_SMOOTHING_HIGH: _ClassVar[VoiceActivitySmoothing]
AUDIO_SOURCE_CONFIG_UNSPECIFIED: AudioSourceConfig
AUDIO_SOURCE_CONFIG_SEPARATE_STREAM: AudioSourceConfig
AUDIO_SOURCE_CONFIG_EMBEDDED_IN_VIDEO: AudioSourceConfig
VOICE_ACTIVITY_SMOOTHING_UNSPECIFIED: VoiceActivitySmoothing
VOICE_ACTIVITY_SMOOTHING_OFF: VoiceActivitySmoothing
VOICE_ACTIVITY_SMOOTHING_LOW: VoiceActivitySmoothing
VOICE_ACTIVITY_SMOOTHING_HIGH: VoiceActivitySmoothing

class DetectActiveSpeakerRequest(_message.Message):
    __slots__ = ("config", "data")
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    config: ActiveSpeakerDetectionConfig
    data: ActiveSpeakerDetectionData
    def __init__(self, config: _Optional[_Union[ActiveSpeakerDetectionConfig, _Mapping]] = ..., data: _Optional[_Union[ActiveSpeakerDetectionData, _Mapping]] = ...) -> None: ...

class ActiveSpeakerDetectionConfig(_message.Message):
    __slots__ = ("input_audio_config", "input_video_config", "audio_source_config", "speaker_detection_threshold", "voice_activity_smoothing")
    INPUT_AUDIO_CONFIG_FIELD_NUMBER: _ClassVar[int]
    INPUT_VIDEO_CONFIG_FIELD_NUMBER: _ClassVar[int]
    AUDIO_SOURCE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SPEAKER_DETECTION_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    VOICE_ACTIVITY_SMOOTHING_FIELD_NUMBER: _ClassVar[int]
    input_audio_config: _audio_pb2.AudioConfig
    input_video_config: _video_pb2.VideoConfig
    audio_source_config: AudioSourceConfig
    speaker_detection_threshold: float
    voice_activity_smoothing: VoiceActivitySmoothing
    def __init__(self, input_audio_config: _Optional[_Union[_audio_pb2.AudioConfig, _Mapping]] = ..., input_video_config: _Optional[_Union[_video_pb2.VideoConfig, _Mapping]] = ..., audio_source_config: _Optional[_Union[AudioSourceConfig, str]] = ..., speaker_detection_threshold: _Optional[float] = ..., voice_activity_smoothing: _Optional[_Union[VoiceActivitySmoothing, str]] = ...) -> None: ...

class ActiveSpeakerDetectionData(_message.Message):
    __slots__ = ("video_data", "audio_data", "diarization_info")
    VIDEO_DATA_FIELD_NUMBER: _ClassVar[int]
    AUDIO_DATA_FIELD_NUMBER: _ClassVar[int]
    DIARIZATION_INFO_FIELD_NUMBER: _ClassVar[int]
    video_data: bytes
    audio_data: bytes
    diarization_info: AudioDiarizationInfo
    def __init__(self, video_data: _Optional[bytes] = ..., audio_data: _Optional[bytes] = ..., diarization_info: _Optional[_Union[AudioDiarizationInfo, _Mapping]] = ...) -> None: ...

class AudioDiarizationInfo(_message.Message):
    __slots__ = ("segments", "transcript")
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIPT_FIELD_NUMBER: _ClassVar[int]
    segments: _containers.RepeatedCompositeFieldContainer[AudioSegmentInfo]
    transcript: str
    def __init__(self, segments: _Optional[_Iterable[_Union[AudioSegmentInfo, _Mapping]]] = ..., transcript: _Optional[str] = ...) -> None: ...

class AudioSegmentInfo(_message.Message):
    __slots__ = ("start_time", "end_time", "speaker_id", "word", "language_code")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    SPEAKER_ID_FIELD_NUMBER: _ClassVar[int]
    WORD_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_CODE_FIELD_NUMBER: _ClassVar[int]
    start_time: int
    end_time: int
    speaker_id: int
    word: str
    language_code: str
    def __init__(self, start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., speaker_id: _Optional[int] = ..., word: _Optional[str] = ..., language_code: _Optional[str] = ...) -> None: ...

class SpeakerInfo(_message.Message):
    __slots__ = ("speaker_bbox", "diarized_speaker_id", "face_id", "is_speaking", "face_detection_confidence")
    SPEAKER_BBOX_FIELD_NUMBER: _ClassVar[int]
    DIARIZED_SPEAKER_ID_FIELD_NUMBER: _ClassVar[int]
    FACE_ID_FIELD_NUMBER: _ClassVar[int]
    IS_SPEAKING_FIELD_NUMBER: _ClassVar[int]
    FACE_DETECTION_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    speaker_bbox: _common_pb2.BoundingBox
    diarized_speaker_id: int
    face_id: int
    is_speaking: bool
    face_detection_confidence: float
    def __init__(self, speaker_bbox: _Optional[_Union[_common_pb2.BoundingBox, _Mapping]] = ..., diarized_speaker_id: _Optional[int] = ..., face_id: _Optional[int] = ..., is_speaking: bool = ..., face_detection_confidence: _Optional[float] = ...) -> None: ...

class DetectActiveSpeakerResponse(_message.Message):
    __slots__ = ("config", "active_speaker_detection_result", "keepalive", "service_info")
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_SPEAKER_DETECTION_RESULT_FIELD_NUMBER: _ClassVar[int]
    KEEPALIVE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_INFO_FIELD_NUMBER: _ClassVar[int]
    config: ActiveSpeakerDetectionConfig
    active_speaker_detection_result: ActiveSpeakerDetectionResult
    keepalive: _empty_pb2.Empty
    service_info: _service_info_pb2.ServiceInfo
    def __init__(self, config: _Optional[_Union[ActiveSpeakerDetectionConfig, _Mapping]] = ..., active_speaker_detection_result: _Optional[_Union[ActiveSpeakerDetectionResult, _Mapping]] = ..., keepalive: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ..., service_info: _Optional[_Union[_service_info_pb2.ServiceInfo, _Mapping]] = ...) -> None: ...

class ActiveSpeakerDetectionResult(_message.Message):
    __slots__ = ("frame_id", "speaker_data")
    FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    SPEAKER_DATA_FIELD_NUMBER: _ClassVar[int]
    frame_id: int
    speaker_data: _containers.RepeatedCompositeFieldContainer[SpeakerInfo]
    def __init__(self, frame_id: _Optional[int] = ..., speaker_data: _Optional[_Iterable[_Union[SpeakerInfo, _Mapping]]] = ...) -> None: ...
