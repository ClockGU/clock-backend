from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ReportConsumer(AsyncJsonWebsocketConsumer):
    @property
    def room_group_name(self):
        return f'ReportsSocket_{self.scope["user"].id}'

    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close(
                code=4000, reason="User is not authenticated or token is missing"
            )
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self.send_json({"type": "websocket.connect"})

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def report_message(self, event):
        await self.send_json({"type": "report.update", "data": event["data"]})
