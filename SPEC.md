# last30days Skill Specification

## Overview

`last30days` is a Claude Code skill that researches a given topic across Reddit and X (Twitter) using x402 payment proxies. It enforces a strict 30-day recency window, popularity-aware ranking, and produces actionable outputs including best practices, a prompt pack, and a reusable context snippet.

The skill uses **x402 payments** via FluxA Agent Wallet - no API keys required. Cost is ~$0.03 per research (Reddit $0.02 + X $0.01).

## Architecture

The orchestrator (`last30days.py`) coordinates discovery, enrichment, normalization, scoring, deduplication, and rendering. Each concern is isolated in `scripts/lib/`:

- **x402.py**: x402 payment protocol - proxy endpoints and paid request handling
- **env.py**: Load configuration (model preferences) from `~/.config/last30days/.env`
- **dates.py**: Date range calculation and confidence scoring
- **http.py**: stdlib-only HTTP client with retry logic
- **models.py**: Model selection (defaults: gpt-4o, grok-4-1-fast-reasoning)
- **openai_reddit.py**: Reddit search via x402 proxy (OpenAI web_search)
- **xai_x.py**: X search via x402 proxy (xAI x_search)
- **reddit_enrich.py**: Fetch Reddit thread JSON for real engagement metrics
- **normalize.py**: Convert raw API responses to canonical schema
- **score.py**: Compute popularity-aware scores (relevance + recency + engagement)
- **dedupe.py**: Near-duplicate detection via text similarity
- **render.py**: Generate markdown and JSON outputs
- **schema.py**: Type definitions and validation

## x402 Payment Flow

1. Calling agent invokes `fluxa-agent-wallet` skill to get X-Payment tokens
2. Tokens passed to script via `--x-payment-reddit` and `--x-payment-x` arguments
3. Script makes paid requests to x402 proxy endpoints
4. Results processed and returned

**Proxy Endpoints:**
- Reddit (OpenAI): `https://proxy-monetize.fluxapay.xyz/api/4dbb5253-9974-427c-81b1-c52d00bcb28a/web_search`
- X (xAI): `https://proxy-monetize.fluxapay.xyz/api/19dd44d4-216a-4204-97da-1233e5a23685/v1/responses`

## Embedding in Other Skills

Other skills can import the research context in several ways:

### Inline Context Injection
```markdown
## Recent Research Context
!python3 ~/.claude/skills/last30days/scripts/last30days.py "your topic" --emit=context
```

### Read from File
```markdown
## Research Context
!cat ~/.local/share/last30days/out/last30days.context.md
```

### Get Path for Dynamic Loading
```bash
CONTEXT_PATH=$(python3 ~/.claude/skills/last30days/scripts/last30days.py "topic" --emit=path)
cat "$CONTEXT_PATH"
```

### JSON for Programmatic Use
```bash
python3 ~/.claude/skills/last30days/scripts/last30days.py "topic" --emit=json > research.json
```

## CLI Reference

```
python3 ~/.claude/skills/last30days/scripts/last30days.py <topic> [options]

Options:
  --mock                      Use fixtures instead of real API calls
  --emit=MODE                 Output mode: compact|json|md|context|path (default: compact)
  --sources=MODE              Source selection: auto|reddit|x|both (default: auto)
  --x-payment-reddit=TOKEN    X-Payment header for Reddit search
  --x-payment-x=TOKEN         X-Payment header for X search
  --quick                     Faster research with fewer sources
  --deep                      Comprehensive research with more sources
```

## Output Files

All outputs are written to `~/.local/share/last30days/out/`:

- `report.md` - Human-readable full report
- `report.json` - Normalized data with scores
- `last30days.context.md` - Compact reusable snippet for other skills
- `raw_openai.json` - Raw OpenAI API response
- `raw_xai.json` - Raw xAI API response
- `raw_reddit_threads_enriched.json` - Enriched Reddit thread data
