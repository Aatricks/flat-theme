# Flat-Theme

Flat-Theme is a minimal, flat color theme for Visual Studio Code that ships both a dark (`Flat-Theme (Dark)`) and a light (`Flat-Theme (Light)`) variant.

This extension provides two themes located in the `themes/` folder:

- `flat-theme-gray-color-theme.json` — Flat-Theme (Dark)
- `flat-theme-light-color-theme.json` — Flat-Theme (Light)

## Features

- Low-contrast, flat colors designed for focus and readability
- Carefully chosen syntax colors for clarity across multiple languages
- Both dark and light variants so you can switch depending on ambient lighting

## Installation

There are a few ways to install this theme:

1. Install from the VS Code Marketplace (if published).
2. Install from the VSIX file (build locally then install).
3. Use the repository locally for development and move it into `~/.vscode/extensions`.

## Usage

After installation or when running the extension host:

1. Open the Command Palette (Ctrl+Shift+P / Cmd+Shift+P).
2. Type `Preferences: Color Theme` and select `Flat-Theme (Dark)` or `Flat-Theme (Light)`.

## Development

If you want to modify the theme or add variants:

1. Edit the JSON color files in the `themes/` folder.
2. Run `npm install` (if there are dev dependencies) and `npm run` scripts if present.
3. Use the VS Code Extension Development Host (F5) to preview changes.

Tip: Use the `Developer: Inspect Editor Tokens and Scopes` command in the Command Palette to verify which token scopes your colors apply to.

## Contributing

Contributions are welcome. A suggested workflow:

1. Fork the repository
2. Create a branch for your change
3. Update or add a theme file in `themes/`
4. Open a pull request with a description of your changes

Please keep changes small and focused when possible and include screenshots for visual changes.

## License

This project is published under MIT License. See the [LICENSE](./LICENSE) file for details.

## Credits

Created Aatricks. Thanks to the VS Code theming community for examples and guidance.

