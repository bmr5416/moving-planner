#!/usr/bin/env python3
import json
import os
from datetime import datetime, timedelta


class TaskGenerator:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.load_configs()

    def load_configs(self):
        with open(os.path.join(self.data_dir, 'rooms_config.json'), 'r') as f:
            self.rooms = json.load(f)
        with open(os.path.join(self.data_dir, 'task_templates.json'), 'r') as f:
            self.templates = json.load(f)
        with open(os.path.join(self.data_dir, 'calculation_formulas.json'), 'r') as f:
            self.formulas = json.load(f)

    def determine_staging_area(self, floor):
        return "Lounge" if floor >= 2 else "Grow Room"

    def is_laundry_category(self, category_name, room_name):
        laundry_keywords = ['clothes', 'linens', 'bedding']
        laundry_rooms = ['Bedroom', 'In-Law Bedroom', 'Garage']
        category_lower = category_name.lower()
        return room_name in laundry_rooms and any(kw in category_lower for kw in laundry_keywords)

    def generate_tasks_for_category(self, room_name, category_name, category_data):
        tasks = []
        box_count = category_data['boxes']
        box_type = category_data['box_type']
        is_heavy = category_data.get('heavy', False)
        is_fragile = category_data.get('fragile', False)

        room_floor = self.rooms[room_name]['floor']
        staging_area = self.determine_staging_area(room_floor)
        is_laundry = self.is_laundry_category(category_name, room_name)

        if is_laundry:
            collection_desc = f"🧺 WASH FIRST: Do all laundry for {category_name}. Once clean and dry, gather in {room_name}. Keep ONLY this week's outfits unpacked."
            collection_icon = "🧺"
        else:
            collection_desc = self.templates['collection']['template'].format(
                category=category_name.lower(),
                room=room_name
            )
            collection_icon = self.templates['collection']['icon']

        collection_task = {
            'id': f"{room_name}_{category_name}_collection",
            'type': 'collection',
            'icon': collection_icon,
            'room': room_name,
            'category': category_name,
            'description': collection_desc,
            'assignee': 'Brad' if not is_heavy else 'Andie',
            'completed': False,
            'day': None,
            'order': 1,
            'is_laundry': is_laundry
        }
        tasks.append(collection_task)
        packing_desc = self.templates['packing']['template'].format(
            box_count=box_count,
            box_type=box_type,
            room=room_name,
            category=category_name
        )
        if is_laundry:
            packing_desc += " (clean laundry only, this week's outfits stay out)"

        packing_task = {
            'id': f"{room_name}_{category_name}_packing",
            'type': 'packing',
            'icon': self.templates['packing']['icon'],
            'room': room_name,
            'category': category_name,
            'box_count': box_count,
            'box_type': box_type,
            'description': packing_desc,
            'assignee': 'Andie',
            'completed': False,
            'day': None,
            'order': 2,
            'heavy': is_heavy,
            'fragile': is_fragile,
            'is_laundry': is_laundry
        }
        tasks.append(packing_task)
        staging_task = {
            'id': f"{room_name}_{category_name}_staging",
            'type': 'staging',
            'icon': self.templates['staging']['icon'],
            'room': room_name,
            'category': category_name,
            'box_count': box_count,
            'staging_area': staging_area,
            'description': f"Move {box_count} {box_type} boxes to {staging_area} staging area (Floor {room_floor}) - {room_name}: {category_name}",
            'assignee': 'Andie',
            'completed': False,
            'day': None,
            'order': 3
        }
        tasks.append(staging_task)
        verification_desc = self.templates['verification']['template'].format(
            room=room_name,
            category=category_name.lower()
        )
        if is_laundry:
            verification_desc = f"Final sweep: {room_name} - verify only this week's {category_name.lower()} remain, all else packed"

        verification_task = {
            'id': f"{room_name}_{category_name}_verification",
            'type': 'verification',
            'icon': self.templates['verification']['icon'],
            'room': room_name,
            'category': category_name,
            'description': verification_desc,
            'assignee': 'Brad',
            'completed': False,
            'day': None,
            'order': 4,
            'is_laundry': is_laundry
        }
        tasks.append(verification_task)

        return tasks

    def assign_tasks_to_days(self, tasks, priority_order):
        packing_days = ['2025-10-22', '2025-10-23', '2025-10-24']
        day_labels = {
            '2025-10-22': 'Tuesday, October 22',
            '2025-10-23': 'Wednesday, October 23',
            '2025-10-24': 'Thursday, October 24'
        }

        rooms_per_day = max(1, len(priority_order) // len(packing_days))
        day_index = 0
        room_count = 0

        for room_name, priority, floor in priority_order:
            room_tasks = [t for t in tasks if t['room'] == room_name]
            for task in room_tasks:
                task['day'] = packing_days[day_index]
                task['day_label'] = day_labels[packing_days[day_index]]
            room_count += 1
            if room_count >= rooms_per_day and day_index < len(packing_days) - 1:
                day_index += 1
                room_count = 0

        return tasks

    def generate_all_tasks(self, calculation_results):
        all_tasks = []

        for room_name, room_data in calculation_results['room_totals'].items():
            for category_name, category_data in room_data['categories'].items():
                tasks = self.generate_tasks_for_category(
                    room_name, category_name, category_data
                )
                all_tasks.extend(tasks)

        priority_order = calculation_results['priority_order']
        all_tasks = self.assign_tasks_to_days(all_tasks, priority_order)
        all_tasks.sort(key=lambda x: (x['day'] or '9999', x['room'], x['order']))

        return {
            'tasks': all_tasks,
            'totals': calculation_results['grand_totals'],
            'room_totals': calculation_results['room_totals'],
            'task_counts': {
                'collection': len([t for t in all_tasks if t['type'] == 'collection']),
                'packing': len([t for t in all_tasks if t['type'] == 'packing']),
                'staging': len([t for t in all_tasks if t['type'] == 'staging']),
                'verification': len([t for t in all_tasks if t['type'] == 'verification']),
                'total': len(all_tasks)
            },
            'assignee_counts': {
                'Andie': len([t for t in all_tasks if t['assignee'] == 'Andie']),
                'Brad': len([t for t in all_tasks if t['assignee'] == 'Brad'])
            },
            'generated_at': datetime.now().isoformat()
        }

    def save_tasks(self, task_data):
        output_path = os.path.join(self.data_dir, 'generated_tasks.json')
        with open(output_path, 'w') as f:
            json.dump(task_data, f, indent=2)
        print(f"✅ Tasks saved to {output_path}")
