# GH-600 · Inventario de fuentes para preparar preguntas

Referencia para generar bancos de preguntas del Exam Room. Cada pregunta debe salir de una habilidad del *study guide* y tener su respuesta verificada en una fuente de nivel 1.

Actualizado: 27/11/2026. Las rutas de GitHub Docs sobre Copilot cambian a menudo. Si un enlace falla, busca su título en docs.github.com; GitHub suele redirigir las rutas antiguas.

---

## 1. Jerarquía de fuentes

| Nivel | Fuente | Para qué sirve | Cuándo manda |
|---|---|---|---|
| **0 · Contrato** | [Study guide GH-600](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-600) (*Skills measured*) | Qué se puede preguntar y con qué peso | Decide **qué** preguntar |
| **1 · Verdad del producto** | [GitHub Docs](https://docs.github.com/en/copilot) (Copilot, Actions, repos, code security) | Cómo funciona realmente cada cosa | Decide **la respuesta correcta**. Si contradice a Learn, gana Docs |
| **1b · Agentic Workflows** | [gh-aw docs](https://github.github.com/gh-aw/introduction/how-they-work/) | Frontmatter, compilación, *safe outputs*, observabilidad | Igual que Docs, para `gh aw` |
| **2 · Enfoque del examen** | Los 6 módulos de Microsoft Learn (abajo) | Vocabulario, escenarios y cómo plantea Microsoft los conceptos | Para el **estilo** de la pregunta. Tienen errores conocidos (sección 5) |
| **3 · Actualidad** | [GitHub Changelog](https://github.blog/changelog/) | Qué es GA y qué es preview, y cambios recientes | Para no preguntar por cosas obsoletas o solo en preview |
| **4 · Formato** | [Exam duration and experience](https://learn.microsoft.com/en-us/credentials/support/exam-duration-exam-experience), [sandbox](https://aka.ms/examdemo) | Tipos de pregunta, reglas de navegación | Para el **formato** |
| **Excluidas** | *Dumps*, explicaciones de Udemy, mi propia memoria sin verificar | — | Nunca como fuente de una respuesta |

Nota del study guide: *"Most questions cover features that are GA. The exam may contain questions on Preview features if those features are commonly used."*

---

## 2. Módulos oficiales de Microsoft Learn

| # | Módulo | Dominios | En el study guide |
|---|---|---|---|
| M1 | [Foundations of Agentic AI in GitHub](https://learn.microsoft.com/en-us/training/modules/foundations-agentic-ai/) | General | Sí |
| M2 | [Designing Agent Architecture and SDLC Integration](https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/) | D1 | Sí |
| M3 | [Tooling, MCP, and Agent Execution Environments](https://learn.microsoft.com/en-us/training/modules/agent-tooling-mcp-execution-environments/) | D2 | Sí |
| M4 | [Multi-Agent systems and orchestration](https://learn.microsoft.com/en-us/training/modules/multi-agent-systems-orchestration/) | D5 | No (Part 2) |
| M5 | [Memory, State, and Evaluation](https://learn.microsoft.com/en-us/training/modules/memory-state-evaluation/) | D3, D4 | No (Part 2) |
| M6 | [Governance, guardrails, and operations](https://learn.microsoft.com/en-us/training/modules/governance-guardrails-operations/) | D6 | No (Part 2) |

---

## 3. Mapa habilidad → fuentes

✅ = página consultada en esta preparación o enlazada desde una fuente oficial (study guide, Learn) · ◻️ = enlace de búsqueda o de memoria; comprobar antes de citarlo.

### D1 · Agent architecture and SDLC (15–20 %)

| Habilidad (study guide) | Fuentes nivel 1 | Learn |
|---|---|---|
| Pasos, antipatrones, inputs/outputs/criterios de éxito | ✅ [Prepare for custom agents](https://docs.github.com/copilot/how-tos/administer-copilot/manage-for-organization/prepare-for-custom-agents) (enlace oficial de la guía para D1) · ✅ [Best practices for tasks](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results) | M1, M2 u.2–3 |
| Separar planificación y ejecución; plan estructurado; validar el plan | ✅ [Implementation planner](https://docs.github.com/en/copilot/tutorials/customization-library/custom-agents/implementation-planner) · ✅ [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration) (`tools`) | M2 u.4 |
| Autonomía, artefactos inspeccionables, intervención humana sin frenar | ✅ [Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) · ✅ [Troubleshooting required status checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/troubleshooting-required-status-checks) · ✅ [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) | M2 u.5–7 |

### D2 · Tool use and environment interaction (20–25 %)

| Habilidad | Fuentes nivel 1 | Learn |
|---|---|---|
| Herramientas y permisos del agente | ✅ [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration) · ✅ [Custom agents en el Copilot SDK](https://docs.github.com/copilot/how-tos/copilot-sdk/use-copilot-sdk/custom-agents) (enlace oficial de la guía para D2 y D5) | M3 u.2 |
| MCP: añadir servidor, GitHub MCP remoto, registros, allowlists | ✅ [About MCP](https://docs.github.com/en/copilot/concepts/context/mcp) · ◻️ [Configure MCP servers (cloud agent)](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/configure-mcp-servers) · ◻️ [Set up the GitHub MCP server](https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp-in-your-ide/set-up-the-github-mcp-server) · ✅ [MCP usage in your company](https://docs.github.com/en/copilot/concepts/mcp-management) · ✅ [Restrict MCP to a registry](https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-mcp-usage/configure-mcp-server-access) | M3 u.3 |
| Contexto de ejecución, alcance a un repo o una rama, agente en CI, PRs autónomos, restricciones de entorno | ✅ [About cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent) · ✅ [Customize the agent environment](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/customize-the-agent-environment) · ✅ [Secrets and variables for cloud agent](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/configure-secrets-and-variables) · ✅ [Customize the firewall](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-the-firewall) · ✅ [GITHUB_TOKEN](https://docs.github.com/en/actions/concepts/security/github_token) · ✅ [Workflow syntax (`permissions`)](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) · ✅ [Use cloud agent from the CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-from-cli) · ✅ [gh-aw](https://github.github.com/gh-aw/introduction/how-they-work/) | M3 u.2, 4, ejercicio |
| Errores, reintentos, rollback, escalado, trazabilidad | ✅ [Hooks reference](https://docs.github.com/en/copilot/reference/hooks-reference) · ◻️ [Troubleshoot cloud agent](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/troubleshoot-cloud-agent) · ✅ [Track Copilot sessions](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/track-copilot-sessions) | M3 u.5, M2 u.7 |

### D3 · Memory, state and execution (10–15 %)

| Habilidad | Fuentes nivel 1 | Learn |
|---|---|---|
| Memoria corta, larga y externa; expiración y poda | ✅ [About Copilot Memory](https://docs.github.com/en/copilot/concepts/prompting-and-context/copilot-memory) (enlace oficial de la guía para D3) · ✅ [Manage Copilot Memory](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/copilot-memory/manage-for-yourself) | M5 u.2 |
| Estado duradero, retomar sin repetir, *drift* | ✅ [Store and share data with artifacts](https://docs.github.com/en/actions/tutorials/store-and-share-data) · ◻️ [Custom instructions](https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions) · [Spec Kit](https://github.com/github/spec-kit) (no oficial del examen) | M5 u.3 |
| Continuidad entre herramientas; contexto en conflicto u obsoleto | Las mismas páginas, más ✅ [Use cloud agent from the CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-from-cli) | M5 u.4 |

### D4 · Evaluation, error analysis and tuning (15–20 %)

| Habilidad | Fuentes nivel 1 | Learn |
|---|---|---|
| Criterios de éxito; señales cualitativas y cuantitativas; escaneo automático | ✅ [Implementation planner](https://docs.github.com/en/copilot/tutorials/customization-library/custom-agents/implementation-planner) (enlace oficial de la guía para D4) · ✅ [Code scanning merge protection](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/manage-your-configuration/set-merge-protection) · ◻️ [SARIF support](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning) · ◻️ [About dependency review](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-dependency-review) · ◻️ [dependency-review-action](https://github.com/actions/dependency-review-action) | M5 u.5 |
| Análisis de fallos y causa raíz (razonamiento, herramienta, contexto o entorno) | ✅ [Troubleshoot cloud agent](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/troubleshoot-cloud-agent) · ✅ [OpenTelemetry for Copilot](https://docs.github.com/en/copilot/concepts/enterprise/opentelemetry) · ✅ [OTel reference](https://docs.github.com/en/copilot/reference/enterprise-administrators/opentelemetry-reference) | M5 u.6 |
| Ajuste: instrucciones, memoria, herramientas | ◻️ [Comparing customizations](https://docs.github.com/en/copilot/concepts/customizations/comparing-customizations) · ◻️ [Add repository instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions) · ✅ [Customization cheat sheet](https://docs.github.com/en/copilot/reference/customization-cheat-sheet) | M5 u.6 |

### D5 · Multi-agent coordination (15–20 %)

| Habilidad | Fuentes nivel 1 | Learn |
|---|---|---|
| Orquestación, aislamiento en paralelo, conflictos | ✅ [Custom agents en el Copilot SDK](https://docs.github.com/copilot/how-tos/copilot-sdk/use-copilot-sdk/custom-agents) · ◻️ [Fleet mode](https://docs.github.com/en/copilot/how-tos/copilot-sdk/features/fleet-mode) · ◻️ [Subagents in your IDE](https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/use-copilot-agents/use-subagents) · ✅ [Control concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency) · ✅ [Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows) · ◻️ [Merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue) · [Multi-agent patterns (Microsoft)](https://learn.microsoft.com/agents/architecture/multi-agent-patterns) | M4 u.2–5 |
| Observabilidad, decisiones, *handoffs*, análisis posterior | ✅ [Track Copilot sessions](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/track-copilot-sessions) · ✅ [Copilot SDK OpenTelemetry](https://docs.github.com/en/copilot/how-tos/copilot-sdk/observability/opentelemetry) · ✅ [gh-aw OpenTelemetry](https://github.github.com/gh-aw/reference/open-telemetry/) | M4 u.6 |
| Fallos, degradación, recuperación; ciclo de vida de los agentes | Sin página dedicada en Docs: usar M4 u.7 más los mecanismos de GitHub (revert del PR, environments, aprobaciones) | M4 u.7 |

### D6 · Guardrails and accountability (10–15 %)

| Habilidad | Fuentes nivel 1 | Learn |
|---|---|---|
| Niveles de autonomía según el riesgo; Responsible AI | ✅ [Build guardrails](https://docs.github.com/en/copilot/tutorials/cloud-agent/build-guardrails) (enlace oficial de la guía para D6) · ✅ [Risks and mitigations](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/risks-and-mitigations) (la guía da otra ruta: `concepts/agents/cloud-agent/risks-and-mitigations`) · ✅ [Responsible use: agents](https://docs.github.com/en/copilot/responsible-use/agents) | M6 u.2 |
| Human-in-the-loop, bloqueo de acciones, mínimo privilegio, cambios irreversibles | ✅ [Deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) · ✅ [Manage environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments) · ✅ [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) · ✅ [Hooks reference](https://docs.github.com/en/copilot/reference/hooks-reference) · ✅ [Safe outputs](https://github.github.com/gh-aw/reference/safe-outputs/) · ✅ [Cloud sandboxes](https://docs.github.com/en/copilot/concepts/security-governance-and-network-settings/about-cloud-sandboxes) | M6 u.3–5 |

---

## 4. Banco de hechos verificados (para respuestas y distractores)

| Hecho | Fuente |
|---|---|
| El cloud agent **no** accede a los secretos de Actions, Codespaces ni Dependabot, solo a los de **Agents**. Un secreto `COPILOT_MCP_*` solo llega a los servidores MCP que lo referencian. A igual nombre, el de repo gana al de organización. Las variables solo funcionan cuando el agente corre en Actions, no en el *cloud sandbox* | Secrets and variables for cloud agent |
| El job de setup debe llamarse `copilot-setup-steps` | Customize the agent environment |
| El agente solo empuja a ramas `copilot/…` y no hace merge. Quien le pide el PR no puede aprobarlo. Por defecto, los workflows de sus PR esperan aprobación. Si el repo exige ≥1 aprobación, se exige una aprobación extra para cambios no atribuidos | Risks and mitigations |
| Los eventos de `GITHUB_TOKEN` no disparan runs, salvo `workflow_dispatch` y `repository_dispatch`. Los PR abiertos o actualizados con él generan runs pendientes de aprobación. El token es por job y por repo | GITHUB_TOKEN |
| Si declaras un permiso en `permissions:`, los demás pasan a `none`. Los PR desde forks reciben un token de solo lectura y ningún secreto | Workflow syntax, Secure use |
| Un check obligatorio **saltado** pasa; uno **ausente** bloquea. Se puede fijar el origen de un check | Troubleshooting required status checks |
| CODEOWNERS: gana la **última** coincidencia, y solo bloquea si el ruleset exige revisión de code owners | About code owners |
| Los secretos de un environment solo llegan a los jobs que lo declaran, tras pasar las reglas. Un nombre inexistente crea un environment sin protección. Admite hasta 6 revisores (basta 1) y *prevent self-review*. En el plan Free, las reglas de protección solo funcionan en repos públicos | Deployments and environments, Manage environments |
| `concurrency`: un grupo compartido serializa. `cancel-in-progress: true` cancela el run en curso. Solo puede haber un run pendiente: uno nuevo reemplaza al pendiente | Control concurrency |
| Hooks del cloud agent: solo `.github/hooks/*.json` y solo bash; `ask` cuenta como deny; *exit 2* deniega; si el hook falla, deniega (*fail-closed*); si hay *timeout* o error HTTP, deja pasar (*fail-open*) | Hooks reference |
| Copilot Memory: guarda dos tipos de memoria, hechos de repositorio y preferencias de usuario. Antes de usar un hecho de repositorio comprueba sus citas contra la rama actual; es un juicio de Copilot, no una garantía, así que una regla que deba aplicarse siempre va en instrucciones personalizadas. Caducidad por defecto: 90 días sin refuerzo, configurable entre 7 y 180 para los hechos de repositorio. **Corregido el 27-11-2026: aquí figuraban 28 días, cifra que aún repiten guías de la comunidad** | [About Copilot Memory](https://docs.github.com/en/copilot/concepts/prompting-and-context/copilot-memory) |
| Custom agent sin `tools` = **todas** las herramientas. En MCP, `"tools": ["*"]` = todas | Custom agents configuration, Configure MCP |
| Agentic Workflows: un `.md` con frontmatter se compila a `.lock.yml`. El agente es de solo lectura y escribe mediante *safe outputs*. Hay soporte de OTel con `otel.jsonl` | gh-aw |
| OTel: Copilot CLI, el SDK, VS Code y la app exportan telemetría. El contenido (prompts, tool args) está **desactivado por defecto** y un admin puede imponer la configuración | OpenTelemetry concepts y reference |
| `gh agent-task` está en *public preview* y requiere `gh` ≥ 2.80 | Use cloud agent from the CLI |
| `concurrency` (añadido el 27-11-2026): los nombres de grupo deben ser únicos entre workflows, o un workflow cancela los runs de otro; de ahí `${{ github.workflow }}-${{ github.ref }}`. Existe la opción `queue: max` (hasta 100 pendientes), incompatible con `cancel-in-progress: true`. La `concurrency` a nivel de job también actúa entre runs | Control workflow concurrency |
| Retención: 90 días por defecto para artefactos y logs; 1–90 en repos públicos y 1–400 en privados. El cambio no es retroactivo, y `retention-days` de un artefacto no puede superar el límite del repositorio. Un artefacto borrado no se recupera, y su borrado manual queda en el audit log de la organización como `artifact.destroy` | Managing GitHub Actions settings for a repository, Audit log events |
| Un job saltado por un `if` informa *Success* y no bloquea aunque el check sea obligatorio. Un workflow saltado por filtros de ruta o rama deja el check en *Pending* y bloquea | Control jobs with conditions, Skip workflow runs |
| OIDC: el job necesita `permissions: id-token: write` para pedir el token; no concede escritura sobre ningún recurso | OpenID Connect, OIDC in Azure |
| Cloud agent: solo lo activan usuarios con permiso de escritura; hace push a una única rama (`copilot/…`); no puede aprobar ni fusionar; quien pidió el PR no puede aprobarlo; los workflows esperan a **Approve and run workflows**; una regla puede bloquearlo y el administrador puede añadir a Copilot como *bypass* del ruleset; sesión máxima de 59 minutos en Actions. El firewall solo cubre los procesos lanzados desde la herramienta Bash, no los servidores MCP configurados | Risks and mitigations, Copilot on GitHub, Customize the firewall |
| Custom agents: `disable-model-invocation: true` impide el uso automático (hay que seleccionarlo a mano); `user-invocable: false` impide seleccionarlo (solo acceso programático); `infer` está retirado; `handoffs` de VS Code se ignora en el cloud agent | Custom agents configuration |
| Copilot CLI: `--allow-tool='shell(git)'` aprueba un comando; `--deny-tool` prevalece sobre `--allow-tool` y `--allow-all-tools`; en `git` y `gh` se puede indicar el subcomando, p. ej. `shell(git push)` | About Copilot CLI |
| MCP: la página de referencia se llama ahora *MCP private registry enforcement* y existe además una *enterprise allowlist* por URL, más estricta. La política sigue ligada a la organización o empresa que asigna la licencia | MCP private registry enforcement |
| Agentic Workflows: el frontmatter se incrusta al compilar y exige `gh aw compile` tras cada cambio; el cuerpo Markdown se carga en ejecución. Hay que confirmar los dos ficheros | [gh-aw FAQ](https://github.github.com/gh-aw/reference/faq/) |
| Examen: 120 min, 700 puntos para aprobar, solo en inglés (+30 min a petición). Casi todo GA. En los exámenes de GitHub **no** hay acceso a Learn. Tras una pausa no se puede volver atrás, y no se puede pausar dentro de un set problema-solución | Study guide, Exam duration and experience |

---

## 5. Errores conocidos en los módulos de Learn (no usarlos como respuesta)

- M2: el ejemplo de *Plan Gate* comprueba que exista la plantilla, no que el PR la cumpla.
- M2: el ejemplo de CODEOWNERS pone `*` al final, lo que anula las rutas específicas.
- M2/M6: el JSON de hooks es ilustrativo; el formato real está en el Hooks reference.
- M2: usa `applyTo` en un fichero de agente, pero `applyTo` es de los ficheros `*.instructions.md`.
- M3: el bucle de reintentos termina en verde aunque haya fallado.
- M3: describe el MCP local vía `localhost`, cuando el transporte local habitual es `stdio`.
- Las unidades se contradicen sobre quién crea el PR.
- M3: *"Agents don't execute on your machine"* solo es cierto para el cloud agent y Agentic Workflows, no para el modo agente de VS Code ni Copilot CLI.

---

## 6. Huecos: habilidades sin página oficial clara

Escribirlas con más cuidado y apoyarlas en los mecanismos generales de GitHub:

- **Reintentos, rollback y escalado (D2):** no hay patrón oficial de Copilot. Usar revert del PR, re-run de jobs, environments y hooks con `deny` + motivo.
- **Ciclo de vida de los agentes (D5):** añadir, sustituir o retirar agentes. Usar ficheros `.agent.md` versionados, PRs con CODEOWNERS e historial de git.
- **Responsible AI (D6):** usar la [application card de agentes](https://docs.github.com/en/copilot/responsible-use/agents) y la unidad de M6.

---

## 7. Protocolo para generar una pregunta

1. **Habilidad:** cita la viñeta exacta del study guide en la que se basa.
2. **Respuesta:** verifícala en nivel 1 y ponla en `sources`. Si no se puede verificar, no se publica.
3. **Distractores:** cada uno, plausible y falso por un motivo concreto. Escribe el `rationale` de cada opción.
4. **Formato:** varía el tipo (single, select two, statements, problem-solution, build, match, dropdown, case) y reparte la letra correcta.
5. **Volatilidad:** si el hecho es reciente o está en preview, anota la fecha y vuelve a comprobarlo antes de usarlo.
6. **Restricción:** incluye un *"must not…"* o *"least privilege"* que descarte los atajos. Es el estilo de Microsoft.
