# Moving Planner

Data-driven moving task planner for Brad & Andie's SF → San Rafael move.

## Features

- Room-by-room box calculations with optimized formulas
- Auto-generated tasks (Collection, Packing, Staging, Verification)
- Smart task assignment (Andie: physical, Brad: organizational)
- Day-by-day packing schedule (Oct 22-24)
- Static GitHub Pages deployment
- Task completion tracking via localStorage
- Reassignment dropdowns for flexible planning

## Local Development

### Prerequisites

- Python 3.x (no external dependencies)

### Workflow

1. **Edit volumes**: Update `data/user_inputs.json` with your room volumes
   ```json
   {
     "Kitchen_Dishes & Cookware": 30,
     "Office_Books": 25
   }
   ```

2. **Generate tasks**: Run the task calculation script
   ```bash
   python3 scripts/rebuild_planner.py
   ```

3. **Create static HTML**: Generate the deployable HTML
   ```bash
   python3 scripts/generate_static.py
   ```

4. **Test locally**: Open `docs/index.html` in your browser

5. **Deploy**: Commit and push to GitHub
   ```bash
   git add -A
   git commit -m "Update moving tasks"
   git push
   ```

## Project Structure

```
/
├── scripts/               # Python build tools
│   ├── calculator.py      # Box calculation engine
│   ├── task_generator.py  # Task generation logic
│   ├── rebuild_planner.py # Main orchestrator
│   └── generate_static.py # Static HTML generator
├── data/                  # Configuration & data
│   ├── rooms_config.json          # Room definitions
│   ├── calculation_formulas.json  # Box sizes & formulas
│   ├── task_templates.json        # Task type templates
│   ├── user_inputs.json           # Your volume estimates
│   └── generated_tasks.json       # Generated task data
└── docs/                  # GitHub Pages deployment
    └── index.html         # Generated static HTML
```

## GitHub Pages Setup

1. Push this repository to GitHub
2. Go to Settings → Pages
3. Set Source to "Deploy from a branch"
4. Select branch: `main`, folder: `/docs`
5. Click Save

Your planner will be live at: `https://<username>.github.io/<repo-name>/`

## Configuration

### Box Calculations

Edit `data/calculation_formulas.json`:

```json
{
  "box_sizes": {
    "small": 1.5,
    "large": 8.5,
    "wardrobe": 2.8
  },
  "buffer_percentage": 0.08,
  "packing_efficiency": {
    "small": 0.98,
    "large": 0.98,
    "wardrobe": 0.99
  }
}
```

### Room Setup

Edit `data/rooms_config.json` to modify rooms, categories, priorities, and floor assignments.

### Packing Schedule

Modify dates in `scripts/task_generator.py` (lines 102-107):

```python
packing_days = ['2025-10-22', '2025-10-23', '2025-10-24']
```

## Task Types

1. **Collection** (🔍): Gather all items in category
2. **Packing** (📦): Pack calculated number of boxes
3. **Staging** (🚚): Move to Grow Room staging area
4. **Verification** (✅): Final sweep to ensure nothing left

## Moving Timeline

- **Oct 20-21**: Setup & planning
- **Oct 22-24**: Pack all rooms
- **Oct 25**: Pet transport day
- **Oct 26**: Moving day

## Tech Stack

- **Python 3**: Calculation engine & task generation
- **Vanilla JavaScript**: Client-side interactivity
- **localStorage**: Task persistence
- **GitHub Pages**: Static hosting
- **Dark mode CSS**: Custom theming

## Notes

- Grow Room is staging area only (no packing)
- Box estimates include 8% buffer
- Large boxes preferred for efficiency
- All scripts are idempotent (safe to re-run)

---

**Status**: Active project for October 2025 move
**Deployed at**: GitHub Pages (configure in Settings)
