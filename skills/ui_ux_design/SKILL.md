---
name: Professional UI/UX Design
description: Guide for creating professional, minimalist, and high-retention web interfaces.
---

# Professional UI/UX Design Skill

This skill guides the AI in creating "WOW" factor interfaces that are minimal, professional, and optimized for user retention.

## 1. Core Design Philosophy: "Midnight Glass"
- **Backgrounds**: Deep, rich dark backgrounds (e.g., `#0a0a0a` or `#0f172a`) instead of pure black.
- **Cards/Containers**: Glassmorphism effect with low opacity, subtle borders, and background blur.
  - *CSS*: `background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1);`
- **Typography**: Sans-serif, cleaner fonts (Inter, Geist, or SF Pro). High contrast for readability.
- **Spacing**: Generous padding (at least `2rem` or `32px` between sections). "White space equals luxury."

## 2. User Retention & "Attraction"
- **Micro-interactions**: Everything interactive must react.
  - *Hover*: Slight lift (`transform: translateY(-2px)`), glow, or border color change.
  - *Active*: Scale down (`transform: scale(0.98)`).
- **Onboarding**: The first screen must explain the value immediately.
- **Feedback**: Loading states, success toasts, and error messages must be animated and smooth.

## 3. Implementation Rules for AssetFlow
1. **Sidebar**: Clean, not cluttered. Use icons.
2. **Buttons**: Gradient backgrounds or clean outlines. No default browser styles.
3. **Data Display**: Use clear data tables or "metric cards" instead of raw text dumps.
4. **Animations**: Use `st.empty()` or CSS `@keyframes` for fade-ins on load.

## 4. Checklist for Every UI Change
- [ ] Does it look good on mobile?
- [ ] Is the contrast ratio accessible?
- [ ] active state feedback?
- [ ] Is there too much text? (If yes, structure it into columns or cards).
