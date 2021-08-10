"""Base of output formatters."""


class FormatterBase:
    """Base class of output formatters."""

    def contest_begin(self, contest):
        """Begin processing a contest.

        Can be overridden in subclasses.
        """

    def contest_end(self, contest, results):
        """End processing a contest.

        Can be overridden in subclasses.
        """

    def contestant_begin(self, contestant):
        """Begin processing a contestant.

        Can be overridden in subclasses.
        """

    def contestant_end(self, contestant, results):
        """End processing a contestant.

        Can be overridden in subclasses.
        """

    def problem_begin(self, problem):
        """Begin processing a problem.

        Can be overridden in subclasses.
        """

    def problem_end(self, problem, results):
        """End processing a problem.

        Can be overridden in subclasses.
        """

    def problem_verdict(self, problem, verdict):
        """Print problem verdict.

        This is only called when the verdict causes no test cases to be
        run, like compile error.

        Can be overridden in subclasses.
        """

    def testcase_begin(self, testcase):
        """Begin processing a test case.

        Can be overridden in subclasses.
        """

    def testcase_end(self, testcase, results):
        """End processing a test case.

        Can be overridden in subclasses.
        """
