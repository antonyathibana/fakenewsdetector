# Premium Futuristic UI Theme System

A comprehensive luxury, futuristic UI theme for the AI-Powered Fake News Detector platform.

## Theme Overview

This theme provides a premium, futuristic aesthetic with:
- **Dark Mode Primary**: Deep space black background with glassmorphism effects
- **Luxury Tech Brand Feel**: High-end cybersecurity aesthetic
- **AI Intelligence Vibe**: Neon gradients and glow effects
- **Minimal Yet Powerful**: Clean interfaces with impactful visual elements

## Color System

### Primary Dark Theme

| Color Name | Hex Code | Usage |
|------------|----------|-------|
| Base Background | `#0B0F19` | Main page background |
| Surface | `#111827` | Card backgrounds, navbar |
| Elevated | `#1F2937` | Hover states, elevated surfaces |
| Primary Accent | `#6366F1` | Electric Indigo - main actions |
| Secondary Accent | `#06B6D4` | Neon Cyan - highlights |
| Success | `#10F0A0` | Emerald Glow - verified results |
| Alert/Danger | `#FF2E63` | Crimson Neon - fake news |

### Text Colors

| Usage | Hex Code |
|-------|----------|
| Primary Text | `#F9FAFB` |
| Secondary Text | `#9CA3AF` |
| Muted Text | `#64748B` |

### Light Theme Variant

| Color Name | Hex Code |
|------------|----------|
| Base Background | `#F3F4F6` |
| Surface | `#FFFFFF` |
| Elevated | `#F9FAFB` |

## Typography

### Heading Fonts
- **Sora** - Primary heading font (recommended)
- **Orbitron** - Display/hero typography
- **Poppins** - Alternative modern font

### Body Fonts
- **Inter** - Primary body text
- **Manrope** - Alternative body font
- **JetBrains Mono** - Code/monospace

### Font Weights
- Headings: 700-800 (Bold)
- Body: 400-500 (Regular)
- Letter spacing: -0.02em for headings

## Included Files

### CSS
- `theme.css` - Complete theme system with all components

### JavaScript
- `theme.js` - Interactive components and animations

## Usage

### 1. Include Theme Files

Add to your HTML head:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/theme.css') }}">
<script src="{{ url_for('static', filename='js/theme.js') }}"></script>
```

### 2. Google Fonts (Optional)

Add premium fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Sora:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
```

### 3. Theme Toggle

Add theme toggle button:
```html
<button class="btn btn-icon btn-ghost" id="themeToggle">
    <i class="fas fa-moon"></i>
</button>
```

### 4. Dark/Light Mode

Set default theme in HTML:
```html
<html lang="en" data-theme="dark">
```

## Component Classes

### Buttons
- `.btn-primary` - Gradient indigo to cyan with glow
- `.btn-secondary` - Outline style
- `.btn-outline-neon` - Neon border effect
- `.btn-ghost` - Transparent with subtle border
- `.btn-icon` - Square icon button
- `.btn-lg` / `.btn-sm` - Size variants

### Cards
- `.card` - Glassmorphism card
- `.card-feature` - Feature card with icon
- `.card-stats` - Statistics card
- `.card-glow-primary` - Glow border variants
- `.card-glow-success`
- `.card-glow-danger`

### Form Elements
- `.form-control` - Standard input
- `.input-glow` - Glowing border input
- `.input-type-btn` - Toggle button for input types

### Utility Classes
- `.glass` - Glassmorphism effect
- `.glow-primary` - Primary glow effect
- `.text-gradient` - Gradient text
- `.fade-in` - Fade in animation
- `.glow-pulse` - Pulsing glow animation

### Badge Variants
- `.badge-primary`
- `.badge-secondary`
- `.badge-success`
- `.badge-danger`
- `.badge-glow` - Animated badge

## Animations

### Available Animations
- `fadeIn` - Fade in from bottom
- `fadeInUp` - Fade in upward
- `glowPulse` - Pulsing glow effect
- `shimmer` - Light sweep effect
- `pulse` - Simple pulse
- `float` - Floating motion
- `gradient-animate` - Moving gradient
- `spin` - Rotation
- `bounce` - Bouncing motion

### Usage
```html
<div class="glow-pulse">Pulsing Element</div>
<div class="float">Floating Element</div>
<div class="fade-in-up">Fading In</div>
```

## Result Display

### Fake News Result
```html
<div class="result-header fake">
    <div class="result-icon">
        <i class="fas fa-times"></i>
    </div>
    <h2>FAKE NEWS</h2>
    <div class="result-confidence">92%</div>
</div>
```

### Real News Result
```html
<div class="result-header real">
    <div class="result-icon">
        <i class="fas fa-check"></i>
    </div>
    <h2>REAL NEWS</h2>
    <div class="result-confidence">87%</div>
</div>
```

## Spacing System

Based on 8px grid:
- `xs`: 4px
- `sm`: 8px
- `md`: 16px
- `lg`: 24px
- `xl`: 32px
- `2xl`: 48px
- `3xl`: 64px

## Border Radius

- `sm`: 8px
- `md`: 12px
- `lg`: 16px
- `xl`: 20px
- `full`: 9999px (pill)

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Android)

## Demo Page

A complete demo page is available at `templates/theme-demo.html` showcasing all theme components.

## Customization

### CSS Variables

Override in your CSS:
```css
:root {
    --accent-primary: #your-color;
    --accent-secondary: #your-color;
    --bg-base: #your-color;
}
```

### Adding Custom Gradients

```css
.custom-gradient {
    background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
}
```

## License

This theme is provided as part of the Fake News Detector project.

