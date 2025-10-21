#!/usr/bin/env python3
"""
Setup Rooms Configuration
Generates intelligent room and category mappings for the moving planner.
"""

import json
import os

def create_rooms_config():
    """Create comprehensive room configuration with intelligent category mapping."""

    rooms = {
        "Kitchen": {
            "floor": 1,
            "priority": 2,
            "description": "Main kitchen area",
            "categories": [
                {
                    "name": "Dishes & Cookware",
                    "box_type": "medium",
                    "typical_volume": 30,
                    "heavy": False,
                    "fragile": True
                },
                {
                    "name": "Pantry Items",
                    "box_type": "large",
                    "typical_volume": 20,
                    "heavy": False,
                    "fragile": False
                },
                {
                    "name": "Small Appliances",
                    "box_type": "medium",
                    "typical_volume": 15,
                    "heavy": False,
                    "fragile": True
                },
                {
                    "name": "Utensils & Drawers",
                    "box_type": "small",
                    "typical_volume": 10,
                    "heavy": False,
                    "fragile": False
                }
            ]
        },
        "Office": {
            "floor": 2,
            "priority": 2,
            "description": "Home office workspace",
            "categories": [
                {
                    "name": "Books",
                    "box_type": "small",
                    "typical_volume": 25,
                    "heavy": True,
                    "fragile": False
                },
                {
                    "name": "Files & Papers",
                    "box_type": "medium",
                    "typical_volume": 15,
                    "heavy": False,
                    "fragile": False
                },
                {
                    "name": "Electronics",
                    "box_type": "medium",
                    "typical_volume": 20,
                    "heavy": False,
                    "fragile": True
                },
                {
                    "name": "Office Supplies",
                    "box_type": "small",
                    "typical_volume": 10,
                    "heavy": False,
                    "fragile": False
                }
            ]
        },
        "Bedroom": {
            "floor": 2,
            "priority": 3,
            "description": "Main bedroom",
            "categories": [
                {
                    "name": "Clothes (Hanging)",
                    "box_type": "wardrobe",
                    "typical_volume": 30,
                    "heavy": False,
                    "fragile": False
                },
                {
                    "name": "Clothes (Folded)",
                    "box_type": "medium",
                    "typical_volume": 25,
                    "heavy": False,
                    "fragile": False
                },
                {
                    "name": "Shoes & Accessories",
                    "box_type": "medium",
                    "typical_volume": 15,
                    "heavy": False,
                    "fragile": False
                },
                {
                    "name": "Linens & Bedding",
                    "box_type": "large",
                    "typical_volume": 20,
                    "heavy": False,
                    "fragile": False
                },
                {
                    "name": "Personal Items",
                    "box_type": "small",
                    "typical_volume": 10,
                    "heavy": False,
                    "fragile": True
                }
            ]
        },
        "Top Bathroom": {
            "floor": 3,
            "priority": 1,
            "description": "Upstairs bathroom",
            "categories": [
                {
                    "name": "Toiletries",
                    "box_type": "small",
                    "typical_volume": 8,
                    "heavy": False,
                    "fragile": True
                },
                {
                    "name": "Towels & Linens",
                    "box_type": "medium",
                    "typical_volume": 12,
                    "heavy": False,
                    "fragile": False
                },
                {
                    "name": "Medicines & First Aid",
                    "box_type": "small",
                    "typical_volume": 5,
                    "heavy": False,
                    "fragile": True
                },
                {
                    "name": "Cleaning Supplies",
                    "box_type": "small",
                    "typical_volume": 6,
                    "heavy": False,
                    "fragile": False
                }
            ]
        },
        "Lounge": {
            "floor": 2,
            "priority": 3,
            "description": "Lounge area",
            "categories": [
                {
                    "name": "Decor & Art",
                    "box_type": "medium",
                    "typical_volume": 15,
                    "heavy": False,
                    "fragile": True
                },
                {
                    "name": "Media (Books/DVDs)",
                    "box_type": "small",
                    "typical_volume": 12,
                    "heavy": True,
                    "fragile": False
                },
                {
                    "name": "Cushions & Textiles",
                    "box_type": "large",
                    "typical_volume": 10,
                    "heavy": False,
                    "fragile": False
                },
                {
                    "name": "Miscellaneous",
                    "box_type": "medium",
                    "typical_volume": 8,
                    "heavy": False,
                    "fragile": False
                }
            ]
        },
        "Living Room": {
            "floor": 1,
            "priority": 3,
            "description": "Main living area",
            "categories": [
                {
                    "name": "Decor & Art",
                    "box_type": "medium",
                    "typical_volume": 18,
                    "heavy": False,
                    "fragile": True
                },
                {
                    "name": "Media & Books",
                    "box_type": "small",
                    "typical_volume": 15,
                    "heavy": True,
                    "fragile": False
                },
                {
                    "name": "Electronics & Cables",
                    "box_type": "medium",
                    "typical_volume": 12,
                    "heavy": False,
                    "fragile": True
                },
                {
                    "name": "Cushions & Throws",
                    "box_type": "large",
                    "typical_volume": 10,
                    "heavy": False,
                    "fragile": False
                }
            ]
        },
        "Dog Room": {
            "floor": 1,
            "priority": 4,
            "description": "Dedicated pet space",
            "categories": [
                {
                    "name": "Pet Supplies",
                    "box_type": "medium",
                    "typical_volume": 15,
                    "heavy": False,
                    "fragile": False
                },
                {
                    "name": "Toys & Accessories",
                    "box_type": "small",
                    "typical_volume": 8,
                    "heavy": False,
                    "fragile": False
                },
                {
                    "name": "Food & Treats",
                    "box_type": "medium",
                    "typical_volume": 10,
                    "heavy": True,
                    "fragile": False
                },
                {
                    "name": "Bedding & Crates",
                    "box_type": "large",
                    "typical_volume": 12,
                    "heavy": False,
                    "fragile": False
                }
            ]
        },
        "Dining Room": {
            "floor": 1,
            "priority": 2,
            "description": "Formal dining area",
            "categories": [
                {
                    "name": "Dining Ware",
                    "box_type": "medium",
                    "typical_volume": 20,
                    "heavy": False,
                    "fragile": True
                },
                {
                    "name": "Table Linens",
                    "box_type": "medium",
                    "typical_volume": 8,
                    "heavy": False,
                    "fragile": False
                },
                {
                    "name": "Decor & Centerpieces",
                    "box_type": "small",
                    "typical_volume": 10,
                    "heavy": False,
                    "fragile": True
                },
                {
                    "name": "Serving Items",
                    "box_type": "medium",
                    "typical_volume": 12,
                    "heavy": False,
                    "fragile": True
                }
            ]
        },
        "Garage": {
            "floor": 0,
            "priority": 1,
            "description": "Garage storage",
            "categories": [
                {
                    "name": "Tools & Hardware",
                    "box_type": "small",
                    "typical_volume": 20,
                    "heavy": True,
                    "fragile": False
                },
                {
                    "name": "Sports Equipment",
                    "box_type": "large",
                    "typical_volume": 25,
                    "heavy": False,
                    "fragile": False
                },
                {
                    "name": "Storage Boxes",
                    "box_type": "large",
                    "typical_volume": 30,
                    "heavy": True,
                    "fragile": False
                },
                {
                    "name": "Outdoor Gear",
                    "box_type": "medium",
                    "typical_volume": 18,
                    "heavy": False,
                    "fragile": False
                }
            ]
        },
        "Grow Room": {
            "floor": 1,
            "priority": 0,
            "description": "⭐ STAGING AREA - Pack boxes from other rooms here",
            "staging_only": True,
            "categories": []
        },
        "In-Law": {
            "floor": 0,
            "priority": 2,
            "description": "In-law suite living area",
            "categories": [
                {
                    "name": "Mixed Storage",
                    "box_type": "medium",
                    "typical_volume": 20,
                    "heavy": False,
                    "fragile": False
                },
                {
                    "name": "Furniture Items",
                    "box_type": "large",
                    "typical_volume": 15,
                    "heavy": True,
                    "fragile": False
                },
                {
                    "name": "Miscellaneous",
                    "box_type": "medium",
                    "typical_volume": 12,
                    "heavy": False,
                    "fragile": False
                }
            ]
        },
        "In-Law Bedroom": {
            "floor": 0,
            "priority": 2,
            "description": "In-law suite bedroom",
            "categories": [
                {
                    "name": "Clothes & Accessories",
                    "box_type": "medium",
                    "typical_volume": 20,
                    "heavy": False,
                    "fragile": False
                },
                {
                    "name": "Linens & Bedding",
                    "box_type": "large",
                    "typical_volume": 15,
                    "heavy": False,
                    "fragile": False
                },
                {
                    "name": "Personal Items",
                    "box_type": "small",
                    "typical_volume": 10,
                    "heavy": False,
                    "fragile": True
                }
            ]
        },
        "Patio": {
            "floor": 0,
            "priority": 1,
            "description": "Outdoor patio area",
            "categories": [
                {
                    "name": "Outdoor Furniture",
                    "box_type": "large",
                    "typical_volume": 25,
                    "heavy": True,
                    "fragile": False
                },
                {
                    "name": "Plants & Planters",
                    "box_type": "medium",
                    "typical_volume": 15,
                    "heavy": False,
                    "fragile": True
                },
                {
                    "name": "Grilling Equipment",
                    "box_type": "medium",
                    "typical_volume": 12,
                    "heavy": False,
                    "fragile": False
                },
                {
                    "name": "Outdoor Decor",
                    "box_type": "small",
                    "typical_volume": 10,
                    "heavy": False,
                    "fragile": True
                }
            ]
        }
    }

    return rooms


