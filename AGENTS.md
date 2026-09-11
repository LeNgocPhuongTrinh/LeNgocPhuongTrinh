# Profile README engineering rules

Apply `.docs/universal-clean-coding-rules.md`, using only rules relevant to this Markdown and asset repository.

- Keep the profile native to GitHub: Markdown, supported HTML, and local image assets. No frontend, runtime JavaScript, or page-level CSS.
- Keep identity, skills, project descriptions, and destinations selectable and accessible in README.md. Use artwork to support the content.
- Preserve existing useful files. Reuse verified personal artwork; never invent projects, qualifications, screenshots, or statistics.
- Use cream, near-black, and red for authored artwork. Preserve the original colors of real project screenshots.
- Keep asset generation reproducible in `scripts/`; document sources and refresh commands in `.docs/readme-maintenance.md`.
- Verify local links, SVG validity, animation frames/looping and file sizes. Check wide and narrow rendering when a browser is available; distinguish local checks from published GitHub verification.
- Never commit local environments, preview output, credentials, or private reference files.
