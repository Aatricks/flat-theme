#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE = ROOT / "themes" / "source-theme.json"
PACKAGE_FILE = ROOT / "package.json"
README_FILE = ROOT / "README.md"
THEMES_DIR = ROOT / "themes"


def hex_to_rgba(color: str, alpha: str) -> str:
    return f"{color}{alpha}"


def slugify_variant(name: str) -> str:
    return name.lower().replace(" ", "-").replace("é", "e")


def theme_filename(variant: dict[str, object]) -> str:
    return f"{slugify_variant(variant['name'])}-color-theme.json"


def theme_label(variant: dict[str, object]) -> str:
    label_map = {
        "Flat Gray": "Flat-Theme (Dark)",
        "Flat Light": "Flat-Theme (Light)",
        "Flat Frappé": "Flat-Theme (Frappé)",
    }
    return label_map.get(variant["name"], f"Flat-Theme ({variant['name']})")


def token(foreground: str, font_style: str | None = None, bold: bool = False) -> dict[str, str]:
    settings = {"foreground": foreground}
    styles = []
    if font_style == "italic":
        styles.append("italic")
    if bold:
        styles.append("bold")
    if styles:
        settings["fontStyle"] = " ".join(styles)
    return settings


def token_colors(variant: dict[str, object]) -> list[dict[str, object]]:
    palette = variant["syntax_palette"]
    text = variant["ui"]["text"]
    return [
        {
            "name": "COMMENT",
            "scope": [
                "comment",
                "punctuation.definition.comment",
                "comment.block.documentation",
                "comment.line",
            ],
            "settings": token(palette["comment"], "italic"),
        },
        {
            "name": "VARIABLE",
            "scope": ["variable", "variable.other", "variable.object"],
            "settings": token(text),
        },
        {
            "name": "VARIABLE BUILTIN",
            "scope": [
                "variable.language",
                "variable.language.this",
                "variable.language.self",
                "variable.language.super",
            ],
            "settings": token(palette["builtin"], "italic"),
        },
        {
            "name": "SPECIAL VARIABLE",
            "scope": [
                "variable.other.constant",
                "variable.other.readwrite.instance",
                "variable.other.enummember",
            ],
            "settings": token(palette["special_variable"], "italic"),
        },
        {
            "name": "VARIABLE PARAMETER",
            "scope": [
                "variable.parameter",
                "variable.parameter.function",
                "meta.function.parameters variable",
            ],
            "settings": token(palette["parameter"]),
        },
        {
            "name": "VARIABLE MEMBER/PROPERTY",
            "scope": [
                "variable.other.property",
                "variable.other.member",
                "variable.other.object.property",
                "support.variable.property",
            ],
            "settings": token(palette["member"]),
        },
        {
            "name": "CONSTANT",
            "scope": [
                "constant",
                "constant.numeric",
                "constant.language",
                "constant.character",
                "variable.other.constant",
            ],
            "settings": token(palette["constant"]),
        },
        {
            "name": "STRING",
            "scope": ["string", "string.quoted", "punctuation.definition.string"],
            "settings": token(palette["string"]),
        },
        {
            "name": "STRING ESCAPE/REGEXP",
            "scope": [
                "string.regexp",
                "constant.character.escape",
                "string.template",
                "punctuation.definition.template-expression",
            ],
            "settings": token(palette["regexp"]),
        },
        {
            "name": "MODULE",
            "scope": [
                "entity.name.namespace",
                "entity.name.module",
                "entity.name.package",
                "support.module",
            ],
            "settings": token(palette["module"], "italic"),
        },
        {
            "name": "TYPE",
            "scope": [
                "entity.name.type",
                "entity.name.class",
                "support.type",
                "support.class",
                "entity.other.inherited-class",
            ],
            "settings": token(palette["type"]),
        },
        {
            "name": "TYPE BUILTIN",
            "scope": [
                "support.type.builtin",
                "storage.type.builtin",
                "storage.type.primitive",
            ],
            "settings": token(palette["type"], "italic"),
        },
        {
            "name": "FUNCTION",
            "scope": [
                "entity.name.function",
                "support.function",
                "variable.function",
                "meta.function-call",
            ],
            "settings": token(palette["function"]),
        },
        {
            "name": "ATTRIBUTE/DECORATOR",
            "scope": [
                "entity.name.function.macro",
                "support.function.macro",
                "entity.other.attribute-name",
                "entity.other.attribute-name.html",
                "meta.annotation",
                "storage.type.annotation",
                "punctuation.definition.annotation",
            ],
            "settings": token(palette["attribute"]),
        },
        {
            "name": "KEYWORD",
            "scope": [
                "keyword",
                "keyword.control",
                "keyword.operator.new",
                "keyword.operator.expression",
                "storage.modifier",
                "storage.type.function",
            ],
            "settings": token(palette["keyword"]),
        },
        {
            "name": "OPERATOR",
            "scope": [
                "keyword.operator",
                "keyword.operator.expression",
                "punctuation.accessor",
            ],
            "settings": token(palette["operator"]),
        },
        {
            "name": "PUNCTUATION",
            "scope": [
                "punctuation",
                "punctuation.definition.block",
                "punctuation.definition.parameters",
                "punctuation.section",
                "meta.brace",
            ],
            "settings": token(palette["punctuation"]),
        },
        {
            "name": "JSON KEY",
            "scope": [
                "support.type.property-name.json",
                "source.json meta.structure.dictionary.json support.type.property-name.json",
            ],
            "settings": token(palette["member"]),
        },
        {
            "name": "MARKUP HEADING",
            "scope": ["markup.heading", "entity.name.section"],
            "settings": token(palette["title"], bold=True),
        },
        {
            "name": "MARKUP BOLD",
            "scope": ["markup.bold"],
            "settings": token(palette["parameter"], bold=True),
        },
        {
            "name": "MARKUP ITALIC",
            "scope": ["markup.italic"],
            "settings": token(palette["parameter"], "italic"),
        },
        {
            "name": "MARKUP LINK",
            "scope": ["markup.underline.link"],
            "settings": token(palette["function"], "italic"),
        },
        {
            "name": "MARKUP CODE",
            "scope": ["markup.inline.raw", "markup.raw.block", "markup.fenced_code.block"],
            "settings": token(palette["text_literal"]),
        },
        {
            "name": "DIFF ADDED",
            "scope": ["markup.inserted", "markup.inserted.diff"],
            "settings": token(palette["string"]),
        },
        {
            "name": "DIFF DELETED",
            "scope": ["markup.deleted", "markup.deleted.diff"],
            "settings": token(palette["parameter"]),
        },
        {
            "name": "INVALID",
            "scope": ["invalid", "invalid.illegal"],
            "settings": token(palette["parameter"], bold=True),
        },
    ]


