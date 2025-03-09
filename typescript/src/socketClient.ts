import type { WebSocketHandler } from "bun"
import type { SocketMessage } from "../types";

class SocketClient implements WebSocketHandler {
    message(ws: WebSocket, message: SocketMessage) {
        console.log('Message received:', message);
        
    }

    open(ws: WebSocket) {
        console.log('Socket opened');
    }

    close(ws: WebSocket, code: number, message: string) {
        console.log('Socket closed:', code, message);
    }
}