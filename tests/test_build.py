import tempfile
import unittest
from pathlib import Path

import build


class BuildTests(unittest.TestCase):
    def test_markdown_renderer_handles_headings_lists_links_and_emphasis(self):
        source = """## About Me

I work on **matrix optimization**. See [Google Scholar](https://scholar.google.com) and [CV](CV.pdf).

- Perturbation analysis
- Matrix optimization
"""
        html = build.markdown_to_html(source)

        self.assertIn('<h2 id="about-me">About Me</h2>', html)
        self.assertIn("<strong>matrix optimization</strong>", html)
        self.assertIn('<a href="https://scholar.google.com">Google Scholar</a>', html)
        self.assertIn('<a href="CV.pdf">CV</a>', html)
        self.assertIn("<li>Perturbation analysis</li>", html)

    def test_build_site_combines_profile_and_publications(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            content = root / "content"
            content.mkdir()
            (content / "profile.md").write_text(
                """# Shiwei Wang

## Contact

- Email: [wangshiwei@amss.ac.cn](mailto:wangshiwei@amss.ac.cn)
""",
                encoding="utf-8",
            )
            (content / "publications.md").write_text(
                """## Publications

- An Exact Penalty Approach for Equality Constrained Optimization over a Convex Set.
""",
                encoding="utf-8",
            )

            output = root / "index.html"
            build.build_site(root=root, output_path=output)
            html = output.read_text(encoding="utf-8")

        self.assertIn("Shiwei Wang", html)
        self.assertIn("wangshiwei@amss.ac.cn", html)
        self.assertIn("An Exact Penalty Approach", html)
        self.assertIn('href="style.css"', html)


if __name__ == "__main__":
    unittest.main()
