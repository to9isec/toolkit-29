import { Result, success, failure } from '@/shared/types/Result';

interface LoginInput {
  email: string;
  password: string;
}

interface LoginOutput {
  token: string;
}

export class LoginUseCase {
  async execute(input: LoginInput): Promise<Result<LoginOutput>> {
    // Lógica de autenticação fictícia
    if (input.email === 'admin@29.com') {
      return success({ token: 'mock-jwt-token' });
    }

    return failure(new Error('Credenciais inválidas'));
  }
}
