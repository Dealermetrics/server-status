export interface Server {
    status?: number;
    error?: string;
    logs?: string;
}
export interface Servers {
    [key: string]: Server;
}