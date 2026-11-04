---
name: hogwarts-brand-style
description: Brand voice and visual style for a hypothetical, fan-made Hogwarts School of Witchcraft and Wizardry corporate identity, with subtle Netlight-inspired touches. Use when creating Hogwarts staff or teacher documents, onboarding material, letters, slides, web pages, or any copy that must sound and look unmistakably like the Harry Potter universe. Triggers include "Hogwarts", "Harry Potter", "wizarding", "teacher onboarding", "Hogwarts brand", "house colours", "owl post".
---

# Hogwarts Brand Style (hypothetical, fan-made)

> Unofficial concept for a fictional scenario. Not affiliated with or endorsed by the rights holders of the Harry Potter franchise. Do NOT use official logos, film stills, official artwork, or the official Harry Potter wordmark font. Use the simplified crest and free fonts below.

## 0. The one-line brief
**Hogwarts first, Netlight as a quiet signature.** Anyone should recognise the Harry Potter world within two seconds. A Netlighter should only notice, on a second look, the sharp corners, hard shadows, square bullets, British English, and one lavender-and-yellow accent.

Ratio rule: ~70% parchment / ink / midnight, ~20% house colours + gold, ≤10% Netlight bridge colours.

## 1. Pick a canon anchor first
Before writing, fix an era and stay consistent. Default: a timeless modern Hogwarts with **no named living headteacher**. Use "[the Headmaster/Headmistress]" as a placeholder unless the user names one. Never mix timelines (e.g. a named Headmaster from one era with details from another).

