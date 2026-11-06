import { AuthenticatedUser } from "@/types/auth.types";

/**
 * Enterprise Volatile Memory Store.
 * Strictly adheres to MY EDUCATION INDIA security rules:
 * NEVER uses LocalStorage, SessionStorage, IndexedDB, or Browser Cache for tokens or application data.
 * Access token & CSRF token live exclusively in JavaScript closure memory, backed by an HttpOnly,
 * Secure, SameSite=Strict refresh token cookie managed by FastAPI + PostgreSQL.
 */
interface VolatileAuthState {
  accessToken: string | null;
  csrfToken: string | null;
  user: AuthenticatedUser | null;
}

type AuthSubscriber = (state: Readonly<VolatileAuthState>) => void;

class EnterpriseVolatileAuthStore {
  private state: VolatileAuthState = {
    accessToken: null,
    csrfToken: null,
    user: null,
  };

  private subscribers: Set<AuthSubscriber> = new Set();

  public getState(): Readonly<VolatileAuthState> {
    return { ...this.state };
  }

  public setSession(accessToken: string, csrfToken: string, user: AuthenticatedUser): void {
    this.state = {
      accessToken,
      csrfToken,
      user,
    };
    this.notify();
  }

  public updateAccessToken(accessToken: string, csrfToken: string): void {
    this.state = {
      ...this.state,
      accessToken,
      csrfToken,
    };
    this.notify();
  }

  public clearSession(): void {
    this.state = {
      accessToken: null,
      csrfToken: null,
      user: null,
    };
    this.notify();
  }

  public subscribe(listener: AuthSubscriber): () => void {
    this.subscribers.add(listener);
    return () => {
      this.subscribers.delete(listener);
    };
  }

  private notify(): void {
    const snapshot = this.getState();
    this.subscribers.forEach((listener) => listener(snapshot));
  }
}

export const authMemoryStore = new EnterpriseVolatileAuthStore();
