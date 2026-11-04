---
name: hogwarts-brand-style
description: Complete brand voice and visual identity for Hogwarts School of Witchcraft and Wizardry, with subtle Netlight-inspired touches. Covers logo system, crest usage, house identities, colour, typography, imagery, letter anatomy, canon facts and tone of voice. Use when creating Hogwarts staff or teacher documents, onboarding material, letters, slides, web pages, or any copy that must sound and look unmistakably like the Harry Potter universe. Triggers include "Hogwarts", "Harry Potter", "wizarding", "teacher onboarding", "Hogwarts brand", "house colours", "owl post", "crest".
---

# Hogwarts Brand Style

## 0. The one-line brief
**Hogwarts first, Netlight as a quiet signature.** Anyone should recognise the Harry Potter world within two seconds. A Netlighter should only notice, on a second look, the sharp corners, hard shadows, square bullets, British English, and one lavender-and-yellow accent.

Ratio rule: ~70% parchment / ink / midnight, ~20% house colours + gold, ≤10% Netlight bridge colours.

## 1. Pick a canon anchor first
Before writing, fix an era and stay consistent. Never mix timelines.

| Era | Headmaster/Headmistress | Deputy | Notes |
|---|---|---|---|
| **Classic (1991–1997)** | Albus Dumbledore | Minerva McGonagall | The era most people picture; the films' warm opening look |
| **Post-war (1998 onwards)** | Minerva McGonagall | (placeholder) | Rebuilt castle, hopeful tone |
| **Timeless (default)** | "[the Headmaster/Headmistress]" | "[the Deputy]" | No named person; safest for generic documents |

If the user names an era, use its canon staff. If not, use the Timeless default with placeholders.

### Canon staff reference (Classic era, for names and titles)
| Role | Person |
|---|---|
| Transfiguration, Head of Gryffindor, Deputy Headmistress | Minerva McGonagall |
| Potions, Head of Slytherin | Severus Snape |
| Charms, Head of Ravenclaw | Filius Flitwick |
| Herbology, Head of Hufflepuff | Pomona Sprout |
| History of Magic | Cuthbert Binns (a ghost) |
| Astronomy | Aurora Sinistra |
| Divination | Sybill Trelawney |
| Flying | Madam Rolanda Hooch |
| Arithmancy / Ancient Runes / Muggle Studies | Septima Vector / Bathsheda Babbling / Charity Burbage |
| Gamekeeper and Keeper of Keys and Grounds | Rubeus Hagrid |
| Caretaker | Argus Filch |
| Matron (Hospital Wing) | Madam Poppy Pomfrey |
| Librarian | Madam Irma Pince |
Defence Against the Dark Arts changes teacher almost every year, which is itself a well-known running joke. Use it only with a light touch and never about a real colleague.

