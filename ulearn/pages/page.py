from abc import abstractmethod


class UlearnPage:
    @abstractmethod
    def generate_prompt(self) -> str:
        """Генерирует готовый промпт для нейросети"""
        pass
