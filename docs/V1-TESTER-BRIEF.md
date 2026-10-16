# What we're asking of the V1 relying-party tester

> Draft by the owner instance (Claude Opus 5.5), 2026-10-12, for the author to use when asking someone. It
> implements author decision C (2026-10-10): a human tester, zero unsafe accepts, false rejects allowed only on
> the registered cases. The scenario set is A9.1's mapping. The materials it describes do not exist yet; they are
> due with V1 (4 December 2026).

## The ask, in one paragraph

You'll get a folder of about a dozen digital "receipts" and the public documentation for checking them. For each
receipt, a short note says what someone wants to rely on it for. For example: "Alice says this contract was signed by
both parties before 1 November." Using only the documentation and the verification tool it describes, decide for
each one whether it supports that use, and write a sentence saying why. Nobody from the project will help you, and
that's the point: we're testing whether the documentation works for a careful person who has never heard of us.

## Who fits

- A CS background: comfortable running a command-line tool and reading technical documentation.
- **No** knowledge of attestation, timestamping, blockchains or this project. Expertise would spoil the test.
- Not someone who has discussed Tessera with the author.

## What it takes

- **Time:** about 2–3 hours, in one sitting or two. You set the schedule within a two-week window in December 2026.
- **Equipment:** your own Linux or macOS machine. Installing one tool, offline after download.
- **Output:** a short form with one row per receipt: accept or reject for the stated use, and one sentence on why.
  Optionally, notes on where the documentation confused you. Those notes are as valuable as the answers.
- **No preparation,** and nothing to read beforehand.

## What we measure, and what we don't

- We count **unsafe accepts**: receipts you accept for a use they don't support. The target is zero.
- Some honest receipts are deliberately ones V1 can't confirm. Rejecting those is correct, not a mistake.
- We are testing the documentation, not you. If you're misled, the documentation failed.
- Your answers and notes go into the project's public record under the pseudonym **"Aki Doe"**, not your name, unless you ask to be named.

## Why it matters

Tessera's promise is that anyone can check a receipt decades from now without us. A promise like that is only real if a
stranger, using only what we publish, reaches the right decision. You'd be that stranger.
