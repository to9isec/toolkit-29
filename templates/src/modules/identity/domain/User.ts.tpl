import { Entity } from '@/shared/kernel/Entity';

interface UserProps {
  email: string;
  name: string;
  isActive: boolean;
}

export class User extends Entity<UserProps> {
  private constructor(props: UserProps, id?: string) {
    super(props, id);
  }

  public static create(props: UserProps, id?: string): User {
    return new User(props, id);
  }

  get email(): string {
    return this.props.email;
  }
}
