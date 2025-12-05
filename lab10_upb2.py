from uprotobuf import *


@registerMessage
class MeowMessage(Message):
    _proto_fields=[
        dict(name='client_id', type=WireType.Varint, subType=VarintSubType.Int32, fieldType=FieldType.Required, id=1),
        dict(name='temperature', type=WireType.Bit32, subType=FixedSubType.Float, fieldType=FieldType.Required, id=2),
        dict(name='time', type=WireType.Varint, subType=VarintSubType.UInt64, fieldType=FieldType.Required, id=3),
    ]
