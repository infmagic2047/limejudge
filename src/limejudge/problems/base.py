"""Base of problems."""

from abc import ABCMeta, abstractmethod


class ProblemBase(metaclass=ABCMeta):
    """Base class of problems."""

    def __init__(self, name, testcases):
        self.name = name
        self.testcases = testcases

    @property
    def full_score(self):
        """Return full score of this problem."""
        return sum(tc.full_score for tc in self.testcases)

    @abstractmethod
    def judge(self, src_path, formatter):
        """Judge this problem with source code in src_path.

        Return the results.
        """

    @classmethod
    @abstractmethod
    def from_dict(cls, problem_data):
        """Create a problem from dict problem_data."""
