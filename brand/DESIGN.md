# Visual guide — {{BRAND_NAME}}

Fill this optional guide before creating visuals. It is a plain Markdown specification: no renderer, font service or external lint tool is implied. Values must come from your approved brand references.

## Tokens

| Token | Approved value | Use |
|---|---|---|
| background | {{COLOR_BACKGROUND}} | Main canvas |
| text | {{COLOR_TEXT}} | Primary text |
| accent | {{COLOR_ACCENT}} | Deliberate emphasis |
| muted | {{COLOR_MUTED}} | Secondary information |
| display font | {{FONT_DISPLAY}} | Headings |
| body font | {{FONT_BODY}} | Paragraphs and labels |
| fallback font | {{FONT_FALLBACK}} | Explicit fallback if approved fonts are unavailable |
| spacing scale | {{SPACING_SCALE}} | Layout gaps and padding |
| radius | {{CORNER_RADIUS}} | Corners where relevant |

## Composition and assets

- Approved visual references and why they fit: {{VISUAL_REFERENCES}}
- Logo file, rights, clear space and minimum size, or `no logo supplied`: {{LOGO_ASSET_RULES}}
- Image sources, usage rights and credit requirements: {{IMAGE_ASSET_RULES}}
- Layout, hierarchy and text-density guidance: {{LAYOUT_RULES}}
- Motion, shadows and decorative effects: {{EFFECT_RULES}}
- Supported languages and font/glyph exceptions: {{LANGUAGE_AND_GLYPH_RULES}}

## Visual review

1. **V1 — Traceable choices.** Colors, type and spacing follow the filled tokens; record intentional exceptions.
2. **V2 — Readable in context.** Inspect the actual export at the target screen or print size, including contrast, cropping and overflow. Do not treat a token file as proof of accessibility.
3. **V3 — Assets used as authorized.** Use supplied logos and images under their stated permissions. Do not recreate a missing logo or claim a generated image is a real product screenshot.
4. **V4 — Render checked.** Verify the output, fonts and relevant glyphs in the target format. Record the file reviewed and any fallback; a source file alone is not a visual check.
5. **V5 — Claims match the copy.** Labels, charts and captions need the same evidence as prose.

- Visual owner and date last checked: {{DESIGN_OWNER_AND_DATE}}
