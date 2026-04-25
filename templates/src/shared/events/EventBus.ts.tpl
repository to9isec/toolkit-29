type Handler<T = any> = (data: T) => void | Promise<void>;

export class EventBus {
  private static instance: EventBus;
  private handlers: Map<string, Handler[]> = new Map();

  private constructor() {}

  public static getInstance(): EventBus {
    if (!EventBus.instance) {
      EventBus.instance = new EventBus();
    }
    return EventBus.instance;
  }

  public publish<T>(event: string, data: T): void {
    const eventHandlers = this.handlers.get(event);
    if (eventHandlers) {
      eventHandlers.forEach((handler) => handler(data));
    }
  }

  public subscribe<T>(event: string, handler: Handler<T>): void {
    const eventHandlers = this.handlers.get(event) || [];
    eventHandlers.push(handler);
    this.handlers.set(event, eventHandlers);
  }
}

export const eventBus = EventBus.getInstance();
