from abc import ABC, abstractmethod
from orchestartors.SemanticKernelOrchestrator import conversation_with_data, conversation_without_data

class Orchestrator(ABC):
    @abstractmethod
    def conversation_with_data(self, request_body):
        conversation_with_data(request_body)
        pass

    @abstractmethod
    def conversation_without_data(self, request_body):
        conversation_without_data(request_body)
        pass