## 2. Brand idea
**"Where every light finds its flock."** Learning, safety and quiet mischief inside an ancient castle that rewards curiosity. Tone pillars (Netlight's "Playful Professionalism", in wizarding clothes):

| Pillar | Sounds like | Never sounds like |
|---|---|---|
| **Warm** (Hagrid's welcome) | "You'll find the kettle in the staff room. Do help yourself." | Cold HR boilerplate |
| **Clear** (McGonagall's precision) | Short sentences, numbered steps, exact times | Vague, rambling |
| **Wise** (Dumbledore's aphorisms) | One reflective line per section, max | Fortune-cookie overload |
| **Wry** (understated British humour) | "The staircases move. This is considered normal." | Slapstick, memes, sarcasm at colleagues |

## 3. Voice and language rules
- **British English** always (colour, organise, programme, realise). It is canon-correct and also matches Netlight style.
- Address people formally and warmly: "Dear Professor Okonkwo", "Welcome to Hogwarts". Staff are **Professors**; use correct canon titles (Headmaster/Headmistress, Deputy Headmaster/Headmistress, Head of House, Librarian, Matron, Caretaker, Groundskeeper).
- Dates and times as the wizarding world would: "Term begins 1 September. The Hogwarts Express leaves Platform 9¾, King's Cross, at eleven o'clock." Replies are "by owl, no later than [date]".
- Money in **Galleons, Sickles and Knuts** (1 Galleon = 17 Sickles; 1 Sickle = 29 Knuts).
- Use **real canon vocabulary**, not invented lookalikes: Great Hall, Common Room, Staff Room, Owlery, Hospital Wing, Room of Requirement, Library (Restricted Section), Hogsmeade, Forbidden Forest, Black Lake, Floo Network, Ministry of Magic, Board of Governors, O.W.L.s, N.E.W.T.s, House points, the Sorting Hat, Hogwarts Express.
- Subjects (exact names): Transfiguration, Charms, Potions, Defence Against the Dark Arts, Herbology, History of Magic, Astronomy, Divination, Care of Magical Creatures, Arithmancy, Ancient Runes, Muggle Studies, Flying.
- Use **"Muggle"** only for non-magical people or things. Keep spells correctly spelled (Lumos, Nox, Accio, Alohomora, Wingardium Leviosa) and harmless. No Unforgivable Curse jokes in HR-type documents.
- Hogwarts motto, correctly: *Draco dormiens nunquam titillandus* ("Never tickle a sleeping dragon"). Use as a footer or crest banner, not in running text.
- Easter eggs: **max one per page or slide** (e.g. "Mischief managed." as a final sign-off). Never explain the joke.
- Keep it **house-neutral**. Never rank or mock a House. Describe Houses only with their positive canon traits.
- Avoid corporate-speak: synergy, leverage, KPI, stakeholder, bandwidth. Replace per the glossary below.

### Quote policy
Short, well-known lines (≤ one per document) are fine, such as Dumbledore's "Help will always be given at Hogwarts to those who ask for it." Do not reproduce passages from the books or films. Paraphrase.

## 4. Netlight touches (the hybrid layer)
Netlight idea → Hogwarts expression. Use as translation, never name-drop "Netlight" in the doc body unless the user asks (an optional footer line is allowed, see section 9).

| Netlight concept | Hogwarts expression |
|---|---|
| OneNetlight / 1+1=3 | **One Hogwarts, four Houses.** Together we achieve more than any House alone. |
| Create Together | Hufflepuff-style loyalty and fair play: teaching teams share lesson plans and cover each other |
| Engage in Challenge | Taking on the hard lesson, the difficult class, the unfamiliar creature |
| Grow Talent | Students *and* staff grow; professors have mentors |
| CCB (Creativity, Competence, Business Sense) | Creativity ≈ courage to act (Gryffindor spirit); Competence ≈ learning and wit (Ravenclaw spirit); Business Sense ≈ ambition and resourcefulness (Slytherin spirit); Create Together ≈ the Hufflepuff glue. Playful framing only, never a ranking. |
| Perfect Match | The Sorting Hat moment: the right fit for the person *and* the school |
| Mentor / Buddy / DC | Staff Mentor, Staff Buddy (the colleague who shows you which staircase moves today), Teaching Coach |
| Evolution Review (bi-annual) | Term reflection (a Pensieve-style look back, then forward) |
| Edge / knowledge sharing | The Library and staff seminars; "the Restricted Section is for those who ask properly" |
| In Command | Every Professor is master of their classroom, and answerable to the whole school |
| The flock / BOID | A parliament of owls: everyone steers, the group moves as one |
| Slack | The Floo Network or Owl Post |
| The Weekly | The Weekly Owl Post (staff bulletin) |
| Summit | The annual Staff Gathering at a destination unknown |
| "Turn on the light" | **Lumos**: the wand-tip glow is the Netlight yellow accent |
| Young at heart, senior mind | The ancient castle that still surprises you |

## 5. Colour system (digital HEX)
Use CSS variables:

```css
:root {
  /* Hogwarts core */
  --hw-parchment: #F4EAD0;       /* main background (cf. Netlight beige: background only, never text) */
  --hw-parchment-deep: #E4D2A5;  /* cards, panels */
  --hw-ink: #2B1B12;             /* body text (never pure black) */
  --hw-emerald-ink: #0E5A36;     /* letter headings and signatures (the letters are written in green ink) */
  --hw-midnight: #0D1230;        /* dark mode / Great Hall ceiling at night */
  --hw-gold: #D3A625;            /* rules, bullets, borders, candlelight */
  --hw-scarlet: #740001;         /* Hogwarts Express, wax seal, key callouts */

  /* Houses (use together, evenly, never favour one) */
  --gryffindor: #740001;  --gryffindor-accent: #D3A625;
  --slytherin:  #1A472A;  --slytherin-accent:  #AAAAAA;
  --ravenclaw:  #0E1A40;  --ravenclaw-accent:  #946B2D;
  --hufflepuff: #ECB939;  --hufflepuff-accent: #372E29;

  /* Netlight bridge (≤10% of any layout) */
  --hw-knight-bus: #785AF2;  /* section tags, links, active states (the Knight Bus is purple) */
  --hw-enchant:    #A29AFF;  /* soft fills, tag backgrounds */
  --hw-lumos:      #FFF4A4;  /* highlight / "Lumos note" background; #FFF400 for one spark only */
}
```

Rules:
- Default page: parchment background + ink text + gold rules.
- Dark variant: midnight background + parchment text + gold accents.
- The four house colours appear as a **balanced set** (e.g. four equal stripes or tabs) or not at all.
- Knight-Bus purple on parchment is only ~3.9:1 contrast, so use it for **bold or large (≥18px) uppercase labels** only. Body text stays ink.
- Don't use neon yellow as a large fill. Use `--hw-lumos` (pale) for fills.
- Approved Netlight-style pairings: purple + parchment (beige), purple + midnight (black), purple + lumos yellow.

## 6. Typography (free fonts, Google Fonts)
| Role | Font | Netlight echo |
|---|---|---|
| Hero / display (all caps, wide tracking) | **Cinzel Decorative** or **Cinzel** 700 | Video: caps, display only |
| Headings | **Cinzel** 600–700 | Strong headline weight |
| Body | **EB Garamond** 400, 18px / line-height 1.3–1.5 | Clean, generous whitespace |
| Quill / signature / marginalia | **IM Fell English Italic** (sparingly) | none, pure Hogwarts |
| Section tags and small labels | Cinzel uppercase, letter-spacing 0.1em (or Inter 500 if a UI sans is required) | Netlight "section tag" style |

Never use the official Harry Potter wordmark font or a generic "magic" font. Don't mix more than three families.

## 7. Layout and component language
- **Sharp corners only** (`border-radius: 0`). Pointed Gothic arches (`clip-path`) are allowed for hero images.
- **Hard offset shadows**, no blur: `box-shadow: 8px 8px 0 0 var(--hw-ink);` (the "stack of parchment" look).
- **Square bullets**, coloured gold: `ul { list-style-type: square; } li::marker { color: var(--hw-gold); }`
- Generous whitespace. Thin double gold rules between sections (`border-top: 3px double var(--hw-gold)`).
- Optional faint grid or ruled-parchment texture, never a busy image.
- Images: warm, high-contrast, slightly grainy sepia or black-and-white with a thick ink border. No soft stock photography, no distortion.
- Components:
  - **Wax-seal stamp** (scarlet circle with "H") for official confirmations.
  - **Lumos note**: pale-yellow box, ink text, gold left bar, for tips and helpful hints.
  - **Restricted Section box**: scarlet border, for policies and safety rules.
  - **House stripe**: four equal bars (scarlet / green / blue / yellow) as a footer divider.
  - **Footprints / Marauder's-style dotted path** for step-by-step timelines (optional).

### Simplified crest (placeholder, safe to use)
```svg
<svg viewBox="0 0 120 150" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Hogwarts-style crest">
  <path d="M10 10H60V70H10Z" fill="#740001"/>
  <path d="M60 10H110V70H60Z" fill="#1A472A"/>
  <path d="M10 70H60V130L10 80Z" fill="#ECB939"/>
  <path d="M60 70H110V80L60 130Z" fill="#0E1A40"/>
  <path d="M10 10H110V80L60 130L10 80Z" fill="none" stroke="#2B1B12" stroke-width="4"/>
  <text x="60" y="78" text-anchor="middle" font-family="Cinzel, serif" font-size="46" font-weight="700" fill="#D3A625" stroke="#2B1B12" stroke-width="1.5">H</text>
  <text x="60" y="146" text-anchor="middle" font-family="Cinzel, serif" font-size="6" letter-spacing="1" fill="#2B1B12">DRACO DORMIENS NUNQUAM TITILLANDUS</text>
</svg>
```
Quarter layout follows the well-known arrangement: Gryffindor top-left, Slytherin top-right, Hufflepuff bottom-left, Ravenclaw bottom-right. Official animal emblems are omitted on purpose.

## 8. Document patterns
**Letter / welcome (the signature format)**
1. Parchment page, crest top-centre.
2. Header in caps: HOGWARTS SCHOOL of WITCHCRAFT and WIZARDRY. Below it the Headmaster/Headmistress line (placeholder allowed).
3. Salutation "Dear Professor [Surname],".
4. Short, warm body. Headings and signature in **emerald ink**, body in ink.
5. "We await your owl by no later than [date]."
6. Sign-off "Yours sincerely," + role title + wax seal.

**Slides**: Cover = midnight with gold crest and Cinzel title. Section break = scarlet or midnight with one Knight-Bus-purple tag. Content = parchment. One idea per slide.

**Web / handbook**: Parchment page, sticky midnight header, Cinzel headings, house-stripe footer, Lumos notes for tips, Restricted Section boxes for rules.

**Sentence-level pattern for instructions**: *One wry line of welcome → numbered steps → one Lumos tip.*

## 9. Optional Netlight signature
Allowed once per document, in the footer, small: *"Concept & craft: Netlight"* in Cinzel uppercase 10–11px, Knight-Bus purple. Omit it unless the user wants attribution.

## 10. Glossary: plain business term → Hogwarts voice
| Instead of | Say |
|---|---|
| Onboarding | Welcome to Hogwarts / Your first term |
| New hire | New member of staff / newly appointed Professor |
| HR | The Deputy Headmaster's/Headmistress's office / Staff Office |
| IT support | The Caretaker's office (and Owl Post for urgent matters) |
| Deadline | "By owl, no later than…" |
| Team meeting | Staff meeting in the Staff Room |
| Performance review | Term reflection |
| Policy / compliance | The Rules of the School (Restricted Section box) |
| Training | Staff seminar / a session in the Library |
| Org chart | Who's who at Hogwarts |
| KPI / goals | Learning goals / House points to aim for |
| Payroll | Your Galleons, paid monthly (adjust as needed) |
| Sick leave | A visit to the Hospital Wing |
| Mentor | Staff Mentor |
