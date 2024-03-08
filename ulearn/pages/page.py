from abc import abstractmethod


class UlearnPage:
    system_message: str = None

    @abstractmethod
    def generate_prompt(self) -> str:
        """Генерирует готовый промпт для нейросети"""
        pass
