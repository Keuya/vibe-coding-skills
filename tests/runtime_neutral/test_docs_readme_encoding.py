from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_README = REPO_ROOT / "docs" / "README.md"


class DocsReadmeEncodingTests(unittest.TestCase):
    def test_runtime_entry_copy_is_human_readable(self) -> None:
        text = DOCS_README.read_text(encoding="utf-8")

        self.assertIn(
            "- [`install/one-click-install-release-copy.md`](./install/one-click-install-release-copy.md)：面向普通用户的一键安装发布文案与 AI 助手复制提示词",
            text,
        )
        self.assertIn(
            "- [`install/one-click-install-release-copy.en.md`](./install/one-click-install-release-copy.en.md)：ordinary-user public release copy and copy-paste onboarding prompt",
            text,
        )
        self.assertNotIn(
            "锛氶潰鍚戞櫘閫氱敤鎴风殑涓€閿畨瑁呭彂甯冩枃妗堜笌 AI 鍔╂墜澶嶅埗鎻愮ず璇?",
            text,
        )
        self.assertNotIn(
            "锛歡rdinary-user public release copy and copy-paste onboarding prompt",
            text,
        )


if __name__ == "__main__":
    unittest.main()
