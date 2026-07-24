# claude-laconic

A Claude Code plugin that ships the Laconic output style: blunt, pragmatic answers with a hard length budget and none of the usual AI writing tells.

What it changes:

- Replies lead with the answer or the next action. Context follows only if it changes a decision.
- Hard length limits: simple answers in 1 to 3 sentences, work reports under 150 words, one screen as the ceiling.
- Time estimates assume the agent does the work, not a human. Minutes, not hours.
- Bans the common AI writing tells: em dashes, filler openers, hedged offers, "delve", "robust", "seamless", and the rest.
- Text written on your behalf (issues, PRs, commits, emails) reads as written by you.

The style is applied automatically when the plugin is enabled. Code, quoted errors, and safety warnings stay unstylized, and the length limits govern the reporting, not the work itself.

## Install

```
/plugin marketplace add spenhouet/claude-laconic
/plugin install laconic@claude-laconic
```

## Uninstall

```
/plugin uninstall laconic@claude-laconic
```

## License

MIT
