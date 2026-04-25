import { eventBus } from '@/shared/events/EventBus';

// Bootstrap da Aplicação Modular
async function bootstrap() {
  console.log('🚀 Iniciando {{project-name}}...');

  // Inicializar Módulos Núcleo
  // Aqui é o único lugar onde os módulos podem ser importados para composição
  
  // 1. Audit escuta tudo
  eventBus.subscribe('*', (event) => {
    console.log(`[Audit] Evento recebido: ${JSON.stringify(event)}`);
  });

  // 2. Notifications escuta eventos específicos
  eventBus.subscribe('CredentialCreated', (data) => {
    console.log(`[Notifications] Enviando e-mail de boas-vindas para ${data.email}`);
  });

  console.log('✅ Sistema pronto.');
}

bootstrap().catch(console.error);
