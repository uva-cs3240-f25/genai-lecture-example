# CS 3240 — Responsible Use of GenAI for Coding (Django Demo)

This repo supports a lecture and in-class demo on **responsible** use of generative AI in software engineering.

## What’s inside
- **Two code paths**: an *AI first draft* (intentionally flawed) and a *reviewed & corrected* version.
- A small **Django project** with a `library` app (Books, Authors, Borrow).
- **Unit tests** showing a weak "AI-ish" test vs a meaningful, constraint-enforcing test.
- A **Canvas-ready HTML** page (`canvas_page.html`) you can paste into UVA Canvas.

## Quick start

```bash
# 1) create venv (recommended)
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) install deps
pip install -r requirements.txt

# 3) migrate & create a superuser
python manage.py migrate
python manage.py createsuperuser

# 4) (optional) seed demo data
python manage.py seed_demo

# 5) run server
python manage.py runserver
```

Visit:
- `/books/` to browse & borrow
- `/books/new/` to create a book (requires `library.add_book` permission)
- `/users/` to show the simple users list demo

## Using this in class
1. Open `library/models.py` and `library/forms.py` **AI first draft** blocks to discuss missing requirements.
2. Switch to the **corrected** blocks (already in the files below the first-draft sections).
3. Run tests:

```bash
pytest -q
```

4. Use `canvas_page.html` for your slides/notes in Canvas.

## Attribution / Citing GenAI
Examples are included in comments and suggested commit messages. Teams should document AI usage in commits and READMEs and **accept responsibility** for all deployed code.
