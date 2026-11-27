# AGENTS.md

Instructions for AI coding agents that work in this repository. Keep this file
short. Put the reason next to each rule.

## Project

compressor-log is a multi-tenant app, hosted or self-hosted, that tracks high-pressure breathing-gas equipment: compressors, booster pumps, and nitrox membrane systems. It records hour meters, filtration stacks, filter cartridges, maintenance, fills, and the cost of each fill. An organization that operates 2 to 10 compressors is the typical user.

## Run and test

```bash
# start the app
docker compose up --build --wait
# run the tests
docker compose run --rm api pytest && docker compose run --rm web pnpm test
```

## Rules

- Make the smallest change that solves the problem. A small change is easy to review
  and easy to undo.
- Write a test for each change in behavior. The test is the proof that it works.
- Never commit a secret. Read secrets from environment variables. `.env.example` lists
  the names.
- Open a pull request for each change. Do not push to the default branch.
- Before an action that deletes data or costs money, state the risk and ask.

## Workflow

This repository uses `sdlc-crew`. Start a change with `/sdlc-crew "<what you want>"`.
The config is in `.sdlc-crew.yaml`.
