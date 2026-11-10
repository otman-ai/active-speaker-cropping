from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ServiceInfo(_message.Message):
    __slots__ = ("feature_version", "feature_name", "model_info", "server_request_id", "client_session_id")
    FEATURE_VERSION_FIELD_NUMBER: _ClassVar[int]
    FEATURE_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_INFO_FIELD_NUMBER: _ClassVar[int]
    SERVER_REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    feature_version: str
    feature_name: str
    model_info: str
    server_request_id: str
    client_session_id: str
    def __init__(self, feature_version: _Optional[str] = ..., feature_name: _Optional[str] = ..., model_info: _Optional[str] = ..., server_request_id: _Optional[str] = ..., client_session_id: _Optional[str] = ...) -> None: ...
