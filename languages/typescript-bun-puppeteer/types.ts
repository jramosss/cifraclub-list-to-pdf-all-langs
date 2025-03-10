import type { BunRequest } from "bun";

export type GenerateRequestParams = BunRequest & {
    params: {
        id: string;
    }
    listUrl: string;
    json: () => Promise<{ listUrl: string }>;
}

export type SocketMessage = string & {
    connection_id: string;
    message: string;
}