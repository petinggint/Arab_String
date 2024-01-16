import os

ENVIRONMENT = os.environ.get('ENVIRONMENT', False)

if ENVIRONMENT:
    try:
        API_ID = int(os.environ.get('API_ID', 23371587))
    except ValueError:
        raise Exception("Your API_ID is not a valid integer.")
    API_HASH = os.environ.get('API_HASH', None)
    BOT_TOKEN = os.environ.get('BOT_TOKEN', None)
    DATABASE_URL = os.environ.get('DATABASE_URL', None)
    DATABASE_URL = DATABASE_URL.replace("postgres", "postgresql")  # Sqlalchemy dropped support for "postgres" name.
    # https://stackoverflow.com/questions/62688256/sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy-dialectspostgre
    MUST_JOIN = os.environ.get('MUST_JOIN', None)
    #if MUST_JOIN.startswith("@"):
        #MUST_JOIN = MUST_JOIN.replace("@", "")
else:
    # Fill the Values
    API_ID = 23371587
    API_HASH = "a014ed669df0aa68734b5ecf93e65a3a"
    BOT_TOKEN = "6742240257:AAHH7RDQILs6eHQFtdXwy02eLFsuNheQsx0"
    DATABASE_URL = "postgres://rwiubjut:GC9GMoJd3JZc9srWVcw2jtKmCOlosbn9@rosie.db.elephantsql.com/rwiubjut"
    DATABASE_URL = DATABASE_URL.replace("postgres", "postgresql")
    MUST_JOIN = "@Berlinmusic_support"
    #if MUST_JOIN.startswith("@"):
       # MUST_JOIN = MUST_JOIN[1:]