## 2. Brand idea
**"Where every light finds its flock."** Learning, safety and quiet mischief inside an ancient castle that rewards curiosity. Tone pillars (Netlight's "Playful Professionalism", in wizarding clothes):

| Pillar | Sounds like | Never sounds like |
|---|---|---|
| **Warm** (Hagrid's welcome) | "You'll find the kettle in the staff room. Do help yourself." | Cold HR boilerplate |
| **Clear** (McGonagall's precision) | Short sentences, numbered steps, exact times | Vague, rambling |
| **Wise** (Dumbledore's aphorisms) | One reflective line per section, max | Fortune-cookie overload |
| **Wry** (understated British humour) | "The staircases move. This is considered normal." | Slapstick, memes, sarcasm at colleagues |

## 3. Logo and crest system

### 3.1 Logo inventory
Always use the official file when it exists in `assets/`. Fall back to the built-in SVG (3.5) only when it doesn't.

| Logo | Expected file | Use for |
|---|---|---|
| **Hogwarts crest (full colour)** | `assets/hogwarts-crest-colour.svg` (or `.png`) | Covers, letter heads, wax-seal, slide covers, web header |
| **Hogwarts crest (one colour: gold, ink, white)** | `assets/hogwarts-crest-mono-*.svg` | Embossing, watermarks, footers, small sizes |
| **Hogwarts crest with motto banner** | `assets/hogwarts-crest-banner.svg` | Formal documents, certificates, contracts |
| **House crests (Gryffindor, Slytherin, Hufflepuff, Ravenclaw)** | `assets/house-*.svg` | House sections only; always shown as a complete set of four |
| **"Harry Potter" title logotype** | `assets/harry-potter-logo.svg` | Franchise-level covers and credits only, never as the school's own wordmark |
| **"Wizarding World" logo** | `assets/wizarding-world-logo.svg` | Franchise-level footers only |
| **Platform 9¾ sign** | `assets/platform-9-3-4.svg` | Travel and arrival sections |

The school wordmark itself is **typeset, not a graphic**: HOGWARTS SCHOOL of WITCHCRAFT and WIZARDRY in Cinzel, with "of" and "and" set smaller (see 6).

### 3.2 Crest anatomy (canon)
- A **shield** divided into four quarters, one for each House, with a large **H** at the centre.
- The four House animals: **lion** (Gryffindor), **snake** (Slytherin), **badger** (Hufflepuff), **eagle** (Ravenclaw). Quadrant placement and styling differ between book, film and merchandise versions, so **follow the supplied file exactly and never re-arrange the quarters**.
- Motto banner beneath: ***Draco dormiens nunquam titillandus*** ("Never tickle a sleeping dragon").
- Metal tone is gold or silver; the film version is a weathered, engraved look.

### 3.3 Clear space and size
- Clear space on all sides = the height of the central **H**.
- Minimum size: 24 px (digital) or 12 mm (print) for the shield alone; use the banner version only at 120 px / 40 mm or wider so the motto stays legible.
- Place the crest top-centre on letters, top-left in slide headers, and centre on covers.

### 3.4 Logo don'ts (borrowed from Netlight's logo discipline)
- Do not recolour outside: full colour, gold, ink or white.
- Do not stretch, rotate, tilt, add shadows or glows, or put it on a busy image.
- Do not rearrange or remove quarters, or mix House crests from different sources.
- Do not place other logos (including any Netlight mark) within one clear-space unit.
- Ensure sufficient contrast: gold or colour on parchment and midnight; white on scarlet.
- Never show only one or two House crests where the context is "all of Hogwarts".

### 3.5 Fallback crest (SVG, use only if no official file exists)
```svg
<svg viewBox="0 0 120 170" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Hogwarts crest (fallback)">
  <!-- Shield with four quarters: replace with the official crest file when available -->
  <path d="M10 10H110V80Q110 118 60 140Q10 118 10 80Z" fill="#F4EAD0" stroke="#2B1B12" stroke-width="4"/>
  <path d="M10 10H60V75H10Z" fill="#740001"/>
  <path d="M60 10H110V75H60Z" fill="#1A472A"/>
  <path d="M10 75H60V132Q10 118 10 80Z" fill="#ECB939"/>
  <path d="M60 75H110V80Q110 118 60 132Z" fill="#0E1A40"/>
  <path d="M10 10H110V80Q110 118 60 140Q10 118 10 80Z" fill="none" stroke="#D3A625" stroke-width="4"/>
  <!-- Central H -->
  <circle cx="60" cy="75" r="22" fill="#0D1230" stroke="#D3A625" stroke-width="3"/>
  <text x="60" y="86" text-anchor="middle" font-family="Cinzel, serif" font-size="32" font-weight="700" fill="#D3A625">H</text>
  <!-- Motto banner -->
  <path d="M6 148H114V166H6Z" fill="#740001" stroke="#D3A625" stroke-width="2"/>
  <text x="60" y="160" text-anchor="middle" font-family="Cinzel, serif" font-size="6.2" letter-spacing="0.6" fill="#F4EAD0">DRACO DORMIENS NUNQUAM TITILLANDUS</text>
</svg>
```

## 4. The Houses (identity set)
Always present all four together, evenly weighted, and describe each only by positive canon traits.

| House | Colours (canon) | Founder | Animal | Traits | Common Room | Ghost |
|---|---|---|---|---|---|---|
| **Gryffindor** | Scarlet and gold | Godric Gryffindor | Lion | Courage, daring, chivalry | Gryffindor Tower | Nearly Headless Nick |
| **Slytherin** | Green and silver | Salazar Slytherin | Snake | Ambition, cunning, resourcefulness | Dungeons, beneath the Black Lake | The Bloody Baron |
| **Hufflepuff** | Yellow and black | Helga Hufflepuff | Badger | Loyalty, patience, fair play, hard work | Basement, near the kitchens | The Fat Friar |
| **Ravenclaw** | Blue and bronze (film merchandise often shows silver) | Rowena Ravenclaw | Eagle | Wit, learning, wisdom | Ravenclaw Tower | The Grey Lady |

Rules: the House Cup and House points are the only competitive device. Never imply a House is "better", and never use House stereotypes as jokes about a colleague.

## 5. Voice and language rules
- **British English** always (colour, organise, programme, realise). It is canon-correct and also matches Netlight style.
- Address people formally and warmly: "Dear Professor Okonkwo", "Welcome to Hogwarts". Staff are **Professors**; use correct canon titles (Headmaster/Headmistress, Deputy Headmaster/Headmistress, Head of House, Librarian, Matron, Caretaker, Gamekeeper).
- Dates and times as the wizarding world would: "Term begins on 1 September. The Hogwarts Express leaves Platform 9¾, King's Cross, at eleven o'clock." Replies are "by owl, no later than [date]".
- Money in **Galleons, Sickles and Knuts** (1 Galleon = 17 Sickles; 1 Sickle = 29 Knuts).
- Use **real canon vocabulary**, not invented lookalikes: Great Hall, Common Room, Staff Room, Owlery, Hospital Wing, Room of Requirement, Library (Restricted Section), Hogsmeade, Forbidden Forest, Black Lake, Floo Network, Ministry of Magic, Board of Governors, O.W.L.s, N.E.W.T.s, House points, House Cup, the Sorting Hat, Prefects, Head Boy/Girl, Hogwarts Express.
- Subjects (exact names): Transfiguration, Charms, Potions, Defence Against the Dark Arts, Herbology, History of Magic, Astronomy, Divination, Care of Magical Creatures, Arithmancy, Ancient Runes, Muggle Studies, Flying.
- Use **"Muggle"** only for non-magical people or things. Keep spells correctly spelled (Lumos, Nox, Accio, Alohomora, Wingardium Leviosa) and harmless.
- Hogwarts motto: *Draco dormiens nunquam titillandus*. Use as a footer or crest banner, not in running text.
- Easter eggs: **max one per page or slide** (e.g. "Mischief managed." as a final sign-off). Never explain the joke.
- Avoid corporate-speak: synergy, leverage, KPI, stakeholder, bandwidth. Replace per the glossary in section 12.

### Quote policy
Short, well-known lines (≤ one per document) are fine, such as Dumbledore's "Help will always be given at Hogwarts to those who ask for it." Don't reproduce long passages from the books or films; paraphrase.

## 6. Netlight touches (the hybrid layer)
Netlight idea → Hogwarts expression. Use as translation. Don't name-drop "Netlight" in the document body unless the user asks (an optional footer line is allowed, see section 11).

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

## 7. Colour system (digital HEX)
```css
:root {
  /* Hogwarts core */
  --hw-parchment: #F4EAD0;       /* main background (cf. Netlight beige: background only, never text) */
  --hw-parchment-deep: #E4D2A5;  /* cards, panels */
  --hw-ink: #2B1B12;             /* body text (never pure black) */
  --hw-emerald-ink: #0E5A36;     /* letter headings, addresses and signatures (the school writes in emerald-green ink) */
  --hw-midnight: #0D1230;        /* dark mode / enchanted Great Hall ceiling at night */
  --hw-gold: #D3A625;            /* rules, bullets, borders, candlelight */
  --hw-scarlet: #740001;         /* Hogwarts Express, key callouts */
  --hw-wax-purple: #6B3FA0;      /* seal on the acceptance letter (book canon: purple wax) */
  --hw-wax-burgundy: #5A1020;    /* seal alternative (film look) */

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
- The four House colours appear as a **balanced set** (e.g. four equal stripes or tabs) or not at all.
- Knight-Bus purple on parchment is only ~3.9:1 contrast, so use it for **bold or large (≥18px) uppercase labels** only. Body text stays ink.
- Don't use neon yellow as a large fill. Use `--hw-lumos` (pale) for fills.
- Approved Netlight-style pairings: purple + parchment (beige), purple + midnight (black), purple + lumos yellow.
- The purple wax seal is a deliberate Netlight bridge, as it is both canon and on-palette.

## 8. Typography
| Role | Font | Netlight echo |
|---|---|---|
| School wordmark and hero display (all caps, wide tracking; "of" and "and" at ~60% size) | **Cinzel Decorative** or **Cinzel** 700 | Video: caps, display only |
| Headings | **Cinzel** 600–700 | Strong headline weight |
| Body | **EB Garamond** 400, 18px / line-height 1.3–1.5 | Clean, generous whitespace |
| Handwritten notes, signatures, marginalia | **IM Fell English Italic** (sparingly; emerald ink) | none, pure Hogwarts |
| Section tags and small labels | Cinzel uppercase, letter-spacing 0.1em (or Inter 500 if a UI sans is required) | Netlight "section tag" style |

The "Harry Potter" title is a custom logotype. Use the supplied logo file (3.1) rather than typesetting it, and don't mimic it with a look-alike font. Don't mix more than three families.

## 9. Layout, imagery and components

### Layout
- **Sharp corners only** (`border-radius: 0`). Pointed Gothic arches (`clip-path`) are allowed for hero images.
- **Hard offset shadows**, no blur: `box-shadow: 8px 8px 0 0 var(--hw-ink);` (the "stack of parchment" look).
- **Square bullets**, coloured gold: `ul { list-style-type: square; } li::marker { color: var(--hw-gold); }`
- Generous whitespace. Thin double gold rules between sections (`border-top: 3px double var(--hw-gold)`).
- Optional faint ruled-parchment texture, never a busy image.

### Imagery and motifs
- **Grade:** warm and golden for the Classic era (candlelit stone, amber light); cooler blue-grey for darker or post-war themes. Rich contrast, slight grain, optional sepia or black-and-white with a thick ink border.
- **Motifs (use sparingly, one dominant per page):** floating candles, owls and the Owlery, the Hogwarts Express (scarlet engine), the Platform 9¾ sign, the castle on the Black Lake, the enchanted ceiling, moving portraits, wands, the Sorting Hat, the Golden Snitch, quills and parchment, a Marauder's-style footprint path.
- Avoid soft stock photography, distortion, and cartoon "wizard" clichés (star-spangled robes, cheap hat icons).

### Components
- **Wax seal** (`--hw-wax-purple`, with the crest or "H") for official confirmations.
- **Lumos note**: pale-yellow box, ink text, gold left bar, for tips and helpful hints.
- **Restricted Section box**: scarlet border, for policies and safety rules.
- **House stripe**: four equal bars (scarlet / green / blue / yellow) as a footer divider.
- **Footprint path**: dotted line for step-by-step timelines (optional).
- **Platform 9¾ ticket**: for arrival-day details (date, time, platform).

## 10. Document patterns

### The Hogwarts letter (signature format)
Canon anatomy of the acceptance letter, adapt for staff:
1. **Envelope:** heavy, yellowish parchment, address in **emerald-green ink**, sealed with **purple wax** showing the crest.
2. **Letterhead:** HOGWARTS SCHOOL of WITCHCRAFT and WIZARDRY, centred, with the Headmaster's/Headmistress's name and titles beneath it in small type.
3. **Salutation:** "Dear Professor [Surname],".
4. **Opening:** "We are pleased to inform you…" (keep the formal, warm register).
5. **Practical lines:** enclosed list, term start and train time, and the reply deadline: "We await your owl by no later than [date]."
6. **Sign-off:** "Yours sincerely," + name + role (e.g. Deputy Headmistress) + wax seal.
Set headings, address lines and the signature in emerald ink; body in ink on parchment.

### Slides
Cover = midnight with gold crest and Cinzel title. Section break = scarlet or midnight with one Knight-Bus-purple tag. Content = parchment. One idea per slide.

### Web / handbook
Parchment page, sticky midnight header with the crest, Cinzel headings, house-stripe footer, Lumos notes for tips, Restricted Section boxes for rules.

### Instruction pattern
*One wry line of welcome → numbered steps → one Lumos tip.*

## 11. Optional Netlight signature
Allowed once per document, in the footer, small: *"Concept & craft: Netlight"* in Cinzel uppercase 10–11px, Knight-Bus purple. Omit it unless the user wants attribution. No Netlight logo is placed near the crest.

## 12. Glossary: plain business term → Hogwarts voice
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
| Office / workspace | Your classroom, office or tower room |
| Relocation | Your quarters in the castle (staff live at Hogwarts) |
