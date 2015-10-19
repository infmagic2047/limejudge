"""Contest information container."""

import yaml

from limejudge.problems import create_problem_from_dict


class Contestant:
    """A contestant.

    Contains the contestant's name and the path to the contestant's
    directory.
    """

    def __init__(self, *, name, path):
        self.name = name
        self.path = path

    @classmethod
    def from_dict(cls, contestant_data):
        name = contestant_data['name']
        path = contestant_data['path']
        return cls(name=name, path=path)


class ContestMetadata:
    """Contest Metadata.

    Contains metadata like title.
    """

    def __init__(self, *, title=None):
        self.title = title

    @classmethod
    def from_dict(cls, metadata_data):
        title = metadata_data['title']
        return cls(title=title)

    def to_dict(self):
        return {
            'title': self.title,
        }


class Contest:
    """A contest.

    Contains some problems and some contestants.
    """

    def __init__(self, metadata, problems, contestants):
        """Initialize contest with problems and contestants."""
        self.metadata = metadata
        self.problems = problems
        self.contestants = contestants

    @property
    def full_score(self):
        return sum(prob.full_score for prob in self.problems)

    def judge_all(self, formatter):
        """Judge all problems with all contestants.

        Return the results.
        """
        formatter.contest_begin(self)
        contestant_results = []
        for contestant in self.contestants:
            contestant_results.append(
                self.judge_contestant(contestant, formatter))
        results = {
            'metadata': self.metadata.to_dict(),
            'contestants': contestant_results,
        }
        formatter.contest_end(self, results)
        return results

    def judge_contestant(self, contestant, formatter):
        """Judge all problems with this contestant.

        Return the results.
        """
        formatter.contestant_begin(contestant)
        results = self.judge_contestant_path(contestant.path, formatter)
        results['name'] = contestant.name
        formatter.contestant_end(contestant, results)
        return results

    def judge_contestant_path(self, src_path, formatter):
        """Judge all problems with contestant in src_path.

        Return the results.
        """
        prob_results = []
        for problem in self.problems:
            prob_result = problem.judge(src_path, formatter)
            prob_results.append(prob_result)
        total_score = sum(result['total-score']
                          for result in prob_results)
        return {
            'problems': prob_results,
            'total-score': total_score,
        }

    @classmethod
    def from_dict(cls, contest_data):
        metadata_data = contest_data['metadata']
        problems_data = contest_data['problems']
        contestants_data = contest_data['contestants']
        metadata = ContestMetadata.from_dict(metadata_data)
        problems = [create_problem_from_dict(problem_data)
                    for problem_data in problems_data]
        contestants = [Contestant.from_dict(contestant_data)
                       for contestant_data in contestants_data]
        return cls(metadata, problems, contestants)

    @classmethod
    def from_yaml(cls, stream):
        contest_data = yaml.safe_load(stream)
        return cls.from_dict(contest_data)

    @classmethod
    def from_yaml_file(cls, filename):
        with open(filename, 'r') as f:
            content = f.read()
        return cls.from_yaml(content)
