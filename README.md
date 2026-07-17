# Arthur de Souza Molina

Construo sistemas que orquestram modelos de linguagem: roteamento entre provedores,
fallback automático e agentes que decompõem trabalho.

Vim da física — iniciação científica em cosmologia — e trouxe de lá o hábito de medir
antes de afirmar. É por isso que quase tudo aqui tem suíte de teste e número em vez de
adjetivo.

## Projetos

**Orquestração de LLM**

- [model-chain-proxy](https://github.com/asm444/model-chain-proxy): proxy HTTP compatível
  com a API da OpenAI que encadeia 7 provedores (OpenAI, Anthropic, Gemini, Mistral, xAI,
  Ollama, OpenRouter), caindo para o próximo em erro 5xx, 429 ou timeout. Zero dependências
  npm, streaming SSE, `/health` e `/metrics` no formato Prometheus. JavaScript, Node 18+.
- [maestro](https://github.com/asm444/maestro): sistema multi-agente que quebra um objetivo
  em tickets e despacha para 7 agentes de departamento, com verificação de QA no fim.
  TypeScript, testes no runner nativo do Node, sem dependência de runtime.
- [BestModel.ai](https://github.com/asm444/BestModel.ai): ordena os modelos do OpenRouter
  por qualidade real cruzando com os scores Elo do LMArena, em tiers S/A/B. Python puro.

**Computação científica**

- [Algebrow](https://github.com/asm444/Algebrow): sistema de álgebra computacional escrito
  do zero, com resolução passo a passo e geração de LaTeX — 21 módulos de teste cobrindo
  cálculo, EDO, EDP, séries, tensores, grupos, geometria diferencial e Fourier. Motor em
  Python, API em FastAPI, frontend em React.

**Automação e integração**

- [WhatsHeelper](https://github.com/asm444/WhatsHeelper): atendimento por WhatsApp com
  triagem por IA e escalamento para humano sob SLA. 7 serviços orquestrados via Docker
  Compose (PostgreSQL 16, n8n, WAHA, business-engine, chat-simulator, dashboard-api,
  agent-dashboard), npm workspaces, testes unitários, de integração e e2e.
- [down-news](https://github.com/asm444/down-news): monitora 11 serviços (Claude, ChatGPT,
  Gemini, AWS, Azure, Cloudflare e outros) a cada 5 minutos e alerta no Discord. Sem
  servidor: a única infraestrutura é um cron do GitHub Actions.
- [telinha](https://github.com/asm444/smartClaude): cliente, daemon e pipeline de build para
  o display IPS de 240x240 embutido no chassi do notebook Positivo Vision R15M. Python +
  Pillow, protocolo de transporte próprio, testes de hardware isolados por marker do pytest.

**Segurança aplicada**

- [weather-cli](https://github.com/asm444/weather-cli): previsão do tempo no terminal, com
  cache local cifrado em Fernet (AES-128-CBC + HMAC-SHA256) derivado por PBKDF2, escrita
  atômica, permissões 0600/0700 e proteção anti-symlink via `O_NOFOLLOW` + `lstat()`.

Puxando esse último fio: meu próximo projeto é ferramental de segurança, aplicando a
orquestração de agentes acima ao reconhecimento e à análise.

## Stack

Cada item aponta para o código que o prova.

| | |
|---|---|
| Python | [Algebrow](https://github.com/asm444/Algebrow), [telinha](https://github.com/asm444/smartClaude), [down-news](https://github.com/asm444/down-news), [weather-cli](https://github.com/asm444/weather-cli) |
| JavaScript / Node | [model-chain-proxy](https://github.com/asm444/model-chain-proxy) |
| TypeScript | [maestro](https://github.com/asm444/maestro), [WhatsHeelper](https://github.com/asm444/WhatsHeelper) |
| FastAPI + React | [Algebrow](https://github.com/asm444/Algebrow) |
| PostgreSQL + Docker | [WhatsHeelper](https://github.com/asm444/WhatsHeelper) |
| APIs de LLM | [model-chain-proxy](https://github.com/asm444/model-chain-proxy), [maestro](https://github.com/asm444/maestro), [BestModel.ai](https://github.com/asm444/BestModel.ai) |
| LaTeX / Jupyter | [Algebrow](https://github.com/asm444/Algebrow), [Python na Prática](https://github.com/asm444/Python-na-Pratica-Fisica-e-Afins) |

## Também

Ministrei o minicurso [Python na Prática: Física e Afins](https://github.com/asm444/Python-na-Pratica-Fisica-e-Afins)
na XXVI Semana da Física. O material continua aberto.

## Contato

[LinkedIn](https://www.linkedin.com/in/arthur-de-souza-molina/) ·
[arthur.souza.molina@gmail.com](mailto:arthur.souza.molina@gmail.com)
