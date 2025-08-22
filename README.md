# AI IDEs & Coding Agents Tracker

A public, extensible catalog to track AI IDEs and AI coding agents with hyperlinks, categories, and notes.

## Features
- Simple YAML catalog in `configs/ai_ides.yaml`
- CLI to list, add, and update the README section

## AI IDEs and AI Coding Agents
<!-- BEGIN: AI_IDE_LIST -->
1. [Emergen.ch](https://emergen.ch) — AI IDE
2. [Code Rabbit](https://coderabbit.ai) — Code Review / Assistant
3. [Factory.ai](https://factory.ai) — AI IDE
4. [Wrapifai.com](https://wrapifai.com) — No-Code
5. [Cursor](https://cursor.so) — AI IDE
6. [bolt.new](https://bolt.new) — Builder / No-Code
7. [lovable](https://lovable.so) — Builder / No-Code
8. [windsurf](https://windsurf.ai) — AI IDE / Agent
9. [GitHub Copilot](https://github.com/features/copilot) — AI Assistant
10. [Replit AI](https://replit.com) — AI IDE / Agent
11. [v0 from Vercel](https://v0.dev) — UI Builder
12. [MarsX](https://marsx.dev) — Builder
13. [Devin](https://devin.ai) — AI Agent
14. [Webdraw](https://webdraw.io) — UI Builder
15. [Tempo Labs](https://tempolabs.io) — Full-Stack Builder
16. [Trae](https://trae.ai) — AI IDE
17. [Cline](https://cline.dev) — VSCode Extension
18. [Databutton](https://databutton.com) — No-Code
19. [Continue.dev](https://continue.dev) — VSCode Extension
20. [Base44](https://base44.io) — Builder
21. [Qodo](https://qodo.dev) — Assistant
22. [Amazon Q](https://aws.amazon.com/amazonq) — Assistant
23. [Caffeine AI](https://caffeine.dev) — Assistant
24. [Aider](https://aider.chat) — Terminal Agent
25. [Pear AI](https://pearai.dev) — AI Assistant
26. [GitHub Spark](https://github.com/features/spark) — Assistant (Early)
27. [IDX](https://idx.dev) — Cloud IDE
28. [Tabnine](https://tabnine.com) — AI Assistant
29. [Amazon CodeWhisperer](https://aws.amazon.com/codewhisperer) — AI Assistant
30. [JetBrains](https://www.jetbrains.com) — IDE Suite
31. [ChatGPT Code Canvas](https://openai.com) — AI Assistant
32. [Grok from Elon and X AI](https://x.ai) — AI Assistant
33. [Haystack](https://haystack.tools) — IDE / Canvas
34. [CreateXyz](https://create.xyz) — Builder
35. [Stitch from Google](https://stitch.google) — UI Builder
36. [Canva Code](https://www.canva.com) — UI Builder
37. [Augment Code](https://augmentcode.dev) — IDE Plugin
38. [Mocha](https://buildwithmocha.com) — Builder
39. [Clark](https://clark.tools) — Enterprise Builder
40. [OpenAI Codex](https://openai.com) — AI Model / Assistant
41. [Jules from Google](https://jules.google) — Assistant
42. [Claude Code](https://github.com/anthropics/claude-code) — Agent / Terminal

<!-- END: AI_IDE_LIST -->

## Project Structure
- `assets/` static assets
- `configs/` configuration and the main catalog YAML
- `data/` datasets or exports (excluded from git)
- `src/` Python source (CLI and utilities)
  - `tests/` basic tests
  - `utilities/` helpers
  - `pipelines/` reserved for future automations
  - `mcp/` reserved for FastMCP integrations

## Quickstart (uv)
```bash
# Create and activate venv
uv venv
source .venv/bin/activate

# Install deps
uv pip install -r requirements.txt

# Use CLI
python -m src.cli list
python -m src.cli generate
python -m src.cli add --name "YourTool" --url "https://example.com" --category "AI IDE" --notes "Optional"
```

## Contributing
- Edit `configs/ai_ides.yaml` or use the CLI `add` command
- Keep entries minimal: name, url, optional category and notes
- Run `python -m src.cli generate` to refresh the README section

## License
MIT — see `LICENSE`.