def semantic_token_colors(variant: dict[str, object]) -> dict[str, object]:
    palette = variant["syntax_palette"]
    text = variant["ui"]["text"]
    return {
        "variable": text,
        "parameter": palette["parameter"],
        "property": palette["member"],
        "enumMember": palette["constant"],
        "function": palette["function"],
        "method": palette["function"],
        "macro": palette["attribute"],
        "type": palette["type"],
        "class": palette["type"],
        "interface": {"foreground": palette["type"], "italic": True},
        "enum": palette["type"],
        "typeParameter": palette["type"],
        "namespace": palette["module"],
        "decorator": palette["attribute"],
        "keyword": palette["keyword"],
        "comment": {"foreground": palette["comment"], "italic": True},
        "string": palette["string"],
        "number": palette["constant"],
        "regexp": palette["regexp"],
        "operator": palette["operator"],
        "builtinVariable": {"foreground": palette["builtin"], "italic": True},
    }


def workbench_colors(variant: dict[str, object]) -> dict[str, str]:
    ui = variant["ui"]
    palette = variant["syntax_palette"]
    accent = ui["accent"]
    background = ui["background"]
    chrome = ui["chrome"]
    editor = ui["editor"]
    elevated = ui["elevated"]
    element = ui["element"]
    element_hover = ui["element_hover"]
    element_active = ui["element_active"]
    text = ui["text"]
    muted = ui["muted"]
    placeholder = ui["placeholder"]
    disabled = ui["disabled"]
    badge_text = "#000000" if variant["appearance"] == "dark" else "#263238"
    return {
        "focusBorder": accent,
        "foreground": text,
        "disabledForeground": disabled,
        "contrastActiveBorder": "#00000000",
        "contrastBorder": "#00000000",
        "window.activeBorder": background,
        "window.inactiveBorder": background,
        "activityBar.background": chrome,
        "activityBar.foreground": text,
        "activityBar.inactiveForeground": muted,
        "activityBar.border": background,
        "activityBarBadge.background": accent,
        "activityBarBadge.foreground": badge_text,
        "badge.background": accent,
        "badge.foreground": badge_text,
        "sideBar.background": chrome,
        "sideBar.foreground": text,
        "sideBar.border": background,
        "sideBarSectionHeader.background": chrome,
        "sideBarSectionHeader.foreground": text,
        "sideBarSectionHeader.border": background,
        "sideBarTitle.foreground": text,
        "list.hoverBackground": element_hover,
        "list.hoverForeground": text,
        "list.inactiveSelectionBackground": element_active,
        "list.inactiveSelectionForeground": text,
        "list.activeSelectionBackground": element_active,
        "list.activeSelectionForeground": text,
        "list.focusBackground": element,
        "list.focusForeground": text,
        "list.highlightForeground": accent,
        "titleBar.activeBackground": chrome,
        "titleBar.activeForeground": text,
        "titleBar.inactiveBackground": background,
        "titleBar.inactiveForeground": muted,
        "statusBar.background": chrome,
        "statusBar.foreground": text,
        "statusBar.border": background,
        "statusBar.noFolderBackground": chrome,
        "statusBar.noFolderForeground": text,
        "editorGroup.border": background,
        "editorGroupHeader.tabsBackground": chrome,
        "editorGroupHeader.tabsBorder": background,
        "tab.border": background,
        "tab.activeBackground": element,
        "tab.activeForeground": text,
        "tab.inactiveBackground": chrome,
        "tab.inactiveForeground": muted,
        "tab.hoverBackground": element_hover,
        "tab.hoverForeground": text,
        "tab.activeBorderTop": background,
        "tab.activeModifiedBorder": accent,
        "tab.inactiveModifiedBorder": placeholder,
        "panel.background": chrome,
        "panel.border": background,
        "panelTitle.activeBorder": accent,
        "panelTitle.activeForeground": text,
        "panelTitle.inactiveForeground": muted,
        "editor.background": editor,
        "editor.foreground": text,
        "editorLineNumber.foreground": ui["line_number"],
        "editorLineNumber.activeForeground": ui["active_line_number"],
        "editorCursor.foreground": accent,
        "editor.selectionBackground": hex_to_rgba(accent, "22"),
        "editor.selectionHighlightBackground": hex_to_rgba(accent, "10"),
        "editor.wordHighlightBackground": hex_to_rgba(accent, "10"),
        "editor.wordHighlightStrongBackground": hex_to_rgba(accent, "22"),
        "editor.findMatchBackground": ui["search_match"],
        "editor.findMatchHighlightBackground": hex_to_rgba(accent, "22"),
        "editor.hoverHighlightBackground": hex_to_rgba(accent, "10"),
        "editor.lineHighlightBackground": ui["active_line"],
        "editorWhitespace.foreground": disabled,
        "editorIndentGuide.background1": ui["guide"],
        "editorIndentGuide.activeBackground1": accent,
        "editorGutter.background": editor,
        "editorWidget.background": elevated,
        "editorWidget.border": background,
        "editorSuggestWidget.background": elevated,
        "editorSuggestWidget.border": background,
        "editorSuggestWidget.foreground": text,
        "editorSuggestWidget.selectedBackground": element,
        "editorHoverWidget.background": elevated,
        "editorHoverWidget.border": accent,
        "editorInfo.foreground": palette["member"],
        "editorWarning.foreground": palette["type"],
        "editorError.foreground": palette["parameter"],
        "input.background": editor,
        "input.foreground": text,
        "input.border": background,
        "input.placeholderForeground": placeholder,
        "inputOption.activeBorder": accent,
        "quickInput.background": elevated,
        "quickInput.foreground": text,
        "quickInputList.focusBackground": element,
        "quickInputList.focusForeground": text,
        "pickerGroup.border": background,
        "pickerGroup.foreground": accent,
        "dropdown.background": editor,
        "dropdown.foreground": text,
        "dropdown.border": background,
        "button.background": accent,
        "button.foreground": badge_text,
        "button.hoverBackground": palette["function"],
        "button.secondaryBackground": element,
        "button.secondaryForeground": text,
        "button.secondaryHoverBackground": element_hover,
        "menu.background": elevated,
        "menu.foreground": text,
        "menu.border": background,
        "menu.selectionBackground": element,
        "menu.selectionForeground": text,
        "menubar.selectionBackground": element,
        "menubar.selectionForeground": text,
        "menubar.selectionBorder": background,
        "scrollbar.shadow": "#00000000",
        "scrollbarSlider.background": ui["scrollbar_thumb"],
        "scrollbarSlider.hoverBackground": ui["scrollbar_thumb_hover"],
        "scrollbarSlider.activeBackground": ui["scrollbar_thumb_hover"],
        "minimap.background": editor,
        "terminal.background": editor,
        "terminal.foreground": text,
        "terminal.selectionBackground": hex_to_rgba(accent, "22"),
        "terminal.ansiBlack": variant["terminal"]["black"],
        "terminal.ansiRed": variant["terminal"]["red"],
        "terminal.ansiGreen": variant["terminal"]["green"],
        "terminal.ansiYellow": variant["terminal"]["yellow"],
        "terminal.ansiBlue": variant["terminal"]["blue"],
        "terminal.ansiMagenta": variant["terminal"]["magenta"],
        "terminal.ansiCyan": variant["terminal"]["cyan"],
        "terminal.ansiWhite": variant["terminal"]["white"],
        "terminal.ansiBrightBlack": variant["terminal"]["bright_black"],
        "terminal.ansiBrightRed": variant["terminal"]["red"],
        "terminal.ansiBrightGreen": variant["terminal"]["green"],
        "terminal.ansiBrightYellow": variant["terminal"]["yellow"],
        "terminal.ansiBrightBlue": variant["terminal"]["blue"],
        "terminal.ansiBrightMagenta": variant["terminal"]["magenta"],
        "terminal.ansiBrightCyan": variant["terminal"]["cyan"],
        "terminal.ansiBrightWhite": variant["terminal"]["bright_white"],
        "gitDecoration.addedResourceForeground": palette["string"],
        "gitDecoration.modifiedResourceForeground": palette["type"],
        "gitDecoration.deletedResourceForeground": palette["parameter"],
        "gitDecoration.untrackedResourceForeground": palette["string"],
        "gitDecoration.conflictingResourceForeground": palette["type"],
        "gitDecoration.ignoredResourceForeground": muted,
        "settings.headerForeground": text,
        "settings.headerBorder": background,
        "settings.settingsHeaderHoverForeground": text,
        "settings.rowHoverBackground": element_hover,
        "settings.focusedRowBackground": element,
        "settings.focusedRowBorder": accent,
        "settings.dropdownBackground": editor,
        "settings.dropdownForeground": text,
        "settings.dropdownBorder": background,
        "settings.checkboxBackground": editor,
        "settings.checkboxForeground": text,
        "settings.checkboxBorder": background,
        "settings.numberInputBackground": editor,
        "settings.numberInputForeground": text,
        "settings.numberInputBorder": background,
        "settings.textInputBackground": editor,
        "settings.textInputForeground": text,
        "settings.textInputBorder": background,
        "settings.modifiedItemIndicator": accent,
    }


