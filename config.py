import os
import boto3

GRAPH_API_VERSION = os.environ["GRAPH_API_VERSION"]
PHONE_NUMBER_ID   = os.environ["PHONE_NUMBER_ID"]
WHATSAPP_TOKEN    = os.environ["WHATSAPP_TOKEN"]
VERIFY_TOKEN      = os.environ["VERIFY_TOKEN"]
DEFAULT_FALLBACK_LANG = os.getenv("DEFAULT_FALLBACK_LANG", "en")
DDB_TABLE = os.environ["DDB_TABLE"]

# AWS clients (use Lambda's region automatically)
comprehend = boto3.client("comprehend")
translate  = boto3.client("translate")
ddb = boto3.resource("dynamodb").Table(DDB_TABLE)

# Basic language constants
SUPPORTED_TRANSLATE_BIDI = {"ha"}  # two-way translation en<->ha

YORUBA_DIAC = set("ẹọṣáéíóúàèìòùń")
IGBO_DIAC   = set("ịụọṅńḿ")
HAUSA_DIAC  = set("ƙɗɓ")
PIDGIN_TOKENS = {"dey", "abi", "wey", "wetin", "una", "go", "no dey", "wahala", "sha", "abeg"}