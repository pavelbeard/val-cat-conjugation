from bson import ObjectId
from datetime import datetime
from fastapi.encoders import jsonable_encoder


custom_encoder = {
    ObjectId: str,
    datetime: lambda dt: dt.isoformat(),
}


def custom_jsonable_encoder(obj):
    """
    Custom JSON encoder that uses the custom_encoder for specific types.
    """
    return jsonable_encoder(obj, custom_encoder=custom_encoder)
