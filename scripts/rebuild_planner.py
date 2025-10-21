#!/usr/bin/env python3
import json
import os
import sys
from calculator import MovingCalculator
from task_generator import TaskGenerator


def load_user_inputs():
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    input_path = os.path.join(data_dir, 'user_inputs.json')

    try:
        with open(input_path, 'r') as f:
            inputs = json.load(f)
    except FileNotFoundError:
        print("❌ No user inputs found. Please fill out the calculator in index.html first.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Invalid user_inputs.json file. Please check the format.")
        sys.exit(1)

    return inputs


def validate_inputs(inputs):
    if not inputs:
        print("⚠️  Warning: No inputs provided. Nothing to calculate.")
        return False

    has_data = any(v > 0 for v in inputs.values() if isinstance(v, (int, float)))
    if not has_data:
        print("⚠️  Warning: All volumes are 0. Please enter some data first.")
        return False

    return True


def print_summary(task_data):
    print("\n" + "="*60)
    print("                  MOVING PLAN SUMMARY")
    print("="*60)

    print("\n📦 BOX TOTALS (with buffer):")
    totals = task_data['totals']['with_buffer']
    print(f"   Small boxes:    {totals['small']:3d}")
    print(f"   Medium boxes:   {totals['medium']:3d}")
    print(f"   Large boxes:    {totals['large']:3d}")
    print(f"   Wardrobe boxes: {totals['wardrobe']:3d}")
    print(f"   {'─'*25}")
    total_boxes = sum(totals.values())
    print(f"   TOTAL:          {total_boxes:3d} boxes")

    print("\n✅ TASK BREAKDOWN:")
    counts = task_data['task_counts']
    print(f"   Collection tasks:    {counts['collection']:3d}")
    print(f"   Packing tasks:       {counts['packing']:3d}")
    print(f"   Staging tasks:       {counts['staging']:3d}")
    print(f"   Verification tasks:  {counts['verification']:3d}")
    print(f"   {'─'*30}")
    print(f"   TOTAL TASKS:         {counts['total']:3d}")

    print("\n👥 TASK DISTRIBUTION:")
    assignees = task_data['assignee_counts']
    print(f"   Andie's tasks: {assignees['Andie']:3d} (physical work)")
    print(f"   Brad's tasks:  {assignees['Brad']:3d} (organizing, no lifting)")

    print("\n🏠 ROOMS TO PACK:")
    room_count = 0
    for room_name, room_data in task_data['room_totals'].items():
        room_boxes = sum([room_data['small'], room_data['medium'],
                          room_data['large'], room_data['wardrobe']])
        room_count += 1
        cat_count = len(room_data['categories'])
        print(f"   {room_count}. {room_name}: {room_boxes} boxes ({cat_count} categories)")

    print("\n" + "="*60)
    print(f"✅ Plan generated successfully!")
    print(f"   Generated at: {task_data['generated_at']}")
    print("="*60)


def print_day_schedule(task_data):
    print("\n\n📅 PACKING SCHEDULE:")
    print("="*60)

    tasks_by_day = {}
    for task in task_data['tasks']:
        day = task.get('day_label', 'Unscheduled')
        if day not in tasks_by_day:
            tasks_by_day[day] = []
        tasks_by_day[day].append(task)

    for day in sorted(tasks_by_day.keys()):
        if day == 'Unscheduled':
            continue

        print(f"\n{day}")
        print("─" * 60)

        day_tasks = tasks_by_day[day]
        andie_tasks = [t for t in day_tasks if t['assignee'] == 'Andie']
        brad_tasks = [t for t in day_tasks if t['assignee'] == 'Brad']

        print(f"\n  Andie's Tasks ({len(andie_tasks)}):")
        for task in andie_tasks[:5]:
            print(f"    {task['icon']} {task['description']}")
        if len(andie_tasks) > 5:
            print(f"    ... and {len(andie_tasks) - 5} more tasks")

        print(f"\n  Brad's Tasks ({len(brad_tasks)}):")
        for task in brad_tasks[:5]:
            print(f"    {task['icon']} {task['description']}")
        if len(brad_tasks) > 5:
            print(f"    ... and {len(brad_tasks) - 5} more tasks")

    print("\n" + "="*60)


def main():
    print("\n🔄 REBUILDING MOVING PLANNER...")
    print("="*60)

    print("\n1. Loading user inputs...")
    inputs = load_user_inputs()

    if not validate_inputs(inputs):
        return

    print(f"   ✓ Loaded {len(inputs)} input values")

    print("\n2. Calculating box requirements...")
    calculator = MovingCalculator()
    calc_results = calculator.calculate_all(inputs)
    print(f"   ✓ Calculated totals for {len(calc_results['room_totals'])} rooms")

    print("\n3. Generating tasks...")
    generator = TaskGenerator()
    task_data = generator.generate_all_tasks(calc_results)
    print(f"   ✓ Generated {task_data['task_counts']['total']} tasks")

    print("\n4. Saving to file...")
    generator.save_tasks(task_data)
    print_summary(task_data)
    print_day_schedule(task_data)

    print("\n\n💡 NEXT STEPS:")
    print("   1. Refresh index.html in your browser")
    print("   2. Review the generated tasks")
    print("   3. Adjust assignees if needed (Andie ↔ Brad)")
    print("   4. Start checking off tasks as you pack!\n")


if __name__ == "__main__":
    main()
