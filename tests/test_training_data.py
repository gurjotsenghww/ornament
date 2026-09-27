"""
Unit tests for the Ornàment Training Data Pipeline System.
Tests ExampleStore, Deduplicator, QualityScorer, Validators, and DatasetBuilder.
"""

import json
import pytest
import shutil
from pathlib import Path

from ornament.training_data.storage.example_store import ExampleStore
from ornament.training_data.processors.deduplicator import Deduplicator
from ornament.training_data.processors.quality_scorer import QualityScorer
from ornament.training_data.validators.html_validator import HtmlValidator
from ornament.training_data.validators.css_validator import CssValidator
from ornament.training_data.dataset.dataset_builder import DatasetBuilder

@pytest.fixture
def temp_training_dir(tmp_path):
    d = tmp_path / "training_data"
    d.mkdir()
    (d / "codes" / "html").mkdir(parents=True)
    (d / "codes" / "css").mkdir(parents=True)
    (d / "debugging").mkdir(parents=True)
    (d / "storage").mkdir(parents=True)
    (d / "processed").mkdir(parents=True)
    (d / "datasets").mkdir(parents=True)
    (d / "manifests").mkdir(parents=True)
    yield d
    shutil.rmtree(tmp_path, ignore_errors=True)

def test_deduplicator_all_three_levels(tmp_path):
    dedup = Deduplicator(tmp_path / "dedup.json")
    html1 = "<header><h1>Title</h1><p>Description</p></header>"
    html1_exact = "<header><h1>Title</h1><p>Description</p></header>"
    html1_normalized = "  <!-- comment -->\n<header>\n  <h1>Title</h1>\n  <p>Description</p>\n</header>  "
    html_different = "<main><section><h2>Different Content</h2></section></main>"

    # 1. Initially unique
    is_dup, _, _ = dedup.check_duplicate(html1, "html")
    assert is_dup is False

    # Register
    dedup.register(html1, "html_000001", "html")

    # 2. Exact duplicate
    is_dup, match_type, matched_id = dedup.check_duplicate(html1_exact, "html")
    assert is_dup is True
    assert match_type == "exact"
    assert matched_id == "html_000001"

    # 3. Normalized duplicate (whitespace and comment difference)
    is_dup, match_type, matched_id = dedup.check_duplicate(html1_normalized, "html")
    assert is_dup is True
    assert match_type == "normalized"

    # 4. Different content is unique
    is_dup, _, _ = dedup.check_duplicate(html_different, "html")
    assert is_dup is False

def test_html_and_css_validators():
    # Valid HTML
    valid_html = "<header><nav><a href='/'>Home</a></nav></header><main><p>Content</p></main>"
    is_valid, errors, score = HtmlValidator.validate(valid_html)
    assert is_valid is True
    assert score > 0.8

    # Malformed HTML (unclosed tag)
    invalid_html = "<header><nav><p>Unclosed paragraph</header>"
    is_valid, errors, score = HtmlValidator.validate(invalid_html)
    assert is_valid is False
    assert len(errors) > 0

    # Valid CSS
    valid_css = ":root { --accent: #6366f1; } .btn { color: var(--accent); padding: 8px; }"
    is_valid, errors, score = CssValidator.validate(valid_css)
    assert is_valid is True
    assert score > 0.8

    # Malformed CSS (unbalanced braces)
    invalid_css = ".btn { color: red; "
    is_valid, errors, score = CssValidator.validate(invalid_css)
    assert is_valid is False
    assert len(errors) > 0

def test_quality_scorer():
    high_qual_html = """<header class="sticky top-0 z-50 bg-zinc-900 border-b border-zinc-800">
  <nav aria-label="Main Navigation" class="max-w-7xl mx-auto flex items-center justify-between p-4">
    <a href="/" class="text-white font-bold">Logo</a>
    <img src="/logo.png" alt="Company Logo" class="w-8 h-8" />
  </nav>
</header>
<main class="py-12 bg-black text-white">
  <section class="max-w-4xl mx-auto">
    <h1 class="text-4xl font-extrabold">Autonomous Systems</h1>
    <p class="text-zinc-400">High-performance verifiable architecture.</p>
  </section>
</main>"""
    score = QualityScorer.score_example(high_qual_html, "html")
    assert score["passed"] is True
    assert score["overall"] >= 0.75
    assert score["syntax"] >= 0.9
    assert score["structure"] >= 0.8

def test_example_store_lifecycle_and_resumability(temp_training_dir):
    store = ExampleStore(temp_training_dir)
    example = {
        "instruction": "Build hero",
        "output": "<header><nav aria-label='Primary'><a href='/'>Home</a></nav></header><main><h1>Title</h1></main>",
        "metadata": {"category": "heroes", "framework": "HTML5"}
    }

    # 1. Save valid example
    success, ex_id, reason = store.save_example("html", example)
    assert success is True
    assert ex_id == "html_000001"

    # Verify files created on disk
    ex_dir = temp_training_dir / "codes" / "html" / "example_000001"
    assert (ex_dir / "code.html").exists()
    assert (ex_dir / "metadata.json").exists()
    assert (ex_dir / "source.json").exists()

    meta = json.loads((ex_dir / "metadata.json").read_text(encoding="utf-8"))
    assert meta["id"] == "html_000001"
    assert meta["category"] == "heroes"
    assert meta["validated"] is True

    # 2. Duplicate detection prevents redundant storage
    dup_success, dup_id, dup_reason = store.save_example("html", example)
    assert dup_success is False
    assert "Duplicate detected" in dup_reason

    # 3. Resumability check
    store.save_state()
    resumed_store = ExampleStore(temp_training_dir)
    assert resumed_store.counts["html"] == 1
    assert resumed_store.counts["validated"] == 1
    assert resumed_store.counts["duplicates"] == 1

def test_dataset_builder_jsonl_splits_and_isolation(temp_training_dir):
    store = ExampleStore(temp_training_dir)

    # Save 10 distinct examples across categories
    categories = ["heroes", "cards", "forms", "pricing", "testimonials", "footers", "dashboards", "portfolios", "projects", "ecommerce"]
    for i, cat in enumerate(categories):
        ex = {
            "instruction": f"Build {cat} component {i}",
            "output": f"<section id='sec-{cat}-{i}' class='p-6 bg-zinc-900 text-white'><header><h2 class='text-xl font-bold'>{cat.title()} {i}</h2></header><p class='text-zinc-400'>Rich distinct description for {cat} module {i}.</p><a href='/details-{i}' class='px-4 py-2 bg-indigo-600 rounded text-xs'>View {cat}</a></section>",
            "metadata": {"category": cat, "framework": "HTML5"}
        }
        store.save_example("html", ex)

    builder = DatasetBuilder(temp_training_dir)
    summary = builder.build("dataset-v0.1")

    html_splits = summary["datasets_created"]["html"]
    assert html_splits["train"] > 0
    assert html_splits["validation"] > 0
    assert html_splits["test"] > 0
    assert html_splits["train"] + html_splits["validation"] + html_splits["test"] == 10

    # Test set isolation: Verify no ID in test exists in train
    def read_ids(file_name):
        p = temp_training_dir / "datasets" / file_name
        lines = [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
        return set(x["id"] for x in lines)

    train_ids = read_ids("html_train.jsonl")
    test_ids = read_ids("html_test.jsonl")
    val_ids = read_ids("html_validation.jsonl")

    # Strict partition isolation
    assert len(train_ids.intersection(test_ids)) == 0
    assert len(train_ids.intersection(val_ids)) == 0
    assert len(val_ids.intersection(test_ids)) == 0
