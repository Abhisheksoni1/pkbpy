from django.conf import settings

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from libraries.utils import get_kitchen_or_error


class OrderConsumer(AsyncJsonWebsocketConsumer):
    """
    This order consumer handles websocket connections for kitchen clients.
    It uses AsyncJsonWebsocketConsumer, which means all the handling functions
    must be async functions, and any sync work (like ORM access) has to be
    behind database_sync_to_async or sync_to_async. For more, read
    http://channels.readthedocs.io/en/latest/topics/consumers.html
    """

    # WebSocket event handlers

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kitchens = set()

    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        # Are they logged in?
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()
        else:
            # Accept the connection
            await self.accept()
        # Store which rooms the user has joined on this connection

    async def receive_json(self, content):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Messages will have a "command" key we can switch on
        command = content.get("command", None)
        # kitchen_id = content.get("kitchen", None)
        try:
            if command == "join":
                # Make them join the room
                await self.join_kitchen()
            elif command == "leave":
                # Leave the room
                await self.leave_kitchen()
            elif command == "send":
                await self.send_kitchen(content["message"])
        except Exception as e:
            # Catch any errors and send it back
            await self.send_json({"error": content})

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave all the rooms we are still in
        for kitchen_id in list(self.kitchens):
            try:
                await self.leave_kitchen(kitchen_id)
            except Exception:
                pass

    # Command helper methods called by receive_json

    async def join_kitchen(self):
        """
        Called by receive_json when someone sent a join command.
        """
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
            await self.channel_layer.group_send(
                'kitchen',
                {
                    "type": "kitchen.join",
                    "username": self.scope["user"].username,
                }
            )
        # Store that we're in the room
        # self.kitchens.add(kitchen_id)
        # Add them to the group so they get room messages
        await self.channel_layer.group_add(
            # kitchen.group_name,
            'kitchen',
            self.channel_name,
        )

    async def leave_kitchen(self):
        """
        Called by receive_json when someone sent a leave command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        # kitchen = await get_kitchen_or_error(kitchen_id, self.scope["user"])
        # Send a leave message if it's turned on
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
            await self.channel_layer.group_send(
                'kitchen',
                {
                    "type": "kitchen.leave",
                    "username": self.scope["user"].username,
                }
            )
        # Remove that we're in the room
        # self.kitchens.discard(kitchen_id)
        # Remove them from the group so they no longer get room messages
        await self.channel_layer.group_discard(
            'kitchen',
            self.channel_name,
        )

    async def send_kitchen(self, message):
        """
        Called by receive_json when someone sends a message to a room.
        """
        # Check they are in this room
        # kitchen = await get_kitchen_or_error(kitchen_id, self.scope["user"])
        await self.channel_layer.group_send(
            'kitchen',
            {
                "type": "kitchen.message",
                "username": self.scope["user"].username,
                "message": message,
            }
        )

    # Handlers for messages sent over the channel layer

    # These helper methods are named by the types we send - so kitchen.join becomes kitchen_join
    async def kitchen_join(self, event):
        """
        Called when someone has joined our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_ENTER,
                "username": event["username"],
            },
        )

    async def kitchen_leave(self, event):
        """
        Called when someone has left our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_LEAVE,
                "username": event["username"],
            },
        )

    async def kitchen_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        print(event)
        message = {
                "msg_type": settings.MSG_TYPE_MESSAGE,
                "username": event["username"],
                "message": event["message"],
            }
        if event.get("kitchen_id", False):
            message['kitchen_id'] = event.get("kitchen_id")
        await self.send_json(
            message,
        )
