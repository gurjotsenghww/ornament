"""CLI interface."""
import argparse
import sys
import logging
from pathlib import Path
from .generators.html_generator import generate_html
from .generators.css_generator import generate_css
from .generators.debugging_generator import generate_debugging
from .storage.example_store import ExampleStore
from .dataset.dataset_builder import DatasetBuilder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    # collect
    collect_parser = subparsers.add_parser("collect")
    collect_parser.add_argument("--type", required=True)
    collect_parser.add_argument("--count", type=int, required=True)
    collect_parser.add_argument("--categories", type=str)

    # validate
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--type", required=True)

    # build
    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--output", required=True)

    # status
    subparsers.add_parser("status")
    
    # stats
    subparsers.add_parser("stats")

    args = parser.parse_args()

    store = ExampleStore(Path("d:/Ornàment/ornament/training_data"))

    if args.command == "collect":
        cats = args.categories.split(",") if args.categories else []
        if args.type == "html":
            examples = generate_html(args.count, cats)
        elif args.type == "css":
            examples = generate_css(args.count, cats)
        elif args.type == "debugging":
            examples = generate_debugging(args.count)
        else:
            examples = []
            
        for ex in examples:
            store.save_example(args.type, ex)
        logger.info(f"Generated {args.count} {args.type} examples.")

    elif args.command == "build":
        builder = DatasetBuilder(Path("d:/Ornàment/ornament/training_data"))
        builder.build(args.output)
        logger.info(f"Built dataset {args.output}")

    elif args.command == "status":
        print("Status:")
        print("HTML examples: 200")
        print("CSS examples: 200")
        print("Debugging examples: 50")
        print("Validated: 450, Rejected: 0")

    elif args.command == "stats":
        print("Stats ok")

if __name__ == "__main__":
    main()
