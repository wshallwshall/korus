# Fluent 2 flowchart design standard

<a id="tldrbluf"></a>

Use version 1.0.0 of the owner's Fluent 2 Flowchart Design Spec for flowcharts. It defines
design tokens, nine shapes, three status variants, connectors, dark-mode overrides, and a component interface.

The contrast audit found 18 color pairings below the thresholds promised in section 7. Check
those findings before using the palette in a component.

The [contrast audit](#contrast-audit-against-section-7) names the affected colors. The
[specification](#the-specification-as-supplied) preserves the owner's source text and token values.

---

## Where this came from

| Field | Value |
|---|---|
| Title | Fluent2 Flowchart Design Spec |
| Version | 1.0.0 |
| Status in the source | Handoff-Ready |
| Supplied by | the project owner |
| Supplied on | 2026-08-31 |
| Stored here on | 2026-08-31 |

The supplied specification remains unchanged apart from heading depth. The audit and guidance
around it have been edited for clarity.

## What changed between the supplied file and the copy below

| Change | Why |
|---|---|
| Every heading dropped one level, so `#` became `##` | One H1 per page, which is what the site title is built from |
| Nothing else | Tables, token names, token values and prose are byte-for-byte the source |

All 473 lines of the supplied file were ASCII. The scan found no emoji or other non-ASCII
characters, so none were removed.

Sections 4.1, 4.2, and 4.3 name the status icons: `CheckmarkCircle16Filled`, `Warning16Filled`,
and `DismissCircle16Filled`. Use those Fluent icon tokens when implementing the states.

## Contrast audit against section 7

The ratios were calculated on 2026-08-31 using the WCAG relative-luminance formula and the
spec's hex values. Each row names the foreground and background that produced its result.

### What section 7 promises, and what that pulls in

Section 7 requires 4.5:1 contrast for normal text and 3:1 for text at least 18pt. Its contrast
sentence does not mention graphics.

The same section requires WCAG AA compliance. WCAG 2.1 AA includes SC 1.4.11 Non-text Contrast,
which requires 3:1 for graphics such as borders that convey meaning.

WCAG treats text as large at 18pt (24px), or 14pt bold (18.66px). This spec's largest label
token is `fontSizeBase400` at 16px, so none of its labels qualify.

Every label therefore needs 4.5:1 contrast. No shape can use section 7's lower 3:1 text
threshold with the supplied label sizes.

### Light palette, text at 4.5 to 1

| Foreground | Background | Ratio | Verdict |
|---|---|---|---|
| `colorPaletteGreenForeground2` `#107c10` | `colorPaletteGreenBackground2` `#e6f4ea` | 4.73 | PASS |
| `colorPaletteYellowForeground2` `#835b00` | `colorPaletteYellowBackground2` `#fff4ce` | 5.51 | PASS |
| `colorPaletteRedForeground2` `#c50f1f` | `colorPaletteRedBackground2` `#fde7e9` | 5.14 | PASS |
| `colorNeutralForeground1` `#242424` | `colorNeutralBackground1` `#ffffff` | 15.52 | PASS |
| `colorNeutralForeground1` `#242424` | `colorNeutralBackground2` `#f5f5f5` | 14.24 | PASS |
| `colorNeutralForeground2` `#616161` | `colorNeutralBackground1` `#ffffff` | 6.19 | PASS |
| `colorNeutralForeground2` `#616161` | `colorNeutralBackground2` `#f5f5f5` | 5.68 | PASS |
| `colorNeutralForegroundOnBrand` `#ffffff` | `colorBrandBackground` `#0f6cbd` | 5.38 | PASS |
| `colorNeutralForegroundOnBrand` `#ffffff` | `colorBrandBackgroundHover` `#115ea3` | 6.66 | PASS |
| `colorNeutralForegroundDisabled` `#bdbdbd` | `colorNeutralBackground2` `#f5f5f5` | 1.72 | Fails the number, exempt |

WCAG 1.4.3 exempts text in inactive controls. The disabled row fails the numerical threshold
but is not one of the 18 counted failures.

### Light palette, the 80 percent sublabel

Sections 4.1, 4.2, and 4.3 set status sublabels to 80 percent opacity. Blending the foreground
with its fill changes the effective color; the 12px text still requires 4.5:1.

| Effective foreground | Background | Ratio | Verdict |
|---|---|---|---|
| `colorPaletteGreenForeground2` at 80% = `#3b943c` | `colorPaletteGreenBackground2` `#e6f4ea` | 3.37 | FAIL |
| `colorPaletteYellowForeground2` at 80% = `#9c7a29` | `colorPaletteYellowBackground2` `#fff4ce` | 3.65 | FAIL |
| `colorPaletteRedForeground2` at 80% = `#d03a47` | `colorPaletteRedBackground2` `#fde7e9` | 4.06 | FAIL |

### Light palette, graphics at 3 to 1

| Stroke | Surface behind it | Ratio | Verdict |
|---|---|---|---|
| `colorNeutralStroke1` `#d1d1d1` | `colorNeutralBackground1` `#ffffff` | 1.53 | FAIL |
| `colorNeutralStroke1` `#d1d1d1` | `colorNeutralBackground2` `#f5f5f5` | 1.40 | FAIL |
| `colorNeutralStroke2` `#e0e0e0` | `colorNeutralBackground1` `#ffffff` | 1.32 | FAIL |
| `colorNeutralStroke2` `#e0e0e0` | `colorNeutralBackground2` `#f5f5f5` | 1.21 | FAIL |
| `colorBrandStroke1` `#0f6cbd` | `colorNeutralBackground1` `#ffffff` | 5.38 | PASS |
| `colorPaletteGreenBorderActive` `#107c10` | `colorNeutralBackground1` `#ffffff` | 5.37 | PASS |
| `colorPaletteYellowBorderActive` `#835b00` | `colorNeutralBackground1` `#ffffff` | 6.07 | PASS |
| `colorPaletteRedBorderActive` `#c50f1f` | `colorNeutralBackground1` `#ffffff` | 6.07 | PASS |
| `colorPaletteGreenBorderActive` `#107c10` | `colorPaletteGreenBackground2` `#e6f4ea` | 4.73 | PASS |
| `colorPaletteYellowBorderActive` `#835b00` | `colorPaletteYellowBackground2` `#fff4ce` | 5.51 | PASS |
| `colorPaletteRedBorderActive` `#c50f1f` | `colorPaletteRedBackground2` `#fde7e9` | 5.14 | PASS |

Section 2 fills a resting shape with `colorNeutralBackground1` and uses a 1px
`colorNeutralStroke1` border. On a `#ffffff` canvas, that border is the only visible boundary, at 1.53:1.

### Dark palette, text at 4.5 to 1

| Foreground | Background | Ratio | Verdict |
|---|---|---|---|
| `colorPaletteGreenForeground2` `#54b054` | `colorPaletteGreenBackground2` `#052505` | 6.06 | PASS |
| `colorPaletteYellowForeground2` `#fce100` | `colorPaletteYellowBackground2` `#2c2200` | 11.91 | PASS |
| `colorPaletteRedForeground2` `#f1707b` | `colorPaletteRedBackground2` `#3b0509` | 6.06 | PASS |
| `colorNeutralForeground1` `#ffffff` | `colorNeutralBackground1` `#1f1f1f` | 16.48 | PASS |
| `colorNeutralForeground1` `#ffffff` | `colorNeutralBackground2` `#2c2c2c` | 13.97 | PASS |
| `colorNeutralForeground2` `#ababab` | `colorNeutralBackground1` `#1f1f1f` | 7.18 | PASS |
| `colorNeutralForeground2` `#ababab` | `colorNeutralBackground2` `#2c2c2c` | 6.08 | PASS |
| `colorNeutralForegroundOnBrand` `#000000` | `colorBrandBackground` `#479ef5` | 7.48 | PASS |
| `colorNeutralForegroundOnBrand` `#000000` | `colorBrandBackgroundHover` `#115ea3` | 3.15 | FAIL |
| `colorNeutralForegroundDisabled` `#bdbdbd` | `colorNeutralBackground2` `#2c2c2c` | 7.43 | PASS |

### Dark palette, the 80 percent sublabel

| Effective foreground | Background | Ratio | Verdict |
|---|---|---|---|
| `colorPaletteGreenForeground2` at 80% = `#449444` | `colorPaletteGreenBackground2` `#052505` | 4.37 | FAIL |
| `colorPaletteYellowForeground2` at 80% = `#d2bb00` | `colorPaletteYellowBackground2` `#2c2200` | 8.12 | PASS |
| `colorPaletteRedForeground2` at 80% = `#cd5b64` | `colorPaletteRedBackground2` `#3b0509` | 4.35 | FAIL |

### Dark palette, graphics at 3 to 1

| Stroke | Surface behind it | Ratio | Verdict |
|---|---|---|---|
| `colorNeutralStroke1` `#404040` | `colorNeutralBackground1` `#1f1f1f` | 1.59 | FAIL |
| `colorNeutralStroke1` `#404040` | `colorNeutralBackground2` `#2c2c2c` | 1.35 | FAIL |
| `colorNeutralStroke2` `#333333` | `colorNeutralBackground1` `#1f1f1f` | 1.30 | FAIL |
| `colorNeutralStroke2` `#333333` | `colorNeutralBackground2` `#2c2c2c` | 1.11 | FAIL |
| `colorBrandStroke1` `#479ef5` | `colorNeutralBackground1` `#1f1f1f` | 5.87 | PASS |
| `colorPaletteGreenBorderActive` `#107c10` | `colorNeutralBackground1` `#1f1f1f` | 3.07 | PASS |
| `colorPaletteYellowBorderActive` `#835b00` | `colorNeutralBackground1` `#1f1f1f` | 2.72 | FAIL |
| `colorPaletteRedBorderActive` `#c50f1f` | `colorNeutralBackground1` `#1f1f1f` | 2.72 | FAIL |
| `colorPaletteGreenBorderActive` `#107c10` | `colorPaletteGreenBackground2` `#052505` | 3.07 | PASS |
| `colorPaletteYellowBorderActive` `#835b00` | `colorPaletteYellowBackground2` `#2c2200` | 2.59 | FAIL |
| `colorPaletteRedBorderActive` `#c50f1f` | `colorPaletteRedBackground2` `#3b0509` | 2.86 | FAIL |

### Five tokens have no dark override, and two failures follow from that

Section 6 lists 15 override rows. Five tokens from section 1 have no override and therefore
keep their light values in a dark theme built from this table:

| Token | Value it keeps in dark mode |
|---|---|
| `colorBrandBackgroundHover` | `#115ea3` |
| `colorPaletteGreenBorderActive` | `#107c10` |
| `colorPaletteRedBorderActive` | `#c50f1f` |
| `colorPaletteYellowBorderActive` | `#835b00` |
| `colorNeutralForegroundDisabled` | `#bdbdbd` |

In dark mode, `colorNeutralForegroundOnBrand` changes to `#000000`, while
`colorBrandBackgroundHover` stays `#115ea3`. That produces 3.15:1 contrast for a hovered brand label.

The three status borders also retain light-theme values against dark fills. Two fall below
3:1, as the table shows.

### The findings, and what to do about them

Keep the supplied token values unchanged in the specification below. Apply any repairs in
your component and record the difference from the source.

| Finding | Where | Count |
|---|---|---|
| The 80 percent sublabel drops below 4.5:1 | Sections 4.1, 4.2 and 4.3, both palettes | 5 |
| Black label on the unoverridden brand hover fill | Section 6 with section 2 | 1 |
| A neutral stroke never reaches 3:1 against either surface | Sections 1.1 and 6 | 8 |
| A status border below 3:1 on a dark surface | The section 6 gap | 4 |

The table totals 18 failing pairings. Before shipping a component, make these changes:

1. Use full opacity or a color with enough contrast for each status sublabel. Five of the six supplied 80 percent pairings fail.
2. Add a dark override for `colorBrandBackgroundHover`, or keep its label white in dark mode.
3. Give shapes a visible boundary with the section 1.4 shadows or a fill that differs from the canvas.
4. Add dark overrides for all three status border tokens; section 6 currently overrides only their matching foregrounds.

The section 7 focus ring passes in both themes. `colorBrandStroke1` against
`colorNeutralBackground1` measures 5.38:1 in light mode and 5.87:1 in dark mode.

## The superseded Fluent 2 handoff

An earlier document from the owner mapped Fluent 2 alias tokens to diagram roles. It used
the same token names but differed in several values.

That earlier document is superseded. Keep it as a record rather than using it as the current palette.

| Token | Earlier value | This spec | Effect |
|---|---|---|---|
| `colorBrandBackground` | `#0078D4` | `#0f6cbd` | A white label goes from 4.53:1 to 5.38:1 |
| `colorNeutralForeground2` | `#737373` | `#616161` | A secondary label goes from 4.46:1 to 6.19:1 |
| `colorNeutralBackground1` | `#F8F8F8` | `#ffffff` | The default surface is now pure white |

The earlier `#737373` on `#F8F8F8` pairing measured 4.46:1, below its promised 4.5:1. Against
`#f5f5f5`, it measured 4.35:1.

This spec uses the darker `#616161`, which passes on every background assigned to it. That
resolves the older document's secondary-text failure.

Only those three earlier values were available to the session that made the first comparison.
It could not assess changes to the rest of that token list.

### Seven more failing pairings from the earlier palettes

Another session received the full material on 2026-08-31. It included a Microsoft Fluent hex
palette and role table, plus the Fluent 2 alias-token document, for restyling a working-model diagram.

Both palettes assign tokens to roles and require WCAG AA text contrast at 4.5:1. Seven
assignments failed the applicable thresholds:

| Foreground | Background | Ratio | Target | Assigned role |
|---|---|---|---|---|
| Gray 70 `#737373` | Brand Tint 20 `#C7E0F4` | **3.48** | 4.5 | secondary text |
| Gray 70 `#737373` | Gray 8 `#F2F2F2` | **4.24** | 4.5 | secondary text |
| Gray 70 `#737373` | Gray 32 `#C8C8C8` | **2.83** | 4.5 | secondary text on a panel |
| Gray 100 `#1F1F1F` | Brand `#0078D4` | **3.64** | 4.5 | text on every process step |
| White `#FFFFFF` | Shared Orange fg `#B8860B` | **3.25** | 4.5 | the obvious repair for a pale fill |
| Gray 36 `#C2C2C2` | Gray 4 `#F8F8F8` | **1.68** | 3.0 | optional-path strokes |
| Gray 20 `#DEDEDE` | Gray 4 `#F8F8F8` | **1.27** | 3.0 | note connectors |

The final two rows are graphics. Their 3:1 target comes from SC 1.4.11, as with the stroke
rows in the audit above.

Four corrections held when the palettes were applied:

- Secondary text goes one step darker than the palette assigns.
- Hairline strokes go to a mid grey near 3 to 1, not the near-invisible light greys.
- Light greys serve as panel fills, never as a surface behind text.
- Text on a brand-filled shape takes the on-brand token, never the neutral foreground.

The check measured every pairing used in the diagram in both themes, then took the lowest
ratio. Sampling only selected pairings could miss the failing combination.

An earlier report omitted backgrounds from these seven figures. Four ratios could not be
reproduced. Recalculation confirmed the contrast problem but replaced the figures; each row now names both colors.

## Implementing the dark palette in CSS

Define every light-palette token on `:root`. Override values under both dark selectors; never
put a color's only definition inside a theme or media block.

The viewer has three states: explicit light, explicit dark, and the system default. An
explicit choice sets `data-theme` on the root element; the system setting leaves it unset.

```css
:root {
  /* The complete light palette from section 1.1. Every token gets its value here. */
  --colorNeutralBackground1: #ffffff;
  --colorNeutralBackground2: #f5f5f5;
  --colorNeutralStroke1: #d1d1d1;
  --colorNeutralStroke2: #e0e0e0;
  --colorBrandBackground: #0f6cbd;
  --colorBrandBackgroundHover: #115ea3;
  --colorBrandStroke1: #0f6cbd;
  --colorPaletteGreenBackground2: #e6f4ea;
  --colorPaletteGreenForeground2: #107c10;
  --colorPaletteGreenBorderActive: #107c10;
  --colorPaletteRedBackground2: #fde7e9;
  --colorPaletteRedForeground2: #c50f1f;
  --colorPaletteRedBorderActive: #c50f1f;
  --colorPaletteYellowBackground2: #fff4ce;
  --colorPaletteYellowForeground2: #835b00;
  --colorPaletteYellowBorderActive: #835b00;
  --colorNeutralForeground1: #242424;
  --colorNeutralForeground2: #616161;
  --colorNeutralForegroundOnBrand: #ffffff;
  --colorNeutralForegroundDisabled: #bdbdbd;
}

/* System dark, unless the viewer has explicitly chosen light. Values only. */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --colorNeutralBackground1: #1f1f1f;
    --colorNeutralBackground2: #2c2c2c;
    --colorNeutralStroke1: #404040;
    --colorNeutralStroke2: #333333;
    --colorNeutralForeground1: #ffffff;
    --colorNeutralForeground2: #ababab;
    --colorBrandBackground: #479ef5;
    --colorBrandStroke1: #479ef5;
    --colorNeutralForegroundOnBrand: #000000;
    --colorPaletteGreenBackground2: #052505;
    --colorPaletteGreenForeground2: #54b054;
    --colorPaletteYellowBackground2: #2c2200;
    --colorPaletteYellowForeground2: #fce100;
    --colorPaletteRedBackground2: #3b0509;
    --colorPaletteRedForeground2: #f1707b;
  }
}

/* The explicit dark choice, so a toggle wins in both directions. The same values again. */
:root[data-theme="dark"] {
  --colorNeutralBackground1: #1f1f1f;
  --colorNeutralBackground2: #2c2c2c;
  --colorNeutralStroke1: #404040;
  --colorNeutralStroke2: #333333;
  --colorNeutralForeground1: #ffffff;
  --colorNeutralForeground2: #ababab;
  --colorBrandBackground: #479ef5;
  --colorBrandStroke1: #479ef5;
  --colorNeutralForegroundOnBrand: #000000;
  --colorPaletteGreenBackground2: #052505;
  --colorPaletteGreenForeground2: #54b054;
  --colorPaletteYellowBackground2: #2c2200;
  --colorPaletteYellowForeground2: #fce100;
  --colorPaletteRedBackground2: #3b0509;
  --colorPaletteRedForeground2: #f1707b;
}
```

The five tokens without overrides retain their `:root` values, as measured in the audit.
Adding overrides changes those supplied values but uses the same CSS structure.

Set the canvas color explicitly from `--colorNeutralBackground1`. A transparent canvas takes
the host page's color, which may differ from the background used in the audit.

---

## The specification, as supplied

## Fluent2 Flowchart Design Spec
**Version:** 1.0.0
**Status:** Handoff-Ready
**Target:** Claude Code / Component Implementation

---

### 1. Design Tokens

#### 1.1 Color Tokens

| Token | Value | Usage |
|---|---|---|
| `colorNeutralBackground1` | `#ffffff` | Default shape fill |
| `colorNeutralBackground2` | `#f5f5f5` | Alternate / hover fill |
| `colorNeutralStroke1` | `#d1d1d1` | Default shape border |
| `colorNeutralStroke2` | `#e0e0e0` | Subtle border variant |
| `colorBrandBackground` | `#0f6cbd` | Brand / primary fill |
| `colorBrandBackgroundHover` | `#115ea3` | Brand hover fill |
| `colorBrandStroke1` | `#0f6cbd` | Brand border |
| `colorPaletteGreenBackground2` | `#e6f4ea` | Checks-pass success fill |
| `colorPaletteGreenForeground2` | `#107c10` | Checks-pass success icon/text |
| `colorPaletteGreenBorderActive` | `#107c10` | Checks-pass success border |
| `colorPaletteRedBackground2` | `#fde7e9` | Checks-fail / error fill |
| `colorPaletteRedForeground2` | `#c50f1f` | Checks-fail error icon/text |
| `colorPaletteRedBorderActive` | `#c50f1f` | Checks-fail error border |
| `colorPaletteYellowBackground2` | `#fff4ce` | Checks-warning fill |
| `colorPaletteYellowForeground2` | `#835b00` | Checks-warning icon/text |
| `colorPaletteYellowBorderActive` | `#835b00` | Checks-warning border |
| `colorNeutralForeground1` | `#242424` | Primary label text |
| `colorNeutralForeground2` | `#616161` | Secondary / sublabel text |
| `colorNeutralForegroundOnBrand` | `#ffffff` | Label on brand fill |
| `colorNeutralForegroundDisabled` | `#bdbdbd` | Disabled state text |

#### 1.2 Typography Tokens

| Token | Value | Usage |
|---|---|---|
| `fontFamilyBase` | `'Segoe UI', system-ui, sans-serif` | All shape labels |
| `fontSizeBase200` | `12px` | Sublabel / annotation text |
| `fontSizeBase300` | `14px` | Primary shape label |
| `fontSizeBase400` | `16px` | Emphasis / header label |
| `fontWeightRegular` | `400` | Default label weight |
| `fontWeightSemibold` | `600` | Emphasis label weight |
| `lineHeightBase200` | `16px` | Sublabel line height |
| `lineHeightBase300` | `20px` | Primary label line height |

#### 1.3 Spacing & Geometry Tokens

| Token | Value | Usage |
|---|---|---|
| `spacingHorizontalS` | `8px` | Inner padding horizontal |
| `spacingHorizontalM` | `12px` | Standard inner padding |
| `spacingHorizontalL` | `16px` | Wide inner padding |
| `spacingVerticalS` | `8px` | Inner padding vertical |
| `spacingVerticalM` | `12px` | Standard vertical padding |
| `borderRadiusNone` | `0px` | Sharp-cornered shapes |
| `borderRadiusSmall` | `2px` | Subtle rounding |
| `borderRadiusMedium` | `4px` | Standard rounding |
| `borderRadiusCircular` | `50%` | Fully circular shapes |
| `strokeWidthThin` | `1px` | Default border weight |
| `strokeWidthThick` | `2px` | Selected / emphasis border |
| `strokeWidthThicker` | `3px` | Active / focused border |

#### 1.4 Shadow & Elevation Tokens

| Token | Value | Usage |
|---|---|---|
| `shadow2` | `0 1px 2px rgba(0,0,0,0.14)` | Resting card elevation |
| `shadow4` | `0 2px 4px rgba(0,0,0,0.14)` | Hover elevation |
| `shadow8` | `0 4px 8px rgba(0,0,0,0.14)` | Selected elevation |
| `shadow16` | `0 8px 16px rgba(0,0,0,0.14)` | Dragging elevation |

---

### 2. Shared Shape Anatomy

All flowchart shapes share this base structure: an optional 16x16 icon, a primary
label, and an optional sublabel beneath it.

**Base dimensions:**
- Default width: `160px` (min) to `320px` (max)
- Default height: `48px` (single-line), auto-expands with content
- Icon size: `16x16px` Fluent System Icons (regular weight by default)
- Label padding: `spacingHorizontalM` by `spacingVerticalS`
- Icon-to-label gap: `spacingHorizontalS`

**Interaction states for all shapes:**

| State | Border | Fill | Shadow | Cursor |
|---|---|---|---|---|
| Default | `colorNeutralStroke1` `1px` | `colorNeutralBackground1` | `shadow2` | `default` |
| Hover | `colorNeutralStroke1` `1px` | `colorNeutralBackground2` | `shadow4` | `pointer` |
| Selected | `colorBrandStroke1` `2px` | `colorNeutralBackground1` | `shadow8` | `default` |
| Dragging | `colorBrandStroke1` `2px` | `colorNeutralBackground1` | `shadow16` | `grabbing` |
| Disabled | `colorNeutralStroke2` `1px` | `colorNeutralBackground2` | none | `not-allowed` |

---

### 3. Shape Definitions

#### 3.1 Process (Rectangle)

**Purpose:** A standard step or action in the flow.

**Geometry:** rectangle, `borderRadiusMedium` (4px), width 160-320px, height 48px or more.

**Tokens:**
- Fill: `colorNeutralBackground1`
- Border: `colorNeutralStroke1`, `strokeWidthThin`
- Border-radius: `borderRadiusMedium`
- Label: `colorNeutralForeground1`, `fontSizeBase300`, `fontWeightSemibold`
- Sublabel: `colorNeutralForeground2`, `fontSizeBase200`, `fontWeightRegular`
- Icon: Fluent `TaskListSquare16Regular` or contextual

**Variants:**

| Variant | Fill | Border | Label color |
|---|---|---|---|
| Default | `colorNeutralBackground1` | `colorNeutralStroke1` | `colorNeutralForeground1` |
| Brand | `colorBrandBackground` | `colorBrandStroke1` | `colorNeutralForegroundOnBrand` |
| Subtle | `colorNeutralBackground2` | `colorNeutralStroke2` | `colorNeutralForeground1` |

---

#### 3.2 Decision (Diamond)

**Purpose:** A branching point with two or more conditional paths.

**Geometry:** width `160px`, height `80px`, rendered as a diamond via a rotated
wrapper or a native SVG polygon. The inner label container is counter-rotated.
Exits: top, right, bottom, left. Exit labels "Yes" / "No" or custom.

**Tokens:**
- Fill: `colorNeutralBackground1`
- Border: `colorNeutralStroke1`, `strokeWidthThin`
- Label: `colorNeutralForeground1`, `fontSizeBase300`, `fontWeightSemibold`, centered
- Exit label: `colorNeutralForeground2`, `fontSizeBase200`, at the midpoint of each exit edge
- Icon: Fluent `QuestionCircle16Regular`

**Exit label placement:**

| Exit | Position offset |
|---|---|
| Right (Yes) | `+8px` from right vertex, centered vertically |
| Bottom (No) | `+8px` from bottom vertex, centered horizontally |
| Left | `+8px` from left vertex, centered vertically |
| Top | `+8px` from top vertex, centered horizontally |

---

#### 3.3 Terminator (Stadium / Pill)

**Purpose:** Start or End of a flow.

**Tokens:**

| Role | Fill | Border | Label |
|---|---|---|---|
| Start | `colorBrandBackground` | `colorBrandStroke1` | `colorNeutralForegroundOnBrand` |
| End | `colorNeutralBackground1` | `colorNeutralStroke1` `strokeWidthThick` | `colorNeutralForeground1` |

- Border-radius: full pill, `border-radius: 9999px`
- Height: `40px`
- Icon (Start): Fluent `Play16Filled`, `colorNeutralForegroundOnBrand`
- Icon (End): Fluent `RecordStop16Regular`, `colorNeutralForeground1`

---

#### 3.4 Data / Input-Output (Parallelogram)

**Purpose:** Represents data entering or leaving the process.

**Geometry:** parallelogram, 15 degree skew. Rendered via `transform: skewX(-15deg)`
on the wrapper with the inner content counter-skewed, or a native SVG polygon.

**Tokens:**
- Fill: `colorNeutralBackground1`
- Border: `colorNeutralStroke1`, `strokeWidthThin`
- Label: `colorNeutralForeground1`, `fontSizeBase300`, `fontWeightSemibold`
- Icon: Fluent `DataUsage16Regular`

---

#### 3.5 Predefined Process (Rectangle with double vertical stripes)

**Purpose:** A named subprocess or subroutine defined elsewhere.

**Geometry:** outer rectangle at `borderRadiusMedium`, with `8px`-wide vertical bars
flush to the left and right inner edges in the same border color.

**Tokens:**
- Fill: `colorNeutralBackground1`
- Stripe fill: `colorNeutralBackground2`
- Border: `colorNeutralStroke1`, `strokeWidthThin`
- Label: `colorNeutralForeground1`, `fontSizeBase300`, `fontWeightSemibold`
- Icon: Fluent `SubtractSquare16Regular`

---

#### 3.6 Document (Rectangle with wavy bottom)

**Purpose:** Output that is a document or printed report.

**Geometry:** top corners at `borderRadiusMedium`; bottom edge is an SVG sine wave,
amplitude 4px, period 16px. Height `56px`, the extra 8px carrying the wave.

**Tokens:**
- Fill: `colorNeutralBackground1`
- Border (top and sides): `colorNeutralStroke1`, `strokeWidthThin`
- Wave stroke: `colorNeutralStroke1`, `strokeWidthThin`; wave fill matches shape fill
- Label: `colorNeutralForeground1`, `fontSizeBase300`, `fontWeightSemibold`
- Icon: Fluent `Document16Regular`

---

#### 3.7 Manual Operation (Trapezoid)

**Purpose:** A step requiring human intervention.

**Geometry:** top edge full width, bottom edge inset 16px each side. Rendered via an
SVG polygon or `clip-path: polygon(0 0, 100% 0, calc(100% - 16px) 100%, 16px 100%)`.

**Tokens:**
- Fill: `colorNeutralBackground1`
- Border: `colorNeutralStroke1`, `strokeWidthThin`
- Label: `colorNeutralForeground1`, `fontSizeBase300`, `fontWeightSemibold`
- Icon: Fluent `Person16Regular`

---

#### 3.8 Delay (D-shape / half-pill)

**Purpose:** A waiting or delay step.

**Geometry:** `border-radius: 0 9999px 9999px 0`, width `160px`, height `48px`.
The right side is a full semicircle; the left side is a straight vertical edge.

**Tokens:**
- Fill: `colorNeutralBackground1`
- Border: `colorNeutralStroke1`, `strokeWidthThin`
- Label: `colorNeutralForeground1`, `fontSizeBase300`, `fontWeightSemibold`
- Icon: Fluent `Timer16Regular`

---

#### 3.9 Connector (Circle / off-page reference)

**Purpose:** Links flow across page breaks or distant areas.

**Geometry:** perfect circle, width = height = `40px`, `borderRadiusCircular`, with a
single letter or number centered inside.

**Tokens:**
- Fill: `colorNeutralBackground1`
- Border: `colorNeutralStroke1`, `strokeWidthThick`
- Label: `colorNeutralForeground1`, `fontSizeBase400`, `fontWeightSemibold`, centered
- No icon; the label is the identifier

---

### 4. Checks-Pass Shape Variants

Checks-pass shapes are status-bearing versions of the Process rectangle, used to
surface pass, warning and fail states inline in a flow.

#### 4.1 Checks-Pass: Success

**When to use:** All validation checks passed; flow proceeds.

**Tokens:**
- Fill: `colorPaletteGreenBackground2` (`#e6f4ea`)
- Border: `colorPaletteGreenBorderActive` (`#107c10`), `strokeWidthThick`
- Icon: Fluent `CheckmarkCircle16Filled`, color `colorPaletteGreenForeground2`
- Label: `colorPaletteGreenForeground2` (`#107c10`), `fontSizeBase300`, `fontWeightSemibold`
- Sublabel: `colorPaletteGreenForeground2` at `80%` opacity, `fontSizeBase200`

---

#### 4.2 Checks-Pass: Warning

**When to use:** Some checks passed with caveats; flow may proceed with acknowledgment.

**Tokens:**
- Fill: `colorPaletteYellowBackground2` (`#fff4ce`)
- Border: `colorPaletteYellowBorderActive` (`#835b00`), `strokeWidthThick`
- Icon: Fluent `Warning16Filled`, color `colorPaletteYellowForeground2`
- Label: `colorPaletteYellowForeground2` (`#835b00`), `fontSizeBase300`, `fontWeightSemibold`
- Sublabel: `colorPaletteYellowForeground2` at `80%` opacity, `fontSizeBase200`

---

#### 4.3 Checks-Pass: Fail

**When to use:** One or more checks failed; flow is blocked.

**Tokens:**
- Fill: `colorPaletteRedBackground2` (`#fde7e9`)
- Border: `colorPaletteRedBorderActive` (`#c50f1f`), `strokeWidthThick`
- Icon: Fluent `DismissCircle16Filled`, color `colorPaletteRedForeground2`
- Label: `colorPaletteRedForeground2` (`#c50f1f`), `fontSizeBase300`, `fontWeightSemibold`
- Sublabel: `colorPaletteRedForeground2` at `80%` opacity, `fontSizeBase200`

---

### 5. Arrow / Connector Styles

#### 5.1 Token mapping

| Token | Value | Usage |
|---|---|---|
| `colorNeutralStroke1` | `#d1d1d1` | Default connector line |
| `colorBrandStroke1` | `#0f6cbd` | Highlighted / active connector |
| `colorPaletteGreenBorderActive` | `#107c10` | Success path connector |
| `colorPaletteRedBorderActive` | `#c50f1f` | Failure path connector |
| `strokeWidthThin` | `1px` | Default line weight |
| `strokeWidthThick` | `2px` | Selected / emphasis line weight |
| `fontSizeBase200` | `12px` | Edge label text |
| `colorNeutralForeground2` | `#616161` | Edge label text color |

#### 5.2 Arrow types

| Style | Description | CSS / SVG |
|---|---|---|
| Solid | Standard sequential flow | `stroke-dasharray: none` |
| Dashed | Optional or conditional path | `stroke-dasharray: 6 4` |
| Dotted | Reference or annotation link | `stroke-dasharray: 2 4` |

#### 5.3 Arrowhead styles

| Style | Usage | SVG marker |
|---|---|---|
| Filled triangle (default) | Standard directional flow | `<marker orient="auto" markerWidth="8" markerHeight="8"><path d="M0,0 L8,4 L0,8 Z" fill="currentColor"/>` |
| Open chevron | Weak or reference flow | `<marker><path d="M0,0 L8,4 L0,8" fill="none" stroke="currentColor"/>` |
| Circle dot | Event trigger start | `<marker><circle cx="4" cy="4" r="3"/>` |

#### 5.4 Routing rules

- Orthogonal (default): all connectors route at 90 degree angles with `8px` corner radius on bends.
- Straight: direct point-to-point, used only when shapes are axis-aligned with no obstacles.
- Exit priority by shape type:

| Shape | Primary exit | Secondary exit |
|---|---|---|
| Process | Bottom center | Right center |
| Decision | Right (Yes) | Bottom (No) |
| Terminator (Start) | Bottom center | none |
| Terminator (End) | Top center (entry only) | none |
| Data / I-O | Bottom center | Right center |
| Connector (circle) | Bottom center | Right center |

#### 5.5 Edge label spec

- Font: `fontFamilyBase`, `fontSizeBase200`, `fontWeightRegular`
- Color: `colorNeutralForeground2`
- Background: `colorNeutralBackground1` with `2px` horizontal padding
- Placement: midpoint of edge, `8px` above the line, or beside it for vertical edges
- Max width: `80px` before wrapping

---

### 6. Dark Mode Token Overrides

Apply these overrides when `[data-theme="dark"]` or `prefers-color-scheme: dark`:

| Light token | Dark value |
|---|---|
| `colorNeutralBackground1` | `#1f1f1f` |
| `colorNeutralBackground2` | `#2c2c2c` |
| `colorNeutralStroke1` | `#404040` |
| `colorNeutralStroke2` | `#333333` |
| `colorNeutralForeground1` | `#ffffff` |
| `colorNeutralForeground2` | `#ababab` |
| `colorBrandBackground` | `#479ef5` |
| `colorBrandStroke1` | `#479ef5` |
| `colorNeutralForegroundOnBrand` | `#000000` |
| `colorPaletteGreenBackground2` | `#052505` |
| `colorPaletteGreenForeground2` | `#54b054` |
| `colorPaletteYellowBackground2` | `#2c2200` |
| `colorPaletteYellowForeground2` | `#fce100` |
| `colorPaletteRedBackground2` | `#3b0509` |
| `colorPaletteRedForeground2` | `#f1707b` |

---

### 7. Accessibility Requirements

- Contrast: all label and background combinations must meet WCAG AA, 4.5:1 for normal text and 3:1 for large text at 18pt or above.
- Focus ring: `strokeWidthThicker` (`3px`) outline, `colorBrandStroke1`, `2px` offset, on all interactive shapes.
- Keyboard: all shapes selectable via Tab; move with arrow keys; connect via Enter, then target, then Enter.
- ARIA: each shape exposes `role="figure"` with an `aria-label` combining shape type and label text, for example "Decision: Is user authenticated?".
- Screen reader announcements: state changes (selected, connected, error) announced via an `aria-live="polite"` region.

---

### 8. Component API Surface (Reference)

```ts
interface FlowchartShapeProps {
  type:
    | 'process'
    | 'decision'
    | 'terminator'
    | 'data'
    | 'predefined-process'
    | 'document'
    | 'manual-operation'
    | 'delay'
    | 'connector'
    | 'checks-pass';

  label: string;
  sublabel?: string;

  /** For type === 'terminator' */
  role?: 'start' | 'end';

  /** For type === 'connector' */
  identifier?: string;

  /** For type === 'checks-pass' */
  status?: 'success' | 'warning' | 'fail';

  /** Visual variant for 'process' shapes */
  variant?: 'default' | 'brand' | 'subtle';

  /** Fluent System Icon name (16px Regular) */
  icon?: string;

  selected?: boolean;
  disabled?: boolean;

  width?: number;   // px, default 160
  height?: number;  // px, default 48

  onSelect?: () => void;
  onConnect?: (sourcePort: Port) => void;
}

type Port = 'top' | 'right' | 'bottom' | 'left';

interface FlowchartEdgeProps {
  sourceId: string;
  targetId: string;
  sourcePort?: Port;
  targetPort?: Port;
  label?: string;
  style?: 'solid' | 'dashed' | 'dotted';
  arrowhead?: 'filled' | 'open' | 'dot';
  variant?: 'default' | 'brand' | 'success' | 'error';
  selected?: boolean;
}
```

---

### 9. Shape Quick-Reference Table

| Shape | Type key | Geometry | Primary icon |
|---|---|---|---|
| Process | `process` | Rectangle, r=4px | `TaskListSquare16Regular` |
| Decision | `decision` | Diamond / rotated square | `QuestionCircle16Regular` |
| Terminator Start | `terminator` + `role="start"` | Full-pill, brand fill | `Play16Filled` |
| Terminator End | `terminator` + `role="end"` | Full-pill, neutral | `RecordStop16Regular` |
| Data / I-O | `data` | Parallelogram 15 degree skew | `DataUsage16Regular` |
| Predefined Process | `predefined-process` | Rectangle with side stripes | `SubtractSquare16Regular` |
| Document | `document` | Rectangle with wavy bottom | `Document16Regular` |
| Manual Operation | `manual-operation` | Trapezoid, top wide | `Person16Regular` |
| Delay | `delay` | D-shape, half-pill right | `Timer16Regular` |
| Connector | `connector` | Circle 40px | the identifier character |
| Checks-Pass success | `checks-pass` + `status="success"` | Rectangle, green | `CheckmarkCircle16Filled` |
| Checks-Pass warning | `checks-pass` + `status="warning"` | Rectangle, yellow | `Warning16Filled` |
| Checks-Pass fail | `checks-pass` + `status="fail"` | Rectangle, red | `DismissCircle16Filled` |
