#!/usr/bin/env python3
import json
import math
import os


class MovingCalculator:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.load_configs()

    def load_configs(self):
        with open(os.path.join(self.data_dir, 'rooms_config.json'), 'r') as f:
            self.rooms = json.load(f)
        with open(os.path.join(self.data_dir, 'calculation_formulas.json'), 'r') as f:
            self.formulas = json.load(f)

    def calculate_boxes_for_category(self, volume, box_type):
        if volume <= 0:
            return 0
        box_size = self.formulas['box_sizes'][box_type]
        efficiency = self.formulas['packing_efficiency'][box_type]
        effective_volume = box_size * efficiency
        return math.ceil(volume / effective_volume)

    def calculate_room_totals(self, user_inputs):
        room_totals = {}

        for room_name, room_data in self.rooms.items():
            if room_data.get('staging_only'):
                continue

            room_total = {
                'small': 0,
                'medium': 0,
                'large': 0,
                'wardrobe': 0,
                'categories': {}
            }

            for category in room_data['categories']:
                cat_name = category['name']
                input_key = f"{room_name}_{cat_name}"

                if input_key in user_inputs and user_inputs[input_key] > 0:
                    volume = user_inputs[input_key]
                    box_type = category['box_type']
                    boxes = self.calculate_boxes_for_category(volume, box_type)

                    # Add to room total
                    room_total[box_type] += boxes

                    # Store category details
                    room_total['categories'][cat_name] = {
                        'volume': volume,
                        'box_type': box_type,
                        'boxes': boxes,
                        'heavy': category.get('heavy', False),
                        'fragile': category.get('fragile', False)
                    }

            if sum([room_total['small'], room_total['medium'],
                    room_total['large'], room_total['wardrobe']]) > 0:
                room_totals[room_name] = room_total

        return room_totals

    def calculate_grand_totals(self, room_totals):
        grand_totals = {'small': 0, 'medium': 0, 'large': 0, 'wardrobe': 0}

        for room_data in room_totals.values():
            for box_type in grand_totals.keys():
                grand_totals[box_type] += room_data[box_type]

        buffer = self.formulas['buffer_percentage']
        buffered_totals = {}
        for box_type, count in grand_totals.items():
            buffered_totals[box_type] = math.ceil(count * (1 + buffer))

        return {
            'base': grand_totals,
            'with_buffer': buffered_totals,
            'buffer_percentage': buffer * 100
        }

    def get_room_priority_order(self):
        priority_list = []
        for room_name, room_data in self.rooms.items():
            if room_data.get('staging_only'):
                continue
            priority = room_data.get('priority', 5)
            floor = room_data.get('floor', 0)
            priority_list.append((room_name, priority, floor))

        priority_list.sort(key=lambda x: (x[1], -x[2]))
        return priority_list

    def calculate_all(self, user_inputs):
        room_totals = self.calculate_room_totals(user_inputs)
        grand_totals = self.calculate_grand_totals(room_totals)
        priority_order = self.get_room_priority_order()

        return {
            'room_totals': room_totals,
            'grand_totals': grand_totals,
            'priority_order': [(room, pri, floor) for room, pri, floor in priority_order
                                if room in room_totals],
            'timestamp': self.get_timestamp()
        }

    @staticmethod
    def get_timestamp():
        from datetime import datetime
        return datetime.now().isoformat()
