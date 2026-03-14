import sys


def main():
    # Keep backward compatibility for older "python src/main.py" instructions.
    project_root = sys.path[0]
    if project_root.endswith("src"):
        sys.path.insert(0, project_root[:-3])

    from main import main as launch_app

    launch_app()


if __name__ == "__main__":
    main()
