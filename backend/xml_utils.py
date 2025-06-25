"""
XML validation helper using the pure-Python 'xmlschema' library.
"""

from pathlib import Path
import xmlschema

SCHEMA_CACHE: dict[str, xmlschema.XMLSchema] = {}


def _get_schema(xsd_name: str) -> xmlschema.XMLSchema:
    if xsd_name not in SCHEMA_CACHE:
        xsd_path = Path(__file__).parent / "schemas" / xsd_name
        SCHEMA_CACHE[xsd_name] = xmlschema.XMLSchema(xsd_path)
    return SCHEMA_CACHE[xsd_name]


def validate_xml(xml_bytes: bytes, schema_name: str):
    """
    Validate *xml_bytes* against *schema_name* (e.g. 'order.xsd').
    Return an ElementTree root if valid, else raise ValueError.
    """
    schema = _get_schema(schema_name)
    try:
        root = schema.to_etree(xml_bytes)
    except xmlschema.XMLSchemaException as exc:
        raise ValueError(str(exc)) from exc
    return root
