from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import gobang.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            gobang.routing.websocketUrlpatterns
        )
    ),
})
