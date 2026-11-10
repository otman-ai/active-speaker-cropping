from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AudioCodec(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AUDIO_CODEC_UNSPECIFIED: _ClassVar[AudioCodec]
    AUDIO_CODEC_MP3: _ClassVar[AudioCodec]
    AUDIO_CODEC_WAV: _ClassVar[AudioCodec]
    AUDIO_CODEC_OPUS: _ClassVar[AudioCodec]

class AudioFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AUDIO_FORMAT_UNSPECIFIED: _ClassVar[AudioFormat]
    AUDIO_FORMAT_S16LE: _ClassVar[AudioFormat]
AUDIO_CODEC_UNSPECIFIED: AudioCodec
AUDIO_CODEC_MP3: AudioCodec
AUDIO_CODEC_WAV: AudioCodec
AUDIO_CODEC_OPUS: AudioCodec
AUDIO_FORMAT_UNSPECIFIED: AudioFormat
AUDIO_FORMAT_S16LE: AudioFormat

class AudioConfig(_message.Message):
    __slots__ = ("encoding", "format", "bitrate_kbps")
    ENCODING_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    BITRATE_KBPS_FIELD_NUMBER: _ClassVar[int]
    encoding: AudioCodec
    format: AudioFormat
    bitrate_kbps: int
    def __init__(self, encoding: _Optional[_Union[AudioCodec, str]] = ..., format: _Optional[_Union[AudioFormat, str]] = ..., bitrate_kbps: _Optional[int] = ...) -> None: ...

class AudioEncoding(_message.Message):
    __slots__ = ("bitrate_kbps",)
    BITRATE_KBPS_FIELD_NUMBER: _ClassVar[int]
    bitrate_kbps: int
    def __init__(self, bitrate_kbps: _Optional[int] = ...) -> None: ...
