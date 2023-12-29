from abc import ABC, abstractmethod

class Orchestrator(ABC):
    @abstractmethod
    def conversation_with_data(self, request_body):
        pass

    @abstractmethod
    def conversation_without_data(self, request_body):
        pass