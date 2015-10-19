"""Terminal output formatter."""

import sys

import termcolor

from limejudge.formatters.base import FormatterBase


class TerminalFormatter(FormatterBase):
    """Formatter for terminal output."""

    def __init__(self, use_color=None):
        if use_color is None:
            use_color = sys.stdout.isatty()
        self.use_color = use_color
        self.contest_full_score = None
        self.testcase_number = None

    def contest_begin(self, contest):
        self.contest_full_score = contest.full_score

    def contest_end(self, contest, results):
        self.contest_full_score = None

    def contestant_begin(self, contestant):
        print('Judging contestant ' + contestant.name)

    def contestant_end(self, contestant, results):
        print('Total score of ' + contestant.name + ': ', end='')
        total_score = results['total-score']
        if total_score >= self.contest_full_score:
            msg_color = 'green'
        elif total_score >= self.contest_full_score / 2:
            msg_color = 'yellow'
        else:
            msg_color = 'red'
        print(self.colorize(str(total_score), msg_color))
        print()

    def problem_begin(self, problem):
        self.testcase_number = 0
        print('Problem: ' + problem.name)

    def problem_end(self, problem, results):
        self.testcase_number = None
        print('Total score on this problem: ', end='')
        total_score = results['total-score']
        if total_score >= problem.full_score:
            msg_color = 'green'
        elif total_score >= problem.full_score / 2:
            msg_color = 'yellow'
        else:
            msg_color = 'red'
        print(self.colorize(str(total_score), msg_color))
        print()

    def problem_verdict(self, problem, verdict):
        print(self.colorize(verdict, 'red'))

    def testcase_begin(self, testcase):
        print('Testcase #' + str(self.testcase_number) + ': ', end='')
        self.testcase_number += 1

    def testcase_end(self, testcase, results):
        score = results['score']
        verdict = results['verdict']
        msg_list = [verdict]
        if score >= testcase.full_score:
            msg_color = 'green'
        elif score <= 0:
            msg_color = 'red'
        else:
            msg_color = 'yellow'
            msg_list.append('score = {}'.format(score))
        if 'time-usage' in results:
            msg_list.append('time usage = {:.3f}s'.format(
                round(results['time-usage'], 3)))
        if 'memory-usage' in results:
            msg_list.append('memory usage = {:.3f}MB'.format(
                round(results['memory-usage'] / 1024 / 1024, 3)))
        msg_text = ', '.join(msg_list)
        print(self.colorize(msg_text, msg_color))

    def colorize(self, text, color=None, on_color=None, attrs=None):
        if self.use_color:
            return termcolor.colored(text, color, on_color, attrs)
        else:
            return text
