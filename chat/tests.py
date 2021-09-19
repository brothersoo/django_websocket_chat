import asyncio
import pytest

from urllib.parse import unquote

from django.test import TestCase
from django.urls import path
from channels.consumer import AsyncConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.routing import URLRouter
from channels.testing import ApplicationCommunicator, ChannelsLiveServerTestCase, HttpCommunicator, WebsocketCommunicator
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from .consumers import ChatConsumer
from django_websocket_chat.routing import application


class SimpleHttpApp(AsyncConsumer):
    """
    Barebones HTTP ASGI app for testing.
    """

    async def http_request(self, event):
        assert self.scope["path"] == "/test/"
        assert self.scope["method"] == "GET"
        assert self.scope["query_string"] == b"foo=bar"
        await self.send({"type": "http.response.start", "status": 200, "headers": []})
        await self.send({"type": "http.response.body", "body": b"test response"})


@pytest.mark.asyncio
async def test_http_communicator():
    """
    Tests that the HTTP communicator class works at a basic level.
    """
    communicator = HttpCommunicator(SimpleHttpApp(), "GET", "/test/?foo=bar")
    response = await communicator.get_response()
    assert response["body"] == b"test response"
    assert response["status"] == 200


class SimpleWebsocketApp(WebsocketConsumer):
    """
    Barebones WebSocket ASGI app for testing.
    """

    def connect(self):
        assert self.scope["path"] == "/testws/"
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        self.send(text_data=text_data, bytes_data=bytes_data)


class ErrorWebsocketApp(WebsocketConsumer):
    """
    Barebones WebSocket ASGI app for error testing.
    """

    def receive(self, text_data=None, bytes_data=None):
        pass


class KwargsWebSocketApp(WebsocketConsumer):
    """
    WebSocket ASGI app used for testing the kwargs arguments in the url_route.
    """

    def connect(self):
        self.accept()
        self.send(text_data=self.scope["url_route"]["kwargs"]["message"])


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_websocket_communicator():
    """
    Tests that the WebSocket communicator class works at a basic level.
    """
    communicator = WebsocketCommunicator(SimpleWebsocketApp(), "/testws/")
    # Test connection
    connected, subprotocol = await communicator.connect()
    assert connected
    assert subprotocol is None
    # Test sending text
    await communicator.send_to(text_data="hello")
    response = await communicator.receive_from()
    assert response == "hello"
    # Test sending bytes
    await communicator.send_to(bytes_data=b"w\0\0\0")
    response = await communicator.receive_from()
    assert response == b"w\0\0\0"
    # Test sending JSON
    await communicator.send_json_to({"hello": "world"})
    response = await communicator.receive_json_from()
    assert response == {"hello": "world"}
    # Close out
    await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_websocket_application():
    """
    Tests that the WebSocket communicator class works with the
    URLRoute application.
    """
    application = URLRouter([path("testws/<str:message>/", KwargsWebSocketApp())])
    communicator = WebsocketCommunicator(application, "/testws/test/")
    connected, subprotocol = await communicator.connect()
    # Test connection
    assert connected
    assert subprotocol is None
    message = await communicator.receive_from()
    assert message == "test"
    await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_timeout_disconnect():
    """
    Tests that disconnect() still works after a timeout.
    """
    communicator = WebsocketCommunicator(ErrorWebsocketApp(), "/testws/")
    # Test connection
    connected, subprotocol = await communicator.connect()
    assert connected
    assert subprotocol is None
    # Test sending text (will error internally)
    await communicator.send_to(text_data="hello")
    with pytest.raises(asyncio.TimeoutError):
        await communicator.receive_from()
    # Close out
    await communicator.disconnect()


class ConnectionScopeValidator(WebsocketConsumer):
    """
    Tests ASGI specification for the connection scope.
    """

    def connect(self):
        assert self.scope["type"] == "websocket"
        # check if path is a unicode string
        assert isinstance(self.scope["path"], str)
        # check if path has percent escapes decoded
        assert self.scope["path"] == unquote(self.scope["path"])
        # check if query_string is a bytes sequence
        assert isinstance(self.scope["query_string"], bytes)
        self.accept()


paths = [
    "user:pass@example.com:8080/p/a/t/h?query=string#hash",
    "wss://user:pass@example.com:8080/p/a/t/h?query=string#hash",
    (
        "ws://www.example.com/%E9%A6%96%E9%A1%B5/index.php?"
        "foo=%E9%A6%96%E9%A1%B5&spam=eggs"
    ),
]


@pytest.mark.django_db
@pytest.mark.asyncio
@pytest.mark.parametrize("path", paths)
async def test_connection_scope(path):
    """
    Tests ASGI specification for the the connection scope.
    """
    communicator = WebsocketCommunicator(ConnectionScopeValidator(), path)
    connected, _ = await communicator.connect()
    assert connected
    await communicator.disconnect()

