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


# --- Simple locale prompts for better UX in unsupported MT languages ---
PROMPTS = {
    "en": {
        "ask_intent": "How can I help you today? You can say 'check balance' or 'transfer 5000 to 0123456789'.",
        "ask_amount": "How much do you want to transfer? (in NGN)",
        "ask_account": "Please provide the 10-digit destination account number.",
        "confirm": "Confirm transfer of ₦{amount} to account {account}. Reply 'yes' to confirm or 'no' to cancel.",
        "confirmed": "Transfer submitted. You'll receive a confirmation shortly.",
        "cancelled": "Okay, cancelled.",
        "ask_balance": "Fetching your account balance...",
        "balance": "Your account balance is ₦{amount}.",
        "help": "You can say 'check balance' or 'transfer 5000 to 0123456789'.",
        "didnt_get": "I didn't get that. {help}",
    },
    "pcm": {
        "ask_intent": "How I fit help you today? You fit talk 'check balance' or 'transfer 5000 to 0123456789'.",
        "ask_amount": "How much you wan send? (for NGN)",
        "ask_account": "Abeg send the 10-digit account number wey you wan send money to.",
        "confirm": "You sure say you wan send ₦{amount} go account {account}? Reply 'yes' to confirm or 'no' to cancel.",
        "confirmed": "Transfer don go. You go soon get confirm message.",
        "cancelled": "Okay, we don cancel am.",
        "ask_balance": "I dey check your account balance...",
        "balance": "Your balance na ₦{amount}.",
        "help": "You fit talk 'check balance' or 'transfer 5000 to 0123456789'.",
        "didnt_get": "I no understand. {help}",
    },
    "yo": {
        "ask_intent": "Báwo ni mo ṣe lè ràn ẹ lọ́wọ́ lónìí? O lè sọ ‘check balance’ tàbí ‘transfer 5000 to 0123456789’.",
        "ask_amount": "Elo ni o fẹ́ ránṣẹ́? (ní NGN)",
        "ask_account": "Jọ̀wọ́ fi nǹkan ìṣírò (10 díjìtì) tí o fẹ́ rán owó sí.",
        "confirm": "Jẹ́rìí pé o fẹ́ rán ₦{amount} sí àkántì {account}. Dáhùn ‘yes’ láti jẹ́rìí tàbí ‘no’ láti fágilé.",
        "confirmed": "A ti bẹ̀rẹ̀ ìrìn owó. Ìmúlòlùú yóò dé lẹ́sẹkẹsẹ.",
        "cancelled": "Ó dáa, a ti fagilé.",
        "ask_balance": "Mo ń gba ìwòye ìsanwó àkántì rẹ...",
        "balance": "Iye owó inú àkántì rẹ̀ jẹ ₦{amount}.",
        "help": "O lè sọ ‘check balance’ tàbí ‘transfer 5000 to 0123456789’.",
        "didnt_get": "Mi ò lóye. {help}",
    },
    "ig": {
        "ask_intent": "Kedu ka m ga-esi nyere gi taa? Ị nwere ike sị ‘check balance’ ma ọ bụ ‘transfer 5000 to 0123456789’.",
        "ask_amount": "Ego ole ka ịchọrọ iziga? (na NGN)",
        "ask_account": "Biko nye nọmba akaụntụ nke mmadụ ị na-ezigara (digits 10).",
        "confirm": "Kwenye na ị na-eziga ₦{amount} na akaụntụ {account}. Zaa ‘yes’ ka o doo ma ọ bụ ‘no’ ka a kagbuo.",
        "confirmed": "Ezipụla. Ị ga-enweta nkwenye n’oge na-adịghị anya.",
        "cancelled": "Ọ dị mma, e kagburu ya.",
        "ask_balance": "Ana m enweta ego fọdụrụ na akaụntụ gị...",
        "balance": "Ego fọdụrụ na akaụntụ gị bụ ₦{amount}.",
        "help": "Ị nwere ike sị ‘check balance’ ma ọ bụ ‘transfer 5000 to 0123456789’.",
        "didnt_get": "Aghọtaghị m. {help}",
    },
    "ha": {  # will still send through Translate where needed
        "ask_intent": "Ta yaya zan taimake ka? Za ka iya cewa 'check balance' ko 'transfer 5000 to 0123456789'.",
        "ask_amount": "Nawa kake son turawa? (a NGN)",
        "ask_account": "Don Allah ka ba da lambar asusun da za a tura kudi (digits 10).",
        "confirm": "Tabbatar da turawa ₦{amount} zuwa asusun {account}. Amsa da 'yes' don tabbatarwa ko 'no' don soke.",
        "confirmed": "An tura. Za ka sami bayanin tabbaci nan ba da jimawa ba.",
        "cancelled": "To, an soke.",
        "ask_balance": "Ina duba ragowar kuɗin asusunka...",
        "balance": "Ragowar kuɗin asusunka shine ₦{amount}.",
        "help": "Za ka iya cewa 'check balance' ko 'transfer 5000 to 0123456789'.",
        "didnt_get": "Ban gane ba. {help}",
    }
}