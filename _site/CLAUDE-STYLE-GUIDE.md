# Blog Post Style Guide

This guide documents the styling conventions and components available for blog posts.

## Color Philosophy

**Teal (#4ecdc4) is an accent color, not the primary color.**

- **Titles and headings**: White/cream (`--text-primary`)
- **Body text**: Light gray (`--text-secondary`)
- **Teal accent used for**:
  - Links (interactivity indicator)
  - Buttons and interactive controls
  - Category badges/tags
  - Decorative borders and highlights
  - Hover states
  - State node borders in visualizations

This creates visual hierarchy where teal draws attention to interactive or important accent elements rather than dominating the page.

## Front Matter

Every post requires YAML front matter:

```yaml
---
layout: post
title: "Your Post Title"
date: 2026-01-31
excerpt: "A brief description for the post listing."
math: true  # Optional: enables MathJax for equations
---
```

## Typography

### Headings

Use standard markdown headings. The post title uses `h1`, so content should start with `h2`. All headings render in white/cream, not teal.

```markdown
## Section Heading
### Subsection
#### Minor Heading
```

### Text Emphasis

```markdown
**bold text**
*italic text*
`inline code`
```

### Links

Links use teal to indicate interactivity:

```markdown
[Link text](https://example.com)
```

## Code Blocks

Use fenced code blocks with language specification for syntax highlighting:

````markdown
```python
def example():
    return "Hello, world!"
```
````

For manual syntax highlighting within prose, use these classes:

```html
<span class="code-keyword">def</span>
<span class="code-comment"># This is a comment</span>
<span class="code-number">42</span>
```

## Mathematics

Requires `math: true` in front matter.

### Inline Math

```markdown
The equation $E = mc^2$ is famous.
```

### Display Math

```markdown
$$
\hat{A}_t^{GAE(\gamma,\lambda)} = \sum_{l=0}^{\infty} (\gamma\lambda)^l \delta_{t+l}
$$
```

### Math Blocks (styled container)

```html
<div class="math-block">
$$
\text{Your equation here}
$$
</div>
```

Add `.highlight` class for emphasis (adds teal border glow):

```html
<div class="math-block highlight">
$$
\text{Important equation}
$$
</div>
```

## Tables

### Standard Tables

Use markdown tables:

```markdown
| Column 1 | Column 2 |
|----------|----------|
| Data     | Data     |
```

### Comparison Tables

For styled comparison tables:

```html
<table class="comparison-table">
  <thead>
    <tr>
      <th>Feature</th>
      <th>Option A</th>
      <th>Option B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Speed</td>
      <td><span class="badge badge-high">High</span></td>
      <td><span class="badge badge-low">Low</span></td>
    </tr>
  </tbody>
</table>
```

### Badges

Use within tables or inline. Badges use semantic colors (red/green), not teal:

```html
<span class="badge badge-high">High Risk</span>
<span class="badge badge-low">Low Risk</span>
```

## Content Sections

### Visualization Section

Container for interactive visualizations:

```html
<section class="viz-section">
  <h2>Section Title</h2>
  <p class="viz-description">Description of the visualization.</p>

  <!-- Controls, visualization content, etc. -->
</section>
```

### Insight Boxes

Highlight key takeaways. Uses teal accent border and heading:

```html
<div class="insight-box">
  <h4>Key Insight</h4>
  <p>The important point you want readers to remember.</p>
</div>
```

## Interactive Controls

Interactive elements use teal to indicate they're clickable/draggable.

### Control Groups

```html
<div class="controls">
  <div class="control-group">
    <label>Parameter Name</label>
    <div class="control-value" id="value-display">0.95</div>
    <div class="slider-container">
      <input type="range" id="param-slider" min="0" max="1" step="0.01" value="0.95">
    </div>
  </div>
</div>
```

The slider thumb is teal; the displayed value is white.

### Buttons

Primary buttons use teal background. Secondary buttons are neutral with teal on hover:

```html
<div class="button-group">
  <button class="primary" id="action-btn">Primary Action</button>
  <button class="secondary" id="reset-btn">Reset</button>
</div>
```

## Visualization Components

### Rollout Container

For sequential/timeline visualizations:

```html
<div class="rollout-container">
  <div class="rollout">
    <div class="timestep">
      <div class="state-node">S₀</div>
      <div class="value-label">Value</div>
      <div class="value">0.85</div>
    </div>

    <div class="transition">
      <div class="arrow"></div>
      <div class="reward positive">+1.0</div>
      <div class="reward-label">r₀</div>
    </div>

    <!-- More timesteps... -->
  </div>
</div>
```

### State Nodes

State nodes have teal borders to indicate interactivity. Values display in white:

```html
<div class="state-node">S₀</div>
<div class="state-node active">S₁</div>   <!-- Teal glow highlight -->
<div class="state-node computed">S₂</div> <!-- Green border (computed) -->
```

### Rewards

Rewards use semantic colors (green/red), not teal:

```html
<div class="reward positive">+1.0</div>
<div class="reward negative">-0.5</div>
```

### Computation Rows

For showing step-by-step calculations. Values use semantic colors:

```html
<div class="computation-rows">
  <div class="computation-row">
    <div class="label">δ</div>
    <div class="computation-cell">
      <div class="symbol">δ₀</div>
      <div class="value visible td">0.15</div>
    </div>
    <div class="spacer-cell"></div>
    <!-- More cells... -->
  </div>
</div>
```

Value classes: `.td` (purple), `.gae-positive` (orange), `.gae-negative` (blue)

### Step Log

For showing computation history:

```html
<div class="step-log">
  <div class="step-log-title">Computation Log</div>
  <div class="log-entry visible">
    <span class="log-step">Step 1:</span>
    <span class="log-formula">δ₀ = r₀ + γV(s₁) - V(s₀)</span>
    <span class="log-result">= 0.15</span>
  </div>
</div>
```

### Lambda Spectrum

For showing parameter trade-offs:

```html
<div class="lambda-spectrum">
  <div class="spectrum-end left">
    <h4>λ = 0</h4>
    <div class="formula">Â = δₜ</div>
    <p>Low variance, high bias</p>
  </div>
  <div class="spectrum-middle">
    <div class="spectrum-arrow">↔</div>
  </div>
  <div class="spectrum-end right">
    <h4>λ = 1</h4>
    <div class="formula">Â = Σγᵗδₜ</div>
    <p>High variance, low bias</p>
  </div>
</div>
```

## Color Variables

Available CSS custom properties:

| Variable | Color | Use |
|----------|-------|-----|
| `--text-primary` | White (#e6edf3) | Headings, titles, important text |
| `--text-secondary` | Light gray (#8b949e) | Body text |
| `--text-muted` | Gray (#6e7681) | Labels, hints, captions |
| `--accent-primary` | Teal (#4ecdc4) | Links, buttons, interactive elements |
| `--accent-green` | Green (#7ee787) | Positive values, success states |
| `--accent-red` | Red (#f97583) | Negative values, errors |
| `--accent-purple` | Purple (#d2a8ff) | TD errors, special highlights |
| `--accent-orange` | Orange (#ffa657) | Results, warnings |
| `--accent-blue` | Blue (#a5d6ff) | Info, secondary highlights |
| `--accent-yellow` | Yellow (#e3b341) | Caution |

### When to Use Teal

Use `--accent-primary` (teal) for:
- Links and clickable text
- Button backgrounds
- Slider thumbs and interactive controls
- Border highlights on hover/focus
- Category badges
- Decorative accent lines

Do NOT use teal for:
- Headings or titles
- Body text
- Data values in visualizations
- Table headers

## Responsive Design

The site is mobile-responsive. Key breakpoints:

- **768px and below**: Controls stack vertically, spectrum layouts become vertical

Test visualizations at mobile sizes. Use `min-width: max-content` for scrollable horizontal visualizations.

## JavaScript Integration

For interactive posts, include scripts at the end:

```html
<script>
document.addEventListener('DOMContentLoaded', function() {
  // Your visualization code
});
</script>
```

### Animation Classes

Add `.visible` class to trigger CSS transitions:

```javascript
element.classList.add('visible');
```

Elements with built-in transitions:
- `.computation-cell .value` - fade in and slide up
- `.log-entry` - fade in and slide right
- `.state-node.active` - teal glow effect
