# Talk Like A Chipmunk!

A one-page concept site for **talklikeachipmunk.com** — a pitch-shifting microphone booth for school fetes, parties and events.

## What's here

```
index.html                              # the website (single file, no build step)
assets/Talk like a chipmunk sign.png    # original artwork
assets/Talk like a chipmunk poster.png  # print-ready poster with URL added
scripts/make_poster.py                  # regenerates the poster
```

## Run locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Deploy

The site is fully static, so any of these will work:

- **Cloudflare Pages** (recommended since the domain is on Cloudflare): create a Pages project → "Direct Upload" → drag the project folder. Then in your domain settings, add a custom domain `talklikeachipmunk.com` and `www.talklikeachipmunk.com`.
- **Netlify / Vercel**: drag-and-drop the folder.
- **GitHub Pages**: push the folder to a repo and enable Pages.

## How the contact form works

The enquiry form posts to **[FormSubmit](https://formsubmit.co)** at:

```
https://formsubmit.co/stephenanning@gmail.com
```

- **First-time setup:** the very first submission will trigger a confirmation email from FormSubmit to `stephenanning@gmail.com`. Click the link in that email once to activate the endpoint. Subsequent submissions will arrive in your inbox immediately.
- No account, no API key, no backend required.
- After activating, you can switch the form `action` to the hashed alias FormSubmit emails you (e.g. `https://formsubmit.co/abcdef0123456789...`) so the public HTML never exposes your raw email address.

If you'd prefer a different provider, swap the `action="..."` URL on the `<form id="enquiry">` tag for any of: Formspree, Getform, Web3Forms, or your own backend.

## Regenerating the poster

```bash
python3 scripts/make_poster.py
```

Output goes to `assets/Talk like a chipmunk poster.png` (1792 × 2700, suitable for A3 printing).
