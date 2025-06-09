import json
import argparse
from pathlib import Path

DATA_FILE = Path('tasks.json')

def load_tasks():
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_tasks(tasks):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def add_task(args):
    tasks = load_tasks()
    project = tasks.setdefault(args.project, [])
    task = {
        'title': args.title,
        'status': 'todo'
    }
    project.append(task)
    save_tasks(tasks)
    print(f"Task added to project '{args.project}': {args.title}")

def list_tasks(args):
    tasks = load_tasks()
    project_tasks = tasks.get(args.project, [])
    if not project_tasks:
        print(f'No tasks found for project {args.project}')
        return
    for idx, task in enumerate(project_tasks, 1):
        status = '✓' if task['status'] == 'done' else ' '
        print(f"{idx}. [{status}] {task['title']}")

def mark_done(args):
    tasks = load_tasks()
    project_tasks = tasks.get(args.project, [])
    if args.index < 1 or args.index > len(project_tasks):
        print('Invalid task index')
        return
    project_tasks[args.index - 1]['status'] = 'done'
    save_tasks(tasks)
    print('Task marked as done')

def main():
    parser = argparse.ArgumentParser(description='Personal task manager for Figma design projects.')
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('project', help='Project name')
    add_parser.add_argument('title', help='Task description')
    add_parser.set_defaults(func=add_task)

    list_parser = subparsers.add_parser('list', help='List project tasks')
    list_parser.add_argument('project', help='Project name')
    list_parser.set_defaults(func=list_tasks)

    done_parser = subparsers.add_parser('done', help='Mark a task as done')
    done_parser.add_argument('project', help='Project name')
    done_parser.add_argument('index', type=int, help='Task index from list')
    done_parser.set_defaults(func=mark_done)

    args = parser.parse_args()
    if not hasattr(args, 'func'):
        parser.print_help()
        return
    args.func(args)

if __name__ == '__main__':
    main()