# class MyTests(TestCase):

    # async def test_application_communicator(self):
    #     communicator = ApplicationCommunicator(ChatConsumer, {"type": "http"})
    #     await communicator.send_input({
    #         "type": "http.request",
    #         "body": b"chunk one \x01 chunk two",
    #     })
    #
    #     event = await communicator.receive_output(timeout=1)
    #     self.assertEqual(event["type"], "http.response.start")
    #
    #     self.assertEqual(await communicator.receive_nothing(timeout=0.1, interval=0.01), False)
    #     event = await communicator.receive_output()
    #     self.assertEqual(event["type"], "http.response.body")
    #     self.assertEqual(event.get("more_body"), True)
    #
    #     event = await communicator.receive_output()
    #     self.assertEqual(event["type"], "http.response.start")
    #     self.assertEqual(event.get("more_body"), None)
    #
    #     self.assertEqual(await communicator.receive_nothing(), True)

    # async def test_http_communicator(self):
    #     communicator = HttpCommunicator(ChatConsumer, "GET", "/test/")
    #     response = await communicator.get_response()
    #     self.assertEqual(response["body"], b"test response")
    #     self.assertEqual(response["status"], 200)


# @pytest.mark.asyncio
# class TestWebsockets:
#
#     async def test_receives_data(self, settings):
#
#         communicator = WebsocketCommunicator(
#             application=application,
#             path="ws/notifications"
#         )
#         connected, _ = await communicator.connect()
#         assert connected
#         await communicator.send_json_to({"type": "notify", "data": "who knows"})
#         response = await communicator.receive_json_from()
#         await communicator.disconnect()



# class ChatTests(ChannelsLiveServerTestCase):
#     serve_static = True  # emulate StaticLiveServerTestCase
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         try:
#             # NOTE: Requires "chromedriver" binary to be installed in $PATH
#             cls.driver = webdriver.Chrome(ChromeDriverManager().install())
#         except:
#             super().tearDownClass()
#             raise
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.driver.quit()
#         super().tearDownClass()
#
#     def test_when_chat_message_posted_then_seen_by_everyone_in_same_room(self):
#         try:
#             self._enter_chat_room('room_1')
#
#             self._open_new_window()
#             self._enter_chat_room('room_1')
#
#             self._switch_to_window(0)
#             self._post_message('hello')
#             WebDriverWait(self.driver, 2).until(lambda _:
#                 'hello' in self._chat_log_value,
#                 'Message was not received by window 1 from window 1')
#             self._switch_to_window(1)
#             WebDriverWait(self.driver, 2).until(lambda _:
#                 'hello' in self._chat_log_value,
#                 'Message was not received by window 2 from window 1')
#         finally:
#             self._close_all_new_windows()
#
#     def test_when_chat_message_posted_then_not_seen_by_anyone_in_different_room(self):
#         try:
#             self._enter_chat_room('room_1')
#
#             self._open_new_window()
#             self._enter_chat_room('room_2')
#
#             self._switch_to_window(0)
#             self._post_message('hello')
#             WebDriverWait(self.driver, 2).until(lambda _:
#                 'hello' in self._chat_log_value,
#                 'Message was not received by window 1 from window 1')
#
#             self._switch_to_window(1)
#             self._post_message('world')
#             WebDriverWait(self.driver, 2).until(lambda _:
#                 'world' in self._chat_log_value,
#                 'Message was not received by window 2 from window 2')
#             self.assertTrue('hello' not in self._chat_log_value,
#                 'Message was improperly received by window 2 from window 1')
#         finally:
#             self._close_all_new_windows()
#
#     # === Utility ===
#
#     def _enter_chat_room(self, room_name):
#         self.driver.get(self.live_server_url + '/chat/')
#         ActionChains(self.driver).send_keys(room_name + '\n').perform()
#         WebDriverWait(self.driver, 2).until(lambda _:
#                                             room_name in self.driver.current_url)
#
#     def _open_new_window(self):
#         self.driver.execute_script('window.open("about:blank", "_blank");')
#         self.driver.switch_to_window(self.driver.window_handles[-1])
#
#     def _close_all_new_windows(self):
#         while len(self.driver.window_handles) > 1:
#             self.driver.switch_to_window(self.driver.window_handles[-1])
#             self.driver.execute_script('window.close();')
#         if len(self.driver.window_handles) == 1:
#             self.driver.switch_to_window(self.driver.window_handles[0])
#
#     def _switch_to_window(self, window_index):
#         self.driver.switch_to_window(self.driver.window_handles[window_index])
#
#     def _post_message(self, message):
#         ActionChains(self.driver).send_keys(message + '\n').perform()
#
#     @property
#     def _chat_log_value(self):
#         return self.driver.find_element_by_css_selector('#chat-log').get_property('value')
