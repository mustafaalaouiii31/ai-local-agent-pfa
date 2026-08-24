"""
Long-Term Memory

Stores persistent memories of the agent.
"""

import json
import os
from datetime import datetime
from typing import Any


class LongTermMemory:

    def __init__(
        self,
        storage_path: str = "database/memory.json"
    ):

        self.storage_path = storage_path

        directory = os.path.dirname(
            self.storage_path
        )

        if directory:
            os.makedirs(
                directory,
                exist_ok=True
            )

        self.memories = self._load()

    # ==================================================
    # LOAD
    # ==================================================

    def _load(self) -> list[dict[str, Any]]:

        if not os.path.exists(
            self.storage_path
        ):
            return []

        try:

            with open(
                self.storage_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if isinstance(data, list):
                return data

            return []

        except Exception:

            return []

    # ==================================================
    # SAVE
    # ==================================================

    def _save(self) -> None:

        with open(
            self.storage_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.memories,
                file,
                ensure_ascii=False,
                indent=2
            )

    # ==================================================
    # REMEMBER
    # ==================================================

    def remember(
        self,
        content: str,
        memory_type: str = "general",
        metadata: dict | None = None
    ) -> None:

        if not content or not content.strip():
            return

        memory = {
            "content": content.strip(),
            "memory_type": memory_type,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
        }

        self.memories.append(memory)

        self._save()

    # ==================================================
    # GET ALL
    # ==================================================

    def get_all(self) -> list[dict[str, Any]]:

        return list(self.memories)

    # ==================================================
    # SEARCH
    # ==================================================

    def search(
        self,
        keyword: str,
        limit: int = 5
    ) -> list[dict[str, Any]]:

        if not keyword:
            return []

        keyword = keyword.lower()

        results = []

        for memory in reversed(
            self.memories
        ):

            content = memory.get(
                "content",
                ""
            ).lower()

            if keyword in content:

                results.append(memory)

            if len(results) >= limit:
                break

        return results

    # ==================================================
    # CLEAR
    # ==================================================

    def clear(self) -> None:

        self.memories = []

        self._save()