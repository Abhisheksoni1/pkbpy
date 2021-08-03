from channels.db import database_sync_to_async
from apps.stores.models import Kitchen

# This decorator turns this function from a synchronous function into an async one
# we can call from our async consumers, that handles Django DBs correctly.
# For more, see http://channels.readthedocs.io/en/latest/topics/databases.html
@database_sync_to_async
def get_kitchen_or_error(kitchen_id, user):
    """
    Tries to fetch a kitchen for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    if not user.is_authenticated:
        pass
    # Find the room they requested (by ID)
    try:
        kitchen = Kitchen.objects.get(pk=kitchen_id)
    except Kitchen.DoesNotExist:
        kitchen = ""
    return kitchen