def create_calculation_formulas():
    """Define box calculation formulas and constants."""

    formulas = {
        "box_sizes": {
            "small": 1.0,
            "medium": 3.0,
            "large": 4.5,
            "wardrobe": 1.5
        },
        "buffer_percentage": 0.15,
        "packing_efficiency": {
            "small": 0.85,
            "medium": 0.90,
            "large": 0.88,
            "wardrobe": 0.95
        },
        "assignment_rules": {
            "physical_tasks": "Andie",
            "organizational_tasks": "Brad",
            "no_lifting_assignee": "Brad"
        }
    }

    return formulas


def create_task_templates():
    """Define task templates for generation."""

    templates = {
        "collection": {
            "template": "Gather all {category} in {room}",
            "type": "collection",
            "icon": "🔍",
            "default_assignee": "either"
        },
        "packing": {
            "template": "Pack {box_count} {box_type} boxes: {room} - {category}",
            "type": "packing",
            "icon": "📦",
            "default_assignee": "Andie"
        },
        "staging": {
            "template": "Move {box_count} packed boxes to Grow Room staging area",
            "type": "staging",
            "icon": "🚚",
            "default_assignee": "Andie"
        },
        "verification": {
            "template": "Final sweep: {room} - verify {category} section empty",
            "type": "verification",
            "icon": "✅",
            "default_assignee": "Brad"
        }
    }

    return templates


