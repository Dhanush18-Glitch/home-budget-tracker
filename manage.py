import argparse
from app import create_app
from app.extensions import db
from app.services.seed import seed_demo_data, seed_defaults


app = create_app()


def main():
    parser = argparse.ArgumentParser(description="Home Budget maintenance commands")
    parser.add_argument("command", choices=["init-db", "seed-demo", "run"])
    args = parser.parse_args()
    with app.app_context():
        if args.command == "init-db":
            db.create_all()
            seed_defaults()
            print("Database tables and default categories are ready.")
        elif args.command == "seed-demo":
            db.create_all()
            seed_defaults()
            created = seed_demo_data()
            print(f"Demo data {'created' if created else 'already exists'}.")
        else:
            app.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    main()

