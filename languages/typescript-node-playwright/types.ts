export type SocketMessage = string & {
    connection_id: string;
    message: string;
}