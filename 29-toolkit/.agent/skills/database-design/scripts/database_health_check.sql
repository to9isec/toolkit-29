-- FusionONE v2.34.0 - Database Health Check & Governance Audit
-- Autor: Ricardo 29 (Inforsafe)
-- Objetivo: Validar visualmente Row Level Security (RLS), Search Path e Triggers de Integridade.

WITH rls_audit AS (
    SELECT 
        tablename,
        rowsecurity as rls_enabled,
        (SELECT count(*) FROM pg_policies WHERE tablename = t.tablename) as policies_count
    FROM pg_tables t
    WHERE schemaname = 'public'
),
function_audit AS (
    SELECT 
        proname as function_name,
        proconfig as configurations,
        CASE 
            WHEN proconfig IS NULL THEN '🔴 Nao Seguro (Search Path Vulnerable)'
            WHEN 'search_path=public' = ANY(proconfig) THEN '🟢 Seguro (Search Path Fixed)'
            ELSE '🟡 Revisar'
        END as search_path_status
    FROM pg_proc p
    JOIN pg_namespace n ON p.pronamespace = n.oid
    WHERE n.nspname = 'public' 
    AND prokind = 'f'
    AND  prosecdef = true -- Apenas funções Security Definer
),
governance_laws AS (
    SELECT 
        tgname as trigger_name,
        relname as table_name,
        CASE 
            WHEN tgname LIKE '%law_01%' THEN 'Lei 01 (Imutabilidade Faturamento)'
            WHEN tgname LIKE '%law_48%' THEN 'Lei 48 (Auditoria de Retificacao)'
            ELSE 'Trigger Operacional'
        END as law_type
    FROM pg_trigger t
    JOIN pg_class c ON t.tgrelid = c.oid
    WHERE tgname LIKE '%law_%'
)

-- Resultado Consolidado para o Auditor
SELECT '--- 🛡️ RELATÓRIO DE GOVERNANÇA FUSIONONE v2.34.0 ---' as report_section
UNION ALL
SELECT '1. Row Level Security (RLS) Status:'
UNION ALL
SELECT format('- Tabela: %s | RLS: %s | Políticas: %s', tablename, rls_enabled, policies_count) FROM rls_audit
UNION ALL
SELECT ''
UNION ALL
SELECT '2. Segurança de Funções (Anti-Hijacking):'
UNION ALL
SELECT format('- Função: %s | Status: %s', function_name, search_path_status) FROM function_audit
UNION ALL
SELECT ''
UNION ALL
SELECT '3. Leis de Governança Ativas (Triggers):'
UNION ALL
SELECT format('- %s na tabela %s', law_type, table_name) FROM governance_laws;