def main():
    """Main setup function."""

    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)

    # Generate configurations
    rooms = create_rooms_config()
    formulas = create_calculation_formulas()
    templates = create_task_templates()

    # Write configuration files (always safe to regenerate)
    with open(os.path.join(data_dir, 'rooms_config.json'), 'w') as f:
        json.dump(rooms, f, indent=2)

    with open(os.path.join(data_dir, 'calculation_formulas.json'), 'w') as f:
        json.dump(formulas, f, indent=2)

    with open(os.path.join(data_dir, 'task_templates.json'), 'w') as f:
        json.dump(templates, f, indent=2)

    # Create user_inputs.json only if it doesn't exist (preserve user data)
    user_inputs_path = os.path.join(data_dir, 'user_inputs.json')
    if not os.path.exists(user_inputs_path):
        with open(user_inputs_path, 'w') as f:
            json.dump({}, f, indent=2)
        print("   - Created empty user_inputs.json")
    else:
        print("   - Preserved existing user_inputs.json")

    # Create generated_tasks.json only if it doesn't exist (preserve generated tasks)
    tasks_path = os.path.join(data_dir, 'generated_tasks.json')
    if not os.path.exists(tasks_path):
        with open(tasks_path, 'w') as f:
            json.dump({"tasks": [], "totals": {}}, f, indent=2)
        print("   - Created empty generated_tasks.json")
    else:
        print("   - Preserved existing generated_tasks.json")

    print("\n✅ Configuration setup complete!")
    print(f"   - {len(rooms)} rooms configured")
    print(f"   - Data directory: {data_dir}")


if __name__ == "__main__":
    main()
