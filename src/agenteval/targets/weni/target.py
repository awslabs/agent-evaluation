# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json
import os
import uuid
import time
import logging
import threading
from typing import Optional

import requests
import websocket

from agenteval.targets import BaseTarget, TargetResponse

logger = logging.getLogger(__name__)


class WeniTarget(BaseTarget):
    """A target encapsulating a Weni agent."""

    def __init__(
        self,
        weni_project_uuid: Optional[str] = None,
        weni_bearer_token: Optional[str] = None,
        language: str = "en-US",
        timeout: int = 120,
        **kwargs
    ):
        """Initialize the target.

        Args:
            weni_project_uuid (Optional[str]): The Weni project UUID. 
                If not provided, will be read from WENI_PROJECT_UUID env var.
            weni_bearer_token (Optional[str]): The Weni bearer token. 
                If not provided, will be read from WENI_BEARER_TOKEN env var.
            language (str): The language for the conversation. Defaults to "pt-BR".
            timeout (int): Maximum time to wait for agent response in seconds. Defaults to 30.
        """
        super().__init__()
        
        self.project_uuid = weni_project_uuid or os.environ.get("WENI_PROJECT_UUID")
        self.bearer_token = weni_bearer_token or os.environ.get("WENI_BEARER_TOKEN")
        self.language = language
        self.timeout = timeout
        
        if not self.project_uuid:
            raise ValueError(
                "weni_project_uuid must be provided or WENI_PROJECT_UUID must be set as environment variable"
            )
        if not self.bearer_token:
            raise ValueError(
                "weni_bearer_token must be provided or WENI_BEARER_TOKEN must be set as environment variable"
            )
        
        # Generate unique contact URN for this test session
        # This ensures each test case has its own conversation history
        self.contact_urn = f"ext:{uuid.uuid4().hex}"
        
        # API endpoints
        self.api_base_url = "https://nexus.weni.ai"
        self.api_endpoint = f"{self.api_base_url}/api/{self.project_uuid}/preview/"
        self.ws_endpoint = (
            f"wss://nexus.weni.ai/ws/preview/{self.project_uuid}/"
            f"?Token={self.bearer_token}"
        )
        
        logger.debug(f"Initialized WeniTarget with project UUID: {self.project_uuid}")
        logger.debug(f"Using contact URN: {self.contact_urn}")

    def invoke(self, prompt: str) -> TargetResponse:
        """Invoke the target with a prompt.

        Args:
            prompt (str): The prompt as a string.

        Returns:
            TargetResponse
        """
        try:
            logger.debug(f"Invoking Weni agent with prompt: {prompt}")
            
            # Send the prompt via POST request
            self._send_prompt(prompt)
            
            # Connect to WebSocket and wait for response
            response_text = self._wait_for_response()
            
            return TargetResponse(
                response=response_text,
                data={
                    "contact_urn": self.contact_urn,
                    "language": self.language,
                    "session_id": self.contact_urn
                }
            )
            
        except Exception as e:
            logger.error(f"Error invoking Weni agent: {str(e)}")
            raise

    def _send_prompt(self, prompt: str) -> None:
        """Send a prompt to the Weni API.

        Args:
            prompt (str): The message to send.

        Raises:
            requests.HTTPError: If the API request fails.
        """
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7,es;q=0.6,nl;q=0.5,fr;q=0.4",
            "authorization": f"Bearer {self.bearer_token}",
            "content-type": "application/json",
            "origin": "https://intelligence-next.weni.ai",
            "priority": "u=1, i",
            "referer": "https://intelligence-next.weni.ai/agents",
            "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/139.0.0.0 Safari/537.36"
            )
        }
        
        data = {
            "text": prompt,
            "attachments": [],
            "contact_urn": self.contact_urn,
            "language": self.language
        }
        
        logger.debug(f"Sending POST request to {self.api_endpoint}")
        
        response = requests.post(
            self.api_endpoint,
            headers=headers,
            json=data,
            timeout=10
        )
        
        response.raise_for_status()
        logger.debug(f"Successfully sent prompt to Weni API. Status: {response.status_code}")

    def _wait_for_response(self) -> str:
        """Connect to WebSocket and wait for the agent's final response.

        Returns:
            str: The agent's final response text.

        Raises:
            TimeoutError: If no response is received within the timeout period.
        """
        final_response = None
        start_time = time.time()
        ws_error = None
        
        def on_message(ws, message):
            """Handle incoming WebSocket messages."""
            nonlocal final_response
            try:
                data = json.loads(message)
                logger.debug(f"Received WebSocket message: {json.dumps(data, indent=2)[:200]}...")
                
                # Check for preview message format
                if data.get("type") == "preview":
                    message = data.get("message", {})
                    if message.get("type") == "preview":
                        content = message.get("content", {})
                        if content.get("type") == "broadcast" and "message" in content:
                            final_response = content["message"]
                            logger.debug(f"Received preview broadcast message: {final_response[:100]}...")
                            ws.close()
                            
            except json.JSONDecodeError:
                logger.warning(f"Failed to decode WebSocket message: {message[:100]}...")
            except Exception as e:
                logger.error(f"Error processing WebSocket message: {str(e)}")

        def on_error(ws, error):
            """Handle WebSocket errors."""
            nonlocal ws_error
            ws_error = error
            logger.error(f"WebSocket error: {error}")

        def on_close(ws, close_status_code, close_msg):
            """Handle WebSocket closure."""
            logger.debug(f"WebSocket closed with code {close_status_code}: {close_msg}")

        def on_open(ws):
            """Handle WebSocket connection open."""
            logger.debug("WebSocket connection established")

        def on_ping(ws, message):
            """Handle WebSocket ping."""
            logger.debug("Received WebSocket ping")

        def on_pong(ws, message):
            """Handle WebSocket pong."""
            logger.debug("Received WebSocket pong")

        # Configure WebSocket headers
        headers = {
            "Origin": "https://intelligence-next.weni.ai",
            "Accept-Language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7,es;q=0.6,nl;q=0.5,fr;q=0.4",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/139.0.0.0 Safari/537.36"
            )
        }
        
        logger.debug(f"Connecting to WebSocket: {self.ws_endpoint[:50]}...")
        
        # Create WebSocket connection
        ws = websocket.WebSocketApp(
            self.ws_endpoint,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            on_ping=on_ping,
            on_pong=on_pong,
            header=headers
        )
        
        # Run WebSocket in a separate thread
        ws_thread = threading.Thread(target=ws.run_forever)
        ws_thread.daemon = True
        ws_thread.start()
        
        # Wait for response with timeout
        while final_response is None and (time.time() - start_time) < self.timeout:
            if ws_error:
                raise RuntimeError(f"WebSocket error occurred: {ws_error}")
            time.sleep(0.1)
        
        # Ensure WebSocket is closed
        try:
            ws.close()
        except:
            pass
        
        # Wait for thread to finish
        ws_thread.join(timeout=1)
        
        if final_response is None:
            raise TimeoutError(
                f"No response received from Weni agent within {self.timeout} seconds"
            )
        
        return final_response
