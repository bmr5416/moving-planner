#!/usr/bin/env python3
import json
import os
from datetime import datetime

class StaticHTMLGenerator:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.output_dir = os.path.join(os.path.dirname(__file__), '..', 'docs')

    def load_task_data(self):
        task_file = os.path.join(self.data_dir, 'generated_tasks.json')
        with open(task_file, 'r') as f:
            return json.load(f)

    def generate_html(self, task_data):
        tasks_json = json.dumps(task_data, indent=2)

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Moving Planner | SF → San Rafael</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        :root {{
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-tertiary: #334155;
            --surface: #1e293b;
            --surface-hover: #334155;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --border: #334155;
            --border-light: #475569;
            --primary: #3b82f6;
            --primary-dark: #2563eb;
            --success: #22c55e;
            --warning: #f59e0b;
            --danger: #ef4444;
            --info: #06b6d4;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
            --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.4);
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 20px;
        }}

        .container {{ max-width: 1400px; margin: 0 auto; }}

        header {{
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: white;
            padding: 30px;
            border-radius: 16px;
            margin-bottom: 30px;
            box-shadow: var(--shadow-lg);
        }}

        header h1 {{ font-size: 2rem; margin-bottom: 10px; }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}

        .stat-card {{
            background: rgba(255,255,255,0.15);
            padding: 15px;
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }}

        .stat-card .label {{ font-size: 0.85rem; opacity: 0.9; margin-bottom: 5px; }}
        .stat-card .value {{ font-size: 1.5rem; font-weight: 700; }}

        .section {{
            background: var(--surface);
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: var(--shadow);
            border: 1px solid var(--border);
        }}

        .section h2 {{
            color: var(--primary);
            margin-bottom: 20px;
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .progress-bar {{
            background: var(--bg-tertiary);
            height: 10px;
            border-radius: 5px;
            overflow: hidden;
            margin-bottom: 15px;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--success), #22c55e);
            transition: width 0.3s ease;
        }}

        .day-tasks {{ margin-bottom: 30px; }}

        .day-header-bar {{
            background: var(--bg-tertiary);
            padding: 15px 20px;
            border-radius: 8px 8px 0 0;
            border: 1px solid var(--border);
            font-weight: 600;
            font-size: 1.1rem;
        }}

        .day-content {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-top: none;
            border-radius: 0 0 8px 8px;
            padding: 10px;
        }}

        .room-section {{
            background: var(--bg-primary);
            margin-bottom: 15px;
            border-radius: 8px;
            border: 1px solid var(--border);
            overflow: hidden;
        }}

        .room-header {{
            background: var(--bg-tertiary);
            padding: 12px 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s;
        }}

        .room-header:hover {{
            background: var(--surface-hover);
        }}

        .room-header.active {{
            background: var(--primary);
        }}

        .room-title {{
            font-weight: 600;
            font-size: 1.05rem;
        }}

        .room-progress {{
            font-size: 0.85rem;
            opacity: 0.8;
            margin-left: 10px;
        }}

        .room-icon {{
            font-size: 1rem;
            transition: transform 0.3s;
        }}

        .room-header.active .room-icon {{
            transform: rotate(180deg);
        }}

        .room-content {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
        }}

        .room-content.active {{
            max-height: 5000px;
        }}

        .room-columns {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            padding: 15px;
        }}

        .person-column {{
            background: var(--bg-secondary);
            padding: 12px;
            border-radius: 6px;
        }}

        .person-column-header {{
            font-weight: 600;
            font-size: 0.95rem;
            margin-bottom: 12px;
            padding: 8px;
            background: var(--bg-tertiary);
            border-radius: 6px;
            text-align: center;
        }}

        .category-group {{
            margin-bottom: 20px;
            padding-left: 8px;
            border-left: 3px solid var(--primary);
        }}

        .category-header {{
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 8px;
            padding: 4px 8px;
            background: rgba(59, 130, 246, 0.1);
            border-radius: 4px;
        }}

        .task-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            background: var(--bg-primary);
            border-radius: 6px;
            margin-bottom: 6px;
            border: 1px solid var(--border);
            transition: all 0.2s;
        }}

        .task-item:hover {{
            background: var(--bg-tertiary);
            border-color: var(--primary);
        }}

        .task-item.completed {{ opacity: 0.5; }}
        .task-item.completed .task-text {{ text-decoration: line-through; }}

        .task-item input[type="checkbox"] {{
            width: 18px;
            height: 18px;
            cursor: pointer;
        }}

        .task-text {{
            flex: 1;
            font-size: 0.95rem;
            cursor: pointer;
        }}

        .task-assignee-select {{
            padding: 5px 8px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--text-primary);
            cursor: pointer;
            font-size: 0.8rem;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }}

        .badge-primary {{
            background: rgba(59, 130, 246, 0.2);
            color: var(--primary);
            border: 1px solid var(--primary);
        }}

        .badge-success {{
            background: rgba(34, 197, 94, 0.2);
            color: var(--success);
            border: 1px solid var(--success);
        }}

        .badge-warning {{
            background: rgba(245, 158, 11, 0.2);
            color: var(--warning);
            border: 1px solid var(--warning);
        }}

        @media (max-width: 768px) {{
            .room-columns {{ grid-template-columns: 1fr; }}
            .stats {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏠 Moving Planner</h1>
            <p>Brad & Andie • Archie, Indie & Ozzy • SF → San Rafael</p>
            <div class="stats">
                <div class="stat-card">
                    <div class="label">Days Until Movers</div>
                    <div class="value" id="daysUntilMove">-</div>
                </div>
                <div class="stat-card">
                    <div class="label">Total Boxes Needed</div>
                    <div class="value" id="totalBoxes">0</div>
                </div>
                <div class="stat-card">
                    <div class="label">Total Tasks</div>
                    <div class="value" id="totalTasks">0</div>
                </div>
                <div class="stat-card">
                    <div class="label">Rooms to Pack</div>
                    <div class="value" id="totalRooms">0</div>
                </div>
            </div>
        </header>

        <div class="section">
            <h2>✅ Moving Tasks (Room-by-Room)</h2>
            <div class="progress-bar">
                <div class="progress-fill" id="taskProgress" style="width: 0%"></div>
            </div>
            <p style="margin-bottom: 20px; color: var(--text-secondary);">
                <span id="taskStats">Loading tasks...</span>
            </p>
            <div id="tasksContainer"></div>
        </div>
    </div>

    <script>
        const taskData = {tasks_json};

        function init() {{
            loadTaskCompletions();
            loadTaskReassignments();
            displayTasks();
            updateStats();
        }}

        function displayTasks() {{
            const container = document.getElementById('tasksContainer');
            if (!taskData.tasks || taskData.tasks.length === 0) {{
                container.innerHTML = '<p style="color: var(--text-secondary);">No tasks available.</p>';
                return;
            }}

            const tasksByDay = {{}};
            taskData.tasks.forEach(task => {{
                const day = task.day_label || 'Unscheduled';
                if (!tasksByDay[day]) tasksByDay[day] = {{}};
                const room = task.room;
                if (!tasksByDay[day][room]) tasksByDay[day][room] = [];
                tasksByDay[day][room].push(task);
            }});

            container.innerHTML = '';

            Object.entries(tasksByDay).forEach(([day, rooms]) => {{
                const dayDiv = document.createElement('div');
                dayDiv.className = 'day-tasks';

                const dayHeader = document.createElement('div');
                dayHeader.className = 'day-header-bar';
                dayHeader.textContent = day;

                const dayContent = document.createElement('div');
                dayContent.className = 'day-content';

                Object.entries(rooms).forEach(([room, tasks]) => {{
                    const roomSection = createRoomSection(room, tasks, day);
                    dayContent.appendChild(roomSection);
                }});

                dayDiv.appendChild(dayHeader);
                dayDiv.appendChild(dayContent);
                container.appendChild(dayDiv);
            }});

            updateTaskStats();
        }}

        function createRoomSection(room, tasks, day) {{
            const section = document.createElement('div');
            section.className = 'room-section';

            const completed = tasks.filter(t => t.completed).length;
            const total = tasks.length;
            const progress = total > 0 ? Math.round((completed / total) * 100) : 0;

            const header = document.createElement('div');
            header.className = 'room-header';
            header.onclick = () => toggleRoom(header);

            const titleDiv = document.createElement('div');
            titleDiv.style.display = 'flex';
            titleDiv.style.alignItems = 'center';

            const title = document.createElement('span');
            title.className = 'room-title';
            title.textContent = room;

            const progressText = document.createElement('span');
            progressText.className = 'room-progress';
            progressText.textContent = `(${{completed}}/${{total}} - ${{progress}}%)`;

            titleDiv.appendChild(title);
            titleDiv.appendChild(progressText);

            const icon = document.createElement('div');
            icon.className = 'room-icon';
            icon.textContent = '▼';

            header.appendChild(titleDiv);
            header.appendChild(icon);

            const content = document.createElement('div');
            content.className = 'room-content';

            const columns = document.createElement('div');
            columns.className = 'room-columns';

            const andieCol = document.createElement('div');
            andieCol.className = 'person-column';
            const andieHeader = document.createElement('div');
            andieHeader.className = 'person-column-header';
            andieHeader.innerHTML = '<span class="badge badge-success">Andie</span>';
            andieCol.appendChild(andieHeader);

            const bradCol = document.createElement('div');
            bradCol.className = 'person-column';
            const bradHeader = document.createElement('div');
            bradHeader.className = 'person-column-header';
            bradHeader.innerHTML = '<span class="badge badge-primary">Brad</span>';
            bradCol.appendChild(bradHeader);

            const tasksByCategory = {{}};
            tasks.forEach(task => {{
                const category = task.category;
                if (!tasksByCategory[category]) tasksByCategory[category] = [];
                tasksByCategory[category].push(task);
            }});

            Object.entries(tasksByCategory).forEach(([category, catTasks]) => {{
                const andieTasks = catTasks.filter(t => t.assignee === 'Andie');
                const bradTasks = catTasks.filter(t => t.assignee === 'Brad');

                if (andieTasks.length > 0) {{
                    const categoryGroup = createCategoryGroup(category, andieTasks);
                    andieCol.appendChild(categoryGroup);
                }}

                if (bradTasks.length > 0) {{
                    const categoryGroup = createCategoryGroup(category, bradTasks);
                    bradCol.appendChild(categoryGroup);
                }}
            }});

            columns.appendChild(andieCol);
            columns.appendChild(bradCol);
            content.appendChild(columns);

            section.appendChild(header);
            section.appendChild(content);

            return section;
        }}

        function createCategoryGroup(category, tasks) {{
            const group = document.createElement('div');
            group.className = 'category-group';

            const header = document.createElement('div');
            header.className = 'category-header';
            header.textContent = category;

            group.appendChild(header);

            tasks.sort((a, b) => (a.order || 0) - (b.order || 0));

            tasks.forEach(task => {{
                group.appendChild(createTaskElement(task));
            }});

            return group;
        }}

        function createTaskElement(task) {{
            const taskDiv = document.createElement('div');
            taskDiv.className = 'task-item';
            if (task.completed) taskDiv.classList.add('completed');

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.checked = task.completed;
            checkbox.onchange = () => toggleTask(task.id);

            const text = document.createElement('div');
            text.className = 'task-text';
            text.textContent = `${{task.icon}} ${{task.description}}`;
            text.onclick = () => checkbox.click();

            const select = document.createElement('select');
            select.className = 'task-assignee-select';
            select.innerHTML = `
                <option value="Andie" ${{task.assignee === 'Andie' ? 'selected' : ''}}>Andie</option>
                <option value="Brad" ${{task.assignee === 'Brad' ? 'selected' : ''}}>Brad</option>
            `;
            select.onchange = () => reassignTask(task.id, select.value);

            taskDiv.appendChild(checkbox);
            taskDiv.appendChild(text);
            taskDiv.appendChild(select);

            return taskDiv;
        }}

        function toggleRoom(header) {{
            header.classList.toggle('active');
            const content = header.nextElementSibling;
            content.classList.toggle('active');
        }}

        function toggleTask(taskId) {{
            const task = taskData.tasks.find(t => t.id === taskId);
            if (task) {{
                task.completed = !task.completed;
                saveTaskCompletions();
                displayTasks();
            }}
        }}

        function reassignTask(taskId, newAssignee) {{
            const task = taskData.tasks.find(t => t.id === taskId);
            if (task) {{
                task.assignee = newAssignee;
                saveTaskReassignments();
                displayTasks();
            }}
        }}

        function saveTaskCompletions() {{
            const completions = taskData.tasks.reduce((acc, t) => {{
                acc[t.id] = t.completed || false;
                return acc;
            }}, {{}});
            localStorage.setItem('taskCompletions', JSON.stringify(completions));
        }}

        function loadTaskCompletions() {{
            const saved = localStorage.getItem('taskCompletions');
            if (saved) {{
                const completions = JSON.parse(saved);
                taskData.tasks.forEach(task => {{
                    if (completions[task.id] !== undefined) {{
                        task.completed = completions[task.id];
                    }}
                }});
            }}
        }}

        function saveTaskReassignments() {{
            const assignments = taskData.tasks.reduce((acc, t) => {{
                acc[t.id] = t.assignee;
                return acc;
            }}, {{}});
            localStorage.setItem('taskAssignments', JSON.stringify(assignments));
        }}

        function loadTaskReassignments() {{
            const saved = localStorage.getItem('taskAssignments');
            if (saved) {{
                const assignments = JSON.parse(saved);
                taskData.tasks.forEach(task => {{
                    if (assignments[task.id]) {{
                        task.assignee = assignments[task.id];
                    }}
                }});
            }}
        }}

        function updateTaskStats() {{
            const completed = taskData.tasks.filter(t => t.completed).length;
            const total = taskData.tasks.length;
            const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;

            document.getElementById('taskStats').textContent =
                `${{completed}} of ${{total}} tasks completed (${{percentage}}%)`;
            document.getElementById('taskProgress').style.width = `${{percentage}}%`;
        }}

        function updateStats() {{
            const moveDate = new Date('2025-10-26');
            const today = new Date();
            const daysUntil = Math.ceil((moveDate - today) / (1000 * 60 * 60 * 24));
            document.getElementById('daysUntilMove').textContent = daysUntil > 0 ? daysUntil : '0';

            if (taskData.task_counts) {{
                document.getElementById('totalTasks').textContent = taskData.task_counts.total;
            }}

            if (taskData.room_totals) {{
                document.getElementById('totalRooms').textContent = Object.keys(taskData.room_totals).length;
            }}

            if (taskData.totals && taskData.totals.with_buffer) {{
                const totals = taskData.totals.with_buffer;
                const totalBoxes = totals.small + totals.medium + totals.large + totals.wardrobe;
                document.getElementById('totalBoxes').textContent = totalBoxes;
            }}
        }}

        document.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>'''

        return html

    def save_html(self, html):
        os.makedirs(self.output_dir, exist_ok=True)
        output_file = os.path.join(self.output_dir, 'index.html')

        with open(output_file, 'w') as f:
            f.write(html)

        print(f"✅ Static HTML generated: {output_file}")
        return output_file


def main():
    generator = StaticHTMLGenerator()

    print("=" * 60)
    print("  GENERATING STATIC HTML FOR GITHUB PAGES")
    print("=" * 60)
    print()

    print("📂 Loading task data...")
    task_data = generator.load_task_data()

    if not task_data.get('tasks'):
        print("⚠️  No tasks found. Run rebuild_planner.py first!")
        return

    print(f"✅ Loaded {len(task_data['tasks'])} tasks")
    print()

    print("🎨 Generating HTML...")
    html = generator.generate_html(task_data)

    print("💾 Saving to /docs...")
    output_path = generator.save_html(html)

    print()
    print("=" * 60)
    print("  SUCCESS!")
    print("=" * 60)
    print()
    print(f"📄 Static HTML created at: {output_path}")
    print()
    print("Next steps:")
    print("  1. Open docs/index.html in your browser to test")
    print("  2. Commit and push to GitHub")
    print("  3. GitHub Pages will auto-update")
    print()


if __name__ == "__main__":
    main()
