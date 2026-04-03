# Flat-Theme

Flat-Theme is a minimal Visual Studio Code theme collection generated from a standalone source palette in this repository.

## Variants

- `Flat-Theme (Dark)` (dark)
  Uses background `#202124` with accent `#94E2D5` while keeping the flat, low-border UI structure.
- `Flat-Theme (Light)` (light)
  Uses background `#FAFBFC` with accent `#80CBC4` while keeping the flat, low-border UI structure.
- `Flat-Theme (Frappé)` (dark)
  Uses background `#303446` with accent `#ca9ee6` while keeping the flat, low-border UI structure.

## Development

- Edit `themes/source-theme.json` to change palettes or variant definitions.
- Rebuild generated files with `python3 scripts/build_themes.py`.
- Verify generated files are current with `python3 scripts/build_themes.py --check`.

The files in `themes/`, `package.json`, and this README are generated outputs and should not be hand-maintained.

## License

MIT License. See [LICENSE](./LICENSE) for details.