def render_theme(variant: dict[str, object]) -> str:
    theme = {
        "name": theme_label(variant),
        "type": "dark" if variant["appearance"] == "dark" else "light",
        "semanticClass": f"theme.{slugify_variant(variant['name'])}",
        "semanticHighlighting": True,
        "colors": workbench_colors(variant),
        "tokenColors": token_colors(variant),
        "semanticTokenColors": semantic_token_colors(variant),
    }
    return json.dumps(theme, indent=2) + "\n"


def render_package(source: dict[str, object]) -> str:
    package = {
        "name": "flat-theme",
        "displayName": "Flat-Theme",
        "publisher": "Aatricks",
        "version": "0.1.2",
        "engines": {"vscode": "^1.60.0"},
        "categories": ["Themes"],
        "contributes": {
            "themes": [
                {
                    "label": theme_label(variant),
                    "uiTheme": "vs-dark" if variant["appearance"] == "dark" else "vs",
                    "path": f"./themes/{theme_filename(variant)}",
                }
                for variant in source["variants"]
            ]
        },
        "repository": {
            "type": "git",
            "url": "https://github.com/Aatricks/flat-theme",
        },
        "bugs": {"url": "https://github.com/Aatricks/flat-theme/issues"},
        "homepage": "https://github.com/Aatricks/flat-theme#readme",
        "icon": "assets/icon.png",
    }
    return json.dumps(package, indent=2) + "\n"


