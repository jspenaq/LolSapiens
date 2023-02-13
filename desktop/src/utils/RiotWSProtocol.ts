// Code from gist.github.com/Pupix/eb662b1b784bb704a1390643738a8c15
import WebSocket from "ws";
import { type Credentials } from "./LeagueClient";

export const MESSAGE_TYPES = {
  WELCOME: 0,
  PREFIX: 1,
  CALL: 2,
  CALLRESULT: 3,
  CALLERROR: 4,
  SUBSCRIBE: 5,
  UNSUBSCRIBE: 6,
  PUBLISH: 7,
  EVENT: 8,
};

export default class RiotWSProtocol extends WebSocket {
  session: string | null;

  constructor(credentials: Credentials) {
    const { username, password, address, port } = credentials;
    const url = `wss://${username}:${password}@${address}:${port}/`;
    super(url, "wamp");
    this.session = null;
    this.on("message", this._onMessage.bind(this));
  }

  close(): void {
    super.close();
    this.session = null;
  }

  terminate(): void {
    super.terminate();
    this.session = null;
  }

  subscribe(topic: string, callback: (data: any) => void): void {
    super.addListener(topic, callback);
    this.sendRiotMsj(MESSAGE_TYPES.SUBSCRIBE, topic);
  }

  unsubscribe(topic: string, callback: (data: any) => void): void {
    super.removeListener(topic, callback);
    this.sendRiotMsj(MESSAGE_TYPES.UNSUBSCRIBE, topic);
  }

  sendRiotMsj(type: number, message: string): void {
    super.send(JSON.stringify([type, message]));
  }

  _onMessage(message: string): void {
    const [type, ...data] = JSON.parse(message);

    const [topic, payload] = data;
    switch (type) {
      case MESSAGE_TYPES.WELCOME:
        this.session = data[0];
        break;
      case MESSAGE_TYPES.CALLRESULT:
        console.log(data);
        break;
      case MESSAGE_TYPES.EVENT:
        this.emit(topic, payload);
        break;
      default:
        console.log([type, data]);
        break;
    }
  }
}