def render_readme(source: dict[str, object]) -> str:
    lines = [
        "# Flat-Theme",
        "",
        "Flat-Theme is a minimal Visual Studio Code theme collection generated from a standalone source palette in this repository.",
        "",
        "## Variants",
        "",
    ]
    for variant in source["variants"]:
        lines.append(f"- `{theme_label(variant)}` ({variant['appearance']})")
        lines.append(
            f"  Uses background `{variant['readme_palette']['Background']}` with accent `{variant['readme_palette']['Accent']}` while keeping the flat, low-border UI structure."
        )
    lines.extend(
        [
            "",
            "## Development",
            "",
            "- Edit `themes/source-theme.json` to change palettes or variant definitions.",
            "- Rebuild generated files with `python3 scripts/build_themes.py`.",
            "- Verify generated files are current with `python3 scripts/build_themes.py --check`.",
            "",
            "The files in `themes/`, `package.json`, and this README are generated outputs and should not be hand-maintained.",
            "",
            "## License",
            "",
            "MIT License. See [LICENSE](./LICENSE) for details.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def relative_luminance(color: str) -> float:
    color = color.lstrip("#")
    values = [int(color[i : i + 2], 16) / 255 for i in (0, 2, 4)]

    def convert(channel: float) -> float:
        if channel <= 0.04045:
            return channel / 12.92
        return ((channel + 0.055) / 1.055) ** 2.4

    r, g, b = [convert(value) for value in values]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(color_a: str, color_b: str) -> float:
    a = relative_luminance(color_a)
    b = relative_luminance(color_b)
    high, low = sorted((a, b), reverse=True)
    return (high + 0.05) / (low + 0.05)


def validate_theme(variant: dict[str, object], theme: dict[str, object]) -> list[str]:
    colors = theme["colors"]
    editor_background = colors["editor.background"]
    terminal_background = colors["terminal.background"]
    errors = []
    checks = [
        ("editor.foreground", colors["editor.foreground"], editor_background, 7.0),
        ("editorLineNumber.foreground", colors["editorLineNumber.foreground"], editor_background, 4.0),
        ("terminal.foreground", colors["terminal.foreground"], terminal_background, 4.5),
    ]
    for name, foreground, background, minimum in checks:
        value = contrast(foreground, background)
        if value < minimum:
            errors.append(
                f"{variant['name']}: {name} contrast {value:.2f} is below {minimum:.1f}"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    source = json.loads(SOURCE_FILE.read_text())
    themes = {theme_filename(variant): render_theme(variant) for variant in source["variants"]}
    package = render_package(source)
    readme = render_readme(source)

    errors = []
    for variant in source["variants"]:
        errors.extend(validate_theme(variant, json.loads(themes[theme_filename(variant)])))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    if args.check:
        stale = []
        if not PACKAGE_FILE.exists() or PACKAGE_FILE.read_text() != package:
            stale.append("package.json")
        if not README_FILE.exists() or README_FILE.read_text() != readme:
            stale.append("README.md")
        existing_files = {path.name for path in THEMES_DIR.glob("*-color-theme.json")}
        for name, content in themes.items():
            path = THEMES_DIR / name
            if not path.exists() or path.read_text() != content:
                stale.append(str(path.relative_to(ROOT)))
        for extra in sorted(existing_files - set(themes)):
            stale.append(str((THEMES_DIR / extra).relative_to(ROOT)))
        if stale:
            print("Generated files are stale:", ", ".join(stale), file=sys.stderr)
            return 1
        return 0

    THEMES_DIR.mkdir(exist_ok=True)
    for existing in THEMES_DIR.glob("*-color-theme.json"):
        if existing.name not in themes:
            existing.unlink()
    for name, content in themes.items():
        (THEMES_DIR / name).write_text(content)
    PACKAGE_FILE.write_text(package)
    README_FILE.write_text(readme)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
